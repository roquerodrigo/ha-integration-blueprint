from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from sdk_template import (
    SdkTemplateAuthenticationError,
    SdkTemplateClient,
    SdkTemplateConnectionError,
    SdkTemplateError,
)
from sdk_template.client import _sanitized_error_text


def _session(payload=None, status=200, side_effect=None):
    response = AsyncMock()
    response.status = status
    response.raise_for_status = MagicMock()
    response.json = AsyncMock(return_value=payload or {})
    session = MagicMock()
    session.close = AsyncMock()
    if side_effect is not None:
        session.request = AsyncMock(side_effect=side_effect)
    else:
        session.request = AsyncMock(return_value=response)
    return session


def _client(session) -> SdkTemplateClient:
    return SdkTemplateClient(
        base_url="https://example.com", api_key="key", session=session
    )


async def test_get_status_returns_the_payload():
    client = _client(_session(payload={"state": "on"}))
    assert await client.async_get_status() == {"state": "on"}


async def test_unauthorized_raises_authentication_error():
    client = _client(_session(status=401))
    with pytest.raises(SdkTemplateAuthenticationError):
        await client.async_get_status()


async def test_client_error_raises_connection_error():
    client = _client(_session(side_effect=aiohttp.ClientError("boom")))
    with pytest.raises(SdkTemplateConnectionError):
        await client.async_get_status()


async def test_timeout_raises_connection_error():
    client = _client(_session(side_effect=TimeoutError))
    with pytest.raises(SdkTemplateConnectionError):
        await client.async_get_status()


async def test_unexpected_error_raises_the_base_error():
    client = _client(_session(side_effect=RuntimeError("boom")))
    with pytest.raises(SdkTemplateError, match="Failed to process the API response"):
        await client.async_get_status()


async def test_authentication_error_is_not_rewrapped():
    client = _client(_session(status=403))
    with pytest.raises(SdkTemplateAuthenticationError):
        await client.async_get_status()


async def test_close_leaves_a_session_it_did_not_create_alone():
    session = _session()
    client = _client(session)
    await client.async_close()
    session.close.assert_not_awaited()


async def test_context_manager_closes_its_own_session():
    client = SdkTemplateClient(base_url="https://example.com", api_key="key")
    async with client:
        pass
    assert client._session is None


def test_sanitized_error_text_redacts_the_query_string():
    sanitized = _sanitized_error_text(
        aiohttp.ClientError("GET https://example.com/status?api_key=supersecret")
    )
    assert "supersecret" not in sanitized
    assert sanitized.endswith("?<redacted>")


@pytest.mark.live
async def test_reaches_the_real_device():
    async with SdkTemplateClient(
        base_url="https://example.com", api_key="key"
    ) as client:
        assert await client.async_get_status()
