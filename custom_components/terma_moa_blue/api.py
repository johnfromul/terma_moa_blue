"""API for Terma MOA Blue integration - temporary connections with manual retry."""
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

# Connection settings
MAX_CONNECT_ATTEMPTS = 5  # Zvýšeno z 3 na 5
CONNECTION_TIMEOUT = 20.0  # Zvýšeno z 15 na 20 sekund
RETRY_DELAY = 3.0  # Zvýšeno z 2 na 3 sekundy mezi pokusy


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
        """Execute an operation with a temporary BLE connection and retry logic."""
        async with self._lock:
            last_error = None
            
            for attempt in range(MAX_CONNECT_ATTEMPTS):
                client = None
                try:
                    _LOGGER.debug(
                        "Attempt %d/%d: Connecting to %s",
                        attempt + 1,
                        MAX_CONNECT_ATTEMPTS,
                        self.address,
                    )
                    
                    # Create temporary connection
                    client = BleakClient(
                        self._ble_device.address,
                        timeout=CONNECTION_TIMEOUT,
                    )
                    
                    # Connect with pairing
                    await client.connect()
                    
                    # Try to pair if not already paired
                    try:
                        await client.pair()
                        _LOGGER.debug("Pairing successful for %s", self.address)
                    except Exception as pair_err:
                        # Pairing might fail if already paired - that's OK
                        _LOGGER.debug("Pairing skipped for %s: %s", self.address, pair_err)
                    
                    if not client.is_connected:
                        raise BleakError("Failed to establish connection")
                    
                    _LOGGER.debug("Connected to %s, executing operation", self.address)
                    
                    # Execute the operation
                    await operation(client)
                    
                    _LOGGER.debug("Operation completed successfully")
                    return  # Success!
                    
                except BleakError as err:
                    last_error = err
                    _LOGGER.warning(
                        "BLE error on attempt %d/%d for %s: %s",
                        attempt + 1,
                        MAX_CONNECT_ATTEMPTS,
                        self.address,
                        err,
                    )
                except TimeoutError as err:
                    last_error = err
                    _LOGGER.warning(
                        "Timeout on attempt %d/%d for %s: %s",
                        attempt + 1,
                        MAX_CONNECT_ATTEMPTS,
                        self.address,
                        err,
                    )
                except Exception as err:
                    last_error = err
                    _LOGGER.warning(
                        "Unexpected error on attempt %d/%d for %s: %s (%s)",
                        attempt + 1,
                        MAX_CONNECT_ATTEMPTS,
                        self.address,
                        err,
                        type(err).__name__,
                    )
                finally:
                    # Always try to disconnect
                    if client is not None:
                        try:
                            if client.is_connected:
                                await client.disconnect()
                                _LOGGER.debug("Disconnected from %s", self.address)
                        except Exception as disconnect_err:
                            _LOGGER.debug(
                                "Error during disconnect from %s: %s",
                                self.address,
                                disconnect_err,
                            )
                
                # Wait before retry (except on last attempt)
                if attempt < MAX_CONNECT_ATTEMPTS - 1:
                    _LOGGER.debug(
                        "Waiting %.1f seconds before retry...", RETRY_DELAY
                    )
                    await asyncio.sleep(RETRY_DELAY)
            
            # All attempts failed
            error_msg = f"Failed to communicate with device after {MAX_CONNECT_ATTEMPTS} attempts"
            if last_error:
                error_msg = f"{error_msg}: {last_error}"
            _LOGGER.error(error_msg)
            raise BleakError(error_msg)

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
            
            # Mobile app ALWAYS sends [0x00, 0x00, target_low, target_high]
            new_data = bytes([0x00, 0x00]) + struct.pack("<H", temp_value)
            await client.write_gatt_char(CHAR_ROOM_TEMP, new_data)
            
            # Small delay after write to ensure it's processed
            await asyncio.sleep(0.1)
            
            self._target_room_temp = temperature
            _LOGGER.info("Set room temperature to %.1f°C", temperature)

        await self._execute_with_connection(write_temp)

    async def set_element_temperature(self, temperature: float) -> None:
        """Set target element temperature."""
        async def write_temp(client: BleakClient) -> None:
            temp_value = int(temperature * 10)
            
            # Mobile app ALWAYS sends [0x00, 0x00, target_low, target_high]
            # NOT [current_low, current_high, target_low, target_high]
            new_data = bytes([0x00, 0x00]) + struct.pack("<H", temp_value)
            
            _LOGGER.info("Writing element temp %.1f°C: %s (hex: %s)", 
                        temperature, [b for b in new_data], new_data.hex())
            
            await client.write_gatt_char(CHAR_ELEMENT_TEMP, new_data)
            
            # Small delay after write
            await asyncio.sleep(0.1)
            
            # Read back to verify
            verify_data = await client.read_gatt_char(CHAR_ELEMENT_TEMP)
            _LOGGER.info("Verify element temp: %s (hex: %s)", 
                        [b for b in verify_data], verify_data.hex())
            
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
        # Z Frida: režim 0x21 pro zapnutí
        await self.set_mode(OperatingMode.ON)

    async def turn_off(self) -> None:
        """Turn off the heater."""
        # Z Frida: režim 0x20 pro vypnutí (NE 0x00!)
        await self.set_mode(OperatingMode.OFF)
