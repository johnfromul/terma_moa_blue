"""Config flow for Terma MOA Blue integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Terma MOA Blue."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, str] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        self._discovery_info = discovery_info
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        assert self._discovery_info is not None

        if user_input is not None:
            return self.async_create_entry(
                title=self._discovery_info.name or "Terma MOA Blue",
                data={CONF_ADDRESS: self._discovery_info.address},
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders={
                "name": self._discovery_info.name or "Terma MOA Blue"
            },
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step to pick discovered device."""
        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=self._discovered_devices[address],
                data={CONF_ADDRESS: address},
            )

        current_addresses = self._async_current_ids()
        _LOGGER.debug("Current configured addresses: %s", current_addresses)
        
        # Scan all Bluetooth devices for debugging
        all_devices = []
        for discovery_info in async_discovered_service_info(self.hass):
            all_devices.append(f"{discovery_info.name} ({discovery_info.address})")
            _LOGGER.debug(
                "Found BLE device: %s (%s) - RSSI: %s",
                discovery_info.name,
                discovery_info.address,
                discovery_info.rssi,
            )
            
            if (
                discovery_info.address in current_addresses
                or discovery_info.address in self._discovered_devices
            ):
                continue

            # Look for Terma MOA Blue devices
            if discovery_info.name and ("MOA Blue" in discovery_info.name or "MOA" in discovery_info.name or "Terma" in discovery_info.name):
                _LOGGER.info("Found Terma device: %s (%s)", discovery_info.name, discovery_info.address)
                self._discovered_devices[
                    discovery_info.address
                ] = f"{discovery_info.name} ({discovery_info.address})"

        _LOGGER.info("Total BLE devices found: %d", len(all_devices))
        _LOGGER.info("Terma devices found: %d", len(self._discovered_devices))
        
        if not self._discovered_devices:
            _LOGGER.warning("No Terma MOA Blue devices found. All BLE devices: %s", all_devices)
            return self.async_abort(reason="no_devices_found")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): vol.In(self._discovered_devices),
                }
            ),
        )
