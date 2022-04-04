#!/usr/bin/env python3
import pytest, json
from app.main import app
from services.database.init_db import get_db
from fastapi.testclient import TestClient
from services.database.init_db import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


@pytest.fixture(name="session")
def session_fixture():
    db_url = "postgresql://cluepoints:cluepointsPWD@test-db/test"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        yield session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user")
def user():
    return {
        "id": 1,
        "email": "test@hello.com",
        "first_name": "Tom",
        "last_name": "Bombadil",
        "birth_date": "1966-03-27",
        "address": "",
    }


@pytest.fixture(name="account")
def account():
    return {"id": 1, "name": "my super account", "devise": "USD", "owner_id": 1}


@pytest.fixture(name="transaction")
def transaction():
    return {
        "amount": 1,
        "communication": "string",
        "account_id": 1,
        "external_account_id": 2,
    }


def test_client(client: TestClient):
    response = client.get("/")
    data = response.json()
    print(data)
    assert response.status_code == 404
