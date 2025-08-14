from fastapi import FastAPI

from app.auth import routes as auth_routes
from app.courses import routes as courses_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
# app.include_router(courses_routes.router, prefix="/courses", tags=["Courses"])
