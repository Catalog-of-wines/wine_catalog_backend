import logging
import os
from datetime import datetime, timedelta, date
from typing import List, Optional

import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

from server.models import Comment, Wine, User
from server.validation_functions import is_valid_email, is_valid_name, is_valid_password

app = FastAPI()

BASE_URL = "http://3.123.93.54/"

JWT_SECRET = "5abd14e8157a6bfeed7b88e1b5439fc015d16463024344cbc1bdd6d415299dbd"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 5000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://superb-malasada-e059fa.netlify.app",
    "https://64b79ef90dd1ff62287a5770--peppy-seahorse-d9c071.netlify.app/",
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
    logger = logging.getLogger("uvicorn")
    logger.info("Received a request to root endpoint")
    return {"message": "This is root page Catalog of wine"}


def process_wine(wine):
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
        image_url=BASE_URL + "images/" + wine["image_url"],
        small_image_url=BASE_URL + "images/" + wine["small_image_url"],
        description=wine["description"],
    )
    return wine_model


@app.get("/catalog/")
async def get_catalog(request: Request, limit: int = 9, skip: int = 0):
    wines = []
    cursor = collection.find().limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
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
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


# countries must be a list of strings in format "Італія (Italy), Іспанія (Spain)"
@app.get("/by-country/")
async def get_catalog_by_country(
    query: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if query:
        query = {"country": {"$in": query}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


@app.get("/by-color/")
async def get_catalog_by_color(
    query: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if query:
        query = {"color": {"$in": query}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


@app.get("/by-wine-type/")
async def get_catalog_by_wine_type(
    query: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if query:
        query = {"wine_type": {"$in": query}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


@app.get("/by-capacity/")
async def get_catalog_by_capacity(
    query: Optional[List[str]] = Query(None),
    limit: int = 9,
    skip: int = 0,
):
    wines = []
    if query:
        query = {"capacity": {"$in": query}}
    else:
        query = {}

    cursor = collection.find(query).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


@app.get("/catalog/{wine_id}/")
async def get_bottle(wine_id: str):
    try:
        wine_id_obj = ObjectId(wine_id)
        wine = await collection.find_one({"_id": wine_id_obj})
        if wine:
            processed_wine = process_wine(wine)
            return processed_wine
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
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


@app.get("/champagne/")
async def get_champagne(limit: int = 9, skip: int = 0):
    champagne = []
    cursor = (
        collection.find({"kind": {"$in": ["prosecco", "Ігристе"]}})
        .limit(limit)
        .skip(skip)
    )
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        champagne.append(processed_wine)
    return champagne


@app.get("/aroma/")
async def get_by_aroma(
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
        processed_wine = process_wine(wine)
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
        processed_wine = process_wine(food)
        foods.append(processed_wine)
    return foods


@app.get("/romantic/")
async def get_romantic(limit: int = 9):
    romantic_wines = []
    pipeline = [
        {"$match": {"wine_type": {"$in": ["Сододке", "Напівсолодке"]}}},
        {"$sample": {"size": limit}},
    ]
    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        romantic_wines.append(processed_wine)
    return romantic_wines


@app.get("/festive/")
async def get_festive(limit: int = 9):
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
        processed_wine = process_wine(wine)
        festive_wines.append(processed_wine)
    return festive_wines


def create_jwt_token(user_id: str) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    data = {"user_id": user_id, "exp": expiration}
    token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    try:
        decoded_data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_data
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/register")
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


@app.post("/login")
async def login(user: User):
    user_object = await users_collection.find_one({"email": user.email})
    if user_object and pwd_context.verify(user.password, user_object["password"]):
        token = create_jwt_token(str(user_object["_id"]))
        return {"user_id": str(user_object["_id"]), "access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get("/user/{user_id}")
async def get_personal_account(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user_data = {"id": str(user["_id"]), "name": user["name"]}
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def protected_route(token: str = Query(...)):
    token_data = decode_jwt_token(token)
    user = await users_collection.find_one({"_id": ObjectId(token_data["user_id"])})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**user)


@app.post("/comments/")
async def create_comment(token, comment: Comment):
    if protected_route(token):
        comment_document = {
            "user_id": comment.user_id,
            "wine_id": comment.wine_id,
            "text": comment.text,
            "rating": comment.rating,
            "date": str(date.today())
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
