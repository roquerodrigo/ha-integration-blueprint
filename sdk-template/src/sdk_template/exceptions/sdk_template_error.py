"""Base error for the SDK."""

from __future__ import annotations


class SdkTemplateError(Exception):
    """
    Base class every error raised by this SDK derives from.

    Consumers catch this one to mean "the SDK failed"; the integration maps the
    subclasses to Home Assistant's own failure modes.
    """
