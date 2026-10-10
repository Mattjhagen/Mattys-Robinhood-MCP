# P3 Lending Inc - Professional ATM Interface

## Overview

A professional web-based ATM interface for your Robinhood trading account, branded as **P3 Lending Inc**. Runs on TTY2 of the r510 server using Chromium in kiosk mode for an authentic ATM experience.

## Features

### Security Features (Real ATM Protocols)
- 🔐 **PIN Authentication**: 4-digit PIN protection (default: 0213)
- ⏱️ **Auto-Timeout**: 
  - 30 seconds on PIN entry screen
  - 60 seconds of inactivity on any authenticated screen
  - Automatic return to welcome screen
- 🚫 **Failed Attempt Protection**: 3 attempts max, card retention on failure
- 🔒 **Session Management**: Secure logout with session clearing
- 📱 **Activity Tracking**: Resets timeout on any user interaction

### User Interface
- 💎 **Professional Design**: Modern ATM-style interface
- 🎨 **P3 Lending Branding**: Custom branded experience
- 📊 **Real-time Data**: Live portfolio and position updates
- 🖥️ **Full-Screen Kiosk**: Chromium kiosk mode on TTY2
- 🎯 **Touch-Optimized**: Large buttons, easy navigation
- ⚡ **Smooth Animations**: Professional transitions and effects

### Functionality
- 💰 **Balance Inquiry**: View total account value and buying power
- 📈 **Position Viewing**: Detailed breakdown of all holdings with P&L
- 💱 **Trade Interface**: Placeholder for future trading functionality
- 🔄 **Auto-Refresh**: Real-time updates while viewing

## Installation

### Prerequisites
- R510 server with Ubuntu
- Sudo access (required for system service)
- Internet connection

### One-Time Setup

**From the control machine:**

```bash
cd ~/Mattys-Robinhood-MCP
./r510-p3-atm-setup.sh
```

This will:
1. Copy all necessary files to r510
2. Install Chromium browser if needed
3. Install Python Flask dependencies
4. Create systemd service
5. Enable auto-start on boot
6. Launch the P3 ATM on TTY2

**Or manually on r510:**

```bash
ssh matt@100.103.3.35
cd /tmp
sudo bash setup_p3_atm.sh
```

## Usage

### Viewing the ATM

**From any machine:**
```bash
cd ~/Mattys-Robinhood-MCP
./r510-switch-to-p3-atm.sh
```

**Or directly:**
```bash
ssh matt@100.103.3.35 'sudo chvt 2'
```

### Switching Back to GUI
```bash
./r510-switch-to-gui.sh
# Or: ssh matt@100.103.3.35 'sudo chvt 1'
```

### Checking Status
```bash
./r510-p3-atm-status.sh
```

### Default Credentials
- **PIN**: `0213`
- **Account**: ••••2903

⚠️ **Change the PIN** by editing `/home/matt/Mattys-Robinhood-MCP/p3_atm/atm_server.py`:
```python
CORRECT_PIN = "0213"  # Change this to your desired PIN
```

Then restart:
```bash
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-tty2'
```

## ATM Navigation

### Welcome Screen
- Displays P3 Lending Inc branding
- Shows account number (masked)
- Click "Enter PIN" to proceed

### PIN Entry
- Use numeric keypad to enter 4-digit PIN
- ✕ button clears entry
- ✓ ENTER button submits
- **Timeout**: 30 seconds (auto-returns to welcome)
- **Max Attempts**: 3 (card retained on failure)

### Main Menu
- 💰 **Balance Inquiry** - View account totals
- 📊 **View Positions** - See all holdings
- 💱 **Make Trade** - Trading interface (coming soon)
- 🚪 **Exit** - Logout and return to welcome
- **Auto-logout**: After 60 seconds of inactivity

### Balance Inquiry
- Shows total account value
- Displays available buying power
- Real-time timestamps
- Returns to menu automatically

### View Positions
- Lists all cryptocurrency holdings
- Shows quantity and current value
- Displays change percentage (colored)
- Real-time updates

## Technical Details

### Architecture

```
┌─────────────────────────────────────────┐
│         Physical TTY2 Display           │
│    (R510 Monitor - Full Screen)         │
└──────────────┬──────────────────────────┘
               │
               v
┌──────────────────────────────────────────┐
│  X Server on :1 (VT2)                    │
└──────────────┬───────────────────────────┘
               │
               v
┌──────────────────────────────────────────┐
│  Chromium Browser (Kiosk Mode)           │
│  http://localhost:5050                   │
└──────────────┬───────────────────────────┘
               │
               v
┌──────────────────────────────────────────┐
│  Flask Web Server (Port 5050)            │
│  - HTML/CSS/JS Interface                 │
│  - REST API Backend                      │
│  - Session Management                    │
└──────────────┬───────────────────────────┘
               │
               v
┌──────────────────────────────────────────┐
│  ~/.trading-agent-state.json             │
│  (Portfolio Data)                        │
└──────────────────────────────────────────┘
```

### Services

**System Service**: `/etc/systemd/system/p3-atm-tty2.service`
```bash
# Management
sudo systemctl status p3-atm-tty2
sudo systemctl restart p3-atm-tty2
sudo systemctl stop p3-atm-tty2

# Logs
sudo journalctl -u p3-atm-tty2 -f
```

### File Locations

```
/home/matt/Mattys-Robinhood-MCP/p3_atm/
├── atm_server.py              # Flask backend server
├── atm_templates/
│   └── atm.html              # Main ATM interface
├── atm_static/               # Static assets (auto-created)
├── launch_p3_atm.sh          # Launcher script
├── start_x_atm.sh            # X server wrapper
├── atm_server.pid            # Process ID file
└── atm_server.log            # Server logs

/home/matt/Mattys-Robinhood-MCP/
├── r510-p3-atm-setup.sh      # Remote setup script
├── r510-switch-to-p3-atm.sh  # Display switcher
├── r510-p3-atm-status.sh     # Status checker
└── README_P3_ATM.md          # This file
```

### API Endpoints

The Flask server provides these REST endpoints:

- `GET /` - Main ATM interface
- `POST /api/authenticate` - PIN authentication
- `POST /api/logout` - End session
- `GET /api/portfolio` - Get full portfolio data
- `GET /api/balance` - Get account balance
- `GET /api/positions` - Get current positions
- `GET /api/status` - Get ATM status
- `GET /health` - Health check

## Security Considerations

⚠️ **Important:**

1. **Change the default PIN** immediately after setup
2. **Physical Access**: TTY2 is accessible to anyone with access to r510
3. **Auto-Logout**: Enabled - 60 seconds of inactivity
4. **PIN Timeout**: 30 seconds on PIN entry screen
5. **Failed Attempts**: Card retained after 3 failed PIN attempts
6. **Session Clear**: All data cleared on logout/timeout
7. **No Persistence**: PIN must be re-entered after each session

## Troubleshooting

### ATM Not Showing

```bash
# Check service status
ssh matt@100.103.3.35 'sudo systemctl status p3-atm-tty2'

# Check logs
ssh matt@100.103.3.35 'sudo journalctl -u p3-atm-tty2 -n 50'

# Restart service
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-tty2'
```

### Blank Screen on TTY2

```bash
# Check if X server is running
ssh matt@100.103.3.35 'ps aux | grep xinit'

# Check if Flask server is running
ssh matt@100.103.3.35 'curl http://localhost:5050/health'

# Restart the service
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-tty2'
```

### Chromium Not Starting

```bash
# Verify Chromium is installed
ssh matt@100.103.3.35 'which chromium-browser'

# If not installed
ssh matt@100.103.3.35 'sudo apt-get install -y chromium-browser'

# Check X server logs
ssh matt@100.103.3.35 'cat /home/matt/.xsession-errors'
```

### Can't Switch TTY

```bash
# Try switching directly
ssh matt@100.103.3.35 'sudo chvt 2'

# Switch back if stuck
ssh matt@100.103.3.35 'sudo chvt 1'

# Or physically on r510: Ctrl+Alt+F1 or F2
```

### PIN Not Accepting

1. Verify PIN is correct (default: 0213)
2. Check for failed attempt lockout (wait and retry)
3. Check server logs for authentication errors
4. Restart the service to reset attempts

### Port Already in Use

```bash
# Find and kill process on port 5050
ssh matt@100.103.3.35 'sudo lsof -ti:5050 | xargs -r kill'

# Restart service
ssh matt@100.103.3.35 'sudo systemctl restart p3-atm-tty2'
```

## Customization

### Change Branding

Edit `/home/matt/Mattys-Robinhood-MCP/p3_atm/atm_templates/atm.html`:

```html
<div class="atm-logo">P3</div>
<div class="atm-institution">LENDING INC</div>
```

### Change Colors

The interface uses a professional blue/dark theme. Edit the CSS variables in `atm.html`:

```css
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);  /* Main background */
color: #3498db;  /* Primary accent color */
```

### Adjust Timeouts

Edit `/home/matt/Mattys-Robinhood-MCP/p3_atm/atm_templates/atm.html`:

```javascript
const INACTIVITY_TIMEOUT = 60000; // 60 seconds (adjust as needed)
const PIN_TIMEOUT = 30000; // 30 seconds (adjust as needed)
```

Then restart the service.

## Integration with Robinhood MCP

The P3 ATM reads portfolio data from `~/.trading-agent-state.json`. To integrate with live Robinhood data:

1. Ensure Robinhood MCP is configured in `~/.claude.json`
2. The trading agent keeper service maintains the connection
3. Portfolio data flows through the state file
4. Updates happen in real-time when viewing positions/balance

For actual trading, use Claude Code with Robinhood MCP:
```
Buy $10 worth of Bitcoin
Sell 0.001 BTC
Check my Robinhood portfolio
```

## Future Enhancements

- [ ] Live Robinhood API integration
- [ ] Actual trade execution through ATM interface
- [ ] Transaction history screen
- [ ] Receipt printing simulation
- [ ] Multi-language support
- [ ] Card reader simulation
- [ ] Real-time price charts
- [ ] Alert/notification system
- [ ] Administrative panel
- [ ] Usage analytics

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review service logs: `sudo journalctl -u p3-atm-tty2 -f`
3. Verify Flask server: `curl http://localhost:5050/health`
4. Check X server status: `ps aux | grep xinit`

---

**P3 Lending Inc** - Professional Trading Terminal
**Version**: 1.0.0
**Last Updated**: 2026-10-10

**Disclaimer**: This is a portfolio monitoring interface. All actual trades should be executed through Claude Code with appropriate verification and risk management.
