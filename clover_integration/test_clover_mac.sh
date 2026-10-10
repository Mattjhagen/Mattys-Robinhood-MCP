#!/bin/bash
# Test Clover C505 on macOS

echo "======================================"
echo "  Clover C505 Mac Connection Test"
echo "======================================"
echo ""

echo "1. Checking USB devices..."
echo ""
system_profiler SPUSBDataType | grep -B 5 -A 10 -i clover 2>/dev/null
system_profiler SPUSBDataType | grep -B 5 -A 10 -i android 2>/dev/null
echo ""

echo "2. Checking for ADB..."
which adb > /dev/null && echo "✓ ADB installed" || echo "✗ ADB not installed - Run: brew install android-platform-tools"
echo ""

if which adb > /dev/null; then
    echo "3. Checking ADB devices..."
    adb devices -l 2>/dev/null
    echo ""
fi

echo "======================================"
echo "Manual Test Instructions:"
echo "======================================"
echo ""
echo "1. Open TextEdit or Notes on Mac"
echo "2. Click in a text field"
echo "3. Press numbers on C505 PIN pad"
echo ""
echo "   ✅ Numbers appear = USB keyboard mode works!"
echo "   ❌ Nothing happens = Try ADB or check cable"
echo ""
echo "4. Test these keys:"
echo "   - 0-9 (number keys)"
echo "   - * (star key)"
echo "   - # (pound key)"
echo "   - Green button (should be Enter)"
echo "   - Red button (should be Backspace)"
echo ""
echo "Report back what works!"
echo ""
