# Using Clover C505 PIN Pad with P3 ATM

## Quick Start

The Clover C505 is a PIN pad that normally connects to a Clover terminal. We'll use it as an input device for the P3 ATM.

## Easiest Approach: USB HID Mode

Connect C505 to r510 via USB and use it as a keyboard:

```bash
# 1. Connect C505 to r510 USB port
# 2. Check if it appears as HID device
lsusb | grep -i clover

# 3. Make P3 ATM accessible
# Already done - runs on port 5050

# 4. Open browser on r510 to http://localhost:5050
# 5. C505 keystrokes should work as keyboard input
```

## Alternative: Enable ADB

If C505 has developer options:

```bash
# Install ADB on r510
sudo apt-get install -y adb

# Enable developer mode on C505:
# - Tap Clover logo 7 times
# - Enable USB Debugging

# Check connection
adb devices

# Install browser if needed
adb install chrome.apk

# Launch P3 ATM
adb shell am start -a android.intent.action.VIEW -d http://100.103.3.35:5050
```

## Display Specs

- **Screen**: 4" touchscreen, 800x480 pixels
- **Input**: Physical PIN pad + touchscreen  
- **OS**: Android (locked down)
- **Connection**: USB or Bluetooth

## Status

Experimental - C505 designed to work with main terminal, not standalone.

**Recommendation**: A $50 Android tablet might be easier!
