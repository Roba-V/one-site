from typing import AsyncGenerator

import pytest
import pytest_asyncio
import starlette.status
from httpx import ASGITransport, AsyncClient

from backend.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://localhost:8000",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_home(async_client) -> None:
    """
    Test for Hello World API.

    Parameters
    ----------
    async_client

    Returns
    -------
    """
    response = await async_client.get("/")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["message"] == "Hello World!"
