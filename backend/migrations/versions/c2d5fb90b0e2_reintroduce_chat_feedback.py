"""reintroduce chat and feedback tables

Revision ID: c2d5fb90b0e2
Revises: 02c5ad0c45a0
Create Date: 2025-02-09 18:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c2d5fb90b0e2"
down_revision: Union[str, None] = "02c5ad0c45a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chat",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column(
            "created_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_chat_user_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_chat")),
    )
    op.create_index(op.f("ix_chat_created_dt"), "chat", ["created_dt"], unique=False)

    op.create_table(
        "feedback",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("feedback", sa.String(), nullable=True),
        sa.Column(
            "created_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk_feedback_user_id_user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feedback")),
    )
    op.create_index(
        op.f("ix_feedback_created_dt"),
        "feedback",
        ["created_dt"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_feedback_created_dt"), table_name="feedback")
    op.drop_table("feedback")
    op.drop_index(op.f("ix_chat_created_dt"), table_name="chat")
    op.drop_table("chat")
