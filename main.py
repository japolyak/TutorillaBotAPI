from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import allowed_origins
from database.db_setup import init_db
from routes.admin_routes import router as admin_router
from routes.private_course_routes import router as private_course_router
from routes.subject_routes import router as subject_router
from routes.tutor_course_routes import router as tutor_course_router
from routes.user_routes import router as user_router
from routes.web_app_routes import router as web_app_router
from routes.test_routes import router as test_router
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
