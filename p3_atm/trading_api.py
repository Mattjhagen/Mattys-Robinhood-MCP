#!/usr/bin/env python3
"""
Robinhood Trading API Client (PEM-based authentication)
This module provides WRITE access for trading operations.

For READ-ONLY operations, use robinhood_api.py with MCP bridge.
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
from pathlib import Path


class TradingAPI:
    """
    Direct Robinhood Trading API client using PEM key authentication.

    Requires:
    - ROBINHOOD_API_KEY environment variable
    - ROBINHOOD_PRIVATE_KEY_PATH pointing to PEM file
    """

    def __init__(self, api_version='v2'):
        """
        Initialize Trading API

        Args:
            api_version: 'v2' (recommended - fee tiers) or 'v1' (no fee tiers)
        """
        self.base_url = "https://api.robinhood.com"
        self.api_version = api_version  # v2 or v1
        self.api_key = os.getenv('ROBINHOOD_API_KEY')
        self.private_key_path = os.getenv('ROBINHOOD_PRIVATE_KEY_PATH')
        self.private_key = None
        self.authenticated = False

        # Try to load PEM key
        if self.api_key and self.private_key_path:
            try:
                key_path = Path(self.private_key_path).expanduser()
                with open(key_path, 'r') as f:
                    self.private_key = f.read()
                self.authenticated = True
                print("✅ Trading API initialized with PEM key")
            except FileNotFoundError:
                print(f"❌ PEM key file not found: {self.private_key_path}")
            except Exception as e:
                print(f"❌ Error loading PEM key: {e}")
        else:
            print("⚠️  Trading API not configured")
            print("   Set ROBINHOOD_API_KEY and ROBINHOOD_PRIVATE_KEY_PATH")

    def is_authenticated(self) -> bool:
        """Check if Trading API is ready to use"""
        return self.authenticated

    def _generate_signature(self, timestamp: int, method: str, path: str, body: str = "") -> str:
        """
        Generate HMAC-SHA256 signature for API request
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
        Make authenticated API request to Robinhood
        """
        if not self.authenticated:
            return {'error': 'Trading API not authenticated. Set up PEM keys first.'}

        timestamp = int(time.time() * 1000)
        path = f"/api/{self.api_version}{endpoint}"
        body = json.dumps(data) if data else ""

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'x-timestamp': str(timestamp),
            'x-signature': self._generate_signature(timestamp, method, path, body)
        }

        url = f"{self.base_url}{path}"

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"❌ Robinhood API HTTP error: {e}")
            print(f"   Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            return {'error': str(e), 'response': e.response.text if hasattr(e, 'response') else None}
        except requests.exceptions.RequestException as e:
            print(f"❌ Robinhood API error: {e}")
            return {'error': str(e)}

    # ============================================================================
    # TRADING OPERATIONS
    # ============================================================================

    def place_crypto_order(self, symbol: str, side: str, order_type: str = 'market',
                          quantity: float = None, notional: float = None) -> Dict:
        """
        Place a cryptocurrency order

        Args:
            symbol: Trading pair (e.g., 'BTC-USD')
            side: 'buy' or 'sell'
            order_type: 'market' or 'limit'
            quantity: Amount of crypto (for sell orders)
            notional: USD amount (for buy orders)

        Returns:
            Order details or error
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
        Buy cryptocurrency with USD amount

        Args:
            symbol: Crypto symbol (e.g., 'BTC', 'ETH')
            amount_usd: Dollar amount to spend

        Returns:
            Order details
        """
        return self.place_crypto_order(symbol, 'buy', notional=amount_usd)

    def sell_crypto(self, symbol: str, quantity: float) -> Dict:
        """
        Sell cryptocurrency quantity

        Args:
            symbol: Crypto symbol (e.g., 'BTC', 'ETH')
            quantity: Amount to sell

        Returns:
            Order details
        """
        return self.place_crypto_order(symbol, 'sell', quantity=quantity)

    def get_order(self, order_id: str) -> Dict:
        """
        Get status of a specific order

        Args:
            order_id: Order ID to check

        Returns:
            Order status details
        """
        return self._make_request('GET', f'/crypto/trading/orders/{order_id}/')

    def cancel_order(self, order_id: str) -> Dict:
        """
        Cancel a pending order

        Args:
            order_id: Order ID to cancel

        Returns:
            Cancellation confirmation
        """
        return self._make_request('DELETE', f'/crypto/trading/orders/{order_id}/')

    def get_order_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent orders

        Args:
            limit: Number of orders to return

        Returns:
            List of recent orders
        """
        response = self._make_request('GET', f'/crypto/trading/orders/?limit={limit}')
        return response.get('results', [])

    # ============================================================================
    # ACCOUNT & BALANCE INFO
    # ============================================================================

    def get_account(self) -> Dict:
        """Get account information"""
        return self._make_request('GET', '/account/')

    def get_buying_power(self) -> float:
        """Get available buying power"""
        account = self.get_account()
        if 'error' in account:
            return 0.0
        return float(account.get('buying_power', account.get('crypto_buying_power', 0.0)))


# Singleton instance
_trading_api_instance = None

def get_trading_api() -> TradingAPI:
    """
    Get or create Trading API singleton
    """
    global _trading_api_instance
    if _trading_api_instance is None:
        _trading_api_instance = TradingAPI()
    return _trading_api_instance


if __name__ == '__main__':
    # Test the Trading API
    api = get_trading_api()

    print("\n🔐 Robinhood Trading API Test")
    print("=" * 60)
    print(f"Authenticated: {api.is_authenticated()}")

    if api.is_authenticated():
        print("\n📊 Testing Account Access:")
        account = api.get_account()
        if 'error' not in account:
            print(f"  Account Number: {account.get('account_number', 'N/A')}")
            print(f"  Buying Power: ${account.get('buying_power', '0.00')}")
        else:
            print(f"  Error: {account['error']}")

        print("\n💰 Testing Buying Power:")
        buying_power = api.get_buying_power()
        print(f"  Available: ${buying_power:.2f}")

        print("\n📜 Testing Order History:")
        orders = api.get_order_history(limit=5)
        print(f"  Found {len(orders)} recent orders")
    else:
        print("\n⚠️  Cannot test - Trading API not authenticated")
        print("   Follow GET_TRADING_API_KEYS.md to set up PEM keys")

    print("\n✅ API test complete")
