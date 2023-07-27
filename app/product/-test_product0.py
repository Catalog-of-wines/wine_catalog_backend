import pytest
from fastapi.testclient import TestClient
from app.main import app


# client = TestClient(app)
#
#
# def test_get_catalog():
#     response = client.get("/catalog/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#
#
# def test_get_catalog_with_package():
#     response = client.get("/with-package/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

from fastapi import FastAPI
app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
