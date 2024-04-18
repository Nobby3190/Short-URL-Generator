import sys

import pytest
from app import app
from fastapi.testclient import TestClient

sys.path.append("..")


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
