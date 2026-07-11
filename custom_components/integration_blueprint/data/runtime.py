"""Runtime data stored on entry.runtime_data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.loader import Integration

    from ..api import IntegrationBlueprintApiClient
    from ..coordinator import IntegrationBlueprintDataUpdateCoordinator


@dataclass
class IntegrationBlueprintData:
    """Data stored on entry.runtime_data for the Integration Blueprint."""

    client: IntegrationBlueprintApiClient
    coordinator: IntegrationBlueprintDataUpdateCoordinator
    integration: Integration
