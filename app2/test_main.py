from fastapi.testclient import TestClient
from .main import router

client = TestClient(router)

def test_read_root():
    response =client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

