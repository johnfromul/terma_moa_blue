"""Data update coordinator for Terma MOA Blue."""
from __future__ import annotations

from datetime import timedelta
import logging
import random

from bleak.backends.device import BLEDevice

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TermaMoaBlueDevice
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class TermaMoaBlueCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching Terma MOA Blue data."""

    def __init__(self, hass: HomeAssistant, ble_device: BLEDevice) -> None:
        """Initialize the coordinator."""
        # Add 0-60s random jitter to interval to prevent update cycles from synchronizing
        jitter = random.randint(0, 60)
        interval_with_jitter = UPDATE_INTERVAL + jitter
        
        _LOGGER.debug(
            "Initializing coordinator for %s with interval %ds (base %ds + jitter %ds)",
            ble_device.address,
            interval_with_jitter,
            UPDATE_INTERVAL,
            jitter,
        )
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval_with_jitter),
        )
        self.device = TermaMoaBlueDevice(ble_device)

    async def _async_update_data(self) -> None:
        """Fetch data from the device."""
        try:
            await self.device.update()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        # No persistent connection to close
        pass
