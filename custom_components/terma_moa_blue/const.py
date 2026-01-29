"""Constants for the Terma MOA Blue integration."""
from enum import IntEnum

DOMAIN = "terma_moa_blue"

# BLE Service and Characteristics UUIDs
SERVICE_UUID = "d97352b0-d19e-11e2-9e96-0800200c9a66"
CHAR_ROOM_TEMP = "d97352b1-d19e-11e2-9e96-0800200c9a66"
CHAR_ELEMENT_TEMP = "d97352b2-d19e-11e2-9e96-0800200c9a66"
CHAR_MODE = "d97352b3-d19e-11e2-9e96-0800200c9a66"

# Default pairing code
DEFAULT_PAIRING_CODE = "123456"

# Update intervals
UPDATE_INTERVAL = 300  # 5 minutes - reduced BT adapter load - heating elements need longer pause between connections

# Temperature limits
MIN_ROOM_TEMP = 15
MAX_ROOM_TEMP = 30
MIN_ELEMENT_TEMP = 30
MAX_ELEMENT_TEMP = 60


class OperatingMode(IntEnum):
    """Operating modes for Terma MOA Blue."""

    OFF_MANUAL = 0x00  # 0 - turned off manually on device
    OFF = 0x20  # 32 - turned off via app/HA
    ON = 0x21   # 33 - turned on/heating
    
    # Legacy values (possibly unused)
    MANUAL = 1
    ROOM_TEMP_MANUAL = 5
    ELEMENT_TEMP_MANUAL = 6
    ROOM_TEMP_SCHEDULE = 7
    ELEMENT_TEMP_SCHEDULE = 8
