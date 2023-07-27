# wine/app/product/routes.py:
from bson import ObjectId
from fastapi import APIRouter, Query, HTTPException

from app.database import aroma_list_collection, collection
from app.dependencies import CommonsDep
from app.models import Wine
from app.product.utils import process_wine


router_products = APIRouter()


@router_products.get("/catalog/", tags=["products"], response_model=list[Wine])
async def get_catalog(commons: CommonsDep):
    wines = []
    limit = commons["limit"]
    skip = commons["skip"]
    cursor = collection.find().limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


@router_products.get("/with-package/", tags=["products"], response_model=list[Wine])
async def get_catalog_with_package(commons: CommonsDep):
    wines = []
    limit = commons["limit"]
    skip = commons["skip"]
    cursor = (
        collection.find({"package": "подарункова упаковка"}).limit(limit).skip(skip)
    )
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


# countries must be a list of strings in format "Італія (Italy), Іспанія (Spain)"
@router_products.get("/by-country/", tags=["products"], response_model=list[Wine])
async def get_catalog_by_country(commons: CommonsDep):
    wines = []
    query = commons["query"]
    limit = commons["limit"]
    skip = commons["skip"]
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


@router_products.get("/by-color/", tags=["products"], response_model=list[Wine])
async def get_catalog_by_color(commons: CommonsDep):
    wines = []
    query = commons["query"]
    limit = commons["limit"]
    skip = commons["skip"]
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


@router_products.get("/by-wine-type/", tags=["products"], response_model=list[Wine])
async def get_catalog_by_wine_type(commons: CommonsDep):
    wines = []
    query = commons["query"]
    limit = commons["limit"]
    skip = commons["skip"]
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


@router_products.get("/by-capacity/", tags=["products"], response_model=list[Wine])
async def get_catalog_by_capacity(commons: CommonsDep):
    wines = []
    query = commons["query"]
    limit = commons["limit"]
    skip = commons["skip"]
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


@router_products.get("/catalog/{wine_id}/", tags=["products"], response_model=Wine)
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


@router_products.get("/wine/", tags=["products"], response_model=list[Wine])
async def get_wine(commons: CommonsDep):
    wines = []
    limit = commons["limit"]
    skip = commons["skip"]
    cursor = collection.find({"kind": "wine"}).limit(limit).skip(skip)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        wines.append(processed_wine)
    return wines


@router_products.get("/champagne/", tags=["products"], response_model=list[Wine])
async def get_champagne(commons: CommonsDep):
    champagne = []
    limit = commons["limit"]
    skip = commons["skip"]
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


@router_products.get("/aroma/", tags=["products"], response_model=list[Wine])
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


@router_products.get("/aroma_mappings/", tags=["products"])
async def get_aroma_mappings():
    word_mappings = await aroma_list_collection.find_one()
    if not word_mappings:
        raise HTTPException(
            status_code=500, detail="Aroma word mappings not found in the database"
        )

    return list(word_mappings.keys())


@router_products.get("/food/", tags=["products"], response_model=list[Wine])
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


@router_products.get("/romantic/", tags=["products"], response_model=list[Wine])
async def get_romantic(commons: CommonsDep):
    romantic_wines = []
    limit = commons["limit"]
    skip = commons["skip"]
    pipeline = [
        {"$match": {"wine_type": {"$in": ["Сододке", "Напівсолодке"]}}},
        {"$skip": skip},
        {"$sample": {"size": limit}},
    ]
    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        romantic_wines.append(processed_wine)
    return romantic_wines


@router_products.get("/festive/", tags=["products"], response_model=list[Wine])
async def get_festive(commons: CommonsDep):
    festive_wines = []
    limit = commons["limit"]
    skip = commons["skip"]
    pipeline = [
        {
            "$match": {
                "$or": [
                    {"$and": [{"kind": "prosecco"}, {"wine_type": "Солодке"}]},
                    {"$and": [{"kind": "Ігристе"}, {"wine_type": "Солодке"}]},
                ]
            }
        },
        {"$skip": skip},
        {"$sample": {"size": limit}},
    ]
    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        wine = document.copy()
        processed_wine = process_wine(wine)
        festive_wines.append(processed_wine)
    return festive_wines
