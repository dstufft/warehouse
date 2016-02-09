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

import celery.backends

# We need to trick Celery into supporting rediss:// URLs which is how redis-py
# signals that you should use Redis with TLS.
celery.backends.BACKEND_ALIASES["rediss"] = "warehouse.celery:TLSRedisBackend"  # noqa

from celery import Celery, Task, chord
from celery.backends.redis import RedisBackend as _RedisBackend
from celery.signals import celeryd_init
from pyramid import scripting
from pyramid.threadlocal import get_current_request

from warehouse.config import Environment, configure


__all__ = ["task", "chord", "includeme"]


@celeryd_init.connect
def _configure_celery(instance, conf, **kwargs):
    conf["PYRAMID_WSIG_APPI"] = configure().make_wsgi_app()


class TLSRedisBackend(_RedisBackend):

    def _params_from_url(self, url, defaults):
        params = super()._params_from_url(url, defaults)
        params.update({"connection_class": self.redis.SSLConnection})
        return params


class WarehouseTask(Task):

    abstract = True

    def __call__(self, *args, **kwargs):
        pyramid_env = scripting.prepare()

        if getattr(self, "pyramid_request", False):
            args = (pyramid_env["request"],) + args

        try:
            return super().__call__(*args, **kwargs)
        finally:
            pyramid_env["closer"]()

    def apply_async(self, *args, **kwargs):
        # The API design of Celery makes this threadlocal pretty impossible to
        # avoid :(
        request = get_current_request()

        # If for whatever reason we were unable to get a request we'll just
        # skip this and call the original method to send this immediately.
        if (request is None or not hasattr(request, "tm") or
                request.tm._txn is None):
            return super().apply_async(*args, **kwargs)

        # This will break things that expect to get an AsyncResult because
        # we're no longer going to be returning an async result from this when
        # called from within a request, response cycle. Ideally we shouldn't be
        # waiting for responses in a request/response cycle anyways though.
        request.tm.get().addAfterCommitHook(
            self._after_commit_hook,
            args=args,
            kws=kwargs,
        )

    def _after_commit_hook(self, success, *args, **kwargs):
        if success:
            super().apply_async(*args, **kwargs)


app = Celery("warehouse")
app.Task = WarehouseTask


task = app.task


def includeme(config):
    s = config.registry.settings
    app.conf.update(
        BROKER_URL=s["celery.broker_url"],
        BROKER_USE_SSL=s["warehouse.env"] == Environment.production,
        CELERY_DISABLE_RATE_LIMITS=True,
        CELERY_RESULT_BACKEND=s["celery.result_url"],
        CELERY_RESULT_SERIALIZER="json",
        CELERY_TASK_SERIALIZER="json",
        CELERY_ACCEPT_CONTENT=["json", "msgpack"],
        CELERY_MESSAGE_COMPRESSION="gzip",
        CELERY_QUEUE_HA_POLICY="all",
    )
