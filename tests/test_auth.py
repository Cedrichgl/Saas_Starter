import pytest
from fastapi.testclient import TestClient


def test_register(client):
    response = client.post(
        "/auth/register", json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 201


def test_register_duplicate(client):
    payload = {"email": "test@example.com", "password": "secret123"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Cet utilisateur existe déjà"


def test_login(client):
    client.post(
        "/auth/register", json={"email": "test@example.com", "password": "secret123"}
    )
    response = client.post(
        "/auth/login", data={"username": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_me_sans_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
