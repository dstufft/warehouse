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

from apiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials


def bigquery_factory(context, request):
    credentials = request.find_service(name="google.credentials")
    return discovery.build("bigquery", "v2", credentials=credentials)


def includeme(config):
    config.register_service(
        SignedJwtAssertionCredentials(
            "warehouse-local@long-stack-762.iam.gserviceaccount.com",
            "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCAWORWLxcW3iRE\n2xpuPDsCusCr5kN9Vx/m3vtzVOCNF4cslYxRIhsVwUGt23kJ/gKHGxRyTOWPI32J\nXzF/tGFdh6PyjX5o6aYIC6nd6k9ioEuX7vBMYebuSl0LFdSFYH+hZ0UppVBZfQqi\nSVblngzY1+X2L9gUWFBApU7A/2m+iyonImN24YfwPvmX4PV+NA0nt6dShx3QqZEd\nuRqEvrPahpju5tY4fQIRZ4KrCGrYJdA8oSg7xkb/qHyYuLTwet9c+gGvX9HJDtHn\nx02FYC7a6Xv/YTK5s3z4GcATUQn/xIrI5yJphYCSTFNpJJpjOk41pBrZI4u91D3J\n16rHjgvVAgMBAAECggEARAtcmxiCHDyPa/XhUFocSvkplrkQRM5A+oxzMRTpq8Oy\nhX+PkaAMTf9US9EUnaiOPISt1V9RQQ7mykKuom7GQ+jakYhUYVimDpPobd+AUOB8\n00L5IPWykdjY9TyQnFmpsK9oaojbTWZOkfVh3YBqfTgREfERlM+xVGSPmSCQNlUe\na/sKP6I78YLPAw2I3HHir3/rtVDLjQCixDbuHYVP6ModQmbgNsRRH7tI27hPa3LG\nphqBgu2lmoSS71/iK4MmMpIcWIluYogE+zOd0eL0nvtRE0Zdk2jTDVYrjrGPJpD2\nmHR+YWaXiE2YAl5l3pCLGpRfCD8UmojnaErOoDkWYQKBgQDHC075+a1Iv92Drvoi\nPrz7G3SWwkf8jdBz5fOjl5ME+Th7JCNMi8+m6oAs5ng8c7ytPOggGQd0MVRJ3mHs\nZFMrW2w7jqR+lCnnibyNFeg+EXiDU46iwA4TcG77QE6QQ6c3cHeX+NZb6U70NqP8\n3kVBT085tMwBFQxhg8WBHmbc7QKBgQClEsgsmkRkpkyqEZGdg3OCxIA5g0wgxNrA\nY9OflF5mqnj5uNgLsToGrYkWRyyFZRv04Fdqmvtp6DJPPgcrIqS5le9c/zdsnJSj\nQeoAPQHIvC3uCOu/SVty/T5SDfAUMEbuaJmxso3RgYpsAqyG0aW40MqfV2p2s8rF\nbnuP5f/1iQKBgQCxwo6wvuOb4gYRkZZAOSmLVNTFwxKJIZm1t/rj8f1R5sUjbH29\n4er8VddMwjNFQdOSH5/q8o9unJN7OQjZFiwUv5wkgFq11Nqrtp3Wnmb/75hiKKBt\nBvpLMBFdf+vp+RGAeIfGCGxgPzfM8HN55IOTNSI7FhVPLh4VhJpBmwYgbQKBgAq6\n4dAkZvWz6Z/UbIa0mLmTVFJounYW1bFTy9m/pzM9OYfiAAkiiAcPGK4eCkLRg7Oz\nMXt4f4cu1LZZ7dVb9yEpIdoFrPCebPr/udoyHP+TW9jxM4HHnu4mj/p9dXGagcHV\ngsgONzG7HehPdC9/SSpuR/17jSwSG8ghml6MMMshAoGAKcbOq9c8w2F6IUEZSV7s\nVB/+GYaj3xES/O8wYsEXBdaOC3PEytHDBxt1YsiVrhIBwhhLtJEYqAV7/rD2mhDG\nS2dOtkaTdKrHc6pJTrF1qaHgOfWun4DjoZpSpVi21ZNUUqsyMV/DAPLqaGcDIDea\nh8z2gfwt4KKlx99ujN4j4hw=\n-----END PRIVATE KEY-----\n",
            [
                "https://www.googleapis.com/auth/bigquery",
            ],
        ),
        name="google.credentials",
    )

    config.register_service_factory(bigquery_factory, name="google.bigquery")
