from pydantic import BaseModel
from typing import List
from bson import ObjectId


class Wine(BaseModel):
    id: ObjectId
    name: str
    description: str
    color: str
    type: str  # type of wine (Sparkling, Dry wine)
    brand: str
    country: str
    region: str
    grape_variety: str  # the name of grape the wine made from
    capacity: float  # how much of liquor in a bottle
    year: int
    producer: str
    gastronomic_combination: List[str]  # best food combinations
    price: float
    alcohol_percentage: float
    rating: float
    classification: str
    package: bool  # is package available or not
    is_featured: bool
    decantation_necessary: bool
    provider: str
    image_url: str
