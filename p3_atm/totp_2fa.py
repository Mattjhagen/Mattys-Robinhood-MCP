#!/usr/bin/env python3
"""
TOTP 2FA Module for Robinhood ATM
Implements Time-based One-Time Password authentication
"""

import pyotp
import qrcode
import io
import base64
import json
from pathlib import Path

class TOTP2FA:
    """Handle TOTP-based 2FA for ATM transactions"""

    def __init__(self, secret_file=None):
        if secret_file is None:
            secret_file = Path.home() / ".atm-2fa-secret.json"
        self.secret_file = Path(secret_file)
        self.issuer_name = "Robinhood ATM"
        self.account_name = "Trading Terminal"

    def get_or_create_secret(self):
        """Get existing secret or create new one"""
        if self.secret_file.exists():
            with open(self.secret_file, 'r') as f:
                data = json.load(f)
                return data.get('secret')
        else:
            # Generate new secret
            secret = pyotp.random_base32()
            self._save_secret(secret)
            return secret

    def _save_secret(self, secret):
        """Save secret to file"""
        with open(self.secret_file, 'w') as f:
            json.dump({'secret': secret}, f)
        # Set restrictive permissions
        self.secret_file.chmod(0o600)

    def generate_qr_code(self):
        """Generate QR code for authenticator app setup"""
        secret = self.get_or_create_secret()
        totp = pyotp.TOTP(secret)

        # Generate provisioning URI
        uri = totp.provisioning_uri(
            name=self.account_name,
            issuer_name=self.issuer_name
        )

        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)

        # Convert to base64 image
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()

        return {
            'qr_code_base64': img_base64,
            'secret': secret,
            'uri': uri
        }

    def verify_code(self, code):
        """Verify a TOTP code"""
        secret = self.get_or_create_secret()
        totp = pyotp.TOTP(secret)

        # Verify with 1 period tolerance (30 seconds before/after)
        return totp.verify(code, valid_window=1)

    def get_current_code(self):
        """Get current valid code (for testing only)"""
        secret = self.get_or_create_secret()
        totp = pyotp.TOTP(secret)
        return totp.now()

    def reset_secret(self):
        """Delete secret and force regeneration"""
        if self.secret_file.exists():
            self.secret_file.unlink()


# Singleton instance
_totp_instance = None

def get_totp_2fa():
    """Get or create TOTP 2FA singleton"""
    global _totp_instance
    if _totp_instance is None:
        _totp_instance = TOTP2FA()
    return _totp_instance


if __name__ == '__main__':
    # Test the 2FA system
    print("🔐 TOTP 2FA Test")
    print("=" * 60)

    totp = get_totp_2fa()

    # Generate QR code
    qr_data = totp.generate_qr_code()
    print(f"Secret: {qr_data['secret']}")
    print(f"URI: {qr_data['uri']}")
    print()

    # Get current code
    current_code = totp.get_current_code()
    print(f"Current code: {current_code}")
    print()

    # Test verification
    if totp.verify_code(current_code):
        print("✅ Code verification: PASS")
    else:
        print("❌ Code verification: FAIL")

    # Test invalid code
    if totp.verify_code("000000"):
        print("❌ Invalid code test: FAIL (should reject)")
    else:
        print("✅ Invalid code test: PASS (correctly rejected)")
