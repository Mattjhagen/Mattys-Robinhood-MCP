#!/usr/bin/env python3
"""
Robinhood Trading API Client (Ed25519 authentication)
Based on official Robinhood Crypto Trading API documentation
"""

import os
import json
import time
import base64
import requests
from datetime import datetime
from typing import Dict, List, Optional
import nacl.signing


class TradingAPI:
    """
    Direct Robinhood Trading API client using Ed25519 key authentication.

    Requires:
    - ROBINHOOD_API_KEY environment variable (format: rh-api-xxxx-xxxx)
    - ROBINHOOD_PRIVATE_KEY_BASE64 environment variable (Base64 encoded Ed25519 private key)
    """

    def __init__(self, api_version='v2'):
        """
        Initialize Trading API

        Args:
            api_version: 'v2' (recommended - fee tiers) or 'v1' (no fee tiers)
        """
        self.base_url = "https://trading.robinhood.com"
        self.api_version = api_version
        self.api_key = os.getenv('ROBINHOOD_API_KEY')
        self.private_key_base64 = os.getenv('ROBINHOOD_PRIVATE_KEY_BASE64')
        self.private_key = None
        self.authenticated = False

        # Try to load Ed25519 private key
        if self.api_key and self.private_key_base64:
            try:
                private_key_seed = base64.b64decode(self.private_key_base64)
                self.private_key = nacl.signing.SigningKey(private_key_seed)
                self.authenticated = True
                print(f"✅ Trading API initialized with Ed25519 key ({api_version})")
            except Exception as e:
                print(f"❌ Error loading Ed25519 key: {e}")
        else:
            print("⚠️  Trading API not configured")
            print("   Set ROBINHOOD_API_KEY and ROBINHOOD_PRIVATE_KEY_BASE64")

    def is_authenticated(self) -> bool:
        """Check if Trading API is ready to use"""
        return self.authenticated

    def _get_current_timestamp(self) -> int:
        """Get current Unix timestamp"""
        return int(time.time())

    def _generate_signature(self, timestamp: int, method: str, path: str, body: str = "") -> str:
        """
        Generate Ed25519 signature for API request
        Based on official Robinhood documentation
        """
        message = f"{self.api_key}{timestamp}{path}{method}{body}"
        signed = self.private_key.sign(message.encode("utf-8"))
        return base64.b64encode(signed.signature).decode("utf-8")

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """
        Make authenticated API request to Robinhood
        """
        if not self.authenticated:
            return {'error': 'Trading API not authenticated. Run generate_keys.py first.'}

        timestamp = self._get_current_timestamp()
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
                response = requests.post(url, headers=headers, json=data if data else None, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"❌ Robinhood API HTTP error: {e}")
            try:
                error_data = e.response.json()
                return {'error': error_data, 'status_code': e.response.status_code}
            except:
                return {'error': str(e), 'status_code': e.response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"❌ Robinhood API error: {e}")
            return {'error': str(e)}

    # ============================================================================
    # ACCOUNT OPERATIONS
    # ============================================================================

    def get_accounts(self) -> Dict:
        """Get all crypto trading accounts"""
        if self.api_version == 'v2':
            return self._make_request('GET', '/crypto/trading/accounts/')
        else:
            return self._make_request('GET', '/crypto/trading/accounts/')

    def get_account(self) -> Dict:
        """Get primary account information"""
        accounts = self.get_accounts()
        if 'results' in accounts and len(accounts['results']) > 0:
            return accounts['results'][0]
        return accounts

    # ============================================================================
    # TRADING OPERATIONS
    # ============================================================================

    def place_crypto_order(self, symbol: str, side: str, order_type: str = 'market',
                          quantity: float = None, notional: float = None,
                          account_number: str = None) -> Dict:
        """
        Place a cryptocurrency order

        Args:
            symbol: Trading pair (e.g., 'BTC-USD')
            side: 'buy' or 'sell'
            order_type: 'market', 'limit', 'stop_loss', 'stop_limit'
            quantity: Amount of crypto (asset_quantity)
            notional: USD amount (quote_amount) for buy orders
            account_number: Required for v2 API

        Returns:
            Order details or error
        """
        import uuid

        if not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"

        body = {
            'client_order_id': str(uuid.uuid4()),
            'side': side.lower(),
            'symbol': symbol,
            'type': order_type,
        }

        # Configure order based on type
        if order_type == 'market':
            if quantity:
                # Round quantity based on symbol requirements
                if 'ADA' in symbol:
                    # ADA requires 0.01 precision (2 decimal places)
                    rounded_qty = round(quantity, 2)
                elif 'DOGE' in symbol:
                    # DOGE requires 1.0 precision (whole numbers)
                    rounded_qty = round(quantity, 0)
                else:
                    # Most cryptos: 8 decimal places
                    rounded_qty = round(quantity, 8)

                body['market_order_config'] = {'asset_quantity': str(rounded_qty)}
            elif notional:
                body['market_order_config'] = {'quote_amount': str(notional)}
            else:
                return {'error': 'Must specify either quantity or notional'}
        else:
            return {'error': f'Order type {order_type} not yet implemented'}

        # V2 requires account_number as query parameter
        if self.api_version == 'v2':
            if not account_number:
                # Get account number from accounts
                account_info = self.get_account()
                account_number = account_info.get('account_number')
                if not account_number:
                    return {'error': 'Could not determine account number'}

            endpoint = f'/crypto/trading/orders/?account_number={account_number}'
        else:
            endpoint = '/crypto/trading/orders/'

        return self._make_request('POST', endpoint, body)

    def buy_crypto(self, symbol: str, amount_usd: float, account_number: str = None) -> Dict:
        """Buy cryptocurrency with USD amount"""
        return self.place_crypto_order(symbol, 'buy', notional=amount_usd,
                                      account_number=account_number)

    def sell_crypto(self, symbol: str, quantity: float, account_number: str = None) -> Dict:
        """Sell cryptocurrency quantity"""
        return self.place_crypto_order(symbol, 'sell', quantity=quantity,
                                      account_number=account_number)

    # ============================================================================
    # MARKET DATA
    # ============================================================================

    def get_best_bid_ask(self, *symbols: str) -> Dict:
        """Get best bid/ask quotes for symbols"""
        if not symbols:
            return {'error': 'Must specify at least one symbol'}

        # Build query string
        symbol_params = '&'.join([f'symbol={s}' for s in symbols])
        endpoint = f'/crypto/marketdata/best_bid_ask/?{symbol_params}'

        return self._make_request('GET', endpoint)

    def get_holdings(self, account_number: str = None, *asset_codes: str) -> Dict:
        """Get crypto holdings"""
        if self.api_version == 'v2':
            if not account_number:
                account_info = self.get_account()
                account_number = account_info.get('account_number')

            params = [f'account_number={account_number}']
            if asset_codes:
                params.extend([f'asset_code={code}' for code in asset_codes])

            endpoint = f'/crypto/trading/holdings/?{"&".join(params)}'
        else:
            if asset_codes:
                asset_params = '&'.join([f'asset_code={code}' for code in asset_codes])
                endpoint = f'/crypto/trading/holdings/?{asset_params}'
            else:
                endpoint = '/crypto/trading/holdings/'

        return self._make_request('GET', endpoint)

    # ============================================================================
    # ORDER MANAGEMENT
    # ============================================================================

    def get_orders(self, account_number: str = None) -> Dict:
        """Get order history"""
        if self.api_version == 'v2':
            if not account_number:
                account_info = self.get_account()
                account_number = account_info.get('account_number')

            endpoint = f'/crypto/trading/orders/?account_number={account_number}'
        else:
            endpoint = '/crypto/trading/orders/'

        return self._make_request('GET', endpoint)

    def cancel_order(self, order_id: str) -> Dict:
        """Cancel a pending order"""
        endpoint = f'/crypto/trading/orders/{order_id}/cancel/'
        return self._make_request('POST', endpoint)


# Singleton instance
_trading_api_instance = None

def get_trading_api() -> TradingAPI:
    """Get or create Trading API singleton"""
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
            print(f"  Status: {account.get('status', 'N/A')}")
            print(f"  Buying Power: ${account.get('buying_power', '0.00')}")
        else:
            print(f"  Error: {account['error']}")

        print("\n💰 Testing Holdings:")
        holdings = api.get_holdings()
        if 'results' in holdings:
            print(f"  Found {len(holdings['results'])} holdings")
        else:
            print(f"  Error or no holdings: {holdings}")

        print("\n📈 Testing Quotes:")
        quotes = api.get_best_bid_ask('BTC-USD', 'ETH-USD')
        if 'results' in quotes:
            print(f"  Got quotes for {len(quotes['results'])} symbols")
        else:
            print(f"  Error: {quotes}")
    else:
        print("\n⚠️  Cannot test - Trading API not authenticated")
        print("   Run: python3 generate_keys.py")
        print("   Then add keys to ~/.bashrc")

    print("\n✅ API test complete")
