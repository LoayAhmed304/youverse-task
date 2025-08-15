from app.auth.utils import get_current_user
from fastapi import HTTPException, Request, status, UploadFile
from sqlalchemy.orm import Session

from app.db import models, db
from app import schemas


def check_video_permission(course_id: int, request: Request, db: Session) -> bool:

    current_user = get_current_user(request)

    owner_id = db.query(models.Course.owner_id).filter(models.Course.id == course_id).first()
    if not owner_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if owner_id[0] != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create video for this course")

    return True


def validate_all_videos(request: Request, all_files: list[UploadFile], videos_metadata: list, db: Session, current_user: dict) -> None:
    for i, video_data in enumerate(videos_metadata):

        video_request = schemas.VideoRequest(**video_data)

        if video_request.duration <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid video duration")

        if not all_files[i].filename.endswith(('.mp4', '.mkv', '.avi')):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid file format among the files. Only .mp4, .mkv, and .avi are allowed")

        video_exist = db.query(models.Video).filter(models.Video.title == video_request.title,
                                                    models.Video.course_id == video_request.course_id).first()
        if video_exist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Video already exists")

        check_video_creation_permission(video_request.course_id, request, db)
