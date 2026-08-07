"""Sample asynchronous client. Replace with the real one."""

from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING, Any, Self, cast

import aiohttp

from .exceptions import (
    SdkTemplateAuthenticationError,
    SdkTemplateConnectionError,
    SdkTemplateError,
)

if TYPE_CHECKING:
    from types import TracebackType

_REQUEST_TIMEOUT_SECONDS = 10
_UNAUTHORIZED_STATUSES = frozenset({401, 403})
_URL_QUERY_STRING = re.compile(r"\?\S*")


def _sanitized_error_text(exception: BaseException) -> str:
    """
    Strip URL query strings from upstream error text before it is raised.

    HTTP client libraries quote the request URL in their exception messages,
    and the consumer logs whatever the SDK raises. When the API carries a
    credential as a query parameter, an ordinary connection failure would
    otherwise publish it verbatim.
    """
    return _URL_QUERY_STRING.sub("?<redacted>", str(exception))


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Turn an unsuccessful response into the SDK's own error."""
    if response.status in _UNAUTHORIZED_STATUSES:
        message = "Invalid credentials"
        raise SdkTemplateAuthenticationError(message)
    response.raise_for_status()


class SdkTemplateClient:
    """
    Talks to the upstream API and returns plain Python data.

    The client owns no Home Assistant concept on purpose: it takes credentials,
    returns parsed payloads, and raises the SDK's own errors. Accepting an
    external ``aiohttp.ClientSession`` is what lets the integration hand over
    Home Assistant's shared session instead of leaking one per config entry.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Store the credentials and adopt the session, if one was given."""
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._session = session
        self._owns_session = session is None

    async def __aenter__(self) -> Self:
        """Enter the context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the session, but only the one this client created itself."""
        await self.async_close()

    async def async_close(self) -> None:
        """
        Release the session this client created.

        A session handed in from outside belongs to the caller and is left
        alone; closing it would break every other user of it.
        """
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None

    async def async_get_status(self) -> dict[str, Any]:
        """Read the current device status."""
        return await self._request("get", "/status")

    async def _request(self, method: str, path: str) -> dict[str, Any]:
        """Perform one request and return the parsed JSON object."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        try:
            async with asyncio.timeout(_REQUEST_TIMEOUT_SECONDS):
                response = await self._session.request(
                    method=method,
                    url=f"{self._base_url}{path}",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                )
                _verify_response_or_raise(response)
                return cast("dict[str, Any]", await response.json())
        except TimeoutError as exception:
            message = f"Timed out talking to {self._base_url}"
            raise SdkTemplateConnectionError(message) from exception
        except aiohttp.ClientError as exception:
            message = f"Request failed: {_sanitized_error_text(exception)}"
            raise SdkTemplateConnectionError(message) from exception
        except SdkTemplateError:
            raise
        except Exception as exception:
            message = f"Failed to process the API response: {exception}"
            raise SdkTemplateError(message) from exception
