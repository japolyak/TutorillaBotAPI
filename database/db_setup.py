from sqlalchemy import create_engine
from database.models import Base
from sqlalchemy.orm import sessionmaker
from config import db_username as username, db_password, db_host, db_port, db_name


# DATABASE_URL = f"postgresql+psycopg2://{username}:{db_password}@{db_host}:{db_port}/{db_name}"
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def init_db():
    print('test')
    # Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
