"""Climate platform for Terma MOA Blue."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    MAX_ELEMENT_TEMP,
    MAX_ROOM_TEMP,
    MIN_ELEMENT_TEMP,
    MIN_ROOM_TEMP,
    OperatingMode,
)
from .coordinator import TermaMoaBlueCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Terma MOA Blue climate entities."""
    coordinator: TermaMoaBlueCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            TermaMoaBlueClimate(coordinator, use_room_temp=True),
            TermaMoaBlueClimate(coordinator, use_room_temp=False),
        ]
    )


class TermaMoaBlueClimate(CoordinatorEntity[TermaMoaBlueCoordinator], ClimateEntity):
    """Representation of a Terma MOA Blue climate entity."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_OFF
    )
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_has_entity_name = True

    def __init__(
        self, coordinator: TermaMoaBlueCoordinator, use_room_temp: bool
    ) -> None:
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self._use_room_temp = use_room_temp

        # Set entity attributes
        device_name = coordinator.device.name
        if use_room_temp:
            self._attr_name = "Room Temperature"
            self._attr_unique_id = f"{coordinator.device.address}_room_climate"
            self._attr_min_temp = MIN_ROOM_TEMP
            self._attr_max_temp = MAX_ROOM_TEMP
        else:
            self._attr_name = "Element Temperature"
            self._attr_unique_id = f"{coordinator.device.address}_element_climate"
            self._attr_min_temp = MIN_ELEMENT_TEMP
            self._attr_max_temp = MAX_ELEMENT_TEMP

        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device.address)},
            "name": device_name,
            "manufacturer": "Terma",
            "model": "MOA Blue",
        }

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if self._use_room_temp:
            return self.coordinator.device.current_room_temp
        return self.coordinator.device.current_element_temp

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        if self._use_room_temp:
            return self.coordinator.device.target_room_temp
        return self.coordinator.device.target_element_temp

    @property
    def hvac_mode(self) -> HVACMode:
        """Return hvac operation mode."""
        mode = self.coordinator.device.mode

        # Nové hodnoty z Frida: OFF=0x20, ON=0x21
        if mode == OperatingMode.OFF:  # 0x20 (32)
            return HVACMode.OFF
        
        if mode == OperatingMode.ON:  # 0x21 (33)
            return HVACMode.HEAT

        # Fallback pro staré režimy (pokud se ještě používají)
        if self._use_room_temp:
            if mode in (OperatingMode.ROOM_TEMP_MANUAL, OperatingMode.ROOM_TEMP_SCHEDULE):
                return HVACMode.HEAT
        else:
            if mode in (
                OperatingMode.ELEMENT_TEMP_MANUAL,
                OperatingMode.ELEMENT_TEMP_SCHEDULE,
                OperatingMode.MANUAL,
            ):
                return HVACMode.HEAT

        return HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction:
        """Return the current running hvac operation."""
        if self.hvac_mode == HVACMode.OFF:
            return HVACAction.OFF

        current = self.current_temperature
        target = self.target_temperature

        if current is None or target is None:
            return HVACAction.IDLE

        # Simple logic: if current is below target, assume heating
        if current < target - 0.5:
            return HVACAction.HEATING
        return HVACAction.IDLE

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        try:
            if self._use_room_temp:
                await self.coordinator.device.set_room_temperature(temperature)
            else:
                await self.coordinator.device.set_element_temperature(temperature)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to set temperature: %s", err)
            raise

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        try:
            if hvac_mode == HVACMode.OFF:
                await self.coordinator.device.turn_off()
            elif hvac_mode == HVACMode.HEAT:
                await self.coordinator.device.turn_on(use_room_temp=self._use_room_temp)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to set HVAC mode: %s", err)
            raise
