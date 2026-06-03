import asyncio
import logging

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.config import SQLALCHEMY_DATABASE_URI
from app.database.core import BaseModel
from app.database.models import *  # noqa: F403

config = context.config

logger = logging.getLogger(__name__)

config.set_main_option("sqlalchemy.url", str(SQLALCHEMY_DATABASE_URI))

target_metadata = BaseModel.metadata


def do_run_migrations(connection: Connection) -> None:
    def process_revision_directives(context, revision, directives):
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            logger.info("No changes found skipping revision creation.")

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    pass
else:
    run_migrations_online()
