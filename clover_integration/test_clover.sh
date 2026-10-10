#!/bin/bash
# Test Clover C505 connection to r510

echo "=================================="
echo "  Clover C505 Connection Test"
echo "=================================="
echo ""

echo "1. Checking USB devices..."
lsusb | grep -i clover && echo "✓ Clover found via USB" || echo "✗ Clover not found"
echo ""

echo "2. Checking for HID devices..."
ls /dev/input/event* 2>/dev/null | while read device; do
    echo "  Found: $device"
done
echo ""

echo "3. Checking ADB..."
which adb > /dev/null && echo "✓ ADB installed" || echo "✗ ADB not installed (sudo apt-get install -y adb)"
echo ""

if which adb > /dev/null; then
    echo "4. Checking ADB devices..."
    adb devices | tail -n +2 | grep -v "^$" && echo "✓ Device connected via ADB" || echo "✗ No ADB devices"
    echo ""
fi

echo "5. Checking P3 ATM server..."
curl -s http://localhost:5050/health > /dev/null && echo "✓ P3 ATM running on port 5050" || echo "✗ P3 ATM not running"
echo ""

echo "=================================="
echo "Next steps:"
echo "=================================="
echo ""
echo "If Clover found via USB:"
echo "  - Try typing on PIN pad while browser is focused"
echo "  - Keys should register as keyboard input"
echo ""
echo "If ADB device found:"
echo "  - Run: adb shell am start -a android.intent.action.VIEW -d http://100.103.3.35:5050"
echo "  - This opens P3 ATM on Clover screen"
echo ""
echo "If nothing works:"
echo "  - Try factory reset on C505 (hold power 10 sec)"
echo "  - Enable developer mode (tap Clover logo 7 times)"
echo "  - Or use a cheap Android tablet instead!"
echo ""
