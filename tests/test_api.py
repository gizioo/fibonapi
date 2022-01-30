from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_main_sequence():
    test_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    for test_val in test_sequence:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"result": test_val}


def test_main_post():
    response = client.post("/")
    assert response.status_code == 405


def test_main_put():
    response = client.put("/")
    assert response.status_code == 405


def test_main_delete():
    response = client.post("/")
    assert response.status_code == 405
