# Robinhood ATM Interface Explanation

## The Confusion: Two Different ATM Interfaces

You have **TWO completely separate** ATM implementations:

### 1. Terminal-Based ATM (NOT currently used)
- **File**: `~/Mattys-Robinhood-MCP/trading_atm.py`
- **Service**: `/etc/systemd/system/trading-atm-tty2.service` (system)
- **Display**: Raw terminal output on TTY2
- **Status**: ✅ Fixed with quick balance receipt (commit 65e8b96)
- **Issue**: This was NOT actually running on your display

### 2. Web-Based ATM (ACTUALLY running) ⭐
- **Files**: 
  - Server: `~/Mattys-Robinhood-MCP/p3_atm/atm_server.py`
  - HTML: `~/Mattys-Robinhood-MCP/p3_atm/atm_templates/atm.html`
- **Services**:
  - `robinhood-atm-server.service` - Flask web server on port 5050
  - `robinhood-atm-display.service` - Chromium kiosk mode browser
- **Display**: Chromium browser in fullscreen kiosk mode
- **Status**: ✅ Now restarted to clear cache

## What You See on Your Screen

When you look at the R510 display, you're seeing **Chromium browser** running in kiosk mode showing `http://localhost:5050`. This is the **web-based ATM**, not the terminal version.

## The Web ATM Flow (What Should Happen)

1. **Welcome Screen** (loads automatically)
   - "Robinhood ATM Trading Terminal"
   - Button: "Enter PIN to Continue"
   - Press **Enter** or **Space** to go to PIN screen

2. **PIN Entry Screen**
   - Enter 4-digit PIN: `0213`
   - Can use keyboard numbers or numpad
   - Press **Enter** to submit
   - ⚠️ Max 3 attempts or 30-minute lockout

3. **Quick Balance Screen** (after successful PIN)
   - Shows total balance
   - Shows buying power
   - Shows today's P&L (if available)
   - Shows your positions
   - Transaction ID
   - Button: "Continue to Trading"

4. **Main Menu** (after pressing Continue)
   - Buy/Sell cryptocurrency
   - View positions
   - Check balance
   - ESC or Q to logout

## Security Features

- **Hashed PIN**: PIN is stored as SHA-256 hash, not plaintext
- **Environment Variable**: `ATM_PIN_HASH` in `~/.bashrc`
- **Current PIN**: `0213` (hash: `f020272...`)
- **Lockout System**: 3 failed attempts = 30-minute lockout
- **Auto-logout**: Inactivity timeout returns to welcome screen
- **Session Required**: All balance/trade endpoints require authentication

## How to Control It

### Restart Web ATM (clears browser cache)
```bash
~/Mattys-Robinhood-MCP/restart-web-atm.sh
```

### Check Service Status
```bash
# Web server
systemctl --user status robinhood-atm-server.service

# Browser display
systemctl --user status robinhood-atm-display.service
```

### View Logs
```bash
# Server logs
journalctl --user -u robinhood-atm-server.service -f

# Browser logs
journalctl --user -u robinhood-atm-display.service -f
```

### Change PIN
```bash
# Generate new hash
echo -n "YOUR_NEW_PIN" | sha256sum

# Update ~/.bashrc and service file
export ATM_PIN_HASH='new_hash_here'

# Restart services
~/Mattys-Robinhood-MCP/restart-web-atm.sh
```

## Keyboard Shortcuts (in Web ATM)

| Key | Action |
|-----|--------|
| **Welcome Screen** |
| Enter/Space | Go to PIN entry |
| **PIN Screen** |
| 0-9 | Enter digits |
| Enter | Submit PIN |
| Backspace | Delete digit |
| ESC | Back to welcome |
| **Main Menu** |
| 1 or B | Buy |
| 2 or S | Sell |
| 3 | Balance |
| 4 or P | Positions |
| Q or ESC | Logout |
| ? | Show keyboard help |

## Why the Terminal ATM Exists

The terminal ATM (`trading_atm.py`) was created first for direct TTY display without X11/browser overhead. However, the web version offers:
- Better UI/UX
- Keyboard navigation
- Cloudflare tunnel access
- Easier to update (no service restart needed)

So the web version became the production interface.

## If You Want to Switch to Terminal ATM

To use the terminal version instead:

```bash
# Stop web services
systemctl --user stop robinhood-atm-display.service

# Enable terminal service (system level - requires sudo)
sudo systemctl enable trading-atm-tty2.service
sudo systemctl start trading-atm-tty2.service

# Switch to TTY2
sudo chvt 2
```

Note: Terminal ATM now has quick balance receipt (my fix), but lacks the full web features.

## Summary

- ✅ Your display shows the **web-based ATM** (browser kiosk)
- ✅ Web ATM has PIN authentication working
- ✅ Web ATM shows quick balance after PIN entry
- ✅ Services have been restarted to clear cache
- ✅ PIN is `0213`

**Next steps**: 
1. Look at your screen - you should see the welcome screen
2. Press Enter or Space to go to PIN entry
3. Enter PIN: `0213`
4. You should see the quick balance receipt with your positions and P&L
