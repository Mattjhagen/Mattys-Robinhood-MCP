# 🔑 Get Your Trading API Keys RIGHT NOW!

## ✅ You Can Do This Yourself (No Waiting!)

Robinhood lets you generate Crypto Trading API keys directly from their website!

---

## 📋 Step-by-Step Instructions:

### Step 1: Sign In to Robinhood Web (Classic)

**Go to**: https://robinhood.com/login

**Important:** Use "web classic" mode (not the new web interface)

### Step 2: Navigate to Crypto Account Settings

1. Click your **profile icon** (top right)
2. Go to **Settings**
3. Select **Crypto** or **API Settings**
4. Look for **"API Keys"** or **"Developer"** section

### Step 3: Add New API Key

Click **"Add key"** or **"Create API Key"**

You'll need to choose which permissions to enable:

**Select These Permissions:**
- ✅ Read crypto accounts
- ✅ Read crypto holdings
- ✅ Read crypto orders
- ✅ Read crypto products
- ✅ Read crypto quotes
- ✅ **Place crypto orders with fee tiers** (v2 - RECOMMENDED)
  - OR: Place crypto orders without fee tiers (v1)

### Step 4: Choose API Version

**Recommended: v2 API**
- Supports fee-tier trading
- Your trades count toward fee tier eligibility
- Better rates for high volume

**Alternative: v1 API**
- No fee tiers
- Simpler but higher fees
- Still works fine for testing

### Step 5: Download Your Keys

After creating the key, you'll get:

1. **API Key ID** - Format: `rh-api-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
2. **Private Key** - PEM format starting with `-----BEGIN PRIVATE KEY-----`

**⚠️ SAVE THESE IMMEDIATELY! You can only download the private key ONCE!**

---

## 💾 Install Your Keys (Once You Have Them):

### Step 1: Save the Private Key

```bash
# Create secure directory
mkdir -p ~/.robinhood
chmod 700 ~/.robinhood

# Save your private key
# (Copy and paste the ENTIRE key including BEGIN/END lines)
nano ~/.robinhood/trading_key.pem
# Paste your key, then Ctrl+X, Y, Enter

# Secure the file
chmod 600 ~/.robinhood/trading_key.pem
```

### Step 2: Update Environment Variables

```bash
# Add to ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# Robinhood Crypto Trading API
export ROBINHOOD_API_KEY="rh-api-your-actual-key-here"
export ROBINHOOD_PRIVATE_KEY_PATH="$HOME/.robinhood/trading_key.pem"
EOF

# Reload environment
source ~/.bashrc
```

### Step 3: Test Your Keys

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

✅ API test complete
```

### Step 4: Enable Automated Trading

```bash
# Run one cycle manually to test
cd ~/Mattys-Robinhood-MCP
./run_trading_loop.sh

# Should now show "Status: active" instead of "monitoring_only"
```

---

## 🔧 Troubleshooting:

### "I don't see API Keys in settings"

Try these locations:
- Settings → Security → API Access
- Settings → Crypto → API Keys
- Settings → Developer → API Settings
- Account → API Management

If still not visible:
- Make sure you have a **verified crypto account**
- You must be a **US customer**
- Try logging out and back in

### "Cannot create API key"

You may need to:
- Verify your identity
- Enable 2FA (two-factor authentication)
- Complete crypto account setup
- Wait 24 hours after opening account

### "Key created but where's the PEM file?"

The private key is shown **once** on screen after creation.

**Format should look like:**
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
(many lines of base64 text)
...
-----END PRIVATE KEY-----
```

**If you missed it:** Delete the key and create a new one.

---

## 🎯 Once Keys Are Working:

Your automated trading bot will:
- ✅ Run every 15 minutes automatically
- ✅ Place real trades
- ✅ Rebalance portfolio
- ✅ Take profits at 10%
- ✅ Cut losses at 5%
- ✅ Log everything to `/tmp/trading_loop.log`

Check status:
```bash
tail -f /tmp/trading_loop.log
# Should show "Status: active" instead of "monitoring_only"
```

---

## 📚 API Documentation:

**Full technical docs:** https://docs.robinhood.com/crypto/trading/

---

## ⚡ Quick Checklist:

- [ ] Sign in to Robinhood web (classic)
- [ ] Go to Settings → Crypto/API
- [ ] Click "Add key"
- [ ] Select permissions (include "Place crypto orders")
- [ ] Choose v2 API (recommended)
- [ ] Download and save private key IMMEDIATELY
- [ ] Save to `~/.robinhood/trading_key.pem`
- [ ] Add API key to `~/.bashrc`
- [ ] Run `source ~/.bashrc`
- [ ] Test with `python3 p3_atm/trading_api.py`
- [ ] Run `./run_trading_loop.sh`
- [ ] Verify shows "Status: active" ✅

---

## 🎉 You're About to Be Live!

Once you add those keys, your bot goes from "monitoring_only" to **FULLY AUTOMATED TRADING**!

Go generate your keys now! 🚀
