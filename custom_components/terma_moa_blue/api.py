"""API for Terma MOA Blue integration - using temporary connections."""
from __future__ import annotations

import asyncio
import logging
import struct
from typing import Callable

from bleak import BleakClient
from bleak.exc import BleakError
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak

from .const import (
    CHAR_ELEMENT_TEMP,
    CHAR_MODE,
    CHAR_ROOM_TEMP,
    OperatingMode,
)

_LOGGER = logging.getLogger(__name__)


class TermaMoaBlueDevice:
    """Representation of a Terma MOA Blue device."""

    def __init__(self, ble_device: BluetoothServiceInfoBleak) -> None:
        """Initialize the device."""
        self._ble_device = ble_device
        self.address = ble_device.address
        self._lock = asyncio.Lock()
        
        # Cached state
        self._current_room_temp: float | None = None
        self._target_room_temp: float | None = None
        self._current_element_temp: float | None = None
        self._target_element_temp: float | None = None
        self._mode: OperatingMode | None = None

    @property
    def name(self) -> str:
        """Return device name."""
        return self._ble_device.name or f"Terma ({self.address})"

    @property
    def current_room_temp(self) -> float | None:
        """Return current room temperature."""
        return self._current_room_temp

    @property
    def target_room_temp(self) -> float | None:
        """Return target room temperature."""
        return self._target_room_temp

    @property
    def current_element_temp(self) -> float | None:
        """Return current element temperature."""
        return self._current_element_temp

    @property
    def target_element_temp(self) -> float | None:
        """Return target element temperature."""
        return self._target_element_temp

    @property
    def mode(self) -> OperatingMode | None:
        """Return current operating mode."""
        return self._mode

    async def _execute_with_connection(
        self, operation: Callable[[BleakClient], None]
    ) -> None:
        """Execute an operation with a temporary BLE connection."""
        async with self._lock:
            _LOGGER.debug("Connecting to %s for operation", self.address)
            try:
                async with BleakClient(self._ble_device.address, timeout=20.0) as client:
                    _LOGGER.debug("Connected to %s", self.address)
                    await operation(client)
                    _LOGGER.debug("Operation completed, disconnecting")
            except (BleakError, TimeoutError, EOFError) as err:
                _LOGGER.error("Error communicating with device: %s", err)
                raise

    async def update(self) -> None:
        """Update device state by reading characteristics."""
        async def read_state(client: BleakClient) -> None:
            # Read room temperature
            room_temp_data = await client.read_gatt_char(CHAR_ROOM_TEMP)
            if len(room_temp_data) >= 4:
                current = struct.unpack("<H", room_temp_data[0:2])[0] / 10.0
                target = struct.unpack("<H", room_temp_data[2:4])[0] / 10.0
                self._current_room_temp = current
                self._target_room_temp = target
                _LOGGER.debug("Room temp: %.1f°C / %.1f°C", current, target)

            # Read element temperature
            element_temp_data = await client.read_gatt_char(CHAR_ELEMENT_TEMP)
            if len(element_temp_data) >= 4:
                current = struct.unpack("<H", element_temp_data[0:2])[0] / 10.0
                target = struct.unpack("<H", element_temp_data[2:4])[0] / 10.0
                self._current_element_temp = current
                self._target_element_temp = target
                _LOGGER.debug("Element temp: %.1f°C / %.1f°C", current, target)

            # Read mode
            mode_data = await client.read_gatt_char(CHAR_MODE)
            if len(mode_data) >= 1:
                mode_value = mode_data[0]
                try:
                    self._mode = OperatingMode(mode_value)
                    _LOGGER.debug("Mode: %s", self._mode.name)
                except ValueError:
                    _LOGGER.warning("Unknown mode value: %d", mode_value)
                    self._mode = None

        await self._execute_with_connection(read_state)

    async def set_room_temperature(self, temperature: float) -> None:
        """Set target room temperature."""
        async def write_temp(client: BleakClient) -> None:
            temp_value = int(temperature * 10)
            
            # Read current temperature first
            current_data = await client.read_gatt_char(CHAR_ROOM_TEMP)
            if len(current_data) < 4:
                raise ValueError("Invalid data from device")

            # Keep current temp, update target
            new_data = current_data[0:2] + struct.pack("<H", temp_value)
            await client.write_gatt_char(CHAR_ROOM_TEMP, new_data)
            self._target_room_temp = temperature
            _LOGGER.info("Set room temperature to %.1f°C", temperature)

        await self._execute_with_connection(write_temp)

    async def set_element_temperature(self, temperature: float) -> None:
        """Set target element temperature."""
        async def write_temp(client: BleakClient) -> None:
            temp_value = int(temperature * 10)
            
            # Read current temperature first
            current_data = await client.read_gatt_char(CHAR_ELEMENT_TEMP)
            if len(current_data) < 4:
                raise ValueError("Invalid data from device")

            # Keep current temp, update target
            new_data = current_data[0:2] + struct.pack("<H", temp_value)
            await client.write_gatt_char(CHAR_ELEMENT_TEMP, new_data)
            self._target_element_temp = temperature
            _LOGGER.info("Set element temperature to %.1f°C", temperature)

        await self._execute_with_connection(write_temp)

    async def set_mode(self, mode: OperatingMode) -> None:
        """Set operating mode."""
        async def write_mode(client: BleakClient) -> None:
            # Mode is 4 bytes: [mode, 0x00, 0x00, 0x00]
            mode_data = bytes([mode.value, 0x00, 0x00, 0x00])
            await client.write_gatt_char(CHAR_MODE, mode_data)
            self._mode = mode
            _LOGGER.info("Set mode to %s", mode.name)

        await self._execute_with_connection(write_mode)

    async def turn_on(self, use_room_temp: bool = True) -> None:
        """Turn on the heater."""
        await self.set_mode(OperatingMode.MANUAL)

    async def turn_off(self) -> None:
        """Turn off the heater."""
        await self.set_mode(OperatingMode.OFF)
