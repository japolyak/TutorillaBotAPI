from fastapi import APIRouter

from src.routers.api_enpoints import APIEndpoints
from src.routers.admin import router as admin_router
from src.routers.user import router as user_router
from src.routers.subject import router as subject_router
from src.routers.private_course import router as private_course_router
from src.routers.tutor_course import router as tutor_course_router
from src.routers.web_app import router as web_app_router
from src.routers.home import router as home_router


api_router = APIRouter()

api_router.include_router(home_router, prefix=APIEndpoints.Home.Prefix, tags=["home"])
api_router.include_router(admin_router, prefix=APIEndpoints.Admin.Prefix, tags=["admin"])
api_router.include_router(private_course_router, prefix=APIEndpoints.PrivateCourses.Prefix, tags=["private-courses"])
api_router.include_router(subject_router, prefix=APIEndpoints.Subjects.Prefix, tags=["subjects"])
api_router.include_router(tutor_course_router, prefix=APIEndpoints.TutorCourse.Prefix, tags=["tutor-courses"])
api_router.include_router(user_router, prefix=APIEndpoints.Users.Prefix, tags=["users"])
api_router.include_router(web_app_router, prefix=APIEndpoints.WebApp.Prefix, tags=["web-app"])
