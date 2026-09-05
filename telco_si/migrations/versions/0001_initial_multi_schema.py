"""initial_multi_schema

Baseline revision that creates the six empty domain schemas on a fresh
instance (FR-007). Domain tables are added by later sprints.

Revision ID: 0001
Revises:
Create Date: 2026-09-05

"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

DOMAIN_SCHEMAS = ["catalog", "inventory", "crm", "usage", "billing", "dunning"]


def upgrade() -> None:
    for schema in DOMAIN_SCHEMAS:
        op.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")


def downgrade() -> None:
    for schema in reversed(DOMAIN_SCHEMAS):
        op.execute(f"DROP SCHEMA IF EXISTS {schema}")
