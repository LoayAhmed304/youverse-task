from fastapi import HTTPException, status, Request

import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.db import models

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


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
