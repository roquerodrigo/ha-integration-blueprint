"""Custom types for integration_blueprint."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from .config_data import IntegrationBlueprintConfigData
from .diagnostics_entry import IntegrationBlueprintDiagnosticsEntry
from .diagnostics_payload import IntegrationBlueprintDiagnosticsPayload
from .options_data import IntegrationBlueprintOptionsData
from .post import IntegrationBlueprintPost
from .runtime import IntegrationBlueprintData

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry


type JsonPrimitive = str | int | float | bool | None
type JsonValue = JsonPrimitive | list[JsonValue] | Mapping[str, JsonValue]
type JsonObject = Mapping[str, JsonValue]

type IntegrationBlueprintConfigEntry = ConfigEntry[IntegrationBlueprintData]

__all__ = [
    "IntegrationBlueprintConfigData",
    "IntegrationBlueprintConfigEntry",
    "IntegrationBlueprintData",
    "IntegrationBlueprintDiagnosticsEntry",
    "IntegrationBlueprintDiagnosticsPayload",
    "IntegrationBlueprintOptionsData",
    "IntegrationBlueprintPost",
    "JsonObject",
    "JsonPrimitive",
    "JsonValue",
]
