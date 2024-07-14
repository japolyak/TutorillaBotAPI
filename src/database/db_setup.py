from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from src.database.models import Base
from sqlalchemy.orm import sessionmaker
from src.database.mockdata import insert_mock_data
from src.config import is_development, connection_string
import logging

engine = create_engine(connection_string, echo=is_development)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    print(connection_string)
    try:
        db_initialized = False

        if not database_exists(connection_string):
            create_database(connection_string)
            db_initialized = True
            logging.log(logging.INFO, "Database created")

        Base.metadata.create_all(bind=engine)
        logging.log(logging.INFO, "Tables created")

        if db_initialized and is_development:
            insert_mock_data(engine)
            logging.log(logging.INFO, "Mock data inserted")

    except Exception as e:
        logging.exception(f"Error while initializing db: {e}")
        pass


def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
