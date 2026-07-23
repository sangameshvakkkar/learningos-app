import pytest
from httpx import AsyncClient

@pytest.fixture
async def auth_headers(client: AsyncClient):
    email = "course_user@example.com"
    password = "Password123!"
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Course User"}
    )
    res = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_get_courses_empty_or_seeded(client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/courses/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Could be empty or have seed data depending on if seed runs.
    # Since we use SQLite in memory and don't call seed.py in setup, it should be empty.

@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/v1/courses/")
    assert response.status_code == 403 # FastAPI HTTPBearer returns 403 for missing token by default
