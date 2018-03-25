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

from sqlalchemy import sql
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB

from warehouse import db


class Session(db.Model):

    __tablename__ = "sessions"

    data = Column(JSONB, nullable=False, server_default=sql.text("'{}'"))
