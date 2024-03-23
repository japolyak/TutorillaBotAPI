from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import telegram_web_app, my_tg_id
from database.db_setup import init_db
# from routes.admin_routes import router as admin_router
# from routes.private_course_routes import router as private_course_router
# from routes.subject_routes import router as subject_router
# from routes.tutor_course_routes import router as tutor_course_router
# from routes.user_routes import router as user_router
# from routes.web_app_routes import router as web_app_router
from routes.test_routes import router as test_router
from bot_client.message_sender import send_test_message

app = FastAPI()

allowed_origins = [telegram_web_app, "http://localhost:5173", "http://127.0.0.1:4040", "http://127.0.0.1:5173", "http://localhost:4040"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(test_router, prefix="/test", tags=["test"])
# app.include_router(admin_router, prefix="/admin", tags=["admin"])
# app.include_router(private_course_router, prefix="/private-courses", tags=["private-courses"])
# app.include_router(subject_router, prefix="/subjects", tags=["subjects"])
# app.include_router(tutor_course_router, prefix="/tutor-courses", tags=["tutor-courses"])
# app.include_router(user_router, prefix="/users", tags=["users"])
# app.include_router(web_app_router, prefix="/auth", tags=["web_app_authorization"])
