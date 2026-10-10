#!/usr/bin/env python3
"""
Generate Ed25519 Key Pair for Robinhood Crypto Trading API
Based on official Robinhood documentation
"""

import nacl.signing
import base64

print("🔑 Generating Robinhood API Key Pair")
print("=" * 60)
print()

# Generate an Ed25519 keypair
private_key = nacl.signing.SigningKey.generate()
public_key = private_key.verify_key

# Convert keys to base64 strings
private_key_base64 = base64.b64encode(private_key.encode()).decode()
public_key_base64 = base64.b64encode(public_key.encode()).decode()

# Print the keys
print("✅ Keys Generated Successfully!")
print()
print("=" * 60)
print("PRIVATE KEY (Base64) - KEEP THIS SECRET!")
print("=" * 60)
print(private_key_base64)
print()
print("=" * 60)
print("PUBLIC KEY (Base64) - Use this when creating API credential")
print("=" * 60)
print(public_key_base64)
print()
print("=" * 60)
print()
print("📝 NEXT STEPS:")
print()
print("1. COPY the PUBLIC KEY above")
print("2. Go to: Robinhood web → Crypto Settings → API Keys")
print("3. Click 'Add key' and PASTE the PUBLIC KEY")
print("4. Select permissions (include 'Place crypto orders with fee tiers')")
print("5. You'll receive an API KEY ID (rh-api-xxxxx)")
print("6. Save BOTH the API KEY ID and your PRIVATE KEY")
print()
print("⚠️  SECURITY:")
print("   - NEVER share your PRIVATE KEY")
print("   - Save it somewhere secure")
print("   - You'll need it to sign API requests")
print()
print("📚 Add to your ~/.bashrc:")
print(f'   export ROBINHOOD_API_KEY="rh-api-your-key-id-here"')
print(f'   export ROBINHOOD_PRIVATE_KEY_BASE64="{private_key_base64}"')
print()
