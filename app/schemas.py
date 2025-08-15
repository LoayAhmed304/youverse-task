from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class CourseRequest(BaseModel):
    name: str
    description: str
    category: str


class CourseCreate(BaseModel):
    name: str
    description: str
    category: str
    owner_id: int


class VideoRequest(BaseModel):
    title: str
    description: str
    course_id: int
    duration: float
    category: str
    subcategory: str


class VideoCreate(VideoRequest):
    asset_id: str
