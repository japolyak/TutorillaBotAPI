from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from src.database.models import Base
from sqlalchemy.orm import sessionmaker
from src.database.mockdata import insert_mock_data
from src.config import db_username as username, db_password, db_host, db_port, db_name, is_development
import logging


database_url = f"postgresql+psycopg2://{username}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(database_url, echo=is_development)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    try:
        db_initialized = False

        if not database_exists(database_url):
            create_database(database_url)
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
