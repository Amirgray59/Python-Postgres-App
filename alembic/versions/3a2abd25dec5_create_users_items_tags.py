from alembic import op
import sqlalchemy as sa


revision = "3a2abd25dec5"
down_revision = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(200), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("sell_in", sa.Integer(), nullable=False),
        sa.Column("quality", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
    )

    op.create_foreign_key(
        "fk_items_owner_id_users",
        "items",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_index(
        "ix_items_owner_id",
        "items",
        ["owner_id"],
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.UniqueConstraint("name", name="uq_tags_name"),
    )

    op.create_table(
        "item_tags",
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["item_id"], ["items.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tags.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("item_id", "tag_id"),
    )

    op.create_index(
        "ix_item_tags_item_id",
        "item_tags",
        ["item_id"],
    )

    op.create_index(
        "ix_item_tags_tag_id",
        "item_tags",
        ["tag_id"],
    )


def downgrade():
    op.drop_index("ix_item_tags_tag_id", table_name="item_tags")
    op.drop_index("ix_item_tags_item_id", table_name="item_tags")
    op.drop_table("item_tags")

    op.drop_table("tags")

    op.drop_index("ix_items_owner_id", table_name="items")
    op.drop_constraint("fk_items_owner_id_users", "items", type_="foreignkey")
    op.drop_table("items")

    op.drop_table("users")
