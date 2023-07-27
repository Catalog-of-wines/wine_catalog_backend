from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.database import users_collection

router_users = APIRouter()


@router_users.get("/user/{user_id}", tags=["users"])
async def get_personal_account(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user_data = {"id": str(user["_id"]), "name": user["name"]}
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User not found")
