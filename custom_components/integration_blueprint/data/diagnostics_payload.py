"""Typed top-level shape returned by async_get_config_entry_diagnostics."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .diagnostics_entry import IntegrationBlueprintDiagnosticsEntry
    from .post import IntegrationBlueprintPost


class IntegrationBlueprintDiagnosticsPayload(TypedDict):
    """Top-level shape returned by async_get_config_entry_diagnostics."""

    entry: IntegrationBlueprintDiagnosticsEntry
    coordinator_data: IntegrationBlueprintPost | None
