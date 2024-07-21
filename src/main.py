from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src import config
from src.database import db_setup
from .api import authenticated_api_router as api_router
from .logging import configure_logging

log = logging.getLogger(__name__)

configure_logging()

log.warning(msg="Starting app...")

app = FastAPI()

allow_origins = config.allowed_origins.split('&')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_setup.init_db()

log.warning(msg="Start routers initialization...")
app.include_router(api_router)
log.warning(msg="Finish routers initialization...")
