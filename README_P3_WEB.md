# P3 Lending Inc ATM - Web Version

## Simple Installation

Much simpler than the TTY version - just a web service you access through your browser!

### Install (One Time)

```bash
cd ~/Mattys-Robinhood-MCP
./r510-install-p3-atm-web.sh
```

This installs the P3 ATM as a web service on r510 that starts automatically on boot.

**Requires**: sudo password on r510

## Using the ATM

### Option 1: On r510 GUI (Desktop)
Double-click the **"P3 Lending Inc ATM"** icon on the desktop

OR open browser to: `http://localhost:5050`

### Option 2: From Another Machine
Run from this machine:
```bash
cd ~/Mattys-Robinhood-MCP
./open-p3-atm.sh
```

OR open your browser to: `http://100.103.3.35:5050`

### Option 3: Full-Screen Mode
For the authentic ATM experience, press `F11` in the browser for full-screen mode!

## PIN
**Default PIN: 0213**

Change it by editing:
```bash
ssh matt@100.103.3.35
nano ~/Mattys-Robinhood-MCP/p3_atm/atm_server.py
# Find: CORRECT_PIN = "0213"
# Change to your desired PIN
sudo systemctl restart p3-atm-web
```

## Features

✅ **Security**
- PIN authentication (3 attempts max)
- 60-second auto-logout on inactivity
- 30-second PIN entry timeout
- Secure session management

✅ **Interface**
- Professional ATM design
- P3 Lending Inc branding
- Smooth animations
- Touch-optimized buttons

✅ **Functions**
- Balance inquiry
- View positions
- Real-time updates
- Trade interface (coming soon)

## Management

### Check if running:
```bash
ssh matt@100.103.3.35 'systemctl status p3-atm-web'
```

### Restart service:
```bash
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-web'
```

### View logs:
```bash
ssh matt@100.103.3.35 'sudo journalctl -u p3-atm-web -f'
```

### Stop service:
```bash
ssh matt@100.103.3.35 'sudo systemctl stop p3-atm-web'
```

## Troubleshooting

### Can't connect to ATM

1. Check if service is running:
```bash
ssh matt@100.103.3.35 'systemctl status p3-atm-web'
```

2. Test the endpoint:
```bash
curl http://100.103.3.35:5050/health
```

Should return: `{"status":"ok"}`

3. Restart if needed:
```bash
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-web'
```

### Port already in use

```bash
ssh matt@100.103.3.35 'sudo lsof -ti:5050 | xargs -r sudo kill'
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-web'
```

### Desktop icon not working

Make sure Chromium is installed:
```bash
ssh matt@100.103.3.35 'which chromium-browser'
```

If not installed:
```bash
ssh matt@100.103.3.35 'sudo apt-get install -y chromium-browser'
```

## File Locations

```
/home/matt/Mattys-Robinhood-MCP/p3_atm/
├── atm_server.py              # Flask web server
├── atm_templates/
│   └── atm.html              # ATM interface
└── atm_static/               # Static files (auto-created)

/home/matt/Desktop/
└── P3-ATM.desktop            # Desktop shortcut

/etc/systemd/system/
└── p3-atm-web.service        # Service file
```

## Access URLs

- **From r510**: http://localhost:5050
- **From network**: http://100.103.3.35:5050
- **Health check**: http://100.103.3.35:5050/health

## Why Web Version?

The web version is:
- ✅ Easier to install (no X server, no TTY conflicts)
- ✅ Accessible from any device on the network
- ✅ Works in any browser
- ✅ Can run full-screen (press F11)
- ✅ Simpler to troubleshoot
- ✅ Auto-starts on boot

## Security Notes

⚠️ **Network Access**: The service is accessible to anyone on the local network (100.103.3.35:5050)

⚠️ **Authentication**: Only PIN protects access (change from default 0213!)

⚠️ **Auto-Logout**: Enabled - 60 seconds of inactivity

For production use, consider:
- Changing the default PIN
- Adding HTTPS/TLS
- Restricting network access with firewall rules
- Adding additional authentication

## Customization

### Change Port
Edit `/home/matt/Mattys-Robinhood-MCP/p3_atm/atm_server.py`:
```python
app.run(host='127.0.0.1', port=5050)  # Change 5050 to desired port
```

Then restart: `sudo systemctl restart p3-atm-web`

### Allow External Access
To allow access from outside the local network, change:
```python
app.run(host='0.0.0.0', port=5050)  # Listen on all interfaces
```

⚠️ Only do this if you understand the security implications!

## That's It!

Much simpler than the TTY version. Just install once and access it through any browser, anytime.

**Happy trading!** 🏦💰
