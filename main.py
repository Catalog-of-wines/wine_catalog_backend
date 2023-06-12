# import uvicorn
#
# if __name__ == "__main__":
#     uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)
import asyncio
import os

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import motor.motor_asyncio


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.catalog

collection = db["wines"]


@app.get("/catalog")
async def get_wines():
    wines = []
    async for document in collection.find():
        wine = document.copy()
        wine["_id"] = str(wine["_id"])  # Convert ObjectId to string
        wines.append(wine)
    return wines


@app.get("/catalog/{wine_id}")
async def get_wine(wine_id: str):
    try:
        wine_id_obj = ObjectId(wine_id)
        wine = await collection.find_one({"_id": wine_id_obj})
        if wine:
            wine["_id"] = str(wine["_id"])
            return wine
        else:
            raise HTTPException(status_code=404, detail="Wine not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ins_result = collection.insert_one(wine1)
