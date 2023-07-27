from datetime import date

from fastapi import APIRouter, HTTPException

from app.auth.utils import create_jwt_token, pwd_context
from app.auth.validation_functions import (
    is_valid_email,
    is_valid_name,
    is_valid_password,
)
from app.database import users_collection
from app.models import User

router_auth = APIRouter()


@router_auth.post("/register", tags=["auth"])
async def register_user(user: User):
    if not user.name or not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if not is_valid_name(user.name):
        raise HTTPException(status_code=400, detail="Invalid name")

    if not is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")

    if not is_valid_password(user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password! When creating a password, please ensure that it meets the following criteria: Must be 8 or more characters in length, contain at least one uppercase letter (A-Z), contain at least one lowercase letter (a-z), contain at least one number (0-9). Please choose a password that fulfills these requirements for enhanced security.",
        )

    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=409, detail="User with the same email already exists"
        )

    hashed_password = pwd_context.hash(user.password)

    user_data = {
        "name": user.name,
        "email": user.email,
        "phone": user.telephone,
        "password": hashed_password,
    }
    result = await users_collection.insert_one(user_data)

    user_id = str(result.inserted_id)
    token = create_jwt_token(user_id)

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "token_type": "bearer",
        "access_token": token,
    }


@router_auth.post("/login", tags=["auth"])
async def login(user: User):
    user_object = await users_collection.find_one({"email": user.email})
    if user_object and pwd_context.verify(user.password, user_object["password"]):
        token = create_jwt_token(str(user_object["_id"]))
        return {
            "user_id": str(user_object["_id"]),
            "access_token": token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
