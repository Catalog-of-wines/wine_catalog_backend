import pytest
# from fastapi.testclient import TestClient
from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_catalog():
    response = client.get("/catalog/")
    assert response.status_code == 200
    # assert isinstance(response.json(), list)


def test_get_catalog_with_package():
    response = client.get("/with-package/")
    assert response.status_code == 200
    # assert isinstance(response.json(), list)

# полагаю из за вызова и асинхронных функций и также
# подключения к базе данных с помощью асинхронного драйвера -
# нужно писать асинхронные тесты