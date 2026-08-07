from __future__ import annotations

from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import dt as dt_util

from custom_components.integration_blueprint.const import DOMAIN
from custom_components.integration_blueprint.coordinator import (
    FAILURE_GRACE_PERIOD,
    IntegrationBlueprintDataUpdateCoordinator,
)
from custom_components.integration_blueprint.exceptions import (
    IntegrationBlueprintApiClientAuthenticationError,
    IntegrationBlueprintApiClientError,
)


def _make_coordinator(hass, payload=None, scan_interval=timedelta(minutes=5)):
    coord = IntegrationBlueprintDataUpdateCoordinator(
        hass=hass, scan_interval=scan_interval
    )
    client = AsyncMock()
    client.async_get_data = AsyncMock(return_value=payload or {})
    runtime_data = type("D", (), {"client": client})()
    entry = type("E", (), {"entry_id": "eid", "runtime_data": runtime_data})()
    coord.config_entry = entry
    return coord, client


def test_init_sets_domain_name(hass):
    coord = IntegrationBlueprintDataUpdateCoordinator(
        hass=hass, scan_interval=timedelta(seconds=300)
    )
    assert coord.name == DOMAIN


def test_init_sets_update_interval(hass):
    coord = IntegrationBlueprintDataUpdateCoordinator(
        hass=hass, scan_interval=timedelta(seconds=42)
    )
    assert coord.update_interval == timedelta(seconds=42)


async def test_update_data_returns_payload(hass, sample_payload):
    coord, _ = _make_coordinator(hass, payload=sample_payload)
    result = await coord._async_update_data()
    assert result == sample_payload


async def test_update_data_raises_update_failed_on_api_error(hass):
    coord, client = _make_coordinator(hass)
    client.async_get_data.side_effect = IntegrationBlueprintApiClientError("down")
    with pytest.raises(UpdateFailed):
        await coord._async_update_data()


async def test_update_data_raises_auth_failed_on_auth_error(hass):
    coord, client = _make_coordinator(hass)
    client.async_get_data.side_effect = (
        IntegrationBlueprintApiClientAuthenticationError("nope")
    )
    with pytest.raises(ConfigEntryAuthFailed):
        await coord._async_update_data()


async def test_update_data_serves_last_known_data_within_grace_period(
    hass, sample_payload
):
    coord, client = _make_coordinator(hass)
    coord.data = sample_payload
    client.async_get_data.side_effect = IntegrationBlueprintApiClientError("blip")
    assert await coord._async_update_data() == sample_payload


async def test_update_data_raises_update_failed_after_grace_period(
    hass, sample_payload
):
    coord, client = _make_coordinator(hass)
    coord.data = sample_payload
    client.async_get_data.side_effect = IntegrationBlueprintApiClientError("down")
    coord._first_failure_at = (
        dt_util.utcnow() - FAILURE_GRACE_PERIOD - timedelta(seconds=1)
    )
    with pytest.raises(UpdateFailed):
        await coord._async_update_data()


async def test_update_data_raises_update_failed_without_previous_data(hass):
    coord, client = _make_coordinator(hass)
    coord.data = None
    client.async_get_data.side_effect = IntegrationBlueprintApiClientError("down")
    with pytest.raises(UpdateFailed):
        await coord._async_update_data()


async def test_update_data_clears_failure_window_after_success(hass, sample_payload):
    coord, _ = _make_coordinator(hass, payload=sample_payload)
    coord._first_failure_at = dt_util.utcnow()
    await coord._async_update_data()
    assert coord._first_failure_at is None


async def test_auth_error_is_not_absorbed_by_the_grace_period(hass, sample_payload):
    coord, client = _make_coordinator(hass)
    coord.data = sample_payload
    client.async_get_data.side_effect = (
        IntegrationBlueprintApiClientAuthenticationError("nope")
    )
    with pytest.raises(ConfigEntryAuthFailed):
        await coord._async_update_data()
