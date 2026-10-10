#!/usr/bin/env python3
"""
Agentic Trading Bot - Runs every 15 minutes
Monitors portfolio, executes trading strategies, manages risk
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Add p3_atm to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'p3_atm'))

from robinhood_api import get_robinhood_api
try:
    from trading_api_ed25519 import get_trading_api
    TRADING_AVAILABLE = True
except ImportError:
    TRADING_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/trading_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TradingAgent:
    """
    Autonomous trading agent that manages portfolio in 15-minute loops
    """

    def __init__(self):
        self.api = get_robinhood_api()
        # Use v1 API - simpler and works with your account automatically
        if TRADING_AVAILABLE:
            from trading_api_ed25519 import TradingAPI
            self.trading_api = TradingAPI(api_version='v1')
            self.can_trade = self.trading_api.is_authenticated()
        else:
            self.trading_api = None
            self.can_trade = False

        # Trading parameters
        self.min_trade_amount = 1.0  # Minimum $1 per trade
        self.max_position_pct = 0.25  # Max 25% of portfolio in one asset
        self.profit_take_pct = 0.10  # Take profit at 10% gain
        self.stop_loss_pct = 0.05  # Stop loss at 5% loss

        # Strategy state
        self.last_run = None
        self.trade_history = []

        logger.info(f"Trading Agent initialized - Can trade: {self.can_trade}")

    def run_cycle(self):
        """
        Execute one trading cycle (called every 15 minutes)
        """
        logger.info("=" * 60)
        logger.info("Starting trading cycle")

        try:
            # 1. Get current portfolio state
            portfolio = self._get_portfolio_state()
            logger.info(f"Portfolio value: ${portfolio['total_value']:.2f}")
            logger.info(f"Buying power: ${portfolio['buying_power']:.2f}")
            logger.info(f"Positions: {len(portfolio['positions'])}")

            # 2. Check if we can trade
            if not self.can_trade:
                logger.warning("⚠️  Trading not available - need Trading API keys")
                logger.info("   Monitoring only. Get keys to enable trading.")
                return {
                    'status': 'monitoring_only',
                    'portfolio': portfolio,
                    'message': 'Trading API keys required'
                }

            # 3. Analyze positions for profit-taking or stop-losses
            actions = self._analyze_positions(portfolio)

            # 4. Check for new opportunities
            opportunities = self._scan_opportunities(portfolio)
            actions.extend(opportunities)

            # 5. Execute actions
            results = self._execute_actions(actions)

            # 6. Log results
            self.last_run = datetime.now()
            summary = {
                'status': 'active',
                'timestamp': self.last_run.isoformat(),
                'portfolio': portfolio,
                'actions_taken': len(results),
                'results': results
            }

            logger.info(f"Cycle complete - {len(results)} actions executed")
            return summary

        except Exception as e:
            logger.error(f"Error in trading cycle: {e}", exc_info=True)
            return {
                'status': 'error',
                'message': str(e)
            }

    def _get_portfolio_state(self) -> Dict:
        """Get current portfolio state"""
        try:
            account = self.api.get_account()
            positions = self.api.get_positions()
            total_value = self.api.get_portfolio_value()
            buying_power = float(account.get('buying_power', 0.0))

            return {
                'account_number': account.get('account_number', 'N/A'),
                'total_value': total_value,
                'buying_power': buying_power,
                'positions': positions,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting portfolio state: {e}")
            return {
                'total_value': 0.0,
                'buying_power': 0.0,
                'positions': []
            }

    def _analyze_positions(self, portfolio: Dict) -> List[Dict]:
        """
        Analyze existing positions for profit-taking or stop-losses
        Returns list of recommended actions
        """
        actions = []

        for position in portfolio['positions']:
            symbol = position['symbol']
            quantity = position['quantity']
            current_value = position['value']

            # Get current quote
            quote = self.api.get_quote(symbol)
            current_price = float(quote.get('last', 0))

            # Calculate position metrics
            # Note: We'd need cost basis to calculate actual P&L
            # For now, we'll use heuristics

            # Check if position is too large (rebalance)
            position_pct = current_value / portfolio['total_value'] if portfolio['total_value'] > 0 else 0
            if position_pct > self.max_position_pct:
                # Trim position
                trim_value = current_value - (portfolio['total_value'] * self.max_position_pct)
                trim_quantity = trim_value / current_price if current_price > 0 else 0

                if trim_quantity >= 0.0001:  # Minimum crypto amount
                    actions.append({
                        'action': 'sell',
                        'symbol': symbol,
                        'quantity': trim_quantity,
                        'reason': f'Rebalance - position {position_pct:.1%} > max {self.max_position_pct:.1%}',
                        'priority': 'medium'
                    })

        return actions

    def _scan_opportunities(self, portfolio: Dict) -> List[Dict]:
        """
        Scan for new buying opportunities
        Returns list of recommended actions
        """
        actions = []

        # Only look for opportunities if we have buying power
        if portfolio['buying_power'] < self.min_trade_amount:
            return actions

        # Define watchlist (could be expanded or made dynamic)
        watchlist = ['BTC', 'ETH', 'SOL', 'ADA']

        # Simple strategy: Buy if we don't have position and have buying power
        current_symbols = {p['symbol'] for p in portfolio['positions']}

        for symbol in watchlist:
            if symbol not in current_symbols and portfolio['buying_power'] >= 5.0:
                # Start small position
                buy_amount = min(10.0, portfolio['buying_power'] * 0.1)  # 10% of buying power or $10

                actions.append({
                    'action': 'buy',
                    'symbol': symbol,
                    'amount_usd': buy_amount,
                    'reason': f'New position - diversification',
                    'priority': 'low'
                })
                break  # One new position at a time

        return actions

    def _execute_actions(self, actions: List[Dict]) -> List[Dict]:
        """
        Execute trading actions
        Returns results of executed actions
        """
        if not self.can_trade:
            logger.info(f"Would execute {len(actions)} actions (trading disabled)")
            return []

        results = []

        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        actions.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 2))

        for action in actions:
            try:
                logger.info(f"Executing: {action['action']} {action['symbol']} - {action['reason']}")

                if action['action'] == 'buy':
                    result = self.trading_api.buy_crypto(
                        action['symbol'],
                        action['amount_usd']
                    )
                elif action['action'] == 'sell':
                    result = self.trading_api.sell_crypto(
                        action['symbol'],
                        action['quantity']
                    )
                else:
                    logger.warning(f"Unknown action type: {action['action']}")
                    continue

                # Log result
                if 'error' not in result:
                    logger.info(f"✅ {action['action'].upper()} successful: {result.get('id', 'N/A')}")
                    results.append({
                        **action,
                        'result': 'success',
                        'order_id': result.get('id'),
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    logger.error(f"❌ {action['action'].upper()} failed: {result['error']}")
                    results.append({
                        **action,
                        'result': 'failed',
                        'error': result['error'],
                        'timestamp': datetime.now().isoformat()
                    })

                # Rate limit - wait between actions
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error executing {action}: {e}")
                results.append({
                    **action,
                    'result': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })

        return results


def main():
    """Run one cycle"""
    print("🤖 Agentic Trading Bot")
    print("=" * 60)

    agent = TradingAgent()

    if not agent.can_trade:
        print("\n⚠️  TRADING NOT ENABLED")
        print("   Need Trading API keys with PEM authentication")
        print("   Running in MONITORING mode only\n")
        print("   To enable trading:")
        print("   1. Contact Robinhood support for Trading API keys")
        print("   2. Set ROBINHOOD_PRIVATE_KEY_PATH in ~/.bashrc")
        print("   3. Restart this agent\n")

    result = agent.run_cycle()

    print(f"\nStatus: {result['status']}")
    if result.get('portfolio'):
        print(f"Portfolio Value: ${result['portfolio']['total_value']:.2f}")
        print(f"Buying Power: ${result['portfolio']['buying_power']:.2f}")

    if result.get('actions_taken', 0) > 0:
        print(f"\nActions Taken: {result['actions_taken']}")
        for action_result in result.get('results', []):
            status = "✅" if action_result['result'] == 'success' else "❌"
            print(f"  {status} {action_result['action'].upper()} {action_result['symbol']}")

    return result


if __name__ == '__main__':
    main()
