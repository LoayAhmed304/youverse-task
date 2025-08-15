from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import routes as auth_routes
from app.courses import routes as courses_routes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(courses_routes.router, prefix="/courses", tags=["Courses"])
