"""Error raised when the credentials are rejected."""

from __future__ import annotations

from .sdk_template_error import SdkTemplateError


class SdkTemplateAuthenticationError(SdkTemplateError):
    """
    The credentials were rejected.

    Kept apart from the connection error so the integration can start a reauth
    flow instead of retrying forever.
    """
