#test_api

import pytest
from fastapi.testclient import TestClient
from main import app
from fastapi import status


@pytest.fixture
def client():
    return TestClient(app)



def test_create_node(client):
    node_data = {
        "uid": "12345",
        "label": "User",
        "name": "John Doe",
        "about": "Software Developer",
        "home_town": "New York",
        "photo_max": "url_to_photo",
        "screen_name": "johndoe123",
        "sex": "male",
        "style": "casual",
        "visualisation": "url_to_visualisation",
        "follows": ["67890", "23456"],
        "subscribes": ["34567"]
    }

    response = client.post("/node", json=node_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Node and relationships created successfully"

def test_get_node_and_relationships(client):
    node_id = "12345"
    response = client.get(f"/node/{node_id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["uid"] == node_id

    assert "follows" in data
    assert "subscribes" in data

    assert isinstance(data["follows"], list)
    assert isinstance(data["subscribes"], list)

def test_delete_node(client):
    node_id = "12345"

    response = client.delete(f"/node/{node_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Node {node_id} and its relationships deleted successfully"


def test_get_nodes(client):

    response = client.get("/nodes")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Должен быть список узлов
