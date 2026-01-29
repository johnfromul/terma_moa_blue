# Quick Start - Terma MOA Blue

## 5 Steps to Working Integration

### 1️⃣ Install via HACS (2 minutes)

1. Open HACS in Home Assistant
2. Three dots → Custom repositories
3. Enter: `https://github.com/johnfromul/terma_moa_blue`
4. Category: Integration → Add
5. Search "Terma MOA Blue" → Download
6. Restart Home Assistant

### 2️⃣ Pair Heating Element (30 seconds)

**REQUIRED:** Device must be Bluetooth paired before use.

```bash
# Open Home Assistant terminal
bluetoothctl
scan off
pair CC:22:37:11:47:6D
# PIN: 123456
trust CC:22:37:11:47:6D
quit

# Restart Home Assistant
ha core restart
```

### 3️⃣ Add to Home Assistant (1 minute)

1. **Settings** → **Devices & Services**
2. **+ Add Integration**
3. Search: **Terma MOA Blue**
4. Select device from list
5. Done! ✅

### 4️⃣ Verify Functionality (30 seconds)

Check entities in Developer Tools → States:
- ✅ `climate.terma_wireless_room`
- ✅ `climate.terma_wireless_element`
- ✅ `sensor.terma_wireless_current_room_temperature`
- ✅ `sensor.terma_wireless_operating_mode`

### 5️⃣ First Test (30 seconds)

Developer Tools → Services:
```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.terma_wireless_element
data:
  hvac_mode: heat
```

Click **Call Service** - heating element should start heating! 🔥

Check power meter: should show ~600W when heating.

## Basic Lovelace Card (copy & paste)

```yaml
type: thermostat
entity: climate.terma_wireless_element
```

## First Automation

Morning heating at 6:00 AM:

```yaml
automation:
  - alias: "Bathroom Heating - Morning"
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
          minutes: 45
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.terma_wireless_element
        data:
          hvac_mode: "off"
```

## Troubleshooting - Quick Tips

### ❌ "No devices found"
→ Heating element not in pairing mode - press button 5s until blue LED blinks

### ❌ "Unable to connect" or "ATT error 0x0e"
→ Device not paired. Pair via `bluetoothctl` (see step 2)

### ❌ "failed to discover services"
→ Device requires Bluetooth pairing with PIN 123456

### ❌ Integration not showing
→ Clear browser cache (Ctrl+F5), restart HA

### ❌ "Already configured"  
→ Remove old integration in Devices & Services

### ❌ Device won't heat (0.4W power consumption)
→ Update to v1.0.13+ which uses correct operating modes (0x21 ON, 0x20 OFF)

## Next Steps

📚 **Full documentation:** [README.md](README.md)  
🛠️ **Installation guide:** [INSTALL.md](INSTALL.md)  
💡 **Usage examples:** [EXAMPLES.md](EXAMPLES.md)  

## Need Help?

🐛 [Report an issue](https://github.com/johnfromul/terma_moa_blue/issues)  
💬 [Forum discussion](https://community.home-assistant.io/)

---

**Total installation time: ~10 minutes** ⏱️
(includes Bluetooth pairing)
