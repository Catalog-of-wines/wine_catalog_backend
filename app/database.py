# wine/app/database.py
import motor.motor_asyncio

from app.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.catalog

collection = db["wines"]
aroma_list_collection = db["aroma_list"]
users_collection = db["users"]
comments_collection = db["comments"]


# This is the code to restore the existing index if it breaks for some reason
'''
try:
    collection.drop_index("description.aroma_text")
except Exception as e:
    pass

try:
    collection.create_index(
        [("description.aroma", "text")],
        default_language="russian",
        language_override="none",
    )
except Exception as e:
    pass
'''
