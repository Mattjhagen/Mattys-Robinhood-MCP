# 🎯 P3 ATM Trading Setup - Complete Guide

## ✅ What You Have Now (Option C Complete)

### Auto-Start Service Installed
- **Status**: ✅ Installed and running
- **URL**: http://localhost:5050 or http://100.103.3.35:5050
- **Auto-starts**: On every reboot
- **Current Mode**: READ-ONLY (via MCP)

**Service Commands:**
```bash
sudo systemctl status p3-atm     # Check status
sudo systemctl restart p3-atm    # Restart
sudo systemctl stop p3-atm       # Stop
sudo journalctl -u p3-atm -f     # Live logs
```

## 🔐 Trading API Setup (Option B)

You now have TWO ways to get trading capability:

### Path 1: Wait for Gold Card (Easiest)
- **Status**: On waitlist
- **When approved**: Trading automatically works via MCP
- **Effort**: Zero - just wait for email
- **Benefits**: Full agentic trading + automated strategies

### Path 2: Direct Trading API (Available Now)
- **Status**: Keys needed
- **Effort**: Get PEM keys, test, deploy
- **Benefits**: Trade immediately, no waiting

---

## 🚀 Quick Start: Enable Trading Now (Path 2)

### Step 1: Get Your PEM Keys

**⚠️ Important:** The Trading API key process is not publicly documented. Here's what to do:

**Method A: In-App Support (Recommended)**
1. Open Robinhood mobile app
2. Go to: Settings → Help → Contact Us
3. Send message:
```
Hi, I need Trading API access for my account.

Account: 311223129172
Current access: Agent/MCP API (read-only)
Need: PEM-format Trading API keys for direct trading
Purpose: Personal trading automation via Python

How do I get Trading API keys?
```

**Method B: Email Support**
Email: support@robinhood.com
```
Subject: Request Trading API Access

Hi Robinhood Support,

I'm trying to set up direct trading access via your Trading API.

Account number: 311223129172
Current API access: Agent/MCP API (read-only via rh-api-UUID keys)

I need PEM-format Trading API keys to enable trading operations.
The documentation at docs.robinhood.com/crypto/trading references
this authentication method but doesn't explain how to obtain keys.

Can you help me get Trading API access?

Use case: Personal trading automation and portfolio management

Thanks!
```

**Method C: Check Your Account**
Some users report finding API keys in:
- Robinhood website → Account Settings → API
- Settings → Security → API Access
- Settings → Developer → API Keys

If you don't see these options, you'll need to request access via support.

### Step 2: Install Your Keys

Once you have the PEM file:

```bash
# Create secure directory
mkdir -p ~/.robinhood
chmod 700 ~/.robinhood

# Copy your PEM file
# (Replace /path/to/downloaded.pem with actual path)
cp /path/to/downloaded.pem ~/.robinhood/trading_key.pem
chmod 600 ~/.robinhood/trading_key.pem

# Add to ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# Robinhood Trading API
export ROBINHOOD_API_KEY="rh-api-your-key-here"
export ROBINHOOD_PRIVATE_KEY_PATH="$HOME/.robinhood/trading_key.pem"
EOF

# Reload environment
source ~/.bashrc
```

### Step 3: Test Trading API

```bash
cd ~/Mattys-Robinhood-MCP/p3_atm
python3 trading_api.py
```

**Expected output:**
```
✅ Trading API initialized with PEM key
🔐 Robinhood Trading API Test
============================================================
Authenticated: True

📊 Testing Account Access:
  Account Number: 311223129172
  Buying Power: $0.26

💰 Testing Buying Power:
  Available: $0.26

📜 Testing Order History:
  Found X recent orders

✅ API test complete
```

### Step 4: Enable Trading in ATM

The ATM will automatically detect Trading API when keys are present:

```python
# robinhood_api.py will use:
# - trading_api.py for WRITE operations (buy/sell)
# - mcp_bridge.py for READ operations (quotes, balances)
```

Restart the service:
```bash
sudo systemctl restart p3-atm
```

---

## 📊 Current Status Check

Run these to verify your setup:

```bash
# Check MCP (read-only) works
echo $ROBINHOOD_API_KEY
echo $ROBINHOOD_PRIVATE_KEY

# Check Trading API setup
echo $ROBINHOOD_PRIVATE_KEY_PATH
ls -la ~/.robinhood/trading_key.pem

# Test MCP bridge
cd ~/Mattys-Robinhood-MCP/p3_atm
python3 mcp_bridge.py

# Test Trading API (once keys are set up)
python3 trading_api.py

# Check ATM service
sudo systemctl status p3-atm
curl http://localhost:5050/health
```

---

## 🎮 Using the ATM

### Read-Only Operations (Working Now)
- ✅ View balance: Shows your $0.26
- ✅ Check positions: 1 ADA + small ETH
- ✅ Get quotes: Live BTC/ETH prices
- ✅ Order history: View past trades

### Trading Operations (After PEM Keys)
- 🔒 Buy crypto: Enter symbol + amount
- 🔒 Sell crypto: Enter symbol + quantity
- 🔒 Quick trades: $5, $10, $25, $50 buttons
- 🔒 Order tracking: Real-time status

---

## 🔒 Security Checklist

Before trading with real money:

- [ ] PEM key file is chmod 600
- [ ] PEM key is NOT in git (check .gitignore)
- [ ] 2FA enabled on Robinhood account
- [ ] Tested with small amounts first ($1-5)
- [ ] Understand order types (market vs limit)
- [ ] Set up trading limits in Robinhood settings
- [ ] ATM is only accessible on your local network

---

## 🐛 Troubleshooting

### "Trading API not authenticated"
```bash
# Verify keys are loaded
env | grep ROBINHOOD

# Check PEM file exists and is readable
cat ~/.robinhood/trading_key.pem | head -1
# Should show: -----BEGIN PRIVATE KEY-----

# Reload environment
source ~/.bashrc
```

### "401 Unauthorized" from API
- PEM key might be for wrong account
- API key might be expired
- Check key format is correct (full PEM block)

### ATM shows mock data
- MCP bridge not started: Check `python3 mcp_bridge.py`
- API keys not loaded: Run `source ~/.bashrc`
- npm package not installed: Run `npm install -g robinhood-mcp`

### Service won't start
```bash
# Check detailed logs
sudo journalctl -u p3-atm -n 100

# Check port availability
lsof -i:5050

# Restart service
sudo systemctl restart p3-atm
```

---

## 📈 Next Steps

### Immediate (Both Paths)
1. ✅ Auto-start service is installed
2. ✅ Read-only monitoring works
3. ✅ Documentation complete

### Path 1: Gold Card (Wait)
1. Check email for invitation
2. Apply when you receive it
3. Trading automatically enables

### Path 2: Trading API (Now)
1. Get PEM keys (see Step 1 above)
2. Install keys (see Step 2 above)
3. Test API (see Step 3 above)
4. Restart ATM service
5. Start with $1 test trades
6. Scale up once comfortable

---

## 📚 Reference Files

- `GET_TRADING_API_KEYS.md` - Detailed key setup guide
- `trading_api.py` - Direct Trading API client
- `mcp_bridge.py` - Read-only MCP client
- `robinhood_api.py` - Main API interface (auto-detects mode)
- `SERVICE_SETUP.md` - Service management guide
- `README.md` - Project overview

---

## ⚠️ Important Reminders

1. **Start small**: Test with $1-5 trades first
2. **No mock mode**: This needs real keys to function
3. **Network only**: ATM is not exposed to internet
4. **Reboot safe**: Service starts automatically
5. **Dual mode**: Read via MCP, write via Trading API (when available)

---

## 🎉 You're All Set!

Your ATM is:
- ✅ Auto-starting on boot
- ✅ Showing real account data
- ✅ Ready for trading (once keys are added)

**Current balance**: $0.26  
**Current holdings**: 1 ADA + small ETH amount  
**Trading status**: Pending PEM keys OR Gold Card approval

Choose whichever path gets you trading first! 🚀
