import pytest


@pytest.mark.asyncio
async def test_create_task_requires_auth(
    client
):

    response = await client.post(
        "/tasks/project/fake-id",
        json={
            "title":
            "Test Task"
        }
    )

    assert response.status_code in [
        401,
        403
    ]