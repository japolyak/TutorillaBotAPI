from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from . import config
from .database import db_setup
from .routers import admin, user, subject, private_course, tutor_course, web_app, test


logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

logging.log(logging.INFO, "Starting app...")
app = FastAPI()

allow_origins = config.allowed_origins.split('&')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.log(logging.INFO, "Start db initialization...")
db_setup.init_db()
logging.log(logging.INFO, "Finished db initialization...")

app.include_router(test.router)
app.include_router(admin.router)
app.include_router(private_course.router)
app.include_router(subject.router)
app.include_router(tutor_course.router)
app.include_router(user.router)
app.include_router(web_app.router)
