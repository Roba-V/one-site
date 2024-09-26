import sys
from unittest.mock import patch

import pytest
import starlette.status


@patch("backend.common.core.config.config.API_CORS_ORIGINS", "http://localhost")
@patch("fastapi.FastAPI.add_middleware")
def test_main_with_cors_config(mock_add_middleware) -> None:
    # reload app reset instance of Log class
    del sys.modules["backend.main"]
    from backend.main import app  # noqa: F401

    mock_add_middleware.assert_called_once()


@pytest.mark.asyncio
async def test_home(async_client) -> None:
    """
    Test for Hello World API.

    Parameters
    ----------
    async_client
    """
    response = await async_client.get("/hello")

    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["message"] == "World!"
