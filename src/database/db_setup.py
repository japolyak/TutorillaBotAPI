import os
import logging

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from src.config import is_development, sqlalchemy_database_url
from src.database.models import Base
from src.database.mockdata import insert_mock_data


log = logging.getLogger(__name__)
engine = create_engine(sqlalchemy_database_url, echo=is_development)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def version_schema():
    """Applies alembic versioning."""

    alembic_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_location = alembic_ini_path + "/database/migrations"

    alembic_cfg = AlembicConfig(alembic_ini_path)
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_command.upgrade(alembic_cfg, "head")


def initialize_database():
    log.info(msg="Database init...")
    try:
        db_initialized = False

        if not database_exists(sqlalchemy_database_url):
            create_database(sqlalchemy_database_url)
            db_initialized = True
            log.info(msg="Database created")

            Base.metadata.create_all(bind=engine)

        version_schema()

        if db_initialized and is_development:
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
