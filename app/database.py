# wine/app/database.py
import motor.motor_asyncio

from app.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.catalog
collection = db["wines"]
aroma_list_collection = db["aroma_list"]
users_collection = db["users"]
comments_collection = db["comments"]
