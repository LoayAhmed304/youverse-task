from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.db.db import engine, Base
from app.db import models, db
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from app import schemas

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()

    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")


def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't verify user",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("jwt")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token found")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user: models.User = payload.get("user")
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user


@app.post("/signup")
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


@app.post("/login")
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


@app.get("/me")
def read_current_user(request: Request):
    user = get_current_user(request)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return {"status": "success", "data": user}


@app.post("/logout")
def logout(request: Request, response: Response):
    if "jwt" in request.cookies:
        response.delete_cookie("jwt")
        return {"status": "success"}
    else:
        return {"status": "fail", "message": "Already logged out"}
