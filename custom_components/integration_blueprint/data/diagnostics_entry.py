"""Typed entry section of the diagnostics dump."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from collections.abc import Mapping


class IntegrationBlueprintDiagnosticsEntry(TypedDict):
    """Entry section of the diagnostics dump."""

    title: str
    version: int
    domain: str
    data: Mapping[str, str]
    options: Mapping[str, str | int]
