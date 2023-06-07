# import uvicorn
#
# if __name__ == "__main__":
#     uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)

import os
from fastapi import FastAPI
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
# подключаемся к БД catalog, если её нет, то будет создана
db = client.catalog

collection = db["wines"]

wine1 = {
    "name": "Кампаньола Піно Гріджіо Венеціє",
    "description": "some description",
    "color": "White",
    "type": "Dry",
    "brand": "Campagnola",
    "country": "Italy",
    "region": "Veneto",
    "grape_variety": ["аперитив", "морепродукти", "салати"],
    "capacity": 0.75,
    "price": 3257.00,
    "alcohol_percentage": 10.6,
    "classification": "IGT",
}

# ins_result = collection.insert_one(wine1)  # добавляет одну запись в коллекцию collection
