# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import time
import uuid

import arrow
import msgpack

from zope.interface import implementer

from warehouse import celery
from warehouse.packaging.interfaces import IDownloadStatService, StatsPending


__all__ = ["BigQueryDownloadStatService"]


def _make_key(project, version=None, suffix=None):
    key = "stats:downloads:{}".format(project)

    if version is not None:
        key += ":{}".format(version)

    if suffix is not None:
        key += ":{}".format(suffix)

    return key


@celery.task(pyramid_request=True, acks_late=True)
def _generate_stats_daily(request, project, version=None):
    stats_service = request.find_service(IDownloadStatService)
    return stats_service._get_daily(project, version)


@celery.task(pyramid_request=True, acks_late=True)
def _generate_stats_weekly(request, project, version=None):
    stats_service = request.find_service(IDownloadStatService)
    return stats_service._get_weekly(project, version)


@celery.task(pyramid_request=True, acks_late=True)
def _generate_stats_monthly(request, project, version=None):
    stats_service = request.find_service(IDownloadStatService)
    return stats_service._get_monthly(project, version)


@celery.task(pyramid_request=True, acks_late=True)
def _generate_stats_yearly(request, project, version=None):
    stats_service = request.find_service(IDownloadStatService)
    return stats_service._get_yearly(project, version)


@celery.task(pyramid_request=True, ignore_result=True, acks_late=True)
def _collect_stats(request, stats, project, version=None):
    daily, weekly, monthly, yearly = stats
    stats_service = request.find_service(IDownloadStatService)
    stats_service._store_stats(
        {
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly,
            "yearly": yearly,
        },
        project=project,
        version=version,
    )


@implementer(IDownloadStatService)
class BigQueryDownloadStatService:

    def __init__(self, project, bigquery_client, redis):
        self.project = project
        self._client = bigquery_client
        self._redis = redis

    @classmethod
    def create_service(cls, context, request):
        return cls(
            request.registry.settings["google.project"],
            request.find_service(name="google.bigquery"),
            request.redis,
        )

    def get(self, project, version):
        keys = [
            "stats:downloads:{}".format(project),
            "stats:downloads:{}:{}".format(project, version),
        ]
        all_stats, version_stats = self._redis.mget(*keys)

        if all_stats is None or version_stats is None:
            if all_stats is None:
                self._generate_stats(project)
            if version_stats is None:
                self._generate_stats(project, version)

            raise StatsPending

        return {
            "all": msgpack.unpackb(all_stats, encoding="utf-8"),
            "version": msgpack.unpackb(version_stats, encoding="utf-8"),
        }

    def _generate_stats(self, project, version=None):
        lid = str(uuid.uuid4())
        should_process = self._redis.set(
            _make_key(project, version, "processing"), lid, ex=30, nx=True,
        )

        if should_process:
            celery.chord(
                [
                    _generate_stats_daily.s(project, version),
                    _generate_stats_weekly.s(project, version),
                    _generate_stats_monthly.s(project, version),
                    _generate_stats_yearly.s(project, version),
                ],
                _collect_stats.s(project, version),
            ).delay()

    def _store_stats(self, stats, project, version=None):
        key = "stats:downloads:{}".format(project)
        if version is not None:
            key += ":{}".format(version)

        value = msgpack.packb(stats, use_bin_type=True)
        self._redis.setex(key, 15 * 60, value)
        self._redis.delete(_make_key(project, version, "processing"))

    def _get_daily(self, project, version=None):
        return self._get_stats(days=1, project=project, version=version)

    def _get_weekly(self, project, version=None):
        return self._get_stats(days=7, project=project, version=version)

    def _get_monthly(self, project, version=None):
        return self._get_stats(days=30, project=project, version=version)

    def _get_yearly(self, project, version=None):
        return self._get_stats(days=365, project=project, version=version)

    def _get_stats(self, days, project, version=None):
        current = arrow.utcnow()
        results = self._query(
            """ SELECT COUNT(*) as downloads
                FROM TABLE_DATE_RANGE(
                        [long-stack-762:pypi.downloads],
                        TIMESTAMP('{start}'),
                        TIMESTAMP('{end}')
                    )
                WHERE TIMESTAMP_TO_SEC(timestamp) > {cutoff}
                  AND file.project = '{project}'
            """ +
            (" AND file.version = '{version}'" if version is not None else ""),
            start=(current - datetime.timedelta(days=days)).format("YYYYMMDD"),
            end=current.format("YYYYMMDD"),
            cutoff=(current - datetime.timedelta(days=days)).timestamp,
            project=project,
            version=version,
        )
        results = list(results)

        assert len(results) == 1, "One, and only one row should be returned"
        assert len(results[0]["f"]) == 1, "One, and only one column"

        return int(results[0]["f"][0]["v"])

    def _query(self, query, **values):
        # TODO: Figure out how to escape values so they don't contain anything
        #       dangerous.

        data = {
            "jobReference": {
                "projectId": self.project,
                "job_id": str(uuid.uuid4()),
            },
            "configuration": {
                "query": {
                    "query": query.format(**values),
                    "priority": "INTERACTIVE",
                }
            }
        }

        job = (
            self._client.jobs()
                        .insert(projectId=self.project, body=data)
                        .execute()
        )

        request = self._client.jobs().get(
            projectId=job["jobReference"]["projectId"],
            jobId=job["jobReference"]["jobId"],
        )

        # Poll for our query to be complete.
        while True:
            result = request.execute(num_retries=2)
            if result["status"]["state"] == "DONE":
                if "errorResult" in result["status"]:
                    # TODO: Use a better exception
                    raise RuntimeError(result["status"]["errorResult"])
                else:
                    break
            else:
                time.sleep(0.5)

        # Get the results.
        page_token = None
        while True:
            page = self._client.jobs().getQueryResults(
                pageToken=page_token,
                **job["jobReference"]
            ).execute(num_retries=2)

            yield from page["rows"]

            page_token = page.get("pageToken")
            if not page_token:
                break
