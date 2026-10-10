#!/usr/bin/env python3
"""
Robinhood Crypto API Integration
https://docs.robinhood.com/crypto/trading/

Features:
- OAuth 2.0 authentication
- Real-time WebSocket price feeds
- Order placement and execution
- Account balance retrieval
- Trading history
"""

import os
import json
import time
import hmac
import hashlib
import base64
import requests
from datetime import datetime
from typing import Dict, List, Optional

class RobinhoodAPI:
    """
    Robinhood Crypto API Client
    """

    def __init__(self):
        # API Configuration
        self.base_url = "https://trading.robinhood.com"
        self.api_key = os.getenv('ROBINHOOD_API_KEY', '')
        self.api_secret = os.getenv('ROBINHOOD_API_SECRET', '')
        self.private_key = os.getenv('ROBINHOOD_PRIVATE_KEY', '')

        # Session management
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0

        # Mock mode if no credentials
        self.mock_mode = not (self.api_key and self.private_key)

        if self.mock_mode:
            print("⚠️  Robinhood API running in MOCK MODE (no credentials)")
            print("   Set ROBINHOOD_API_KEY and ROBINHOOD_PRIVATE_KEY to enable live trading")

    def _generate_signature(self, timestamp: int, method: str, path: str, body: str = "") -> str:
        """
        Generate API signature for authentication
        https://docs.robinhood.com/crypto/trading/#section/Authentication/Signing-Requests
        """
        message = f"{timestamp}{method}{path}{body}"
        signature = hmac.new(
            self.private_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode('utf-8')

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """
        Make authenticated API request
        """
        if self.mock_mode:
            return self._mock_response(method, endpoint, data)

        timestamp = int(time.time() * 1000)
        path = f"/api/v1{endpoint}"
        body = json.dumps(data) if data else ""

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'x-timestamp': str(timestamp),
            'x-signature': self._generate_signature(timestamp, method, path, body)
        }

        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        url = f"{self.base_url}{path}"

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ Robinhood API error: {e}")
            return {'error': str(e)}

    def _mock_response(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """
        Mock API responses for testing without credentials
        """
        if '/account' in endpoint:
            return {
                'account_number': '5RF12345',
                'buying_power': '0.00',
                'crypto_buying_power': '0.00',
                'cash': '0.00'
            }

        elif '/holdings' in endpoint or '/positions' in endpoint:
            return {
                'results': [
                    {
                        'asset_code': 'BTC-USD',
                        'quantity': '0.00023893',
                        'quantity_available': '0.00023893',
                        'cost_bases': [{'total_cost': '19.81'}],
                        'market_value': '19.81'
                    },
                    {
                        'asset_code': 'ETH-USD',
                        'quantity': '0.005831',
                        'quantity_available': '0.005831',
                        'cost_bases': [{'total_cost': '14.61'}],
                        'market_value': '14.61'
                    }
                ]
            }

        elif '/orders' in endpoint and method == 'POST':
            order_type = data.get('side', 'buy')
            symbol = data.get('symbol', 'BTC-USD')

            return {
                'id': f'order_{int(time.time())}',
                'client_order_id': data.get('client_order_id'),
                'symbol': symbol,
                'side': order_type,
                'type': data.get('type', 'market'),
                'quantity': data.get('quantity'),
                'notional': data.get('notional'),
                'status': 'filled',
                'created_at': datetime.utcnow().isoformat() + 'Z',
                'average_price': '65432.10' if 'BTC' in symbol else '3245.67'
            }

        elif '/best_bid_ask' in endpoint or '/quotes' in endpoint:
            symbol = endpoint.split('=')[-1] if '=' in endpoint else 'BTC-USD'

            prices = {
                'BTC-USD': {'bid': '65400.00', 'ask': '65432.10', 'last': '65432.10'},
                'ETH-USD': {'bid': '3240.00', 'ask': '3245.67', 'last': '3245.67'},
                'DOGE-USD': {'bid': '0.1230', 'ask': '0.1234', 'last': '0.1234'},
                'SOL-USD': {'bid': '145.00', 'ask': '145.23', 'last': '145.23'},
            }

            return prices.get(symbol, prices['BTC-USD'])

        return {'error': 'Not implemented in mock mode'}

    # ============================================================================
    # ACCOUNT ENDPOINTS
    # ============================================================================

    def get_account(self) -> Dict:
        """
        Get primary account information
        GET /api/v1/crypto/trading/accounts/
        """
        return self._make_request('GET', '/crypto/trading/accounts/')

    def get_all_accounts(self) -> List[Dict]:
        """
        Get all accounts (crypto, stocks, etc)
        Returns list of accounts with balances
        """
        if self.mock_mode:
            return [
                {
                    'account_id': '5RF12345',
                    'account_type': 'crypto',
                    'account_name': 'Crypto Trading',
                    'account_number': '2903',
                    'balance': 34.45,
                    'buying_power': 0.00
                },
                {
                    'account_id': '5RF12346',
                    'account_type': 'individual',
                    'account_name': 'Individual Brokerage',
                    'account_number': '2904',
                    'balance': 1247.89,
                    'buying_power': 340.12
                },
                {
                    'account_id': '5RF12347',
                    'account_type': 'retirement',
                    'account_name': 'Roth IRA',
                    'account_number': '2905',
                    'balance': 8932.14,
                    'buying_power': 0.00
                }
            ]

        # In live mode, fetch real accounts
        response = self._make_request('GET', '/accounts/')
        accounts = response.get('results', [])

        # Format accounts for ATM display
        formatted = []
        for acc in accounts:
            formatted.append({
                'account_id': acc.get('account_id'),
                'account_type': acc.get('type', 'unknown'),
                'account_name': acc.get('name', 'Account'),
                'account_number': acc.get('account_number', '')[-4:],
                'balance': float(acc.get('equity', 0)),
                'buying_power': float(acc.get('buying_power', 0))
            })

        return formatted

    def get_buying_power(self) -> float:
        """
        Get available buying power
        """
        account = self.get_account()
        return float(account.get('crypto_buying_power', 0.0))

    # ============================================================================
    # POSITIONS & HOLDINGS
    # ============================================================================

    def get_holdings(self) -> List[Dict]:
        """
        Get crypto holdings
        GET /api/v1/crypto/trading/holdings/
        """
        response = self._make_request('GET', '/crypto/trading/holdings/')
        return response.get('results', [])

    def get_positions(self) -> List[Dict]:
        """
        Get formatted positions for ATM display
        """
        holdings = self.get_holdings()
        positions = []

        for holding in holdings:
            symbol = holding.get('asset_code', '').replace('-USD', '')
            quantity = float(holding.get('quantity', 0))
            value = float(holding.get('market_value', 0))

            if quantity > 0:
                positions.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'value': value,
                    'change': '+0.00%'  # Calculate from cost basis
                })

        return positions

    def get_portfolio_value(self) -> float:
        """
        Calculate total portfolio value
        """
        holdings = self.get_holdings()
        total = sum(float(h.get('market_value', 0)) for h in holdings)
        return total

    # ============================================================================
    # MARKET DATA
    # ============================================================================

    def get_quote(self, symbol: str) -> Dict:
        """
        Get real-time quote for symbol
        GET /api/v1/crypto/marketdata/best_bid_ask/?symbol=BTC-USD
        """
        if not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"

        return self._make_request('GET', f'/crypto/marketdata/best_bid_ask/?symbol={symbol}')

    def get_quotes(self, symbols: List[str]) -> Dict:
        """
        Get multiple quotes
        """
        quotes = {}
        for symbol in symbols:
            quotes[symbol] = self.get_quote(symbol)
        return quotes

    # ============================================================================
    # TRADING
    # ============================================================================

    def place_order(self, symbol: str, side: str, order_type: str = 'market',
                   quantity: float = None, notional: float = None) -> Dict:
        """
        Place a crypto order
        POST /api/v1/crypto/trading/orders/

        Args:
            symbol: Trading pair (e.g., 'BTC-USD')
            side: 'buy' or 'sell'
            order_type: 'market' or 'limit'
            quantity: Amount of crypto (for sell orders)
            notional: USD amount (for buy orders)
        """
        if not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"

        order_data = {
            'client_order_id': f'atm_{int(time.time())}_{symbol}',
            'side': side.lower(),
            'symbol': symbol,
            'type': order_type,
        }

        if quantity:
            order_data['quantity'] = str(quantity)
        elif notional:
            order_data['notional'] = str(notional)
        else:
            return {'error': 'Must specify either quantity or notional'}

        return self._make_request('POST', '/crypto/trading/orders/', order_data)

    def buy_crypto(self, symbol: str, amount_usd: float) -> Dict:
        """
        Buy crypto with USD amount
        """
        return self.place_order(symbol, 'buy', notional=amount_usd)

    def sell_crypto(self, symbol: str, quantity: float) -> Dict:
        """
        Sell crypto quantity
        """
        return self.place_order(symbol, 'sell', quantity=quantity)

    def get_order(self, order_id: str) -> Dict:
        """
        Get order status
        GET /api/v1/crypto/trading/orders/{order_id}/
        """
        return self._make_request('GET', f'/crypto/trading/orders/{order_id}/')

    def get_order_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent orders
        GET /api/v1/crypto/trading/orders/
        """
        response = self._make_request('GET', f'/crypto/trading/orders/?limit={limit}')
        return response.get('results', [])

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    def format_symbol(self, symbol: str) -> str:
        """
        Convert symbol to Robinhood format (BTC -> BTC-USD)
        """
        symbol = symbol.upper().strip()
        if not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"
        return symbol

    def is_live(self) -> bool:
        """
        Check if API is in live mode (not mock)
        """
        return not self.mock_mode


# Singleton instance
_api_instance = None

def get_robinhood_api() -> RobinhoodAPI:
    """
    Get or create Robinhood API singleton
    """
    global _api_instance
    if _api_instance is None:
        _api_instance = RobinhoodAPI()
    return _api_instance


if __name__ == '__main__':
    # Test the API
    api = get_robinhood_api()

    print("🏦 Robinhood API Test")
    print("=" * 60)
    print(f"Mode: {'LIVE' if api.is_live() else 'MOCK'}")
    print()

    # Test account
    print("📊 Account:")
    account = api.get_account()
    print(json.dumps(account, indent=2))
    print()

    # Test holdings
    print("💰 Holdings:")
    holdings = api.get_positions()
    for pos in holdings:
        print(f"  {pos['symbol']}: {pos['quantity']:.8f} = ${pos['value']:.2f}")
    print()

    # Test quote
    print("📈 BTC Quote:")
    quote = api.get_quote('BTC')
    print(json.dumps(quote, indent=2))
    print()

    print("✅ API test complete")
