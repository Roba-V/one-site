from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://localhost:8000",
    ) as client:
        yield client
