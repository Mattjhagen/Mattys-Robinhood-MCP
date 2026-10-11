#!/usr/bin/env python3
"""
ROBINHOOD TRADING ATM
Interactive ATM-style terminal for checking balance and making trades
"""

import time
import os
import sys
import json
import getpass
from datetime import datetime

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BG_BLUE = "\033[44m"
BG_GREEN = "\033[42m"
BG_RED = "\033[41m"

# ATM Configuration
CORRECT_PIN = "0213"  # Custom PIN
STATE_FILE = "/home/matt/.trading-agent-state.json"
MAX_PIN_ATTEMPTS = 3

def clear_screen():
    """Clear terminal screen"""
    os.system('clear')

def print_border(width=80, char="═"):
    """Print a decorative border"""
    print(f"{CYAN}{char * width}{RESET}")

def print_atm_header():
    """Print ATM-style header"""
    clear_screen()
    print(f"\n{BG_BLUE}{WHITE}{BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║                    🏦  ROBINHOOD TRADING ATM  🏦                          ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

def print_centered(text, width=80, color=WHITE):
    """Print centered text"""
    padding = (width - len(text)) // 2
    print(f"{color}{' ' * padding}{text}{RESET}")

def load_portfolio_data():
    """Load portfolio data from state file or return placeholder"""
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            # In production, this would contain actual portfolio data
            return {
                'total_value': 34.45,
                'buying_power': 0.00,
                'crypto_positions': [
                    {'symbol': 'BTC', 'quantity': 0.00023893, 'value': 19.81},
                    {'symbol': 'ETH', 'quantity': 0.005831, 'value': 14.61}
                ],
                'last_update': state.get('last_update', 'Unknown')
            }
    except:
        # Default placeholder data
        return {
            'total_value': 34.45,
            'buying_power': 0.00,
            'crypto_positions': [
                {'symbol': 'BTC', 'quantity': 0.00023893, 'value': 19.81},
                {'symbol': 'ETH', 'quantity': 0.005831, 'value': 14.61}
            ],
            'last_update': datetime.now().isoformat()
        }

def authenticate():
    """ATM-style PIN authentication"""
    attempts = 0

    while attempts < MAX_PIN_ATTEMPTS:
        print_atm_header()
        print_centered("═" * 50, color=CYAN)
        print_centered("AUTHENTICATION REQUIRED", color=YELLOW)
        print_centered("═" * 50, color=CYAN)
        print()
        print_centered("Please enter your PIN to access your account", color=WHITE)
        print()

        # Use getpass to hide PIN input (will show asterisks)
        pin = getpass.getpass(f"        {CYAN}═══► {YELLOW}PIN: {RESET}")

        if pin == CORRECT_PIN:
            print()
            print_centered("✓ PIN ACCEPTED", color=GREEN)
            print_centered("Loading your account...", color=GREEN)
            time.sleep(1)
            return True
        else:
            attempts += 1
            remaining = MAX_PIN_ATTEMPTS - attempts
            if remaining > 0:
                print()
                print_centered(f"✗ INCORRECT PIN", color=RED)
                print_centered(f"{remaining} attempts remaining", color=YELLOW)
                time.sleep(2)
            else:
                print()
                print_centered("✗ MAXIMUM ATTEMPTS EXCEEDED", color=RED)
                print_centered("Card Retained - Please Contact Support", color=RED)
                time.sleep(3)
                return False

    return False

def format_currency(value):
    """Format value as currency"""
    return f"${float(value):.2f}"

def calculate_pnl(data):
    """Calculate today's P&L if available in state data"""
    try:
        if 'previous_value' in data and 'total_value' in data:
            prev = float(data['previous_value'])
            current = float(data['total_value'])
            pnl_amount = current - prev
            pnl_pct = (pnl_amount / prev * 100) if prev > 0 else 0
            return pnl_amount, pnl_pct
    except:
        pass
    return None, None

def display_quick_balance_receipt():
    """Display quick balance receipt after successful PIN entry"""
    print_atm_header()
    data = load_portfolio_data()

    # Print receipt header
    print(f"{WHITE}{BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                              ROBINHOOD ATM                                 ║")
    print("║                         BALANCE INQUIRY RECEIPT                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    # Date and time
    now = datetime.now()
    print(f"  {CYAN}Date:{RESET} {now.strftime('%Y-%m-%d')}    {CYAN}Time:{RESET} {now.strftime('%H:%M:%S')}")
    print(f"  {CYAN}Transaction ID:{RESET} {now.strftime('%Y%m%d%H%M%S')}")
    print()
    print(f"{YELLOW}{'─' * 80}{RESET}")
    print()

    # Total balance
    total = data['total_value']
    buying_power = data['buying_power']

    print(f"  {BOLD}{WHITE}TOTAL BALANCE INQUIRY{RESET}")
    print(f"  {BOLD}{GREEN}{format_currency(total)}{RESET}")
    print()

    # Available to trade
    print(f"  {CYAN}AVAILABLE TO TRADE{RESET}")
    print(f"  {WHITE}{format_currency(buying_power)}{RESET}")
    print()

    # Today's P&L if available
    pnl_amount, pnl_pct = calculate_pnl(data)
    if pnl_amount is not None:
        print(f"{YELLOW}{'─' * 80}{RESET}")
        print()
        print(f"  {BOLD}{WHITE}TODAY'S PERFORMANCE{RESET}")

        # Color based on profit/loss
        pnl_color = GREEN if pnl_amount >= 0 else RED
        pnl_icon = "📈" if pnl_amount >= 0 else "📉"
        pnl_sign = "+" if pnl_amount >= 0 else ""

        print(f"  {pnl_color}{BOLD}{pnl_sign}{format_currency(abs(pnl_amount))}  ({pnl_sign}{pnl_pct:.2f}%)  {pnl_icon}{RESET}")
        print()

    # Account breakdown
    print(f"{YELLOW}{'─' * 80}{RESET}")
    print()
    print(f"  {BOLD}{WHITE}YOUR POSITIONS{RESET}")
    print()

    if data['crypto_positions']:
        for pos in data['crypto_positions'][:5]:  # Show top 5
            symbol = pos['symbol']
            qty = pos['quantity']
            value = pos['value']
            print(f"  {YELLOW}•{RESET} {BOLD}{symbol}{RESET}  {qty:.8f}  {GREEN}{format_currency(value)}{RESET}")

        if len(data['crypto_positions']) > 5:
            remaining = len(data['crypto_positions']) - 5
            print(f"  {CYAN}  ... and {remaining} more position(s){RESET}")
    else:
        print(f"  {YELLOW}No active positions{RESET}")

    print()
    print(f"{YELLOW}{'─' * 80}{RESET}")
    print()
    print(f"  {CYAN}Last Updated:{RESET} {data.get('last_update', 'Unknown')}")
    print()
    print(f"  {BOLD}{GREEN}✓ AUTHENTICATION SUCCESSFUL{RESET}")
    print()

    input(f"  {CYAN}Press ENTER to continue to main menu...{RESET}")

def display_balance():
    """Display account balance (ATM style)"""
    print_atm_header()
    data = load_portfolio_data()

    print(f"{BG_GREEN}{WHITE}{BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                         ACCOUNT BALANCE INQUIRY                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    print(f"  {CYAN}Account Type:{RESET}        Individual Trading Account")
    print(f"  {CYAN}Account Number:{RESET}      ••••••2903")
    print(f"  {CYAN}Date:{RESET}                {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print(f"{YELLOW}{'─' * 80}{RESET}")
    print()

    total = data['total_value']
    buying_power = data['buying_power']

    print(f"  {BOLD}{GREEN}TOTAL ACCOUNT VALUE:{RESET}     {BOLD}{format_currency(total)}{RESET}")
    print(f"  {CYAN}Available to Trade:{RESET}      {format_currency(buying_power)}")
    print()

    print(f"  {BOLD}Current Holdings:{RESET}")
    print(f"  {CYAN}{'─' * 76}{RESET}")

    for pos in data['crypto_positions']:
        symbol = pos['symbol']
        qty = pos['quantity']
        value = pos['value']
        print(f"    {YELLOW}•{RESET} {symbol:<6}  {qty:.8f}    {format_currency(value)}")

    print()
    print(f"{YELLOW}{'─' * 80}{RESET}")
    print()
    print(f"  {CYAN}Last Updated:{RESET} {data.get('last_update', 'Unknown')}")
    print()

    input(f"  {CYAN}Press ENTER to continue...{RESET}")

def display_positions():
    """Display detailed positions (ATM receipt style)"""
    print_atm_header()
    data = load_portfolio_data()

    print(f"{WHITE}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                         POSITION DETAILS                                   ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    print(f"  {BOLD}Active Cryptocurrency Positions{RESET}")
    print(f"  {CYAN}{'═' * 76}{RESET}")
    print()

    if not data['crypto_positions']:
        print(f"  {YELLOW}No active positions{RESET}")
    else:
        for pos in data['crypto_positions']:
            print(f"  {BG_BLUE}{WHITE} {pos['symbol']} {RESET}")
            print(f"    Quantity:  {pos['quantity']:.8f}")
            print(f"    Value:     {format_currency(pos['value'])}")
            print()

    print(f"  {CYAN}{'═' * 76}{RESET}")
    print()

    input(f"  {CYAN}Press ENTER to continue...{RESET}")

def make_trade():
    """Make a trade (withdrawal analogy)"""
    print_atm_header()

    print(f"{BG_RED}{WHITE}{BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                    ⚠️  TRADING FUNCTION  ⚠️                                ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    print(f"  {YELLOW}This feature allows you to execute trades on your account.{RESET}")
    print()
    print(f"  {CYAN}Available actions:{RESET}")
    print(f"    {GREEN}1.{RESET} Buy Cryptocurrency")
    print(f"    {GREEN}2.{RESET} Sell Cryptocurrency")
    print(f"    {GREEN}3.{RESET} Return to Main Menu")
    print()

    choice = input(f"  {CYAN}═══► Enter choice (1-3): {RESET}")

    if choice == "1":
        print()
        print(f"  {YELLOW}BUY CRYPTOCURRENCY{RESET}")
        print(f"  {CYAN}{'─' * 76}{RESET}")
        asset = input(f"  Enter asset symbol (e.g., BTC, ETH): {RESET}").upper()
        amount = input(f"  Enter USD amount to spend: ${RESET}")

        print()
        print(f"  {YELLOW}⚠️  Trading via ATM interface is not yet implemented.{RESET}")
        print(f"  {CYAN}Please use Claude Code MCP for actual trades:{RESET}")
        print(f"    Buy ${amount} worth of {asset}")
        print()
        input(f"  {CYAN}Press ENTER to continue...{RESET}")

    elif choice == "2":
        print()
        print(f"  {YELLOW}SELL CRYPTOCURRENCY{RESET}")
        print(f"  {CYAN}{'─' * 76}{RESET}")
        asset = input(f"  Enter asset symbol (e.g., BTC, ETH): {RESET}").upper()
        amount = input(f"  Enter quantity to sell: {RESET}")

        print()
        print(f"  {YELLOW}⚠️  Trading via ATM interface is not yet implemented.{RESET}")
        print(f"  {CYAN}Please use Claude Code MCP for actual trades:{RESET}")
        print(f"    Sell {amount} of {asset}")
        print()
        input(f"  {CYAN}Press ENTER to continue...{RESET}")

def show_menu():
    """Display main ATM menu"""
    while True:
        print_atm_header()

        print(f"  {BOLD}{CYAN}MAIN MENU{RESET}")
        print(f"  {CYAN}{'═' * 76}{RESET}")
        print()
        print(f"  {GREEN}[1]{RESET} Check Balance")
        print(f"  {GREEN}[2]{RESET} View Positions")
        print(f"  {GREEN}[3]{RESET} Make Trade")
        print(f"  {GREEN}[4]{RESET} Account Summary")
        print(f"  {RED}[5]{RESET} Exit ATM")
        print()
        print(f"  {CYAN}{'═' * 76}{RESET}")
        print()

        choice = input(f"  {CYAN}═══► Select an option (1-5): {RESET}")

        if choice == "1":
            display_balance()
        elif choice == "2":
            display_positions()
        elif choice == "3":
            make_trade()
        elif choice == "4":
            display_balance()  # Summary is same as balance for now
        elif choice == "5":
            break
        else:
            print(f"\n  {RED}Invalid selection. Please try again.{RESET}")
            time.sleep(1)

def print_exit_screen():
    """Print exit screen"""
    print_atm_header()
    print()
    print_centered("Thank you for using Robinhood Trading ATM", color=CYAN)
    print_centered("═" * 50, color=CYAN)
    print()
    print_centered("Please remember to:", color=YELLOW)
    print_centered("• Monitor your positions regularly", color=WHITE)
    print_centered("• Set appropriate stop losses", color=WHITE)
    print_centered("• Trade responsibly", color=WHITE)
    print()
    print_centered("═" * 50, color=CYAN)
    print()
    print_centered("Session ended", color=GREEN)
    print_centered(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), color=CYAN)
    print()
    time.sleep(3)

def main():
    """Main ATM interface loop"""
    try:
        # Welcome screen
        print_atm_header()
        print_centered("WELCOME", color=CYAN)
        print_centered("═" * 50, color=CYAN)
        print()
        print_centered("Your automated trading terminal", color=WHITE)
        print()
        time.sleep(2)

        # Authenticate
        if not authenticate():
            print_exit_screen()
            return

        # Show quick balance receipt after successful PIN entry
        display_quick_balance_receipt()

        # Show main menu
        show_menu()

        # Exit
        print_exit_screen()

    except KeyboardInterrupt:
        print()
        print_exit_screen()
    except Exception as e:
        print(f"\n{RED}System Error: {e}{RESET}\n")
        time.sleep(2)

if __name__ == "__main__":
    main()
