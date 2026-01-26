# Bluetooth Pairing Guide for Terma MOA Blue

## ⚠️ IMPORTANT: Devices REQUIRE Bluetooth Pairing!

Terma MOA Blue heating elements require **Bluetooth pairing with PIN code 123456** BEFORE use in Home Assistant.

## Step-by-Step Pairing Process

### 1. Pair Heating Elements Manually in Home Assistant

```bash
# Connect to Home Assistant terminal (SSH or Terminal & SSH addon)

# Start bluetoothctl
bluetoothctl

# Turn on Bluetooth and disable scanning (to stop log spam)
power on
scan off
```

You should see something like:
```
[bluetooth]# 
```

### 2. Pair First Device

```bash
# Pair FIRST heating element (replace with your MAC address)
pair CC:22:37:11:48:0D
```

When prompted for PIN, enter: **123456**

```bash
# After successful pairing:
trust CC:22:37:11:48:0D
```

### 3. Pair Second Device (if you have multiple)

```bash
# Pair SECOND heating element
pair CC:22:37:11:47:6D

# Enter PIN: 123456

trust CC:22:37:11:47:6D
```

### 4. Verify Pairing

```bash
# List paired devices
paired-devices

# You should see something like:
# Device CC:22:37:11:48:0D Terma Wireless
# Device CC:22:37:11:47:6D balkon

# Exit bluetoothctl
quit
```

### 5. Restart Home Assistant

```bash
ha core restart
```

## Add Integration

1. Settings → Devices & Services
2. + Add Integration
3. Search "Terma MOA Blue"
4. Select heating element from list

## Repeat for Each Device

If you have multiple heating elements, add each as a separate integration.

---

## Notes

- v1.0.9+ includes automatic `client.pair()`, but manual pairing is still recommended for reliability
- PIN code is always **123456**
- Devices must NOT be in pairing mode for terminal pairing (blue LED blinking)
- After pairing, devices are "trusted" and will work without pairing mode

## Troubleshooting

### Pairing Fails

```bash
# Remove old pairing
bluetoothctl
remove CC:22:37:11:48:0D
quit

# Restart Bluetooth service
sudo systemctl restart bluetooth

# Try pairing again
bluetoothctl
pair CC:22:37:11:48:0D
# PIN: 123456
trust CC:22:37:11:48:0D
quit
```

### Device Not Responding

1. Disconnect from power for 30 seconds
2. Reconnect
3. Wait 1 minute
4. Try pairing again

### "ATT error: 0x0e (Unlikely Error)"

This means the device is not paired. Follow the pairing steps above.

### "failed to discover services, device disconnected"

This also means the device requires pairing. Complete the pairing process first.

## Why Is Pairing Required?

Terma MOA Blue devices use **Bluetooth security** that requires authentication before allowing access to GATT characteristics. Without pairing:

- Connection succeeds initially
- But reading/writing characteristics fails
- Device immediately disconnects

The mobile app handles this pairing automatically on first use. For Home Assistant, we need to pair manually via `bluetoothctl`.

## Alternative: Pairing Mode

Some users report success by putting the device in pairing mode (blue LED blinking for 30 seconds) during the terminal pairing process. To do this:

1. Start the `bluetoothctl pair` command
2. While it's attempting to pair, press and hold the button on the heating element for 5 seconds
3. Blue LED should start blinking
4. Enter PIN when prompted

However, manual pairing without pairing mode is generally more reliable.
