# Detailed Installation Instructions

## Preparation

### 1. Check Bluetooth Adapter

First, ensure your Home Assistant has functional Bluetooth:

```bash
# In Home Assistant terminal, run:
hcitool dev
```

You should see your Bluetooth adapter listed. If not, you need to install or enable Bluetooth.

### 2. Prepare Heating Element

1. Ensure the heating element is connected to mains power
2. Ensure the radiator is properly filled with fluid
3. **Never run the heating element dry!**

## Installation via HACS (Recommended)

### Step 1: Install HACS

If you don't have HACS installed yet:

1. Visit https://hacs.xyz/docs/setup/download
2. Follow the installation instructions
3. Restart Home Assistant

### Step 2: Add Custom Repository

1. Open HACS in Home Assistant (`Settings` → `HACS`)
2. Click the three dots in the top right corner
3. Select `Custom repositories`
4. Enter URL: `https://github.com/johnfromul/terma_moa_blue`
5. Select category `Integration`
6. Click `Add`

### Step 3: Install Integration

1. In HACS, search for "Terma MOA Blue"
2. Click on the integration card
3. Click `Download`
4. Restart Home Assistant

## Manual Installation

### Step 1: Download Files

```bash
cd /config
mkdir -p custom_components
cd custom_components
git clone https://github.com/johnfromul/terma_moa_blue.git
```

or download and extract ZIP:

```bash
cd /config/custom_components
wget https://github.com/johnfromul/terma_moa_blue/archive/refs/heads/main.zip
unzip main.zip
mv terma_moa_blue-main terma_moa_blue
```

### Step 2: Verify Structure

Ensure you have the correct structure:

```
custom_components/
└── terma_moa_blue/
    ├── __init__.py
    ├── api.py
    ├── climate.py
    ├── config_flow.py
    ├── const.py
    ├── coordinator.py
    ├── manifest.json
    ├── sensor.py
    ├── strings.json
    └── translations/
        ├── cs.json
        └── en.json
```

### Step 3: Restart

Restart Home Assistant.

## Configuration

### Step 1: Bluetooth Pairing (REQUIRED)

**Important:** Devices must be Bluetooth paired before use.

#### Put Device in Pairing Mode

1. **Press and hold** the button on the heating element for **5 seconds**
2. Release when the **blue LED starts blinking**
3. Pairing mode is active for **30 seconds**
4. You must complete pairing within this time

**Note:** If the heating element is paired with the Terma mobile app, you must unpair it first.

#### Pair via Terminal

```bash
# Open Home Assistant terminal (SSH or Terminal addon)
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

#### Restart Home Assistant

```bash
ha core restart
```

### Step 2: Add Integration

1. Go to `Settings` → `Devices & Services`
2. Click `+ Add Integration`
3. Search for **Terma MOA Blue**

#### Automatic Discovery

If the heating element is in range and in pairing mode, it should be automatically discovered:

1. Select it from the list
2. Confirm addition

#### Manual Selection

If automatic discovery doesn't work:

1. Click the button for manual selection
2. Select device from the list of Bluetooth devices
3. MAC address format: `XX:XX:XX:XX:XX:XX`

### Step 3: Complete Configuration

After successful addition, the following will be created:
- 2× Climate entities (room and element temperature)
- 5× Sensor entities (temperatures and mode)

## Verify Functionality

### Check in Developer Tools

1. Go to `Developer Tools` → `States`
2. Search for entities starting with `climate.terma_wireless_`
3. You should see current state (temperatures, mode)

### Test Control

1. Go to `Developer Tools` → `Services`
2. Select service `climate.set_temperature`
3. Select entity `climate.terma_wireless_room`
4. Set temperature (e.g., 22°C)
5. Click `Call Service`

The heating element should start heating and LEDs should indicate activity.

## Troubleshooting Installation

### Integration Not Showing in List

**Solution:**
1. Verify files are in correct folder
2. Restart Home Assistant
3. Clear browser cache (Ctrl+F5)

### "No devices found"

**Solution:**
1. Ensure heating element is powered on
2. Put it in pairing mode
3. Check Bluetooth range
4. Try restarting Bluetooth:
   ```bash
   sudo systemctl restart bluetooth
   ```

### "Already configured"

**Solution:**
1. Go to `Settings` → `Devices & Services`
2. Find old Terma MOA Blue instance
3. Click three dots and select `Remove`
4. Restart Home Assistant
5. Try again

### "Unable to connect"

**Solution:**
1. Unpair heating element from Terma mobile app
2. Reset Bluetooth pairing on heating element (disconnect from power, wait 10s, reconnect)
3. Put in pairing mode
4. Try connection again

### "Device not paired" or "ATT error 0x0e"

**Solution:**
The device requires Bluetooth pairing. Follow the pairing steps above:
```bash
bluetoothctl
pair CC:22:37:11:47:6D
# PIN: 123456
trust CC:22:37:11:47:6D
```

### Error in log: "bleak not found"

**Solution:**
```bash
# In Home Assistant container or venv:
pip install bleak>=0.21.0 bleak-retry-connector>=3.1.0
```

## Advanced Configuration

### Change Update Interval

If you want to change how often data updates (default is 120s):

1. Edit file `const.py`
2. Change line: `UPDATE_INTERVAL = 120` to desired value in seconds
3. Restart Home Assistant

**Note:** Lower values mean more frequent updates but also higher Bluetooth load.

### Debug Logging

For detailed logs:

1. Add to `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.terma_moa_blue: debug
   ```
2. Restart Home Assistant
3. Find logs in `Settings` → `System` → `Logs`

## Safety Warning

⚠️ **IMPORTANT SAFETY INFORMATION**

1. **Never run heating element dry** - radiator must be fully filled with fluid
2. **Maximum temperature** - do not exceed maximum temperature of 60°C for heating element
3. **Regular checks** - monitor fluid level in radiator
4. **Electrical safety** - installation should only be performed by qualified electrician
5. **Child safety** - keep children away from hot surfaces

## Support

If you have problems:

1. Check Home Assistant logs
2. Search for similar issue in GitHub Issues
3. Create new issue with:
   - Problem description
   - Logs from Home Assistant
   - Home Assistant version
   - Heating element model

## Next Steps

After successful installation:

1. Create automations (see README.md and EXAMPLES.md)
2. Add to Lovelace dashboard
3. Set up scenes for different times of day
4. Use Google Assistant / Alexa integration

## Multiple Devices

To add multiple heating elements:

1. Pair each device via `bluetoothctl` (use different MAC addresses)
2. Add each as separate integration in Home Assistant
3. Each device will have its own set of entities

Example for two devices:
```bash
# First device
bluetoothctl pair CC:22:37:11:48:0D
bluetoothctl trust CC:22:37:11:48:0D

# Second device
bluetoothctl pair CC:22:37:11:47:6D
bluetoothctl trust CC:22:37:11:47:6D
```

Then add both through the integration UI.
