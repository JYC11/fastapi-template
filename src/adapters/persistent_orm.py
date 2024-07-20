import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry, relationship

from src.domain.base import FailedMessageLog
from src.domain.user.model import AuthorizedFeatures, User

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
    sa.Column("type", sa.String(length=100), nullable=False),
)

authorized_features = sa.Table(
    "authorized_features",
    mapper_registry.metadata,
    sa.Column(
        "id",
        sa.String(length=21),
        primary_key=True,
        index=True,
        unique=True,
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
    sa.Column(
        "user_id",
        sa.String(length=21),
        sa.ForeignKey("user.id", ondelete="cascade"),
        index=True,
        nullable=False,
    ),
    sa.Column("feature", sa.String(length=100), nullable=False),
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
    sa.Column("message_type", sa.String(length=255), nullable=False),
    sa.Column("message_name", sa.String(length=255), nullable=False),
    sa.Column("error_message", sa.Text, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(
        User,
        user,
        properties={
            "authorized_features": relationship(
                AuthorizedFeatures,
                back_populates="user",
            )
        },
    )
    mapper_registry.map_imperatively(
        AuthorizedFeatures,
        authorized_features,
        properties={
            "user": relationship(
                User,
                back_populates="authorized_features",
            )
        },
    )
    mapper_registry.map_imperatively(FailedMessageLog, failed_message_log)
