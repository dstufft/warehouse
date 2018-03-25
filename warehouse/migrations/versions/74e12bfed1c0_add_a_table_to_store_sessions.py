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
"""
Add a table to store sessions

Revision ID: 74e12bfed1c0
Revises: 6418f7d86a4b
Create Date: 2018-03-24 23:45:56.557115
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "74e12bfed1c0"
down_revision = "6418f7d86a4b"


def upgrade():
    op.create_table(
        "sessions",
        sa.Column("id",
                  postgresql.UUID(as_uuid=True),
                  server_default=sa.text("gen_random_uuid()"),
                  nullable=False),
        sa.Column("data",
                  postgresql.JSONB(astext_type=sa.Text()),
                  server_default=sa.text("'{}'"),
                  nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table("sessions")
