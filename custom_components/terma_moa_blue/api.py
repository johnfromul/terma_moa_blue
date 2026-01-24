"""Terma MOA Blue BLE API."""
from __future__ import annotations

import asyncio
import logging
import struct
from typing import Callable

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError
from bleak_retry_connector import establish_connection

from .const import (
    CHAR_ELEMENT_TEMP,
    CHAR_MODE,
    CHAR_ROOM_TEMP,
    SERVICE_UUID,
    OperatingMode,
)

_LOGGER = logging.getLogger(__name__)


class TermaMoaBlueDevice:
    """Representation of a Terma MOA Blue device."""

    def __init__(self, ble_device: BLEDevice) -> None:
        """Initialize the device."""
        self._ble_device = ble_device
        self._client: BleakClient | None = None
        self._disconnect_callbacks: list[Callable[[], None]] = []
        self._connect_lock = asyncio.Lock()

        # Cached state
        self._current_room_temp: float | None = None
        self._target_room_temp: float | None = None
        self._current_element_temp: float | None = None
        self._target_element_temp: float | None = None
        self._mode: OperatingMode | None = None

    @property
    def address(self) -> str:
        """Return the device address."""
        return self._ble_device.address

    @property
    def name(self) -> str:
        """Return the device name."""
        return self._ble_device.name or "Terma MOA Blue"

    @property
    def is_connected(self) -> bool:
        """Return connection status."""
        return self._client is not None and self._client.is_connected

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

    def register_disconnect_callback(self, callback: Callable[[], None]) -> None:
        """Register a callback to be called on disconnect."""
        self._disconnect_callbacks.append(callback)

    async def connect(self) -> None:
        """Connect to the device."""
        async with self._connect_lock:
            if self.is_connected:
                return

            _LOGGER.debug("Connecting to %s", self.address)
            try:
                self._client = await establish_connection(
                    BleakClient,
                    self._ble_device,
                    self.address,
                    disconnected_callback=self._on_disconnect,
                    use_services_cache=True,
                    ble_device_callback=lambda: self._ble_device,
                )
                _LOGGER.info("Connected to %s", self.address)
            except (BleakError, TimeoutError) as err:
                _LOGGER.error("Failed to connect to %s: %s", self.address, err)
                raise

    def _on_disconnect(self, client: BleakClient) -> None:
        """Handle disconnection."""
        _LOGGER.warning("Disconnected from %s", self.address)
        for callback in self._disconnect_callbacks:
            callback()

    async def disconnect(self) -> None:
        """Disconnect from the device."""
        if self._client and self._client.is_connected:
            await self._client.disconnect()

    async def update(self) -> None:
        """Update device state by reading characteristics."""
        if not self.is_connected:
            await self.connect()

        try:
            # Read room temperature (current + target)
            room_temp_data = await self._client.read_gatt_char(CHAR_ROOM_TEMP)
            if len(room_temp_data) >= 4:
                current = struct.unpack("<H", room_temp_data[0:2])[0] / 10.0
                target = struct.unpack("<H", room_temp_data[2:4])[0] / 10.0
                self._current_room_temp = current
                self._target_room_temp = target
                _LOGGER.debug(
                    "Room temp: current=%.1f°C, target=%.1f°C", current, target
                )

            # Read element temperature (current + target)
            element_temp_data = await self._client.read_gatt_char(CHAR_ELEMENT_TEMP)
            if len(element_temp_data) >= 4:
                current = struct.unpack("<H", element_temp_data[0:2])[0] / 10.0
                target = struct.unpack("<H", element_temp_data[2:4])[0] / 10.0
                self._current_element_temp = current
                self._target_element_temp = target
                _LOGGER.debug(
                    "Element temp: current=%.1f°C, target=%.1f°C", current, target
                )

            # Read operating mode
            mode_data = await self._client.read_gatt_char(CHAR_MODE)
            if len(mode_data) >= 1:
                mode_value = mode_data[0]
                try:
                    self._mode = OperatingMode(mode_value)
                    _LOGGER.debug("Mode: %s", self._mode.name)
                except ValueError:
                    _LOGGER.warning("Unknown mode value: %d", mode_value)
                    self._mode = None

        except (BleakError, TimeoutError) as err:
            _LOGGER.error("Failed to update device state: %s", err)
            raise

    async def set_room_temperature(self, temperature: float) -> None:
        """Set target room temperature."""
        if not self.is_connected:
            await self.connect()

        # Temperature is sent as integer (temp * 10) in little-endian
        # Format: [current_low, current_high, target_low, target_high]
        temp_value = int(temperature * 10)

        # Read current temperature first
        current_data = await self._client.read_gatt_char(CHAR_ROOM_TEMP)
        if len(current_data) < 4:
            raise ValueError("Invalid data from device")

        # Keep current temperature (first 2 bytes), update target
        new_data = current_data[0:2] + struct.pack("<H", temp_value)

        await self._client.write_gatt_char(CHAR_ROOM_TEMP, new_data)
        self._target_room_temp = temperature
        _LOGGER.info("Set room temperature to %.1f°C", temperature)

    async def set_element_temperature(self, temperature: float) -> None:
        """Set target element temperature."""
        if not self.is_connected:
            await self.connect()

        temp_value = int(temperature * 10)

        current_data = await self._client.read_gatt_char(CHAR_ELEMENT_TEMP)
        if len(current_data) < 4:
            raise ValueError("Invalid data from device")

        new_data = current_data[0:2] + struct.pack("<H", temp_value)

        await self._client.write_gatt_char(CHAR_ELEMENT_TEMP, new_data)
        self._target_element_temp = temperature
        _LOGGER.info("Set element temperature to %.1f°C", temperature)

    async def set_mode(self, mode: OperatingMode) -> None:
        """Set operating mode."""
        if not self.is_connected:
            await self.connect()

        # Režim je 4 bajty: [mode, 0x00, 0x00, 0x00]
        mode_data = bytes([mode.value, 0x00, 0x00, 0x00])
        await self._client.write_gatt_char(CHAR_MODE, mode_data)
        self._mode = mode
        _LOGGER.info("Set mode to %s", mode.name)

    async def turn_on(self, use_room_temp: bool = True) -> None:
        """Turn on the heater."""
        # Podle Frida zachycení používá aplikace režim MANUAL (0x01)
        await self.set_mode(OperatingMode.MANUAL)

    async def turn_off(self) -> None:
        """Turn off the heater."""
        await self.set_mode(OperatingMode.OFF)
