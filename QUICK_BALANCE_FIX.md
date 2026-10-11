# Quick Balance Receipt Fix

## Problem
The ATM app was only showing PIN authentication, but not displaying a receipt with quick balance and P&L after successful PIN entry.

## Solution Implemented

### Changes Made to `trading_atm.py`:

1. **Added `calculate_pnl()` function** (line ~124)
   - Calculates P&L amount and percentage if previous_value is available
   - Returns profit/loss with icon (📈 or 📉)

2. **Added `display_quick_balance_receipt()` function** (line ~136)
   - Shows professional ATM-style receipt after successful PIN entry
   - Displays:
     - Date, time, and transaction ID
     - **Total balance**
     - **Available to trade (buying power)**
     - **Today's P&L** (when data available) with color-coded display
     - **Your positions** (top 5 holdings)
     - Last updated timestamp
     - Authentication success confirmation

3. **Updated `main()` function** (line ~411)
   - Calls `display_quick_balance_receipt()` immediately after successful PIN
   - User must press ENTER to continue to main menu

## Testing Results

✅ PIN authentication works (PIN: 0213)
✅ Quick balance receipt displays after successful PIN
✅ Shows total balance: $34.45
✅ Shows available to trade: $0.00
✅ Shows positions:
   - BTC: 0.00023893 = $19.81
   - ETH: 0.00583100 = $14.61
✅ Shows transaction ID and timestamps
✅ Continues to main menu after pressing ENTER

## How to Apply Changes

### Option 1: Restart the TTY2 Service (Recommended)
```bash
cd ~/Mattys-Robinhood-MCP
./restart-atm.sh
```

### Option 2: Manual Restart
```bash
sudo systemctl restart trading-atm-tty2
sudo systemctl status trading-atm-tty2
```

### Option 3: Switch TTY to View
```bash
# From any machine
ssh matt@100.103.3.35 'sudo chvt 2'

# Or use the helper script
cd ~/Mattys-Robinhood-MCP
./r510-switch-to-atm.sh
```

## P&L Display

The P&L section will display when the state file contains `previous_value` data:

```json
{
  "total_value": 34.45,
  "previous_value": 33.50,  // ← This enables P&L
  "buying_power": 0.00,
  ...
}
```

To enable P&L tracking, the trading agent keeper needs to:
1. Fetch current portfolio value
2. Store it as `previous_value` for next run
3. Update `total_value` with new fetch

## Flow Diagram

```
1. User starts ATM (TTY2)
   ↓
2. Welcome screen
   ↓
3. PIN authentication prompt
   ↓
4. User enters PIN: 0213
   ↓
5. ✅ **NEW: Quick Balance Receipt** ←
   ↓
6. Press ENTER to continue
   ↓
7. Main menu (Check Balance, View Positions, Make Trade, Exit)
```

## File Locations

- Main ATM script: `~/Mattys-Robinhood-MCP/trading_atm.py`
- State file: `~/.trading-agent-state.json`
- Service file: `/etc/systemd/system/trading-atm-tty2.service`
- Restart helper: `~/Mattys-Robinhood-MCP/restart-atm.sh`

## Verification

After restarting, test the flow:
1. Switch to TTY2 (if not already there)
2. Enter PIN: `0213`
3. Verify quick balance receipt displays
4. Check that balance, positions, and timestamps are shown
5. Press ENTER to continue to menu
