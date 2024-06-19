"""init

Revision ID: c3ddf61c1ae1
Revises: 
Create Date: 2024-06-19 21:45:13.982874

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c3ddf61c1ae1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "failed_message_log",
        sa.Column("id", sa.String(length=21), nullable=False),
        sa.Column("create_dt", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("update_dt", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("message_type", sa.String(length=255), nullable=False),
        sa.Column("message_name", sa.String(length=255), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_failed_message_log_id"), "failed_message_log", ["id"], unique=True)
    op.create_table(
        "user",
        sa.Column("id", sa.String(length=21), nullable=False),
        sa.Column("create_dt", postgresql.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("update_dt", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("phone", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_failed_message_log_id"), table_name="failed_message_log")
    op.drop_table("failed_message_log")
    # ### end Alembic commands ###