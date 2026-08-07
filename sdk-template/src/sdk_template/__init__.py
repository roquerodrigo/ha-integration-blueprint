"""
Public surface of the SDK.

Everything a consumer is meant to import is re-exported here, so the module
layout stays free to change without breaking the integration that depends on
it.
"""

from __future__ import annotations

from .client import SdkTemplateClient
from .exceptions import (
    SdkTemplateAuthenticationError,
    SdkTemplateConnectionError,
    SdkTemplateError,
)

__all__ = [
    "SdkTemplateAuthenticationError",
    "SdkTemplateClient",
    "SdkTemplateConnectionError",
    "SdkTemplateError",
]
