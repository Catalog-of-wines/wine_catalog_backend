from typing import Optional, List

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    telephone: Optional[str] = None


class Comment(BaseModel):
    id: int
    text: str
    wine_id: str
    users: List[User]


class Wine(BaseModel):
    kind: str
    name: str
    color: str
    wine_type: str
    capacity: str
    package: str
    country: str
    brand: str
    alcohol_percentage: str
    producer: str
    glass: str
    gastronomic_combination: str
    grape: str
    vintage: str
    diameter: str
    supplier: str
    price: str
    image_url: str
    small_image_url: str
    comment_id: int
