from typing import Dict, Optional

from pydantic import BaseModel, EmailStr


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
    user_id: str
    rating: int

class Wine(BaseModel):
    id: str
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
    description: Dict[str, str]
