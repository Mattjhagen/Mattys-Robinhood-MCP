#!/usr/bin/env python3
"""
P3 Lending Inc - ATM Server
Web-based ATM interface with backend API
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__,
           static_folder='atm_static',
           template_folder='atm_templates')

# Configuration
CORRECT_PIN = "0213"
STATE_FILE = Path.home() / ".trading-agent-state.json"
SESSION_FILE = Path.home() / ".atm-session.json"

class ATMSession:
    def __init__(self):
        self.authenticated = False
        self.pin_attempts = 0
        self.max_attempts = 3

    def to_dict(self):
        return {
            'authenticated': self.authenticated,
            'pin_attempts': self.pin_attempts
        }

session = ATMSession()

def load_portfolio_data():
    """Load portfolio data"""
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            return {
                'total_value': 34.45,
                'buying_power': 0.00,
                'crypto_positions': [
                    {'symbol': 'BTC', 'quantity': 0.00023893, 'value': 19.81, 'change': '+2.3%'},
                    {'symbol': 'ETH', 'quantity': 0.005831, 'value': 14.61, 'change': '-0.8%'}
                ],
                'last_update': state.get('last_update', datetime.now().isoformat())
            }
    except:
        return {
            'total_value': 34.45,
            'buying_power': 0.00,
            'crypto_positions': [
                {'symbol': 'BTC', 'quantity': 0.00023893, 'value': 19.81, 'change': '+2.3%'},
                {'symbol': 'ETH', 'quantity': 0.005831, 'value': 14.61, 'change': '-0.8%'}
            ],
            'last_update': datetime.now().isoformat()
        }

@app.route('/')
def index():
    """Main ATM interface"""
    return render_template('atm.html')

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate with PIN"""
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
        return jsonify({'success': True, 'message': 'Authentication successful'})
    else:
        session.pin_attempts += 1
        remaining = session.max_attempts - session.pin_attempts
        return jsonify({
            'success': False,
            'message': f'Incorrect PIN. {remaining} attempts remaining.',
            'attempts_remaining': remaining
        })

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout and clear session"""
    session.authenticated = False
    session.pin_attempts = 0
    return jsonify({'success': True})

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

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get ATM status"""
    return jsonify({
        'online': True,
        'institution': 'P3 Lending Inc',
        'timestamp': datetime.now().isoformat(),
        'session': session.to_dict()
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Create directories if they don't exist
    Path('atm_static').mkdir(exist_ok=True)
    Path('atm_templates').mkdir(exist_ok=True)

    # Run on port 5050
    app.run(host='127.0.0.1', port=5050, debug=False)
