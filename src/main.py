from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src import config
from src.database import db_setup
from .api import authenticated_api_router as api_router


logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

logging.info(msg="Starting app...")

app = FastAPI()

allow_origins = config.allowed_origins.split('&')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.info(msg="Start db initialization...")
db_setup.init_db()
logging.info(msg="Finished db initialization...")

logging.info(msg="Start routers initialization...")
app.include_router(api_router)
logging.info(msg="Finish routers initialization...")
