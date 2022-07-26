from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.author import create_random_author


def test_create_author(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": "Van Gogh"}
    response = client.post(
        f"{settings.API_V1_STR}/author/", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_author(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = create_random_author(db)
    response = client.get(
        f"{settings.API_V1_STR}/author/", headers=superuser_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == item.name
    assert content["id"] == item.id
