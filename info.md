{% if installed %}
## Changes in This Version

### Version 1.0.14

- ✅ Fixed GUI turn off functionality
- ✅ Climate entity now properly recognizes operating modes
- ✅ Complete protocol analysis via Frida reverse engineering
- ✅ Correct operating mode commands (0x21 ON, 0x20 OFF)
- ✅ Device actually heats (~600W power consumption)
- ✅ LED temperature indicator responds correctly

### Version 1.0.13

- ✅ **CRITICAL FIX:** Correct operating mode commands
- ✅ Turn ON sends 0x21 instead of incorrect 0x01
- ✅ Turn OFF sends 0x20 instead of incorrect 0x00
- ✅ Temperature format fixed to match mobile app

### Version 1.0.0

- ✅ First stable release
- ✅ Full Bluetooth Low Energy support
- ✅ Two climate entities (room and element temperature)
- ✅ Five sensors (current and target temperatures, mode)
- ✅ Automatic device discovery
- ✅ Czech and English language support
- ✅ Complete documentation and examples

{% else %}
## Welcome to Terma MOA Blue Integration!

This integration allows you to control Terma MOA Blue heating elements directly from Home Assistant via Bluetooth.

### Features

- 🔌 **Easy Installation** - automatic Bluetooth device discovery
- 🌡️ **Two Climate Entities** - control by room or element temperature
- 📊 **Sensors** - current and target temperatures, operating mode
- 🔄 **Automations** - full Home Assistant automation support
- 🌍 **Multilingual** - Czech and English support
- 📖 **Documentation** - detailed guides and examples

### Before Installation

Ensure that:
- You have a functional Bluetooth adapter in Home Assistant
- Heating element is powered on and filled with fluid
- **Device must be Bluetooth paired** (PIN: 123456)

### After Installation

#### 1. Pair Device via Terminal (REQUIRED)

```bash
bluetoothctl
scan off
pair CC:22:37:11:47:6D
# PIN: 123456
trust CC:22:37:11:47:6D
quit
```

Then restart Home Assistant: `ha core restart`

#### 2. Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search **Terma MOA Blue**
4. Select device from list

### Useful Links

- 📚 [Complete Documentation](https://github.com/johnfromul/terma_moa_blue/blob/main/README.md)
- 🛠️ [Installation Guide](https://github.com/johnfromul/terma_moa_blue/blob/main/INSTALL.md)
- 💡 [Usage Examples](https://github.com/johnfromul/terma_moa_blue/blob/main/EXAMPLES.md)
- 🐛 [Report Issue](https://github.com/johnfromul/terma_moa_blue/issues)

### Warning

⚠️ **SAFETY:** Never run the heating element dry! Radiator must always be fully filled with fluid.

{% endif %}
