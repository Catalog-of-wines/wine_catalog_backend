import os
from typing import List, Optional

import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext

from server.models import Comment, Wine
from server.validation_functions import (is_valid_email, is_valid_name,
                                         is_valid_password)

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

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
users_collection = db["users"]
comments_collection = db["comments"]


@app.get("/")
async def root():
    return {"message": "This is root page Catalog of wine"}


def process_wine(wine, request: Request):
    vintage = wine.get("vintage")
    diameter = wine.get("diameter")
    brand = wine.get("brand")
    glass = wine.get("glass")
    gastronomic_combination = wine.get("gastronomic_combination")
    color = wine.get("color")

    wine_model = Wine(
        id=str(wine["_id"]),
        kind=wine["kind"],
        name=wine["name"],
        color=color if color is not None else "-",
        wine_type=wine["wine_type"],
        capacity=wine["capacity"],
        package=wine["package"],
        country=wine["country"],
        brand=brand if brand is not None else "-",
        alcohol_percentage=wine["alcohol_percentage"],
        producer=wine["producer"],
        glass=glass if glass is not None else "-",
        gastronomic_combination=gastronomic_combination
        if gastronomic_combination is not None
        else "-",
        grape=wine["grape"],
        vintage=vintage if vintage is not None else "-",
        diameter=diameter if diameter is not None else "-",
        supplier=wine["supplier"],
        price=wine["price"],
        image_url=str(request.url_for("images", path=wine["image_url"])),
        small_image_url=str(request.url_for("images", path=wine["small_image_url"])),
        description=wine["description"],
    )
    return wine_model


@app.get("/catalog/")
async def get_catalog(request: Request, limit: int = 9, skip: int = 0):
    wines = []
    cursor = collection.find().limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


@app.get("/with-package/")
async def get_catalog_with_package(request: Request, limit: int = 9, skip: int = 0):
    wines = []
    cursor = (
        collection.find({"package": "подарункова упаковка"}).limit(limit).skip(skip)
    )
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


# countries must be a list of strings if format "Італія (Italy), Іспанія (Spain)"
@app.get("/by-country/")
async def get_catalog_by_country(
    request: Request,
    countries: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if countries:
        query = {"country": {"$in": countries}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


@app.get("/by-color/")
async def get_catalog_by_color(
    request: Request,
    colors: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if colors:
        query = {"color": {"$in": colors}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


@app.get("/by-wine-type/")
async def get_catalog_by_wine_type(
    request: Request,
    wine_types: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if wine_types:
        query = {"wine_type": {"$in": wine_types}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


@app.get("/by-capacity/")
async def get_catalog_by_capacity(
    request: Request,
    capacities: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if capacities:
        query = {"capacity": {"$in": capacities}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


@app.get("/catalog/{wine_id}/")
async def get_bottle(wine_id: str, request: Request):
    try:
        wine_id_obj = ObjectId(wine_id)
        wine = await collection.find_one({"_id": wine_id_obj})
        if wine:
            processed_wine = process_wine(wine, request)
            return processed_wine
        else:
            raise HTTPException(status_code=404, detail="Wine not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/wine/")
async def get_wine(request: Request, limit: int = 9, skip: int = 0):
    wines = []
    cursor = collection.find({"kind": "wine"}).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


@app.get("/champagne/")
async def get_champagne(request: Request, limit: int = 9, skip: int = 0):
    champagne = []
    cursor = (
        collection.find({"kind": {"$in": ["prosecco", "Ігристе"]}})
        .limit(limit)
        .skip(skip)
    )
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        champagne.append(processed_wine)
    return champagne


@app.get("/aroma/")
async def get_by_aroma(
    request: Request,
    query: str = Query(
        ..., description="Query parameter - gastronomic_combination separated by coma"
    ),
    limit: int = Query(9, gt=0, description="Number of records to return"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
):
    aroma_mappings = await aroma_list_collection.find_one()
    if not aroma_mappings:
        raise HTTPException(
            status_code=500, detail="Word mappings not found in the database"
        )

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
        processed_wine = process_wine(wine, request)
        wines.append(processed_wine)
    return wines


@app.get("/aroma_mappings/")
async def get_aroma_mappings():
    word_mappings = await aroma_list_collection.find_one()
    if not word_mappings:
        raise HTTPException(
            status_code=500, detail="Aroma word mappings not found in the database"
        )

    return list(word_mappings.keys())


@app.get("/food/")
async def get_by_food(
    request: Request,
    query: str = Query(
        ..., description="Query parameter - gastronomic_combination separated by coma"
    ),
    limit: int = Query(9, gt=0, description="Number of records to return"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
):
    foods = []
    query_words = [word.strip() for word in query.split(",")]
    filter_query = {"gastronomic_combination": {"$in": query_words}}
    cursor = collection.find(filter_query).limit(limit).skip(skip)
    async for document in cursor:
        food = document.copy()
        processed_wine = process_wine(food, request)
        foods.append(processed_wine)
    return foods


@app.get("/romantic/")
async def get_romantic(request: Request, limit: int = 9):
    romantic_wines = []
    pipeline = [
        {"$match": {"wine_type": {"$in": ["Сододке", "Напівсолодке"]}}},
        {"$sample": {"size": limit}},
    ]
    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        romantic_wines.append(processed_wine)
    return romantic_wines


@app.get("/festive/")
async def get_festive(request: Request, limit: int = 9):
    festive_wines = []
    pipeline = [
        {
            "$match": {
                "$or": [
                    {"$and": [{"kind": "prosecco"}, {"wine_type": "Солодке"}]},
                    {"$and": [{"kind": "Ігристе"}, {"wine_type": "Солодке"}]},
                ]
            }
        },
        {"$sample": {"size": limit}},
    ]
    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine, request)
        festive_wines.append(processed_wine)
    return festive_wines


@app.post("/register")
async def register_user(
    name: str, email: str, password: str, phone: Optional[str] = None
):

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if not is_valid_name(name):
        raise HTTPException(status_code=400, detail="Invalid name")

    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email")

    if not is_valid_password(password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password! When creating a password, please ensure that it meets the following criteria: Must be 8 or more characters in length, contain at least one uppercase letter (A-Z), contain at least one lowercase letter (a-z), contain at least one number (0-9). Please choose a password that fulfills these requirements for enhanced security.",
        )

    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=409, detail="User with the same email already exists"
        )

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)

    user_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": hashed_password,
    }
    result = await users_collection.insert_one(user_data)
    user_id = str(result.inserted_id)

    return {"message": "User registered successfully", "user_id": user_id}


@app.post("/comments/")
async def create_comment(comment: Comment):
    comment_document = {
        "user_id": comment.user_id,
        "wine_id": comment.wine_id,
        "text": comment.text,
        "rating": comment.rating
    }
    new_comment = await db.comments.insert_one(comment_document)
    comment_id = str(new_comment.inserted_id)
    return {"comment_id": comment_id}


async def get_comments_by_wine_id(wine_id: str):
    comments = await db.comments.find({"wine_id": wine_id}).to_list(length=None)
    comments_with_str_id = [
        {**comment, "_id": str(comment["_id"])} for comment in comments
    ]
    return comments_with_str_id


@app.get("/wine/{wine_id}/comments")
async def get_wine_comments(wine_id: str):
    comments = await get_comments_by_wine_id(wine_id)
    return comments


@app.get("/images/{image_path:path}")
async def get_image(image_path: str):
    full_path = os.path.join(IMAGES_DIR, image_path)
    return FileResponse(full_path)
