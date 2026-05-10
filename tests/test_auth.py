import pytest


@pytest.mark.asyncio
async def test_user_registration(client):

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test4@example.com",
            "username": "testuser4",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "user_id" in data


@pytest.mark.asyncio
async def test_login(client):

    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login4@test.com",
            "username": "loginuser4",
            "password": "password123",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "loginuser4",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
