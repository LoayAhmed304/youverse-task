from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import models, db
from app import mux
from app import schemas
from app.auth.utils import get_current_user
from .utils import check_video_creation_permission

router = APIRouter()


@router.get("/")
def get_courses(db: Session = Depends(db.get_db)):
    courses = db.query(models.Course).all()

    return {"status": "success", "data": courses}


@router.post("/")
def create_course(course: schemas.CourseRequest, request: Request, db: Session = Depends(db.get_db), current_user: dict = Depends(get_current_user)):

    new_course: schemas.CourseCreate = schemas.CourseCreate(**course.model_dump(), owner_id=current_user["user_id"])

    db_course = models.Course(**new_course.model_dump())
    db.add(db_course)
    try:
        db.commit()
        db.refresh(db_course)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course already exists with this name")

    return {"status": "success", "data": db_course}


@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(db.get_db), current_user: dict = Depends(get_current_user)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if db_course.owner_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this course")

    db.delete(db_course)
    db.commit()
    return {"status": "success", "message": "Course deleted successfully"}


@router.post("/videos")
def upload_video(request: Request,
                 title: str = Form(...),
                 description: str = Form(...),
                 duration: float = Form(...),
                 category: str = Form(...),
                 subcategory: str = Form(...),
                 course_id: int = Form(...),
                 file: UploadFile = File(...),
                 db: Session = Depends(db.get_db),
                 current_user: dict = Depends(get_current_user)):

    if not file.filename.endswith(('.mp4', '.mkv', '.avi')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid video format")

    video_exist = db.query(models.Video).filter(models.Video.title == title, models.Video.course_id == course_id).first()
    if video_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Video already exists")

    can_create = check_video_creation_permission(course_id, request, db)

    if not can_create:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create video for this course")

    asset_id = mux.upload_to_mux(file)

    new_video = schemas.VideoCreate(title=title,
                                    description=description,
                                    duration=duration,
                                    category=category,
                                    subcategory=subcategory,
                                    course_id=course_id,
                                    asset_id=asset_id)

    video = models.Video(**new_video.model_dump())
    db.add(video)
    db.commit()
    db.refresh(video)

    return {"status": "success", "data": video}
