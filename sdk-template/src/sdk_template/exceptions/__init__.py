"""Errors raised by the SDK."""

from __future__ import annotations

from .sdk_template_authentication_error import SdkTemplateAuthenticationError
from .sdk_template_connection_error import SdkTemplateConnectionError
from .sdk_template_error import SdkTemplateError

__all__ = [
    "SdkTemplateAuthenticationError",
    "SdkTemplateConnectionError",
    "SdkTemplateError",
]
