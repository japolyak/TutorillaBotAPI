from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from database.models import Base
from sqlalchemy.orm import sessionmaker
from .mockdata import insert_mock_data
from config import db_username as username, db_password, db_host, db_port, db_name, db_initialized, is_development

DATABASE_URL = f"postgresql+psycopg2://{username}:{db_password}@{db_host}:{db_port}/{db_name}"

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
    db_initialized = True

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    global db_initialized
    Base.metadata.create_all(bind=engine)

    if db_initialized and is_development:
        insert_mock_data(engine)
        db_initialized = False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
