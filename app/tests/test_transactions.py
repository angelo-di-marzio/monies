#!/usr/bin/env python3
from fastapi.testclient import TestClient
from tests.test_main import client_fixture as client
from tests.test_main import session_fixture, transaction, account, user


def test_create_transaction(client: TestClient, transaction, account, user):
    # User
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    # First account
    response = client.post("/accounts/", json=account)
    # Second account
    response = client.post("/accounts/", json=account)

    # Transaction
    response = client.post("/transactions/", json=transaction)
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "Not enough money !"

    # deposit to fund account
    response = client.post(
        "/transactions/deposit", json={"amount": 100, "account_id": 1}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["external_account_balance"] == 100

    # Valid Transaction
    response = client.post("/transactions/", json=transaction)
    assert response.status_code == 201
    data = response.json()
    assert data["account_balance"] == 99
    assert data["external_account_balance"] == 1


def test_get_balance(client: TestClient, transaction, account, user):
    response = client.post("/users/", json=user)
    assert response.status_code == 201

    response = client.post("/accounts/", json=account)
    data = response.json()
    print(data)
    assert response.status_code == 201

    response = client.get("/accounts/1/balance")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data == 0
