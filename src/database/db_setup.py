import os
import logging

from alembic import command as alembic_command
from alembic.config import Config
from alembic.runtime import migration
from alembic.script import ScriptDirectory

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from src.config import is_development, sqlalchemy_database_url
from src.database.mockdata import insert_mock_data


log = logging.getLogger(__name__)
engine = create_engine(sqlalchemy_database_url, echo=is_development)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_alembic_config() -> Config:
    alembic_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_location = alembic_ini_path + "/database/migrations"

    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("script_location", script_location)

    return alembic_cfg


def is_migration_pending(engine: Engine, config: Config) -> bool:
    with engine.begin() as conn:
        last_applied_version = migration.MigrationContext.configure(conn).get_current_revision()
        latest_version = ScriptDirectory.from_config(config).get_current_head()

        return last_applied_version != latest_version


def migrate(engine: Engine):
    """Applies migrations."""

    config = get_alembic_config()

    if not is_migration_pending(engine, config):
        return

    alembic_command.upgrade(config, "head")


def initialize_database():
    try:
        if database_exists(sqlalchemy_database_url):
            migrate(engine)
            return

        create_database(sqlalchemy_database_url)
        log.info(msg="Database created")

        migrate(engine)

        if is_development:
            insert_mock_data(engine)
            log.info(msg="Mock data inserted")

    except Exception as e:
        log.error(msg=f"Error while initializing database: {e}")
        pass


def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
