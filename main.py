# import uvicorn
#
# if __name__ == "__main__":
#     uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)
import asyncio
import os
import random

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi import Query
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

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.catalog
collection = db["wines"]
aroma_list_collection = db["aroma_list"]


@app.get("/")
async def root():
    return {"message": "This is root page Catalog of wine"}


@app.get("/catalog/")
async def get_catalog(limit: int = 9, skip: int = 0):
    wines = []
    cursor = collection.find().limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        wine["_id"] = str(wine["_id"])  # Convert ObjectId to string
        wines.append(wine)
    return wines


@app.get("/catalog/{wine_id}/")
async def get_bottle(wine_id: str):
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


@app.get("/wine/")
async def get_wine(limit: int = 9, skip: int = 0):
    wines = []
    cursor = collection.find({"kind": "wine"}).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        wine["_id"] = str(wine["_id"])
        wines.append(wine)
    return wines


@app.get("/champagne/")
async def get_champagne(limit: int = 9, skip: int = 0):
    champagne = []
    cursor = collection.find({"kind": {"$in": ["prosecco", "Ігристе"]}}).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        wine["_id"] = str(wine["_id"])
        champagne.append(wine)
    return champagne


@app.get("/aroma/")
async def get_by_aroma(
        query: str = Query(..., description="Query parameter - gastronomic_combination separated by coma"),
        limit: int = Query(9, gt=0, description="Number of records to return"),
        skip: int = Query(0, ge=0, description="Number of records to skip")
):

    aroma_mappings = await aroma_list_collection.find_one()
    if not aroma_mappings:
        raise HTTPException(status_code=500, detail="Word mappings not found in the database")

    wines = []
    query_words = query.split(",")
    transformed_words = [aroma_mappings.get(word, word) for word in query_words]

    regex_pattern = "(?=.*{})" * len(transformed_words)
    regex_pattern = regex_pattern.format(*transformed_words)
    regex_query = {"$regex": regex_pattern, "$options": "i"}

    filter_query = {"description.aroma": regex_query}
    cursor = collection.find(filter_query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        wine["_id"] = str(wine["_id"])
        wines.append(wine)
    return wines


@app.get("/aroma_mappings/")
async def get_aroma_mappings():
    word_mappings = await aroma_list_collection.find_one()
    if not word_mappings:
        raise HTTPException(status_code=500, detail="Aroma word mappings not found in the database")

    return list(word_mappings.keys())


@app.get("/food/")
async def get_by_food(
        query: str = Query(..., description="Query parameter - gastronomic_combination separated by coma"),
        limit: int = Query(9, gt=0, description="Number of records to return"),
        skip: int = Query(0, ge=0, description="Number of records to skip")
):
    foods = []
    query_words = [word.strip() for word in query.split(",")]
    filter_query = {"gastronomic_combination": {"$in": query_words}}
    cursor = collection.find(filter_query).limit(limit).skip(skip)
    async for document in cursor:
        food = document.copy()
        food["_id"] = str(food["_id"])
        foods.append(food)
    return foods


@app.get("/romantic/")
async def get_romantic(limit: int = 9):
    romantic_wines = []
    pipeline = [{"$match": {"wine_type": {"$in": ["Сододке", "Напівсолодке"]}}}, {"$sample": {"size": limit}}]
    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        wine = document.copy()
        wine["_id"] = str(wine["_id"])
        romantic_wines.append(wine)
    return romantic_wines


@app.get("/festive/")
async def get_festive(limit: int = 9):
    festive_wines = []
    pipeline = [
        {
            "$match": {
                "$or": [
                    {"$and": [{"kind": "prosecco"}, {"wine_type": "Солодке"}]},
                    {"$and": [{"kind": "Ігристе"}, {"wine_type": "Солодке"}]}
                ]
            }
        },
        {"$sample": {"size": limit}}
    ]
    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        wine = document.copy()
        wine["_id"] = str(wine["_id"])
        festive_wines.append(wine)
    return festive_wines
