#!/usr/bin/env python3
from fastapi.testclient import TestClient
from tests.test_main import client_fixture as client
from tests.test_main import session_fixture, account, user


def test_create_account(client: TestClient, account, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    response = client.post("/accounts/", json=account)
    data = response.json()
    print(data)
    assert response.status_code == 201

    assert data["name"] == account["name"]
    assert data["devise"] == account["devise"]
    assert data["owner_id"] == account["owner_id"]


def test_create_account_bad_id(client: TestClient, account):
    response = client.post("/accounts/", json=account)
    data = response.json()
    print(data)
    assert response.status_code == 400
    assert data["detail"] == "Wrong owner_id !"


def test_get_account(client: TestClient, account, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    response = client.post("/accounts/", json=account)
    data = response.json()
    print(data)
    assert response.status_code == 201

    response = client.get("/accounts/1")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["name"] == account["name"]


def test_get_unexistant_account(client: TestClient, account):
    response = client.get("/accounts/0")
    assert response.status_code == 404


def test_get_accounts(client: TestClient, account, user):
    response = client.get("/accounts/")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert len(data) == 0

    response = client.post("/users/", json=user)
    assert response.status_code == 201
    response = client.post("/accounts/", json=account)
    assert response.status_code == 201

    response = client.get("/accounts/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == account["name"]
    assert len(data) == 1


def test_update_account(client: TestClient, account, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    response = client.post("/accounts/", json=account)
    assert response.status_code == 201

    account["name"] = "not great account"
    account["number"] = 1
    account["creation_datetime"] = "2019-10-12T07:20:50.52Z"
    response = client.put("/accounts/", json=account)
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert data["name"] == account["name"]


def test_delete_account(client: TestClient, account, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201
    response = client.post("/accounts/", json=account)
    assert response.status_code == 201

    client.delete(
        "/account/1",
    )
