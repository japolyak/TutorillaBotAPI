from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import allowed_origins
from database.db_setup import init_db
from routers.admin import router as admin_router
from routers.private_course import router as private_course_router
from routers.subject import router as subject_router
from routers.tutor_course import router as tutor_course_router
from routers.user import router as user_router
from routers.web_app import router as web_app_router
from routers.test import router as test_router
import logging


logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

logging.log(logging.INFO, "Starting app...")
app = FastAPI()

allow_origins = allowed_origins.split('&')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.log(logging.INFO, "Start db initialization...")
init_db()
logging.log(logging.INFO, "Finished db initialization...")

app.include_router(test_router)
app.include_router(admin_router)
app.include_router(private_course_router)
app.include_router(subject_router)
app.include_router(tutor_course_router)
app.include_router(user_router)
app.include_router(web_app_router)
