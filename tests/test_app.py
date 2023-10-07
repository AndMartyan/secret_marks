import pytest
import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.main import app
from src.config import DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST, DB_USER_TEST, DB_PASS_TEST

TEST_DATABASE_URL = f"postgresql://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
client = TestClient(app)


# Удаления базы данных перед/после тестов
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    os.remove("encryption_key.txt")


# Создания сессии БД для тестов
@pytest.fixture
def db_session(test_db):
    db = SessionLocal()
    yield db
    db.close()


def test_generate_secret(db_session):
    """ Создания секрета"""
    request_data = {
        "secret": "my_secret",
        "passphrase": "my_passphrase",
        "lifetime_minutes": 30,
    }
    response = client.post("/generate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "secret_key" in data
    assert "lifetime" in data


def test_get_secret(db_session):
    """Корректное получение секрета"""
    # Создание секрета
    request_data = {
        "secret": "my_secret",
        "passphrase": "my_passphrase",
        "lifetime_minutes": 30,
    }
    generate_response = client.post("/generate", json=request_data)
    assert generate_response.status_code == 200
    secret_key = generate_response.json()["secret_key"]
    # Запрос на получение секрета
    passphrase = "my_passphrase"
    response = client.get(f"/secrets/{secret_key}?passphrase={passphrase}")
    assert response.status_code == 200
    data = response.json()
    assert "secret_key" in data
    assert "lifetime" in data


def test_get_secret_invalid_passphrase(db_session):
    """Некорректная кодовая фраза"""
    # Создание секрета
    request_data = {
        "secret": "my_secret",
        "passphrase": "my_passphrase",
        "lifetime_minutes": 30,
    }
    generate_response = client.post("/generate", json=request_data)
    assert generate_response.status_code == 200
    secret_key = generate_response.json()["secret_key"]
    # Запрос на получение секрета с некорректной кодовой фразой
    passphrase = "wrong_passphrase"
    response = client.get(f"/secrets/{secret_key}?passphrase={passphrase}")
    assert response.status_code == 404


def test_get_secret_expired(db_session):
    """Cекрет с истекшим сроком действия"""
    # Создание секрета с истекшим сроком действия
    request_data = {
        "secret": "my_secret",
        "passphrase": "my_passphrase",
        "lifetime_minutes": 0,
    }
    generate_response = client.post("/generate", json=request_data)
    assert generate_response.status_code == 200
    # Запрос на получение секрета с истекшим сроком действия
    secret_key = generate_response.json()["secret_key"]
    passphrase = "my_passphrase"
    response = client.get(f"/secrets/{secret_key}?passphrase={passphrase}")
    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main()

