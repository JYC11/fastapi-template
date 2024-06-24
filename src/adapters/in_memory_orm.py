import sqlalchemy as sa
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import registry

from src.domain import models

metadata = sa.MetaData()
mapper_registry = registry(metadata=metadata)

user = sa.Table(
    "user",
    mapper_registry.metadata,
    sa.Column(
        "id",
        sa.String(length=21),
        primary_key=True,
        index=True,
        unique=True,
    ),
    sa.Column(
        "create_date",
        sqlite.TIMESTAMP(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "update_date",
        sqlite.TIMESTAMP(timezone=True),
        onupdate=sa.func.current_timestamp(),
    ),
    sa.Column("phone", sa.String(length=100), nullable=False),
    sa.Column("email", sa.String(length=100), nullable=False),
    sa.Column("password", sa.Text, nullable=False),
)

failed_message_log = sa.Table(
    "failed_message_log",
    mapper_registry.metadata,
    sa.Column(
        "id",
        sa.String(length=21),
        primary_key=True,
        index=True,
        unique=True,
    ),
    sa.Column(
        "create_date",
        sqlite.TIMESTAMP(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "update_date",
        sqlite.TIMESTAMP(timezone=True),
        onupdate=sa.func.current_timestamp(),
    ),
    sa.Column("message_type", sa.String(length=255), nullable=False),
    sa.Column("message_name", sa.String(length=255), nullable=False),
    sa.Column("error_message", sa.Text, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(models.User, user)
    mapper_registry.map_imperatively(models.FailedMessageLog, failed_message_log)
