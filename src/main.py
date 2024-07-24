import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import config
from src.database.db_setup import initialize_database

from src.api import api_router
from src.logging import configure_logging


log = logging.getLogger(__name__)

# Logging level and format configuration
configure_logging()

log.info(msg="Starting app...")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()
app.include_router(api_router)
