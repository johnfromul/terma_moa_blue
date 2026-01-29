# Terma MOA Blue - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/johnfromul/terma_moa_blue.svg)](https://github.com/johnfromul/terma_moa_blue/releases)
[![License](https://img.shields.io/github/license/johnfromul/terma_moa_blue.svg)](LICENSE)

Home Assistant custom integration for **Terma MOA Blue** electric heating elements via Bluetooth Low Energy (BLE).

This integration allows you to control Terma MOA Blue bathroom radiator heating elements directly from Home Assistant without requiring the official Terma BlueLine Next mobile app.

![Terma MOA Blue](https://en.termaheat.com/images/logo_terma_red_horizontal_2.svg)

## Features

✅ **Full Control**
- Turn heating on/off
- Set target temperature (30-60°C for element, 15-30°C for room)
- Real-time temperature monitoring
- LED temperature indicator support

✅ **Native Home Assistant Integration**
- Climate entity for easy control
- Temperature sensor entities
- Lovelace thermostat card compatible
- Automation support

✅ **Reliable Bluetooth Communication**
- Automatic device discovery
- Multiple retry attempts for stable connection
- Proper BLE pairing support
- Works with Bluetooth adapters and ESPHome Bluetooth proxies

## Compatibility

### Supported Devices
- **Terma MOA Blue** electric heating elements (models with Bluetooth)
- Firmware: Tested with devices from 2023-2024

### Requirements
- Home Assistant 2024.1.0 or newer
- Bluetooth adapter with BLE support **OR** ESPHome Bluetooth proxy
- Python 3.11+

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots (⋮) in the top right
4. Select "Custom repositories"
5. Add repository URL: `https://github.com/johnfromul/terma_moa_blue`
6. Category: `Integration`
7. Click "Add"
8. Click "Install" on the Terma MOA Blue integration
9. Restart Home Assistant

### Manual Installation

1. Download the [latest release](https://github.com/johnfromul/terma_moa_blue/releases)
2. Extract the `terma_moa_blue` folder to your `custom_components` directory:
   ```
   config/
   └── custom_components/
       └── terma_moa_blue/
           ├── __init__.py
           ├── manifest.json
           ├── ...
   ```
3. Restart Home Assistant

## Setup

### Step 1: Bluetooth Pairing

**Important:** Terma MOA Blue devices require Bluetooth pairing before use.

#### Put Device in Pairing Mode
1. Press and hold the button on the heating element for **5 seconds**
2. The **blue LED will start blinking** (pairing mode active for 30 seconds)

#### Pair via Home Assistant Terminal

```bash
# Open Home Assistant terminal (SSH or Terminal & SSH add-on)
bluetoothctl

# Disable scanning to stop log spam
scan off

# Pair with your device (replace with your MAC address)
pair CC:22:37:11:47:6D

# Enter PIN when prompted
123456

# Trust the device
trust CC:22:37:11:47:6D

# Verify pairing
paired-devices

# Exit
quit
```

$\color{red}{\text{### !!! if you have a problem in the terminal with unstopable ble ads scanning.}}$
make a easy bash script \config\terma_pair.sh with this code:
```sh
#!/bin/bash

# Switch the heating element into pairing mode!
echo "!!! SWITCH THE HEATING ELEMENT INTO PAIRING MODE (5s hold button, blue
LED slow blink) !!!"
echo "You have 30 seconds..."
sleep 10

{
  sleep 2
  echo "agent KeyboardDisplay"
  sleep 1
  echo "default-agent"
  sleep 1
  echo "pair CC:22:37:11:48:0D"
  sleep 3
  echo "123456"
  sleep 5
  echo "trust CC:22:37:11:48:0D"
  sleep 2
  echo "quit"
} | bluetoothctl
EOF
```

#### Restart Home Assistant
```bash
ha core restart
```

### Step 2: Add Integration

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Terma MOA Blue"**
4. Select your heating element from the discovered devices
5. Click **Submit**

The integration will create:
- 1 Climate entity (thermostat)
- 2 Temperature sensor entities (current room, current element)

## Usage

### Via Lovelace UI

Add a thermostat card to your dashboard:

```yaml
type: thermostat
entity: climate.terma_wireless_element
```

### Via Services

**Turn on heating:**
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.terma_wireless_element
data:
  hvac_mode: heat
```

**Set temperature:**
```yaml
service: climate.set_temperature
target:
  entity_id: climate.terma_wireless_element
data:
  temperature: 50
```

**Turn off:**
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.terma_wireless_element
data:
  hvac_mode: "off"
```

### Automation Example

Heat bathroom before morning shower:

```yaml
automation:
  - alias: "Morning Bathroom Heat"
    trigger:
      - platform: time
        at: "06:00:00"
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.terma_wireless_element
        data:
          hvac_mode: heat
      - service: climate.set_temperature
        target:
          entity_id: climate.terma_wireless_element
        data:
          temperature: 55
      - delay:
          minutes: 30
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.terma_wireless_element
        data:
          hvac_mode: "off"
```

## Configuration

### Temperature Ranges

- **Element Temperature:** 30-60°C (radiator heating element)
- **Room Temperature:** 15-30°C (ambient room temperature)

### Update Interval

The integration polls the device every **120 seconds** (2 minutes) to preserve battery life and BLE connection stability.

### LED Temperature Indicator

The heating element's LED bars indicate the current target temperature:
- 1 bar: 30-37°C
- 2 bars: 38-43°C
- 3 bars: 44-49°C
- 4 bars: 50-55°C
- 5 bars: 56-60°C

## Troubleshooting

### Device Not Discovered

1. **Check Bluetooth range:** Ensure heating element is within range of your Bluetooth adapter
2. **Put device in pairing mode:** Blue LED should be blinking
3. **Check logs:** Settings → System → Logs, filter by `terma_moa_blue`

### Connection Errors

**Error:** `failed to discover services, device disconnected`

**Solution:** Device is not paired. Follow the Bluetooth pairing steps above.

**Error:** `ATT error: 0x0e (Unlikely Error)`

**Solution:** Authentication failed. Remove old pairing and pair again:
```bash
bluetoothctl
remove CC:22:37:11:47:6D
# Then follow pairing steps again
```

### Heating Not Starting

1. Verify device is powered (connected to mains)
2. Check wattmeter: should show ~600W when heating
3. Enable debug logging (see below)
4. Check that heating mode is set correctly

### Debug Logging

Enable detailed logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.terma_moa_blue: debug
```

Restart Home Assistant and check the logs.

## Technical Details

### Protocol Reverse Engineering

This integration was developed through reverse engineering of the Terma BlueLine Next mobile app using Frida instrumentation.

**Key findings:**
- Device uses Bluetooth Low Energy (BLE) GATT protocol
- Service UUID: `d97352b0-d19e-11e2-9e96-0800200c9a66`
- Operating modes: `0x20` (OFF), `0x21` (ON)
- Temperature format: Little-endian 16-bit integer (value × 10)
- Requires Bluetooth pairing with PIN `123456`

### BLE Characteristics

| UUID | Function | Format |
|------|----------|--------|
| `d97352b1` | Room temperature | `[current_low, current_high, target_low, target_high]` |
| `d97352b2` | Element temperature | `[current_low, current_high, target_low, target_high]` |
| `d97352b3` | Operating mode | `[mode, 0x00, 0x00, 0x00]` |

## Development

### Project Structure

```
custom_components/terma_moa_blue/
├── __init__.py          # Integration setup
├── manifest.json        # Integration metadata
├── config_flow.py       # Configuration flow
├── const.py            # Constants and enums
├── coordinator.py      # Data update coordinator
├── api.py             # BLE communication layer
├── climate.py         # Climate entity
└── sensor.py          # Sensor entities
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Reverse Engineering Process

The protocol was reverse-engineered using:
- Frida instrumentation framework
- Android app decompilation (JADX)
- BLE packet capture (Wireshark)
- Runtime hooking of Bluetooth GATT operations

See [Frida scripts](docs/frida/) for details.

## Credits

- **Developer:** [@johnfromul](https://github.com/johnfromul)
- **Assistant:** Claude (Anthropic) - Protocol analysis and integration development
- **Manufacturer:** [Terma](https://www.terma.com/)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial integration not affiliated with or endorsed by Terma. Use at your own risk.

The integration was developed through reverse engineering for personal use and educational purposes. All trademarks belong to their respective owners.

## Support

- **Issues:** [GitHub Issues](https://github.com/johnfromul/terma_moa_blue/issues)
- **Discussions:** [GitHub Discussions](https://github.com/johnfromul/terma_moa_blue/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Related Projects

- [Home Assistant](https://www.home-assistant.io/)
- [HACS](https://hacs.xyz/)
- [Bleak](https://github.com/hbldh/bleak) - BLE library
- [ESPHome Bluetooth Proxy](https://esphome.io/components/bluetooth_proxy.html)

---

⭐ If you find this integration useful, please star the repository!
