# import pytest
# from motor.motor_asyncio import AsyncIOMotorClient
# from fastapi.testclient import TestClient  # Use TestClient from fastapi.testclient
#
# # Import your FastAPI app from the correct location based on your project structure
# from app.main import app
# from app.settings import settings
#
#
# # @pytest.fixture(scope="function")  # Change scope to "function"
# # def db_client():
# #     # Подключаемся к тестовой базе данных
# #     client = AsyncIOMotorClient(settings.MONGODB_URL)
# #     db = client["wines_copy"]  # Подставьте имя вашей тестовой базы данных
# #     yield db
# #     # Отключаемся от базы данных после выполнения теста
# #     client.close()
#
#
# @pytest.fixture
# def test_client():
#     # Создаем синхронный клиент тестирования с передачей тестового клиента базы данных
#     with TestClient(app) as client:
#         yield client
#
#
# # Теперь вы можете использовать фикстуры test_client и db_client в ваших тестах:
# def test_get_catalog(test_client):
#     response = test_client.get("/catalog/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#
#
# def test_get_catalog_with_package(test_client):
#     response = test_client.get("/with-package/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
