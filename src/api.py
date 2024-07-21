from typing import List, Optional

from fastapi import APIRouter, Depends

from pydantic import BaseModel

from src.routers.api_enpoints import APIEndpoints
from src.routers.admin import router as admin_router
from src.routers.user import router as user_router
from src.routers.subject import router as subject_router
from src.routers.private_course import router as private_course_router
from src.routers.tutor_course import router as tutor_course_router
from src.routers.web_app import router as web_app_router
from src.routers.home import router as home_router


authenticated_api_router = APIRouter()

authenticated_api_router.include_router(home_router, prefix=APIEndpoints.Home.Prefix, tags=["home"])
authenticated_api_router.include_router(admin_router, prefix=APIEndpoints.Admin.Prefix, tags=["admin"])
authenticated_api_router.include_router(private_course_router, prefix=APIEndpoints.PrivateCourses.Prefix, tags=["private-courses"])
authenticated_api_router.include_router(subject_router, prefix=APIEndpoints.Subjects.Prefix, tags=["subjects"])
authenticated_api_router.include_router(tutor_course_router, prefix=APIEndpoints.TutorCourse.Prefix, tags=["tutor-courses"])
authenticated_api_router.include_router(user_router, prefix=APIEndpoints.Users.Prefix, tags=["users"])
authenticated_api_router.include_router(web_app_router, prefix=APIEndpoints.WebApp.Prefix, tags=["web-app"])
