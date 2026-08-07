"""Error raised when the device or service cannot be reached."""

from __future__ import annotations

from .sdk_template_error import SdkTemplateError


class SdkTemplateConnectionError(SdkTemplateError):
    """The request never completed: timeout, DNS, refused connection."""
