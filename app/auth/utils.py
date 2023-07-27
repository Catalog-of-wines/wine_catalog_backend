from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from jwt import PyJWTError
from passlib.context import CryptContext

from app.settings import settings


def create_jwt_token(user_id: str) -> str:
    expiration = datetime.utcnow() + timedelta(
        minutes=settings.JWT_EXPIRATION_TIME_MINUTES
    )
    data = {"user_id": user_id, "exp": expiration}
    token = jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    try:
        decoded_data = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return decoded_data
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
