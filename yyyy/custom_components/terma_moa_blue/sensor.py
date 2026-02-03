"""Sensor platform for Terma MOA Blue."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, OperatingMode
from .coordinator import TermaMoaBlueCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class TermaMoaBlueSensorEntityDescription(SensorEntityDescription):
    """Describes Terma MOA Blue sensor entity."""

    value_fn: Callable[[TermaMoaBlueCoordinator], float | str | None] = None


SENSORS: tuple[TermaMoaBlueSensorEntityDescription, ...] = (
    TermaMoaBlueSensorEntityDescription(
        key="current_room_temperature",
        name="Current Room Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda coord: coord.device.current_room_temp,
    ),
    TermaMoaBlueSensorEntityDescription(
        key="target_room_temperature",
        name="Target Room Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda coord: coord.device.target_room_temp,
    ),
    TermaMoaBlueSensorEntityDescription(
        key="current_element_temperature",
        name="Current Element Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda coord: coord.device.current_element_temp,
    ),
    TermaMoaBlueSensorEntityDescription(
        key="target_element_temperature",
        name="Target Element Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda coord: coord.device.target_element_temp,
    ),
    TermaMoaBlueSensorEntityDescription(
        key="operating_mode",
        name="Operating Mode",
        icon="mdi:cog",
        value_fn=lambda coord: coord.device.mode.name if coord.device.mode else None,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Terma MOA Blue sensor entities."""
    coordinator: TermaMoaBlueCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        TermaMoaBlueSensor(coordinator, description) for description in SENSORS
    )


class TermaMoaBlueSensor(CoordinatorEntity[TermaMoaBlueCoordinator], SensorEntity):
    """Representation of a Terma MOA Blue sensor."""

    entity_description: TermaMoaBlueSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: TermaMoaBlueCoordinator,
        description: TermaMoaBlueSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description

        self._attr_unique_id = f"{coordinator.device.address}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device.address)},
            "name": coordinator.device.name,
            "manufacturer": "Terma",
            "model": "MOA Blue",
        }

    @property
    def native_value(self) -> float | str | None:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator)
