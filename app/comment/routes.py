from fastapi import APIRouter
from datetime import date

from fastapi import HTTPException, Query

from bson import ObjectId

from app.auth.utils import decode_jwt_token
from app.models import Comment, User

from app.database import (
    users_collection,
    comments_collection
)


router = APIRouter()


@router.get("/ccc/", tags=["ccc"])
async def get_temp():
    return {"message": "This is ccccccccccc"}





async def protected_route(token: str = Query(...)):
    token_data = decode_jwt_token(token)
    user = await users_collection.find_one({"_id": ObjectId(token_data["user_id"])})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**user)


@router.post("/comments/")
async def create_comment(token, comment: Comment):
    if protected_route(token):
        comment_document = {
            "user_id": comment.user_id,
            "wine_id": comment.wine_id,
            "text": comment.text,
            "rating": comment.rating,
            "date": str(date.today()),
        }
        new_comment = await comments_collection.insert_one(comment_document)
        comment_id = str(new_comment.inserted_id)
        return {"comment_id": comment_id}


async def get_comments_by_wine_id(wine_id: str):
    comments = await comments_collection.find({"wine_id": wine_id}).to_list(length=None)
    comments_with_str_id = [
        {**comment, "_id": str(comment["_id"])} for comment in comments
    ]
    return comments_with_str_id


@router.get("/wine/{wine_id}/comments")
async def get_wine_comments(wine_id: str):
    comments = await get_comments_by_wine_id(wine_id)
    return comments