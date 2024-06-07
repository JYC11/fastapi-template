import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
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
    ),
    sa.Column(
        "create_dt",
        postgresql.TIMESTAMP(timezone=True),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    ),
    sa.Column(
        "update_dt",
        postgresql.TIMESTAMP(timezone=True),
        onupdate=sa.func.current_timestamp(),
    ),
    sa.Column("phone", sa.String(length=100), nullable=False),
    sa.Column("email", sa.String(length=100), nullable=False),
    sa.Column("password", sa.Text, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(models.User, user)
