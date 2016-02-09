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

import botocore.exceptions

from zope.interface import implementer

from warehouse.packaging.interfaces import IFileStorage


@implementer(IFileStorage)
class S3FileStorage:

    def __init__(self, bucket):
        self.bucket = bucket

    @classmethod
    def create_service(cls, context, request):
        session = request.find_service(name="aws.session")
        s3 = session.resource("s3")
        bucket = s3.Bucket(request.registry.settings["files.bucket"])
        return cls(bucket)

    def get(self, path):
        try:
            return self.bucket.Object(path).get()["Body"]
        except botocore.exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] != "NoSuchKey":
                raise
            raise FileNotFoundError("No such key: {!r}".format(path)) from None

    def store(self, path, file_path, *, meta=None):
        extra_args = {}

        if meta is not None:
            extra_args["Metadata"] = meta

        self.bucket.upload_file(file_path, path, ExtraArgs=extra_args)
