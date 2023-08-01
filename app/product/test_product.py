# code from file wine/app/product/test_product1.py
# There are tests for testing products endpoints

import unittest
import pytest
from httpx import AsyncClient
import nest_asyncio

from app.main import app

nest_asyncio.apply()

@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_get_catalog():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/catalog/")
    assert response.status_code == 200
    assert response.json()[0]["kind"] in ['prosecco', 'wine', 'Ігристе']


@pytest.mark.anyio
async def test_get_catalog_by_country():
    query = ["Італія (Italy)"]
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/by-country/", params={"query": query})
    assert response.status_code == 200
    for wine in response.json():
        assert "Італія (Italy)" in wine["country"]


@pytest.mark.anyio
async def test_get_wine():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/wine/")
    assert response.status_code == 200
    assert response.json()[0]["kind"] == 'wine'


@pytest.mark.anyio
async def test_get_champagne():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/champagne/")

    print()
    print("----------------response.json()", response.json())
    assert response.json()[8]["kind"] in ['prosecco', 'Ігристе']
    assert response.json()[8]["kind"] not in ['prosecco1', 'Ігристе1']


# the end of code from file wine/app/product/test_product1.py