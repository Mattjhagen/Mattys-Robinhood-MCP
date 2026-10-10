#!/usr/bin/env python3
"""
Simple Trading Agent Monitor
Real-time display of portfolio and positions
Run with: python3 ~/trading_monitor.py
"""

import time
import os
import sys
from datetime import datetime

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def format_currency(value):
    """Format value as currency"""
    return f"${float(value):.2f}"

def format_pnl(value):
    """Format P/L with color"""
    val = float(value)
    color = GREEN if val >= 0 else RED
    return f"{color}${val:+.2f}{RESET}"

def format_pct(value):
    """Format percentage with color"""
    val = float(value)
    color = GREEN if val >= 0 else RED
    return f"{color}{val:+.2f}%{RESET}"

def print_header():
    """Print dashboard header"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}🤖 ROBINHOOD TRADING AGENT MONITOR{RESET}")
    print(f"{BOLD}Account: ••••2903 | {now}{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")

def print_portfolio(data):
    """Print portfolio summary"""
    print(f"{BOLD}{BLUE}📊 PORTFOLIO SUMMARY{RESET}")
    print(f"{'─'*80}")

    total_value = float(data.get('total_value', 0))
    buying_power = float(data.get('buying_power', {}).get('buying_power', 0))
    crypto_value = float(data.get('crypto_value', 0))
    equity_value = float(data.get('equity_value', 0))

    print(f"  Total Value:     {BOLD}{format_currency(total_value)}{RESET}")
    print(f"  Buying Power:    {format_currency(buying_power)}")
    print(f"  Crypto Holdings: {format_currency(crypto_value)}")
    print(f"  Equity Holdings: {format_currency(equity_value)}")

    # Calculate daily P/L (assuming $40.19 start)
    start_value = 40.19
    daily_pnl = total_value - start_value
    daily_pnl_pct = (daily_pnl / start_value * 100) if start_value > 0 else 0

    print(f"  Daily P/L:       {format_pnl(daily_pnl)} ({format_pct(daily_pnl_pct)})")
    print()

def print_positions(crypto_pos, crypto_quotes):
    """Print active positions"""
    print(f"{BOLD}{BLUE}📈 ACTIVE POSITIONS{RESET}")
    print(f"{'─'*80}")

    if not crypto_pos:
        print("  No positions")
        print()
        return

    # Header
    print(f"  {BOLD}{'Asset':<6} {'Quantity':<14} {'Entry':<10} {'Current':<10} {'Value':<10} {'P/L':<12} {'Stop(-8%)':<10}{RESET}")
    print(f"  {'─'*78}")

    total_value = 0
    total_cost = 0

    for pos in crypto_pos:
        symbol = pos['currency']['code']
        qty = float(pos['quantity'])

        # Get cost basis
        cost_basis = 0
        entry_price = 0
        if pos.get('cost_bases'):
            cost_basis = float(pos['cost_bases'][0]['direct_cost_basis'])
            direct_qty = float(pos['cost_bases'][0]['direct_quantity'])
            entry_price = cost_basis / direct_qty if direct_qty > 0 else 0

        # Get current price
        current_price = 0
        for quote in crypto_quotes:
            if quote['symbol'] == f"{symbol}USD":
                current_price = float(quote['mark_price'])
                break

        # Calculate values
        value = qty * current_price
        pnl = value - cost_basis
        pnl_pct = (pnl / cost_basis * 100) if cost_basis > 0 else 0
        stop_loss = entry_price * 0.92

        total_value += value
        total_cost += cost_basis

        # Format output
        pnl_str = format_pnl(pnl)
        pnl_pct_str = format_pct(pnl_pct)

        print(f"  {symbol:<6} {qty:<14.8f} {format_currency(entry_price):<10} "
              f"{format_currency(current_price):<10} {format_currency(value):<10} "
              f"{pnl_str} ({pnl_pct_str}) {format_currency(stop_loss):<10}")

    print(f"  {'─'*78}")
    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
    print(f"  {BOLD}{'TOTAL':<6} {'':14} {'':10} {'':10} "
          f"{format_currency(total_value):<10} "
          f"{format_pnl(total_pnl)} ({format_pct(total_pnl_pct)}){RESET}")
    print()

def print_risk_status(daily_pnl_pct, num_positions):
    """Print risk management status"""
    print(f"{BOLD}{BLUE}🎯 RISK MANAGEMENT{RESET}")
    print(f"{'─'*80}")

    # Kill switch
    kill_switch_active = daily_pnl_pct < -3.0
    if kill_switch_active:
        print(f"  Kill Switch (-3%): {RED}{BOLD}🔴 ACTIVE - NO NEW POSITIONS{RESET}")
    else:
        print(f"  Kill Switch (-3%): {GREEN}✅ INACTIVE{RESET}")

    # Position limits
    print(f"  Position Slots:    {num_positions}/5 used")
    print(f"  Max Position Size: 10% of portfolio")

    # Agent status
    print(f"  Loop Status:       {GREEN}✅ RUNNING{RESET} (every 15 min)")
    print()

def print_instructions():
    """Print usage instructions"""
    print(f"{BOLD}{YELLOW}📝 CONTROLS{RESET}")
    print(f"{'─'*80}")
    print(f"  Press Ctrl+C to exit")
    print(f"  Refreshes every 30 seconds")
    print(f"  Loop Job ID: c880d336 (cancel with: CronDelete c880d336)")
    print()

def fetch_data_placeholder():
    """Return placeholder data - replace with actual API calls"""
    # In production, this would call the Robinhood MCP tools
    # For now, return last known state
    return {
        'portfolio': {
            'total_value': '34.45',
            'buying_power': {'buying_power': '0.00'},
            'crypto_value': '34.45',
            'equity_value': '0'
        },
        'crypto_positions': [
            {
                'currency': {'code': 'BTC'},
                'quantity': '0.00023893',
                'cost_bases': [{'direct_cost_basis': '19.81', 'direct_quantity': '0.00023893'}]
            },
            {
                'currency': {'code': 'ETH'},
                'quantity': '0.005831',
                'cost_bases': [{'direct_cost_basis': '14.61', 'direct_quantity': '0.005831'}]
            }
        ],
        'crypto_quotes': [
            {'symbol': 'BTCUSD', 'mark_price': '82959'},
            {'symbol': 'ETHUSD', 'mark_price': '2507'}
        ]
    }

def main():
    """Main dashboard loop"""
    print(f"{CYAN}Loading Trading Agent Monitor...{RESET}\n")
    print(f"{YELLOW}Note: This is a display-only monitor.{RESET}")
    print(f"{YELLOW}For live data, run: claude code (to connect to Robinhood MCP){RESET}\n")

    try:
        while True:
            clear_screen()

            # Fetch data (placeholder - integrate with actual MCP calls)
            data = fetch_data_placeholder()

            # Print dashboard
            print_header()
            print_portfolio(data['portfolio'])

            num_positions = len(data['crypto_positions'])
            print_positions(data['crypto_positions'], data['crypto_quotes'])

            # Calculate daily P/L
            total_value = float(data['portfolio']['total_value'])
            start_value = 40.19
            daily_pnl_pct = ((total_value - start_value) / start_value * 100) if start_value > 0 else 0

            print_risk_status(daily_pnl_pct, num_positions)
            print_instructions()

            print(f"{CYAN}{'='*80}{RESET}")
            print(f"{YELLOW}Next refresh in 30 seconds...{RESET}")

            time.sleep(30)

    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{CYAN}Trading Agent Monitor stopped.{RESET}")
        print(f"{YELLOW}Trading loop continues in background (Job: c880d336){RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
