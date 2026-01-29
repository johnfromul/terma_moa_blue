# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.14] - 2025-01-26

### Fixed
- Fixed GUI turn off functionality - climate entity now properly recognizes new operating modes (0x20 OFF, 0x21 ON)
- Fixed hvac_mode property to correctly map device states to Home Assistant HVAC modes

## [1.0.13] - 2025-01-26

### Fixed
- **CRITICAL:** Fixed operating mode commands based on Frida reverse engineering
  - Turn ON now sends `0x21` (33) instead of incorrect `0x01`
  - Turn OFF now sends `0x20` (32) instead of incorrect `0x00`
  - Device now actually heats (~600W power consumption)
  - LED temperature indicator now responds correctly

### Changed
- Updated OperatingMode enum with correct values from mobile app protocol analysis

## [1.0.11] - 2025-01-26

### Fixed
- **CRITICAL:** Fixed temperature write format - now sends `[0x00, 0x00, target_low, target_high]` matching mobile app behavior
- Removed incorrect current temperature preservation in write operations
- Temperature changes now properly reflected on device LED indicators

## [1.0.10] - 2025-01-26

### Added
- Enhanced debug logging for temperature operations
- Verification reads after temperature writes

## [1.0.9] - 2025-01-26

### Added
- Automatic Bluetooth pairing attempt during connection
- Timing delays between read/write operations (0.2s before write, 0.1s after)

### Fixed
- Improved connection stability with proper delay handling

## [1.0.8] - 2025-01-26

### Changed
- Implemented manual retry logic (3 attempts) with temporary BLE connections
- Connection timeout increased to 15 seconds
- 2-second delay between retry attempts

### Fixed
- More detailed error logging with error type information

## [1.0.7] - 2025-01-26

### Added
- Device discovery by SERVICE UUID (`d97352b0-d19e-11e2-9e96-0800200c9a66`)
- Fallback discovery by device name for compatibility

### Fixed
- Now discovers devices with custom names (e.g., "balkon" instead of "Terma Wireless")

## [1.0.4-1.0.6] - 2025-01-26

### Changed
- Various connection management improvements
- Protocol refinements based on initial Frida analysis

## [1.0.0-1.0.3] - 2025-01-23

### Added
- First stable release of Terma MOA Blue integration
- Bluetooth Low Energy communication with heating elements
- Two climate entities:
  - Room temperature control (15-30°C)
  - Element temperature control (30-60°C)
- Five sensor entities:
  - Current room temperature
  - Target room temperature
  - Current element temperature
  - Target element temperature
  - Operating mode
- Automatic Bluetooth device discovery
- GUI configuration via config flow
- Pairing mode support with PIN code 123456
- Support for all operating modes:
  - OFF (turned off)
  - ROOM_TEMP_MANUAL (manual room temperature control)
  - ELEMENT_TEMP_MANUAL (manual element temperature control)
  - ROOM_TEMP_SCHEDULE (scheduled room temperature)
  - ELEMENT_TEMP_SCHEDULE (scheduled element temperature)
- Complete Czech and English localization
- Comprehensive documentation:
  - README with overview and examples
  - INSTALL.md with detailed installation instructions
  - EXAMPLES.md with Lovelace card and automation examples
  - Code comments
- Automation examples for common scenarios
- Lovelace card examples
- HACS installation support
- MIT License

### Security
- Connection verification before each operation
- Automatic reconnection on connection loss
- Temperature limit validation
- Safety warnings in documentation
- Dry run protection (warnings in documentation)

### Technical Details
- Uses bleak>=0.21.0 for BLE communication
- Uses bleak-retry-connector>=3.1.0 for reliable connections
- DataUpdateCoordinator implementation for efficient data management
- Update interval: 120 seconds (configurable)
- Support for Home Assistant 2023.9.0+

### Inspired By
- [terma-moa-blue-esphome](https://github.com/Andrew-a-g/terma-moa-blue-esphome) by Andrew-a-g
- [homebridge-TERMA-MOA-Blue](https://github.com/J1mbo/homebridge-TERMA-MOA-Blue) by J1mbo
- [ha-hudsonread-heater-control](https://github.com/mecorre1/ha-hudsonread-heater-control) by mecorre1
- [Home Assistant Community](https://community.home-assistant.io/t/terma-blue-line-bluetooth-radiators-and-heating-elements/81325)

## [Unreleased]

### Planned Features
- Support for multiple heating elements simultaneously
- Schedule support
- Boost mode with timer
- Energy consumption statistics
- Automatic eco modes
- Open window detection
- Integration with third-party temperature sensors
- Push notifications on state changes

---

Date format: YYYY-MM-DD
