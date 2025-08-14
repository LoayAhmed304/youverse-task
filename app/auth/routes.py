from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.db.db import engine, Base
from app.db import models, db
from app import schemas
from .utils import hash_password, verify_password, create_token, get_current_user

router = APIRouter()


@router.post("/signup")
def signup(data: schemas.SignupRequest, response: Response, db: Session = Depends(db.get_db)):
    existing_user = db.query(models.User).filter(models.User.username == data.username
                                                 or models.User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username or email already exists")

    hashed_password = hash_password(data.password)

    user = models.User(username=data.username, email=data.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(
        data={"user": {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }})

    response.set_cookie(key="jwt", value=token, httponly=True, samesite="lax")

    return {
        "status": "success",
        "data": {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@router.post("/login")
def login(data: schemas.LoginRequest, response: Response, db: Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_token(
        data={"user": {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }})
    response.set_cookie(key="jwt", value=token, httponly=True, samesite="lax")

    return {
        "status": "success",
        "data": {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@router.get("/me")
def read_current_user(request: Request):
    user = get_current_user(request)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return {"status": "success", "data": user}


@router.post("/logout")
def logout(request: Request, response: Response):
    if "jwt" in request.cookies:
        response.delete_cookie("jwt")
        return {"status": "success"}
    else:
        return {"status": "fail", "message": "Already logged out"}
