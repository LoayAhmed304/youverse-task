from app.auth.utils import get_current_user
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db import models, db


def check_video_creation_permission(course_id: int, request: Request, db: Session) -> bool:

    current_user = get_current_user(request)

    owner_id = db.query(models.Course.owner_id).filter(models.Course.id == course_id).first()

    if not owner_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if owner_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create video for this course")

    return True
