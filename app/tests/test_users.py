#!/usr/bin/env python3
from fastapi.testclient import TestClient
from tests.test_main import client_fixture as client
from tests.test_main import session_fixture, user


def test_create_user(client: TestClient, user):
    response = client.post("/users/", json=user)
    data = response.json()
    print(user)
    print(data)
    assert response.status_code == 201

    assert data["email"] == user["email"]
    assert data["first_name"] == user["first_name"]
    assert data["last_name"] == user["last_name"]
    assert data["birth_date"] == user["birth_date"]
    assert data["address"] == user["address"]


def test_create_existing_user(client: TestClient, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    response = client.post("/users/", json=user)
    assert response.status_code == 400
    data = response.json()
    print(data)
    assert data["detail"] == "Email already registered"


def test_get_user(client: TestClient, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["email"] == user["email"]


def test_get_unexistant_user(client: TestClient, user):
    response = client.get("/user/0")
    assert response.status_code == 404


def test_get_users(client: TestClient, user):
    response = client.get("/users/")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert len(data) == 0

    response = client.post("/users/", json=user)
    assert response.status_code == 201

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_update_user(client: TestClient, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    user["email"] = "hi@google.com"
    response = client.put("/users/", json=user)
    data = response.json()
    print(data)
    assert response.status_code == 200


def test_delete_user(client: TestClient, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    client.delete(
        "/users/1",
    )
