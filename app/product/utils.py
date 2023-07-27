from app.models import Wine
from app.settings import settings


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
        image_url=settings.BASE_URL + "images/" + wine["image_url"],
        small_image_url=settings.BASE_URL + "images/" + wine["small_image_url"],
        description=wine["description"],
    )
    return wine_model

