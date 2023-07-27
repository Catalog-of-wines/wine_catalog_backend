# wine/app/auth/routes.py
from datetime import date

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query, Header

from app.auth.utils import decode_jwt_token
from app.database import comments_collection, users_collection
from app.models import Comment, User

router_comments = APIRouter()


async def protected_route(token: str = Query(...)):
    token_data = decode_jwt_token(token)
    user = await users_collection.find_one({"_id": ObjectId(token_data["user_id"])})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**user)


@router_comments.post("/comments/", tags=["comments"])
async def create_comment(comment: Comment, token: str = Header(...)):
    print("Token", token)
    try:
        user = await protected_route(token)
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)

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


async def get_comments_by_wine_id(wine_id: str, response_model=list[Comment]):
    comments = await comments_collection.find({"wine_id": wine_id}).to_list(length=None)
    comments_with_str_id = [
        {**comment, "_id": str(comment["_id"])} for comment in comments
    ]
    return comments_with_str_id


@router_comments.get("/wine/{wine_id}/comments", tags=["comments"], response_model=list[Comment])
async def get_wine_comments(wine_id: str):
    comments = await get_comments_by_wine_id(wine_id)
    return comments
