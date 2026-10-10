# Robinhood Trading ATM Terminal - Setup Guide

## Overview

An ATM-style interface for your Robinhood trading account that runs on TTY2 of the r510 server. Check balances, view positions, and manage trades with a secure PIN-protected interface.

## Features

- 🏦 **ATM-Style Interface**: Professional banking terminal design
- 🔐 **PIN Protection**: Secure 4-digit PIN authentication
- 📊 **Real-time Balance**: View your current portfolio value
- 📈 **Position Management**: Detailed view of all holdings
- 💼 **Trade Interface**: Placeholder for future trade execution
- 🔄 **Auto-Restart**: Automatically restarts on TTY2 after reboot
- 🤖 **Agent Keeper**: Background service keeps trading agent active

## Installation

### One-Time Setup (Requires sudo)

```bash
cd ~/Mattys-Robinhood-MCP
sudo bash setup-trading-atm-tty2.sh
```

This will:
1. Create a system service at `/etc/systemd/system/trading-atm-tty2.service`
2. Enable the service to start on boot
3. Start the ATM interface on TTY2

## Usage

### Accessing the ATM Terminal

**On r510 (locally):**
```bash
# Switch to TTY2
sudo chvt 2

# Switch back to GUI
sudo chvt 1
# Or press: Ctrl+Alt+F1
```

**From another machine (r510 control server):**
```bash
# Switch r510's display to ATM
ssh matt@100.103.3.35 'sudo chvt 2'

# Switch back to GUI
ssh matt@100.103.3.35 'sudo chvt 1'
```

### Default PIN

**Default PIN: `1234`**

⚠️ **IMPORTANT**: Change the PIN by editing the script:
```bash
nano ~/Mattys-Robinhood-MCP/trading_atm.py
# Find: CORRECT_PIN = "1234"
# Change to your desired 4-digit PIN
# Then restart: sudo systemctl restart trading-atm-tty2
```

### ATM Menu Options

1. **Check Balance** - View total account value and buying power
2. **View Positions** - Detailed breakdown of all holdings
3. **Make Trade** - Trading interface (placeholder for now)
4. **Account Summary** - Complete account overview
5. **Exit ATM** - Log out and return to welcome screen

## Services

### Trading ATM Service (System Service)

```bash
# Check status
sudo systemctl status trading-atm-tty2

# Start/Stop/Restart
sudo systemctl start trading-atm-tty2
sudo systemctl stop trading-atm-tty2
sudo systemctl restart trading-atm-tty2

# View logs
sudo journalctl -u trading-atm-tty2 -f

# Enable/Disable auto-start
sudo systemctl enable trading-atm-tty2
sudo systemctl disable trading-atm-tty2
```

### Trading Agent Keeper (User Service)

Keeps the Robinhood MCP trading agent active in the background.

```bash
# Check status
systemctl --user status trading-agent-keeper

# Start/Stop/Restart
systemctl --user start trading-agent-keeper
systemctl --user stop trading-agent-keeper
systemctl --user restart trading-agent-keeper

# View logs
journalctl --user -u trading-agent-keeper -f
```

## File Locations

```
~/Mattys-Robinhood-MCP/
├── trading_atm.py                  # Main ATM interface script
├── setup-trading-atm-tty2.sh       # System service installer
├── trading_agent_keeper.sh         # Background agent keeper
└── README.md                       # This file

~/.config/systemd/user/
└── trading-agent-keeper.service    # User service for agent keeper

/etc/systemd/system/
└── trading-atm-tty2.service        # System service for ATM display

~/.trading-agent-state.json         # Trading agent state file
~/trading_agent.log                 # Trading agent keeper log
```

## Remote Control Scripts

Create these helper scripts on the r510 control server for easier management:

### Switch to ATM
```bash
#!/bin/bash
# r510-switch-to-atm.sh
ssh matt@100.103.3.35 'sudo chvt 2'
echo "R510 display switched to Trading ATM (TTY2)"
```

### Switch to GUI
```bash
#!/bin/bash
# r510-switch-to-gui.sh
ssh matt@100.103.3.35 'sudo chvt 1'
echo "R510 display switched to GUI (TTY1)"
```

### Check ATM Status
```bash
#!/bin/bash
# r510-atm-status.sh
ssh matt@100.103.3.35 'sudo systemctl status trading-atm-tty2 --no-pager'
```

## Troubleshooting

### ATM not showing on TTY2

```bash
# Check if service is running
sudo systemctl status trading-atm-tty2

# Check logs for errors
sudo journalctl -u trading-atm-tty2 -n 50

# Restart the service
sudo systemctl restart trading-atm-tty2
```

### Can't switch to TTY2

```bash
# Verify chvt command works
sudo chvt 2

# If you're stuck, switch back
sudo chvt 1
# Or press: Ctrl+Alt+F1
```

### Python script errors

```bash
# Test the script manually
python3 ~/Mattys-Robinhood-MCP/trading_atm.py

# Check Python is available
which python3
python3 --version
```

### Agent keeper not running

```bash
# Check if user lingering is enabled
loginctl show-user matt | grep Linger

# Enable if needed
sudo loginctl enable-linger matt

# Restart the keeper
systemctl --user restart trading-agent-keeper
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Change the default PIN** immediately after setup
2. **TTY2 is accessible** to anyone with physical access to the r510
3. **No timeout** - ATM stays logged in until you explicitly exit
4. **State file** at `~/.trading-agent-state.json` contains account data
5. **Logs may contain** sensitive information - review before sharing

## Integration with Robinhood MCP

The ATM currently displays placeholder data. To integrate with live Robinhood data:

1. Ensure Robinhood MCP is configured in `~/.claude.json`
2. Authenticate with `/mcp` command in Claude Code
3. The trading agent keeper will maintain the MCP connection
4. Portfolio data will flow through the state file

For actual trading functionality, use Claude Code with the Robinhood MCP tools:
```
Buy $10 worth of Bitcoin
Sell 0.001 BTC
Check my Robinhood portfolio
```

## Architecture

```
┌─────────────────────────────────────┐
│         Physical TTY2               │
│  (R510 Monitor shows ATM)           │
└──────────────┬──────────────────────┘
               │
               v
┌──────────────────────────────────────┐
│  trading-atm-tty2.service            │
│  (System Service - runs as matt)     │
│  Auto-starts on boot                 │
└──────────────┬───────────────────────┘
               │
               v
┌──────────────────────────────────────┐
│  trading_atm.py                      │
│  • PIN authentication                │
│  • Menu system                       │
│  • Display portfolio                 │
└──────────────┬───────────────────────┘
               │
               v
┌──────────────────────────────────────┐
│  ~/.trading-agent-state.json         │
│  (Shared state file)                 │
└──────────────▲───────────────────────┘
               │
               │
┌──────────────┴───────────────────────┐
│  trading-agent-keeper.service        │
│  (User Service - background)         │
│  Keeps MCP connection active         │
└──────────────────────────────────────┘
```

## Future Enhancements

- [ ] Live Robinhood API integration
- [ ] Actual trade execution through ATM
- [ ] Transaction history view
- [ ] Auto-logout timer
- [ ] Multiple user support
- [ ] Trade confirmation screens
- [ ] Real-time price updates
- [ ] Alert notifications

## Support

For issues or questions:
1. Check the logs: `sudo journalctl -u trading-atm-tty2 -f`
2. Review AGENTS.md for troubleshooting patterns
3. Verify Robinhood MCP configuration in `~/.claude.json`

---

**Disclaimer**: This is a display terminal for portfolio monitoring. All actual trades should be executed through Claude Code with appropriate verification and risk management.
