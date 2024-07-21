from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from src.database.models import Base
from sqlalchemy.orm import sessionmaker
from src.database.mockdata import insert_mock_data
from src.config import is_development, sqlalchemy_database_uri
import logging

log = logging.getLogger(__name__)

engine = create_engine(sqlalchemy_database_uri, echo=is_development)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    log.warning(msg="Start db initialization...")

    try:
        db_initialized = False

        if not database_exists(sqlalchemy_database_uri):
            create_database(sqlalchemy_database_uri)
            db_initialized = True
            log.warning(msg="Database created")

        Base.metadata.create_all(bind=engine)
        log.warning(msg="Tables created")

        if db_initialized and is_development:
            insert_mock_data(engine)
            log.warning(msg="Mock data inserted")

    except Exception as e:
        log.exception(msg=f"Error while initializing db: {e}")
        pass

    log.warning(msg="Finished db initialization...")


def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
