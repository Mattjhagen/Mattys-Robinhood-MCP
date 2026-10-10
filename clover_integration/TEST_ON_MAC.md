# Testing Clover C505 PIN Pad on Mac

## Quick Test Steps

### 1. Check USB Connection

**Plug in C505 via USB**, then open Terminal and run:

```bash
# See all USB devices
system_profiler SPUSBDataType | grep -A 10 -i clover

# Or use ioreg
ioreg -p IOUSB -l -w 0 | grep -i clover
```

**What to look for:**
- Device name (e.g., "Clover C505" or "Android Device")
- Vendor ID and Product ID
- Whether it shows as "HID" (keyboard) or "Android ADB"

### 2. Test as Keyboard

**Open TextEdit or Notes**, then:

1. Click in the text field
2. **Press keys on C505 PIN pad**
3. Watch if numbers appear!

**Try pressing:**
- `0-9` (number keys)
- `*` (asterisk/star)
- `#` (hash/pound)
- Green button (enter/confirm)
- Red button (cancel/backspace)

### 3. Test with P3 ATM

If keyboard mode works:

```bash
# Make sure P3 ATM is running on r510 first
# Then on Mac, open browser to:
http://100.103.3.35:5050

# Or if you're running it locally:
http://localhost:5050
```

**Test the flow:**
1. Browser opens to P3 ATM welcome screen
2. Click in the page (focus it)
3. Press **green button** on C505 (should trigger ENTER)
4. Type **0213** on C505 PIN pad
5. Press **green button** again
6. Should log you in!

### 4. Check for ADB (Android Debugging)

If C505 doesn't work as keyboard, try ADB:

```bash
# Install ADB on Mac (if not installed)
brew install android-platform-tools

# Or download from: https://developer.android.com/studio/releases/platform-tools

# Check if C505 is in ADB mode
adb devices

# If it shows:
# C050UQ12345678    device
# Then it's in ADB mode!
```

### 5. Enable Developer Mode on C505

If ADB doesn't see it:

1. On C505 touchscreen, **tap the Clover logo 7 times rapidly**
2. Look for "Developer Options" or "Settings"
3. Enable "USB Debugging"
4. Reconnect USB cable
5. Run `adb devices` again
6. Accept the "Allow USB debugging?" prompt on C505

## Expected Behaviors

### Scenario A: Works as USB Keyboard ✅
```bash
system_profiler SPUSBDataType | grep -i clover
# Shows: Product ID: 0x1234
#        Manufacturer: Clover
#        bInterfaceClass: 3 (HID)

# In TextEdit:
[Type on C505] → Numbers appear instantly
```

**This is ideal!** Use it directly with P3 ATM.

### Scenario B: Shows as Android Device 📱
```bash
system_profiler SPUSBDataType | grep -i android
# Shows: Android Device
#        or: Clover C505
#        bInterfaceClass: 255 (Vendor Specific)

adb devices
# Shows: C050UQ12345678    device
```

**Solution:** Use ADB to interact with C505's Android OS.

### Scenario C: Not Recognized ❌
```bash
system_profiler SPUSBDataType
# No Clover or Android devices listed
```

**Troubleshooting:**
- Try different USB cable (must be data cable, not charge-only)
- Try different USB port on Mac
- Restart C505 (hold power button 10 seconds)
- Factory reset C505 if you own it
- C505 might be locked to specific Clover terminal

## Test Results Checklist

Run these tests and record results:

- [ ] C505 powers on when plugged into Mac
- [ ] Mac recognizes C505 as USB device
- [ ] Device type: □ HID/Keyboard  □ Android  □ Unknown
- [ ] Number keys (0-9) register as keyboard input
- [ ] Green button works (Enter/Confirm)
- [ ] Red button works (Cancel/Backspace)
- [ ] `*` and `#` keys work
- [ ] ADB recognizes device: `adb devices`
- [ ] C505 screen is responsive to touch
- [ ] C505 can access network (if in ADB mode)

## Quick Test Script for Mac

Save this as `test_clover_mac.sh`:

```bash
#!/bin/bash
echo "======================================"
echo "  Clover C505 Mac Connection Test"
echo "======================================"
echo ""

echo "1. Checking USB devices..."
system_profiler SPUSBDataType | grep -B 5 -A 10 -i clover | head -20
system_profiler SPUSBDataType | grep -B 5 -A 10 -i android | head -20
echo ""

echo "2. Checking for ADB..."
which adb > /dev/null && echo "✓ ADB installed" || echo "✗ ADB not installed (brew install android-platform-tools)"
echo ""

if which adb > /dev/null; then
    echo "3. Checking ADB devices..."
    adb devices -l
    echo ""
fi

echo "======================================"
echo "Manual Tests:"
echo "======================================"
echo ""
echo "1. Open TextEdit or Notes on Mac"
echo "2. Click in a text field"
echo "3. Press numbers on C505 PIN pad"
echo "4. Do numbers appear?"
echo ""
echo "   YES = C505 works as USB keyboard! ✅"
echo "   NO  = Try ADB method or check connection ❌"
echo ""
```

## What to Report Back

After testing, let me know:

1. **USB Recognition:** Does Mac see the C505?
2. **Device Type:** HID (keyboard) or Android?
3. **Keyboard Test:** Do keys register in TextEdit?
4. **Which keys work:** Numbers? * and #? Green/Red buttons?
5. **ADB Status:** Does `adb devices` show it?

## Next Steps Based on Results

### If keyboard mode works:
→ Perfect! Connect to r510 and use with P3 ATM

### If ADB mode works:
→ Can launch P3 ATM URL directly on C505 screen

### If neither works:
→ C505 might be locked to Clover terminal only
→ Consider $50 Android tablet alternative

---

**Run the tests and let me know what you find!** 🧪
