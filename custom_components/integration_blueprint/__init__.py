"""Integration Blueprint integration for Home Assistant."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, cast

from homeassistant.const import CONF_SCAN_INTERVAL, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import IntegrationBlueprintApiClient
from .const import DEFAULT_SCAN_INTERVAL_SECONDS, DOMAIN
from .coordinator import IntegrationBlueprintDataUpdateCoordinator
from .data import IntegrationBlueprintData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.device_registry import DeviceEntry

    from .data import IntegrationBlueprintConfigData, IntegrationBlueprintConfigEntry

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> bool:
    """Set up Integration Blueprint from a config entry."""
    config = cast("IntegrationBlueprintConfigData", entry.data)
    scan_interval_seconds: int = int(
        entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_SECONDS),
    )
    coordinator = IntegrationBlueprintDataUpdateCoordinator(
        hass=hass,
        scan_interval=timedelta(seconds=scan_interval_seconds),
        config_entry=entry,
    )
    entry.runtime_data = IntegrationBlueprintData(
        client=IntegrationBlueprintApiClient(
            username=config["username"],
            password=config["password"],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_config_entry_device(
    hass: HomeAssistant,  # noqa: ARG001 -- part of the signature Home Assistant calls
    entry: IntegrationBlueprintConfigEntry,
    device_entry: DeviceEntry,
) -> bool:
    """
    Allow deleting devices this entry no longer provides.

    Home Assistant hides the "delete device" button unless the integration
    implements this hook, so without it a device that the account stopped
    exposing — hardware that was replaced, an endpoint that disappeared — stays
    in the registry forever with all of its entities unavailable, and the only
    way out is deleting the whole config entry.

    This blueprint serves a single device keyed by the entry id, so that one is
    refused (the next refresh would recreate it anyway) and anything else left
    behind is allowed to go. An integration serving one device per upstream
    item should instead refuse only the identifiers present in the latest
    coordinator payload.
    """
    return (DOMAIN, entry.entry_id) not in device_entry.identifiers
