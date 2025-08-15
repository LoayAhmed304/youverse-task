import json
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import models, db
from app import mux
from app import schemas
from app.auth.utils import get_current_user
from .utils import check_video_permission, validate_all_videos

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

    can_create = check_video_permission(course_id, request, db)

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


"""Upload a batch of videos
This takes a json object containing array of each video's metadata. "[ {}, {} ]"
Note that the list must match the order of the uploaded files.
Currently, it works by sending it as a text on Postman.
"""


@router.post("/videos/batch")
def batch_upload_videos(request: Request,
                        all_data: str = Form(...),
                        all_files: list[UploadFile] = File(...),
                        db: Session = Depends(db.get_db),
                        current_user: dict = Depends(get_current_user)):
    # load all videos meta data into an array
    videos_metadata = []
    try:
        videos_metadata = json.loads(all_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format")

    validate_all_videos(request, all_files, videos_metadata, db, current_user)

    # now all videos are validated and their meta data, now we upload them all.
    videos_result = []
    for i, file in enumerate(all_files):
        file_metadata = videos_metadata[i]
        video_data = upload_video(request=request, **file_metadata, file=file, db=db, current_user=current_user).get("data")
        video = {
            "title": video_data.title,
            "course_id": video_data.course_id,
            "duration": video_data.duration,
            "category": video_data.category,
            "subcategory": video_data.subcategory,
            "description": video_data.description,
            "asset_id": video_data.asset_id
        }
        videos_result.append(video)

    return {"status": "success", "data": videos_result}


@router.delete("/videos/{asset_id}")
def delete_video(request: Request, asset_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(db.get_db)):
    video = db.query(models.Video).filter(models.Video.asset_id == asset_id).first()
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    can_delete = check_video_permission(video.course_id, request, db)

    if not can_delete:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete video for this course")

    try:
        mux.delete_asset(asset_id)
        db.delete(video)
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete video from the service provider")

    return {"status": "success", "detail": "Video deleted successfully"}
