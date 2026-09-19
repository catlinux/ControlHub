"""Associate encrypted secrets with resources."""

import sqlalchemy as sa
from alembic import op

revision = "0003_secret_resource"
down_revision = "0002_secrets"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("secrets") as batch:
        batch.add_column(sa.Column("resource_id", sa.Integer(), nullable=True))
        batch.create_index("ix_secrets_resource_id", ["resource_id"], unique=False)
        batch.create_foreign_key("fk_secrets_resource_id", "resources", ["resource_id"], ["id"])


def downgrade() -> None:
    with op.batch_alter_table("secrets") as batch:
        batch.drop_constraint("fk_secrets_resource_id", type_="foreignkey")
        batch.drop_index("ix_secrets_resource_id")
        batch.drop_column("resource_id")
