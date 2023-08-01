# wine/app/database.py
import asyncio
import motor.motor_asyncio

from app.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
# for async tests
# client.get_io_loop = asyncio.get_running_loop
db = client.catalog

collection = db["wines"]
users_collection = db["users"]
comments_collection = db["comments"]
aroma_list_collection = db["aroma_list"]


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
