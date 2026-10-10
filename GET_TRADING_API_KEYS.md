# Getting Robinhood Trading API Keys (PEM Format)

## What You Need

The Trading API requires **PEM-format keys**, which are different from the agent API keys you currently have.

Your current keys:
- `ROBINHOOD_API_KEY` - Format: `rh-api-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- `ROBINHOOD_PRIVATE_KEY` - Agent private key

Trading API keys:
- `ROBINHOOD_API_KEY` - Still the same rh-api-UUID format
- `ROBINHOOD_PRIVATE_KEY` - **PEM format** (starts with `-----BEGIN PRIVATE KEY-----`)

## How to Get Trading API Keys

**⚠️ Reality Check:** The Trading API key process is not publicly documented. Here are your actual options:

### Option 1: Contact Robinhood Support (Most Likely Path)

The keys you have now (rh-api-UUID format) are for the **Agent/MCP API** (read-only). For trading, you need different keys.

**Contact Robinhood:**
- **Method 1**: In-app support chat
  - Open Robinhood app → Settings → Help → Contact Us
  - Ask: "How do I get Trading API keys for direct API access?"
  
- **Method 2**: Email support
  - Email: support@robinhood.com
  - Subject: "Request Trading API Access"
  - Include:
    - Your account number: 311223129172
    - Current API key type: Agent/MCP API
    - Request: PEM-format Trading API keys
    - Use case: Personal trading automation

### Option 2: Wait for Gold Card (Easiest)

You're already on the waitlist. When approved:
- ✅ Full trading access through MCP
- ✅ No additional API keys needed
- ✅ Works with your existing setup
- ✅ Automated strategies supported

**This is the path Robinhood actually wants you to use.**

### Option 3: Check Crypto Trading API Docs

Robinhood has documented their **Crypto Trading API** at:
- https://docs.robinhood.com/crypto/trading

However, the docs don't clearly explain how to get initial access or generate keys. You may need to:
1. Already have a Robinhood Crypto account
2. Request access through support
3. Receive keys through an onboarding process

### What We Know For Sure

**Agent/MCP API** (what you have now):
- Format: `rh-api-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Access: Read-only
- Use: Portfolio monitoring, quotes, positions
- Works with: `robinhood-mcp` npm package

**Trading API** (what you need):
- Format: Same API key ID + PEM private key
- Private key starts with: `-----BEGIN PRIVATE KEY-----`
- Access: Full read/write trading
- Use: Place orders, buy/sell, manage positions
- Requires: Authentication via HMAC-SHA256 signatures

**Gold Card / Agentic Trading** (on waitlist):
- Access: Full trading through agent MCP
- Keys: Your existing agent keys work
- Benefit: Automated strategies, no manual signing

## Setting Up PEM Keys

Once you have the PEM-format private key:

### Step 1: Save the Private Key

```bash
# Create secure directory
mkdir -p ~/.robinhood
chmod 700 ~/.robinhood

# Save your PEM key (paste when prompted)
cat > ~/.robinhood/trading_key.pem
# Paste your key here (starts with -----BEGIN PRIVATE KEY-----)
# Press Ctrl+D when done

# Secure the file
chmod 600 ~/.robinhood/trading_key.pem
```

### Step 2: Update Environment Variables

Add to `~/.bashrc`:

```bash
# Robinhood Trading API (PEM format)
export ROBINHOOD_API_KEY="rh-api-your-uuid-here"
export ROBINHOOD_PRIVATE_KEY_PATH="$HOME/.robinhood/trading_key.pem"
```

Then reload:
```bash
source ~/.bashrc
```

### Step 3: Update ATM to Use Trading API

The `robinhood_api.py` file will need modification to:
1. Read the PEM key from file
2. Use HMAC-SHA256 signing for requests
3. Add proper authentication headers

## Verification

Test your keys work:

```python
import requests
import hmac
import hashlib
import base64
import time

api_key = "your-rh-api-key"
with open("~/.robinhood/trading_key.pem") as f:
    private_key = f.read()

# Test request
timestamp = int(time.time() * 1000)
method = "GET"
path = "/api/v1/account"
message = f"{timestamp}{method}{path}"

signature = base64.b64encode(
    hmac.new(
        private_key.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
).decode()

headers = {
    'x-api-key': api_key,
    'x-timestamp': str(timestamp),
    'x-signature': signature
}

response = requests.get(f"https://api.robinhood.com{path}", headers=headers)
print(response.status_code, response.json())
```

## Current Limitations

Without PEM keys, your ATM can only:
- ✅ View account data (read-only via MCP)
- ✅ Show balances and positions
- ✅ Get live quotes

With PEM keys, you'll be able to:
- ✅ Place market/limit orders
- ✅ Buy/sell crypto and stocks
- ✅ Manage orders
- ✅ Full trading automation

## Security Notes

⚠️ **IMPORTANT**:

1. **Never commit PEM keys to git** - They're in `.gitignore`
2. **File permissions matter** - Must be 600 (owner read/write only)
3. **Keep keys secure** - They have full trading access to your account
4. **Use test amounts first** - Start with small trades ($1-5) to verify
5. **Set up 2FA** - Enable two-factor authentication on your Robinhood account

## Next Steps

1. Obtain PEM-format Trading API keys
2. Securely store them as shown above
3. Update `robinhood_api.py` to use direct API authentication
4. Test with small amounts
5. Enable full trading in the ATM

---

**Note**: This process is separate from the Gold Card waitlist. You can pursue both paths - whichever comes first will enable trading.
