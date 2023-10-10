import pytest
from httpx import AsyncClient


# Тест для /generate
def test_generate_secret(ac: AsyncClient):
    response = await ac.post("/generate", json={"secret": "test_secret", "passphrase": "test_passphrase"})
    assert response.status_code == 200
    data = response.json()
    assert "secret_key" in data


# Тест для /secrets/{secret_key}
def test_get_secret(ac: AsyncClient):
    # Создаем секрет для теста
    response = await ac.post("/generate", json={"secret": "test_secret", "passphrase": "test_passphrase"})
    data = response.json()
    secret_key = data["secret_key"]
    # Получаем секрет
    response = await ac.get(f"/secrets/{secret_key}", params={"passphrase": "test_passphrase"})
    assert response.status_code == 200
    data = response.json()
    assert "secret" in data
    assert data["secret"] == "test_secret"

    # Попытка получить секрет с неверной фразой
    response = await ac.get(f"/secrets/{secret_key}", params={"passphrase": "incorrect_passphrase"})
    assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()
