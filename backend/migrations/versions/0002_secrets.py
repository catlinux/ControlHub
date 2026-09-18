"""Add encrypted secrets table."""

import sqlalchemy as sa
from alembic import op

revision = "0002_secrets"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "secrets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("encrypted_value", sa.String(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.Column("updated_at", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_secrets_name", "secrets", ["name"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_secrets_name", table_name="secrets")
    op.drop_table("secrets")
