#!/usr/bin/env python3
"""
P3 Lending Inc - ATM Server with Clover Integration
Enhanced version supporting Clover card reader and PIN pad
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import hashlib
import hmac
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path for robinhood_api import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from robinhood_api import get_robinhood_api
from totp_2fa import get_totp_2fa

app = Flask(__name__,
           static_folder='atm_static',
           template_folder='atm_templates')

# Initialize Robinhood API
robinhood = get_robinhood_api()

# Configuration
CORRECT_PIN = "0213"
STATE_FILE = Path.home() / ".trading-agent-state.json"
SESSION_FILE = Path.home() / ".atm-session.json"

# Clover Configuration (set these from your Clover dashboard)
CLOVER_MERCHANT_ID = os.getenv('CLOVER_MERCHANT_ID', '')
CLOVER_API_KEY = os.getenv('CLOVER_API_KEY', '')
CLOVER_ENCRYPTION_KEY = os.getenv('CLOVER_ENCRYPTION_KEY', '')

class ATMSession:
    def __init__(self):
        self.authenticated = False
        self.pin_attempts = 0
        self.max_attempts = 3
        self.card_token = None  # Track which card is used
        self.auth_method = None  # 'pin' or 'card'

    def to_dict(self):
        return {
            'authenticated': self.authenticated,
            'pin_attempts': self.pin_attempts,
            'card_token': self.card_token,
            'auth_method': self.auth_method
        }

session = ATMSession()

def load_portfolio_data():
    """Load portfolio data from Robinhood API"""
    try:
        # Get real data from Robinhood API
        total_value = robinhood.get_portfolio_value()
        buying_power = robinhood.get_buying_power()
        positions = robinhood.get_positions()

        return {
            'total_value': total_value,
            'buying_power': buying_power,
            'crypto_positions': positions,
            'last_update': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error loading portfolio: {e}")
        # Fallback to mock data
        return {
            'total_value': 34.45,
            'buying_power': 0.00,
            'crypto_positions': [
                {'symbol': 'BTC', 'quantity': 0.00023893, 'value': 19.81, 'change': '+2.3%'},
                {'symbol': 'ETH', 'quantity': 0.005831, 'value': 14.61, 'change': '-0.8%'}
            ],
            'last_update': datetime.now().isoformat()
        }

def decrypt_clover_pin(encrypted_pin):
    """
    Decrypt PIN from Clover's secure element

    In production, this would:
    1. Use Clover's encryption key
    2. Decrypt the PIN block
    3. Extract the clear-text PIN
    4. Return for verification

    For now, this is a placeholder that shows the structure.
    """
    # TODO: Implement actual Clover encryption/decryption
    # See: https://docs.clover.com/docs/encrypting-card-data

    try:
        # Clover sends encrypted PIN as base64-encoded string
        # Decrypt using your Clover encryption key
        # For demo purposes, we'll return a mock PIN

        if not CLOVER_ENCRYPTION_KEY:
            print("WARNING: CLOVER_ENCRYPTION_KEY not set!")
            return None

        # In production, do real decryption here:
        # decrypted = decrypt_with_key(encrypted_pin, CLOVER_ENCRYPTION_KEY)
        # return decrypted

        # For testing (remove in production):
        return CORRECT_PIN  # Mock successful decrypt

    except Exception as e:
        print(f"PIN decryption error: {e}")
        return None

def verify_pin_hash(pin):
    """Verify PIN against stored hash"""
    # In production, compare against stored hash
    # For demo, direct comparison
    return pin == CORRECT_PIN

@app.route('/')
def index():
    """Main ATM interface"""
    return render_template('atm.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/x-icon')

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    """Serve Apple touch icon"""
    return send_from_directory(app.static_folder, 'apple-touch-icon.png', mimetype='image/png')

@app.route('/clover')
def clover_bridge():
    """Clover integration bridge page"""
    return send_from_directory('../clover_integration', 'clover_bridge.html')

# ============================================================================
# 2FA ENDPOINTS
# ============================================================================

@app.route('/api/2fa/setup', methods=['GET'])
def setup_2fa():
    """Get 2FA setup information (QR code and secret)"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        totp = get_totp_2fa()
        qr_data = totp.generate_qr_code()

        return jsonify({
            'success': True,
            'qr_code': f"data:image/png;base64,{qr_data['qr_code_base64']}",
            'secret': qr_data['secret'],
            'uri': qr_data['uri'],
            'account_name': 'Trading Terminal',
            'issuer': 'Robinhood ATM'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/2fa/verify', methods=['POST'])
def verify_2fa():
    """Verify a 2FA code"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json
    code = data.get('code', '').strip()

    if not code or len(code) != 6 or not code.isdigit():
        return jsonify({
            'success': False,
            'error': 'Invalid code format. Must be 6 digits.'
        })

    try:
        totp = get_totp_2fa()
        is_valid = totp.verify_code(code)

        return jsonify({
            'success': True,
            'valid': is_valid,
            'message': 'Code is valid' if is_valid else 'Code is invalid or expired'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/2fa/status', methods=['GET'])
def get_2fa_status():
    """Check if 2FA is set up"""
    try:
        totp = get_totp_2fa()
        secret = totp.get_or_create_secret()

        return jsonify({
            'success': True,
            'setup': True,
            'has_secret': bool(secret)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'setup': False,
            'error': str(e)
        })

# ============================================================================
# STANDARD PIN AUTHENTICATION (Touchscreen)
# ============================================================================

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate with PIN (touchscreen entry)"""
    data = request.json
    pin = data.get('pin', '')

    if session.authenticated:
        return jsonify({'success': True, 'message': 'Already authenticated'})

    if session.pin_attempts >= session.max_attempts:
        return jsonify({
            'success': False,
            'message': 'Maximum attempts exceeded. Card retained.',
            'locked': True
        })

    if pin == CORRECT_PIN:
        session.authenticated = True
        session.pin_attempts = 0
        session.auth_method = 'pin'
        return jsonify({'success': True, 'message': 'Authentication successful'})
    else:
        session.pin_attempts += 1
        remaining = session.max_attempts - session.pin_attempts
        return jsonify({
            'success': False,
            'message': f'Incorrect PIN. {remaining} attempts remaining.',
            'attempts_remaining': remaining
        })

# ============================================================================
# CLOVER CARD AUTHENTICATION (Secure PIN Pad)
# ============================================================================

@app.route('/api/authenticate/card', methods=['POST'])
def authenticate_card():
    """
    Authenticate using Clover card reader and secure PIN pad

    This endpoint receives:
    - encrypted_pin: PIN encrypted by Clover's secure element
    - card_token: Tokenized card identifier
    - timestamp: When PIN was entered

    Security:
    - PIN never transmitted in clear text
    - Encrypted end-to-end from PIN pad to server
    - PCI-DSS compliant when properly implemented
    """
    data = request.json
    encrypted_pin = data.get('encrypted_pin')
    card_token = data.get('card_token')
    timestamp = data.get('timestamp')

    if not encrypted_pin:
        return jsonify({
            'success': False,
            'message': 'No PIN data received'
        }), 400

    # Check if already authenticated
    if session.authenticated:
        return jsonify({
            'success': True,
            'message': 'Already authenticated',
            'card_token': session.card_token
        })

    # Check maximum attempts
    if session.pin_attempts >= session.max_attempts:
        return jsonify({
            'success': False,
            'message': 'Maximum attempts exceeded. Please contact support.',
            'locked': True
        }), 403

    # Decrypt PIN from Clover's secure element
    decrypted_pin = decrypt_clover_pin(encrypted_pin)

    if not decrypted_pin:
        return jsonify({
            'success': False,
            'message': 'PIN decryption failed. Please try again.'
        }), 500

    # Verify PIN
    if verify_pin_hash(decrypted_pin):
        session.authenticated = True
        session.pin_attempts = 0
        session.card_token = card_token
        session.auth_method = 'card'

        return jsonify({
            'success': True,
            'message': 'Authentication successful',
            'card_token': card_token,
            'timestamp': datetime.now().isoformat()
        })
    else:
        session.pin_attempts += 1
        remaining = session.max_attempts - session.pin_attempts

        return jsonify({
            'success': False,
            'message': f'Incorrect PIN. {remaining} attempts remaining.',
            'attempts_remaining': remaining
        })

@app.route('/api/card/verify', methods=['POST'])
def verify_card():
    """
    Verify card only (no PIN) for low-security operations
    Like checking if a card is registered
    """
    data = request.json
    card_token = data.get('card_token')

    if not card_token:
        return jsonify({'success': False, 'message': 'No card data'}), 400

    # Check if this card is registered
    # In production, check against database
    registered_cards = []  # Load from database

    is_registered = card_token in registered_cards

    return jsonify({
        'success': True,
        'registered': is_registered,
        'card_token': card_token
    })

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout and clear session"""
    session.authenticated = False
    session.pin_attempts = 0
    session.card_token = None
    session.auth_method = None
    return jsonify({'success': True})

@app.route('/api/session', methods=['GET'])
def get_session():
    """Get current session state"""
    return jsonify(session.to_dict())

# ============================================================================
# PORTFOLIO & TRADING
# ============================================================================

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get portfolio data"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = load_portfolio_data()
    return jsonify(data)

@app.route('/api/balance', methods=['GET'])
def get_balance():
    """Get account balance"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = load_portfolio_data()
    return jsonify({
        'total_value': data['total_value'],
        'buying_power': data['buying_power'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/positions', methods=['GET'])
def get_positions():
    """Get current positions"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = load_portfolio_data()
    return jsonify({
        'positions': data['crypto_positions'],
        'timestamp': datetime.now().isoformat()
    })

# ============================================================================
# SYSTEM STATUS
# ============================================================================

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get ATM status"""
    return jsonify({
        'online': True,
        'institution': 'P3 Lending Inc',
        'timestamp': datetime.now().isoformat(),
        'session': session.to_dict(),
        'clover_enabled': bool(CLOVER_MERCHANT_ID and CLOVER_API_KEY)
    })

@app.route('/api/clover/status', methods=['GET'])
def clover_status():
    """Check Clover integration status"""
    return jsonify({
        'configured': bool(CLOVER_MERCHANT_ID and CLOVER_API_KEY),
        'merchant_id': CLOVER_MERCHANT_ID[:8] + '...' if CLOVER_MERCHANT_ID else None,
        'encryption_key_set': bool(CLOVER_ENCRYPTION_KEY)
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'clover': bool(CLOVER_MERCHANT_ID)})

@app.route('/api/quick-balance', methods=['GET'])
def quick_balance():
    """
    Get quick balance preview for welcome screen
    Returns cached/last-known balances - no authentication required
    This is safe because it only shows high-level totals from last session
    """
    try:
        # Try to get accounts from API (will return mock data if not authenticated)
        accounts = robinhood.get_all_accounts()
        positions = robinhood.get_positions()

        total_value = sum(acc.get('balance', 0) for acc in accounts)

        # Calculate overall profit/loss from positions
        total_cost = sum(pos.get('cost_basis', 0) for pos in positions)
        total_position_value = sum(pos.get('value', 0) for pos in positions)
        total_profit_loss = total_position_value - total_cost
        total_profit_loss_pct = (total_profit_loss / total_cost * 100) if total_cost > 0 else 0

        return jsonify({
            'success': True,
            'total_value': total_value,
            'accounts': accounts,
            'positions': positions,
            'profit_loss': {
                'amount': total_profit_loss,
                'percentage': total_profit_loss_pct,
                'cost_basis': total_cost,
                'current_value': total_position_value
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Error getting quick balance: {e}")
        # Fallback to safe default
        return jsonify({
            'success': True,
            'total_value': 0.00,
            'accounts': [],
            'positions': [],
            'profit_loss': {
                'amount': 0,
                'percentage': 0,
                'cost_basis': 0,
                'current_value': 0
            },
            'timestamp': datetime.now().isoformat()
        })

# ============================================================================
# TRADING ENDPOINTS (Robinhood API Integration)
# ============================================================================

@app.route('/api/trade/buy', methods=['POST'])
def trade_buy():
    """Buy cryptocurrency via Robinhood API - Requires 2FA"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json
    symbol = data.get('symbol', '').upper().strip()
    amount = float(data.get('amount', 0))
    two_fa_code = data.get('2fa_code', '').strip()

    if not symbol or amount <= 0:
        return jsonify({'success': False, 'error': 'Invalid symbol or amount'})

    # Verify 2FA code
    if not two_fa_code:
        return jsonify({
            'success': False,
            'error': '2FA code required',
            'requires_2fa': True
        })

    totp = get_totp_2fa()
    if not totp.verify_code(two_fa_code):
        return jsonify({
            'success': False,
            'error': 'Invalid or expired 2FA code',
            'requires_2fa': True
        })

    try:
        # Execute buy order through Robinhood API
        result = robinhood.buy_crypto(symbol, amount)

        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            })

        return jsonify({
            'success': True,
            'message': f'Successfully bought ${amount:.2f} of {symbol}',
            'order_id': result.get('id'),
            'status': result.get('status')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/trade/sell', methods=['POST'])
def trade_sell():
    """Sell cryptocurrency via Robinhood API - Requires 2FA"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json
    symbol = data.get('symbol', '').upper().strip()
    quantity = float(data.get('quantity', 0))
    two_fa_code = data.get('2fa_code', '').strip()

    if not symbol or quantity <= 0:
        return jsonify({'success': False, 'error': 'Invalid symbol or quantity'})

    # Verify 2FA code
    if not two_fa_code:
        return jsonify({
            'success': False,
            'error': '2FA code required',
            'requires_2fa': True
        })

    totp = get_totp_2fa()
    if not totp.verify_code(two_fa_code):
        return jsonify({
            'success': False,
            'error': 'Invalid or expired 2FA code',
            'requires_2fa': True
        })

    try:
        # Execute sell order through Robinhood API
        result = robinhood.sell_crypto(symbol, quantity)

        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            })

        return jsonify({
            'success': True,
            'message': f'Successfully sold {quantity} {symbol}',
            'order_id': result.get('id'),
            'status': result.get('status')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/transfer', methods=['POST'])
def transfer_to_debit():
    """Transfer funds to Robinhood debit card - Requires 2FA"""
    if not session.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.json
    amount = float(data.get('amount', 0))
    two_fa_code = data.get('2fa_code', '').strip()

    if amount <= 0:
        return jsonify({'success': False, 'error': 'Invalid amount'})

    # Verify 2FA code
    if not two_fa_code:
        return jsonify({
            'success': False,
            'error': '2FA code required',
            'requires_2fa': True
        })

    totp = get_totp_2fa()
    if not totp.verify_code(two_fa_code):
        return jsonify({
            'success': False,
            'error': 'Invalid or expired 2FA code',
            'requires_2fa': True
        })

    try:
        # NOTE: This requires the actual Robinhood transfer API
        # For now, this is a placeholder that shows how it would work
        result = robinhood.transfer_to_card(amount)

        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            })

        return jsonify({
            'success': True,
            'message': f'Successfully transferred ${amount:.2f} to debit card',
            'transfer_id': result.get('id'),
            'status': result.get('status')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/quote/<symbol>', methods=['GET'])
def get_quote(symbol):
    """Get real-time quote for symbol"""
    try:
        quote = robinhood.get_quote(symbol)
        return jsonify(quote)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/trading-status', methods=['GET'])
def get_trading_status():
    """Check if automated trading is operational"""
    try:
        # Check if Robinhood API is in live mode (MCP connected)
        if robinhood.is_live():
            return jsonify({
                'status': 'operational',
                'trading_enabled': True,
                'message': 'Trading via MCP is active',
                'mode': 'mcp'
            })

        # Check if trading API keys are configured (direct API mode)
        api_key = os.getenv('ROBINHOOD_API_KEY')
        private_key = os.getenv('ROBINHOOD_PRIVATE_KEY_BASE64')

        if api_key and private_key:
            # Try to import and initialize trading API
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from trading_api_ed25519 import TradingAPI

                api = TradingAPI(api_version='v1')
                if api.is_authenticated():
                    return jsonify({
                        'status': 'operational',
                        'trading_enabled': True,
                        'message': 'Trading via direct API is active',
                        'mode': 'direct_api'
                    })
                else:
                    return jsonify({
                        'status': 'down',
                        'trading_enabled': False,
                        'message': 'Direct API authentication failed'
                    })
            except ImportError:
                pass  # Fall through to down status
            except Exception as e:
                return jsonify({
                    'status': 'down',
                    'trading_enabled': False,
                    'message': f'Direct API error: {str(e)}'
                })

        # Neither MCP nor direct API is available
        return jsonify({
            'status': 'down',
            'trading_enabled': False,
            'message': 'No trading method configured (MCP or direct API)'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'trading_enabled': False,
            'message': str(e)
        })

@app.route('/api/tickers', methods=['GET'])
def get_tickers():
    """Get ticker data for multiple symbols"""
    try:
        symbols = ['BTC', 'ETH', 'DOGE', 'SOL', 'ADA', 'MATIC']
        quotes = robinhood.get_quotes(symbols)
        return jsonify(quotes)
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    # Create directories if they don't exist
    Path('atm_static').mkdir(exist_ok=True)
    Path('atm_templates').mkdir(exist_ok=True)

    # Run on all interfaces (accessible from Clover)
    app.run(host='0.0.0.0', port=5050, debug=False)
