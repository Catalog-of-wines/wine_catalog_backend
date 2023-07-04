import os
from typing import Optional, List

from pydantic import BaseModel,  EmailStr


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    telephone: Optional[str] = None

    class Config:
        orm_mode = True


class Comment(BaseModel):
    text: str
    wine_id: str
    # user: User_id # надо подправить


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
    # comments: List[comment_id] = []_id: int # надо подправить
    image_url: str
    small_image_url: str



