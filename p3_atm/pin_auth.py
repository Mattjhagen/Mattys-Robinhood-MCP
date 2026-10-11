#!/usr/bin/env python3
"""
Secure PIN Authentication Module
Handles PIN hashing, verification, and lockout management
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict

# Configuration
LOCKOUT_FILE = Path.home() / ".atm-lockout.json"
LOCKOUT_DURATION_MINUTES = 30
MAX_ATTEMPTS = 3

class PINAuthenticator:
    """
    Secure PIN authentication with lockout management

    Features:
    - SHA-256 hashed PIN verification
    - Persistent lockout state (survives restarts)
    - Automatic lockout expiration
    - Attempt tracking
    """

    def __init__(self):
        self.pin_hash = self._get_pin_hash()
        if not self.pin_hash:
            raise ValueError(
                "ATM_PIN_HASH environment variable not set. "
                "Generate with: echo -n 'YOUR_PIN' | sha256sum"
            )

    def _get_pin_hash(self) -> Optional[str]:
        """Get PIN hash from environment variable"""
        return os.getenv('ATM_PIN_HASH')

    def verify_pin(self, input_pin: str) -> bool:
        """
        Verify PIN against stored hash

        Args:
            input_pin: PIN to verify

        Returns:
            True if PIN is correct, False otherwise
        """
        if not input_pin:
            return False

        # Hash the input PIN
        pin_hash = hashlib.sha256(input_pin.encode()).hexdigest()

        # Compare with stored hash
        return pin_hash == self.pin_hash

    def check_lockout(self) -> Dict:
        """
        Check if PIN entry is currently locked out

        Returns:
            Dict with 'locked' (bool) and 'lockout_until' (str) if locked
        """
        if not LOCKOUT_FILE.exists():
            return {'locked': False}

        try:
            with open(LOCKOUT_FILE) as f:
                data = json.load(f)
                lockout_until = datetime.fromisoformat(data['lockout_until'])

                if datetime.now() < lockout_until:
                    return {
                        'locked': True,
                        'lockout_until': data['lockout_until'],
                        'reason': data.get('reason', 'Locked out'),
                        'minutes_remaining': int((lockout_until - datetime.now()).total_seconds() / 60)
                    }

            # Lockout expired, remove file
            LOCKOUT_FILE.unlink()
            return {'locked': False}

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Corrupted lockout file, remove it
            LOCKOUT_FILE.unlink()
            return {'locked': False}

    def apply_lockout(self, attempts: int) -> Dict:
        """
        Apply lockout after max attempts exceeded

        Args:
            attempts: Number of failed attempts

        Returns:
            Dict with lockout details
        """
        lockout_until = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)

        lockout_data = {
            'lockout_until': lockout_until.isoformat(),
            'reason': f'Maximum PIN attempts ({attempts}) exceeded',
            'locked_at': datetime.now().isoformat()
        }

        with open(LOCKOUT_FILE, 'w') as f:
            json.dump(lockout_data, f, indent=2)

        # Make sure file is readable only by owner
        os.chmod(LOCKOUT_FILE, 0o600)

        return {
            'locked': True,
            'lockout_until': lockout_until.isoformat(),
            'minutes': LOCKOUT_DURATION_MINUTES
        }

    def clear_lockout(self):
        """Manually clear lockout (admin function)"""
        if LOCKOUT_FILE.exists():
            LOCKOUT_FILE.unlink()


def generate_pin_hash(pin: str) -> str:
    """
    Generate SHA-256 hash for a PIN

    Usage:
        hash = generate_pin_hash("0213")
        print(f"export ATM_PIN_HASH='{hash}'")
    """
    return hashlib.sha256(pin.encode()).hexdigest()


if __name__ == '__main__':
    # Test/setup mode
    import sys

    if len(sys.argv) > 1:
        pin = sys.argv[1]
        pin_hash = generate_pin_hash(pin)
        print(f"\nGenerated PIN hash for: {pin}")
        print(f"\nAdd this to ~/.bashrc:")
        print(f"export ATM_PIN_HASH='{pin_hash}'")
        print(f"\nThen restart your shell or run:")
        print(f"source ~/.bashrc")
    else:
        print("Usage: python pin_auth.py <PIN>")
        print("Example: python pin_auth.py 0213")
