"""Initial ControlHub schema."""

import sqlalchemy as sa

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("csrf_token", sa.String(), nullable=False),
        sa.Column("expires_at", sa.String(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_log_action", "audit_log", ["action"])
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_categories_name", "categories", ["name"], unique=True)
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_tags_name", "tags", ["name"], unique=True)
    op.create_table(
        "resources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("resource_type", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("host", sa.String(), nullable=False),
        sa.Column("port", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("icon", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("favorite", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.String(), nullable=False),
        sa.Column("metadata_json", sa.String(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.Column("updated_at", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resources_name", "resources", ["name"])
    op.create_index("ix_resources_category_id", "resources", ["category_id"])
    op.create_index("ix_resources_resource_type", "resources", ["resource_type"])
    op.create_table(
        "resource_tags",
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["resource_id"], ["resources.id"]),
        sa.ForeignKeyConstraint(["tag_id"], ["tags.id"]),
        sa.PrimaryKeyConstraint("resource_id", "tag_id"),
    )



def downgrade() -> None:
    op.drop_table("resource_tags")
    for index, table in [
        ("ix_resources_resource_type", "resources"),
        ("ix_resources_category_id", "resources"),
        ("ix_resources_name", "resources"),
        ("ix_tags_name", "tags"),
        ("ix_categories_name", "categories"),
        ("ix_audit_log_action", "audit_log"),
        ("ix_sessions_user_id", "sessions"),
        ("ix_users_username", "users"),
    ]:
        op.drop_index(index, table_name=table)
    for table in ["resources", "tags", "categories", "audit_log", "sessions", "users"]:
        op.drop_table(table)
