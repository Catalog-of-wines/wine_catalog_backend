#conftest.py

import pytest
import mongomock

from app.models import User
# from app.database import db, collection, users_collection, comments_collection, aroma_list_collection

# @pytest.fixture()
# def mongo_mock(monkeypatch):
#     client = mongomock.MongoClient()
#     db = client.get_database("catalog")
#     col = db.get_collection("users_collection")
#     emp_data: User = {
#         "name": "string",
#         "email": "user@example.com",
#         "password": "String123",
#         "telephone": "string"
#     }
#
#     col.insert_one(emp_data)
#
#     def fake_db():
#         return db
#
#     monkeypatch.setattr("main.get_db", fake_db)

