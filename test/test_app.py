import sys

import pytest
from app import app
from db.db import DB
from fastapi.testclient import TestClient

sys.path.append("..")


class TestDB:
    def test_postgresql_table_exists(self):
        db = DB()
        table_name = "short_urls"
        with db.p:
            with db.p.cursor() as cursor:
                query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
                cursor.execute(query)
                if cursor.fetchone()[0]:
                    assert True

    def test_postgresql_columns(self):
        db = DB()
        with db.p:
            with db.p.cursor() as cursor:
                query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'short_urls';"
                cursor.execute(query)
                column_names = [row[0] for row in cursor.fetchall()]
                assert set(column_names) == {"url", "hashed_url"}


class TestAPP:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_generate_hashed_url(self, client):
        pass

    def test_retrieve_url_by_hashed_url(self, client):
        pass
