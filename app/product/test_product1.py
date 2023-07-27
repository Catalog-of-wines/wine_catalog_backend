# # wine/tests/test_product.py
# import pytest
# from motor.motor_asyncio import AsyncIOMotorClient
# from fastapi.testclient import TestClient
#
# # use this import if you want to test from the root directory
# # sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from app.main import app
# from app.settings import settings
#
#
# @pytest.fixture(scope="function")
# def db_client():
#     # Подключаемся к тестовой базе данных
#     client = AsyncIOMotorClient(settings.MONGODB_URL)
#     db = client["wines_copy"]  # Подставьте имя вашей тестовой базы данных
#     yield db
#     # Отключаемся от базы данных после выполнения всех тестов
#     client.close()
#
# @pytest.fixture
# def test_client(db_client):
#     # Создаем асинхронный клиент тестирования с передачей тестового клиента базы данных
#     with TestClient(app) as client:
#         yield client
#
# # Теперь вы можете использовать фикстуры test_client и db_client в ваших тестах:
# def test_get_catalog(test_client):
#     response = test_client.get("/catalog/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#
# def test_get_catalog_with_package(test_client):
#     response = test_client.get("/with-package/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#
#
#
# # run with "pytest" command from command line
