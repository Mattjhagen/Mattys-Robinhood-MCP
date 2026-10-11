# Robinhood ATM - Boot Configuration

## What Happens on Reboot

### ✅ Automatic Services

1. **Web Server (User Service)**
   - Service: `robinhood-atm-server.service`
   - Starts: Automatically on login
   - Port: 5050
   - URL: `http://localhost:5050`
   - Status: ✅ Enabled

2. **Browser Auto-Open (GUI)**
   - File: `~/.config/autostart/robinhood-atm-browser.desktop`
   - Waits: 5 seconds after GUI loads
   - Opens: Default browser to `http://localhost:5050`
   - Status: ✅ Configured

3. **Cloudflare Tunnel**
   - Service: `robinhood-atm-tunnel.service`
   - Public URL: Your configured domain
   - Status: ✅ Running

### ⚠️ Terminal ATM (TTY2)

- Service: `trading-atm-tty2.service` (system-level)
- Status: **Currently crashing** (old hardcoded PIN)
- Recommendation: Disable this or update it
- To disable: `sudo systemctl disable trading-atm-tty2.service`

## Reboot Sequence

```
1. Server boots
2. You log in to GUI
3. [5 seconds delay]
4. Browser opens automatically
5. ATM web interface loads at http://localhost:5050
6. Enter your PIN to access
```

## Manual Access

If auto-open doesn't work:

```bash
# Open in browser manually
xdg-open http://localhost:5050

# Or use direct URL
firefox http://localhost:5050
google-chrome http://localhost:5050
```

## Verify Setup

```bash
# Check web server is running
systemctl --user status robinhood-atm-server

# Check autostart is configured
ls -la ~/.config/autostart/robinhood-atm-browser.desktop

# Test health endpoint
curl http://localhost:5050/health
```

## Troubleshooting

### Browser doesn't open on boot

1. Check if autostart file exists:
   ```bash
   cat ~/.config/autostart/robinhood-atm-browser.desktop
   ```

2. Check display manager loads autostart:
   ```bash
   echo $XDG_CURRENT_DESKTOP
   # Should show your desktop environment
   ```

3. Test manually:
   ```bash
   /bin/bash -c 'sleep 5 && xdg-open http://localhost:5050'
   ```

### Web server not starting

```bash
# Check service status
systemctl --user status robinhood-atm-server

# View logs
journalctl --user -u robinhood-atm-server -n 50

# Restart service
systemctl --user restart robinhood-atm-server
```

### Wrong PIN or locked out

1. Check PIN hash is set:
   ```bash
   echo $ATM_PIN_HASH | head -c 16
   ```

2. Reset PIN:
   ```bash
   cd ~/Mattys-Robinhood-MCP
   bash setup-secure-pin.sh <YOUR_PIN>
   source ~/.bashrc
   systemctl --user restart robinhood-atm-server
   ```

3. Clear lockout (if needed):
   ```bash
   rm ~/.atm-lockout.json
   ```

## To Disable Auto-Open

If you want to stop browser from opening on boot:

```bash
rm ~/.config/autostart/robinhood-atm-browser.desktop
```

## To Enable Fullscreen Kiosk Mode

For a dedicated ATM terminal:

```bash
# Edit autostart to use fullscreen browser
cat > ~/.config/autostart/robinhood-atm-browser.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Robinhood ATM - Kiosk Mode
Exec=/bin/bash -c 'sleep 5 && chromium-browser --kiosk --app=http://localhost:5050'
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
```

## Current Configuration

- **Web Server:** ✅ Auto-starts with user session
- **Browser:** ✅ Opens automatically 5 seconds after login
- **PIN:** ✅ Secure hashed authentication
- **Lockout:** ✅ Persists across reboots
- **Public Access:** ✅ Via Cloudflare tunnel (if configured)

---

**Last Updated:** 2026-10-11  
**Server:** r510 (100.103.3.35)  
**Configuration:** Production-Ready ✅
