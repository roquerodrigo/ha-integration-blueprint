"""DataUpdateCoordinator for integration_blueprint."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN, LOGGER
from .exceptions import (
    IntegrationBlueprintApiClientAuthenticationError,
    IntegrationBlueprintApiClientError,
)

if TYPE_CHECKING:
    from datetime import datetime

    from homeassistant.core import HomeAssistant

    from .data import IntegrationBlueprintConfigEntry, IntegrationBlueprintPost

FAILURE_GRACE_PERIOD = timedelta(minutes=5)


class IntegrationBlueprintDataUpdateCoordinator(
    DataUpdateCoordinator["IntegrationBlueprintPost"]
):
    """Coordinator for fetching the sample post from the API."""

    config_entry: IntegrationBlueprintConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        scan_interval: timedelta,
        config_entry: IntegrationBlueprintConfigEntry | None = None,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
            always_update=False,
            config_entry=config_entry,
        )
        self._first_failure_at: datetime | None = None

    async def _async_update_data(self) -> IntegrationBlueprintPost:
        """Fetch data from the API, tolerating outages shorter than the grace period."""
        try:
            data = await self.config_entry.runtime_data.client.async_get_data()
        except IntegrationBlueprintApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except IntegrationBlueprintApiClientError as exception:
            return self._handle_failure(exception)

        self._first_failure_at = None
        return data

    def _handle_failure(
        self, exception: IntegrationBlueprintApiClientError
    ) -> IntegrationBlueprintPost:
        """
        Serve the last known data while the outage is shorter than the grace period.

        A single failed poll of a remote API is usually a blip, not an outage,
        yet raising ``UpdateFailed`` immediately marks every entity of the
        integration unavailable — which shows up in history, breaks automations
        and templates that read the state, and resolves itself one poll later.
        Holding the last known values for a bounded window trades a little
        staleness for that stability, and a genuine outage still surfaces once
        the window closes.

        Only failures with data to fall back on are absorbed: before the first
        successful refresh there is nothing to serve, and an authentication
        error never reaches here, so re-authentication is still prompted at
        once. Set ``FAILURE_GRACE_PERIOD`` to ``timedelta(0)`` to opt out.
        """
        now = dt_util.utcnow()
        if self._first_failure_at is None:
            self._first_failure_at = now

        last_known_data: IntegrationBlueprintPost | None = self.data
        if (
            last_known_data is not None
            and now - self._first_failure_at < FAILURE_GRACE_PERIOD
        ):
            LOGGER.warning(
                "Failed to fetch data; serving the last known values: %s", exception
            )
            return last_known_data

        raise UpdateFailed(exception) from exception
