import sys
import os

from alembic import context

from sqlalchemy import engine_from_config, pool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.config import sqlalchemy_database_url
from src.database.models import Base
from src.logging import logging

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", str(sqlalchemy_database_url))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
log = logging.getLogger(__name__)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    log.info("Migrating...")
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

    log.info("Migrations applied.")


if context.is_offline_mode():
    log.info("Can't run migrations offline")
else:
    log.info("Run migrations online")
    run_migrations_online()
