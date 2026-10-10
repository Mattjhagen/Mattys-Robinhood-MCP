# Clover POS Integration with P3 ATM

## What You Have
- **Clover Customer Pad**: Touchscreen + secure card reader
- **P3 ATM Server**: Flask backend on r510 (100.103.3.35:5050)
- **Professional ATM Interface**: Black/green theme, trading features

## Integration Options

### 🚀 Option 1: Web Browser (5 Minutes)
**Easiest - Start Here**

1. **Make Flask server accessible from Clover:**
   ```bash
   cd /home/matt/Mattys-Robinhood-MCP/p3_atm
   
   # Edit atm_server.py line 157:
   # Change: app.run(host='127.0.0.1', port=5050)
   # To:     app.run(host='0.0.0.0', port=5050)
   
   # Restart service:
   sudo systemctl restart p3-atm-web
   ```

2. **On Clover device:**
   - Open Chrome/Browser app
   - Navigate to: `http://100.103.3.35:5050`
   - Tap "Add to Home Screen" for easy access
   - Enable fullscreen mode

**Pros:**
- ✅ Works immediately, no coding
- ✅ Touchscreen works perfectly
- ✅ Can test right now

**Cons:**
- ❌ PIN entered on touchscreen (not secure PIN pad)
- ❌ No card reader integration

---

### 🔐 Option 2: Clover PIN Pad Integration (Recommended)
**Most ATM-Like Experience**

Uses Clover's **secure PIN pad** (PCI-compliant) instead of touchscreen.

**What changes:**
- Customer inserts/swipes card
- Enters PIN on physical keypad (encrypted)
- ATM validates and shows interface

**Implementation:**

1. **Install Clover SDK dependencies:**
   ```bash
   pip install clover-python
   ```

2. **Update Flask server** (see `atm_server_with_clover.py`):
   - Add `/api/authenticate/card` endpoint
   - Handle encrypted PIN from Clover
   - Verify against your PIN hash

3. **Deploy bridge HTML** on Clover:
   - Open `clover_bridge.html` on Clover browser
   - Configure with your Clover merchant credentials
   - This handles card reading and PIN capture

**Setup Steps:**

```bash
# 1. Get Clover credentials from dashboard.clover.com
#    - Merchant ID
#    - API Token

# 2. Configure bridge
cd /home/matt/Mattys-Robinhood-MCP/clover_integration
# Edit clover_bridge.html with your credentials

# 3. Serve bridge to Clover (multiple options):

# Option A: Host on Flask server
cp clover_bridge.html /home/matt/Mattys-Robinhood-MCP/p3_atm/atm_templates/
# Access at: http://100.103.3.35:5050/clover

# Option B: USB transfer to Clover
# Copy clover_bridge.html to Clover's internal storage

# Option C: Clover as web app
# Upload to your Clover app market account
```

**Security Flow:**
```
1. Customer: Swipes card on Clover reader
2. Clover: "Enter PIN" on secure pad
3. Clover: Encrypts PIN in hardware
4. Bridge: Sends encrypted PIN to Flask server
5. Server: Decrypts and validates
6. Server: Returns auth token
7. Browser: Loads full ATM interface
```

---

### 🏆 Option 3: Native Android App (Most Professional)
**For Production Deployment**

A custom Android app for Clover that:
- Runs natively (not web browser)
- Full hardware integration
- Professional card reader flow
- Customer-facing display control

**Development Steps:**

1. **Set up Clover development environment:**
   ```bash
   # Install Android Studio
   # Install Clover SDK
   # See: https://docs.clover.com/docs/android-app-development
   ```

2. **Build APK from provided source:**
   ```bash
   cd /home/matt/Mattys-Robinhood-MCP/clover_integration
   # CloverATMActivity.java is the main activity
   # Communicates with Flask backend
   # Uses WebView for UI (your existing HTML)
   ```

3. **Install on Clover:**
   ```bash
   # Via USB debugging:
   adb install p3-atm-clover.apk
   
   # Or upload to Clover app market for distribution
   ```

**Features:**
- ✅ Native card reader integration
- ✅ Secure PIN pad (PCI-compliant)
- ✅ Customer display messages
- ✅ Full-screen kiosk mode
- ✅ Auto-start on device boot
- ✅ Professional ATM experience

---

## Quick Start (Try Now)

**Test in 2 minutes:**

```bash
# 1. On r510 server:
cd /home/matt/Mattys-Robinhood-MCP/p3_atm
sed -i "s/127.0.0.1/0.0.0.0/" atm_server.py
sudo systemctl restart p3-atm-web

# 2. On Clover device:
# Open browser → http://100.103.3.35:5050
```

## Clover Device Models

Works with:
- **Clover Mini** ✅
- **Clover Flex** ✅ 
- **Clover Station** ✅
- **Clover Mobile** ✅

All have:
- Android OS
- Touchscreen
- Secure card reader
- Chrome browser

## Hardware Requirements

**R510 Server:**
- ✅ Already running Flask server
- ✅ Already has ATM interface
- ✅ Connected to network

**Clover Device:**
- Must be on same network as r510
- Browser access to 100.103.3.35:5050
- For Option 2/3: Clover merchant account

**Network:**
- Clover → r510 connectivity
- Port 5050 accessible
- Optional: VPN for remote access

## Security Considerations

**Option 1 (Browser):**
- 🔴 PIN visible on touchscreen
- 🟡 Use only for demo/testing
- 🟡 Consider SSL/TLS

**Option 2 (PIN Pad):**
- 🟢 Encrypted PIN entry
- 🟢 Card data never touches browser
- 🟢 PCI-DSS compliant
- 🟡 Requires Clover SDK setup

**Option 3 (Native App):**
- 🟢 Fully PCI-compliant
- 🟢 Hardware security module
- 🟢 Secure element for keys
- 🟢 Production-ready

## Next Steps

1. **Start with Option 1** to verify connectivity
2. **Upgrade to Option 2** for secure PIN entry
3. **Build Option 3** when ready for customers

## Troubleshooting

**Clover can't reach server:**
```bash
# Check if Flask is listening on 0.0.0.0:
ss -tlnp | grep 5050

# Check firewall:
sudo ufw status
sudo ufw allow 5050/tcp

# Test from Clover:
# Open browser → http://100.103.3.35:5050/health
# Should see: {"status": "ok"}
```

**Clover SDK issues:**
- Verify merchant ID and API token
- Check Clover dashboard permissions
- Ensure device is activated

**Native app won't install:**
```bash
# Enable developer mode on Clover
# Settings → About → Tap build number 7 times
# Connect via USB and verify:
adb devices
```

## Resources

- **Clover Developer Docs**: https://docs.clover.com
- **Clover SDK**: https://github.com/clover/remote-pay-android
- **Your ATM Server**: http://100.103.3.35:5050
- **Server Code**: `/home/matt/Mattys-Robinhood-MCP/p3_atm/`

## Support Files Created

```
clover_integration/
├── CLOVER_INTEGRATION_GUIDE.md      # This file
├── clover_bridge.html                # Option 2: Web bridge
├── CloverATMActivity.java            # Option 3: Android app
├── atm_server_with_clover.py         # Enhanced Flask server
└── install_clover_option2.sh         # Automated setup script
```
