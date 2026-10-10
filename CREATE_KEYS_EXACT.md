# 🔑 Create Robinhood API Keys - EXACT STEPS

## Based on Official Robinhood Documentation

Source: https://robinhood.com/us/en/support/articles/crypto-api/

---

## 📋 Prerequisites:

- ✅ Robinhood Crypto account (US customers only)
- ✅ Verified identity
- ✅ 2FA enabled (recommended)
- ✅ Desktop/laptop (not mobile app)

---

## 🎯 EXACT STEPS:

### Step 1: Sign In to Robinhood Web (Classic)

**URL**: https://robinhood.com/login

**Important**: Use the **web classic** interface (not the new beta interface)

If you land on the new interface, look for:
- "Switch to classic" link
- Or use: https://robinhood.com/account/crypto

---

### Step 2: Navigate to Crypto Account Settings

From the main page:

1. **Click** your **profile icon** or **account menu** (top right corner)
2. **Select** "Settings" or "Account Settings"
3. **Click** "Crypto" or "Cryptocurrency"
4. **Look for** "API" or "API Keys" section

**Alternative paths** (if above doesn't work):
- Account → Crypto → API Keys
- Settings → Security → API Access
- Settings → Developer → API Management

---

### Step 3: Create New API Key

**Click**: "Add key" button

You'll see a form asking for:

#### 3a. Key Name (Optional)
- Example: "Trading Bot" or "ATM API"
- Just for your reference

#### 3b. Select API Actions/Permissions

**Check these boxes:**

**Read Permissions** (all of these):
- ☑️ Read crypto accounts
- ☑️ Read crypto holdings
- ☑️ Read crypto orders
- ☑️ Read crypto products  
- ☑️ Read crypto quotes

**Write Permissions** (choose ONE):
- ☑️ **Place crypto orders with fee tiers** (v2) ← RECOMMENDED
  - Better rates for volume traders
  - Your trades count toward fee tier eligibility
  
- OR: Place crypto orders without fee tiers (v1)
  - Simpler but higher fees
  - Good for low-volume trading

#### 3c. Confirm and Generate

- Review your selections
- **Click** "Generate" or "Create Key"
- May need to verify with 2FA code

---

### Step 4: SAVE YOUR KEYS IMMEDIATELY!

⚠️ **CRITICAL**: The private key is shown **ONLY ONCE**!

You'll see two pieces of information:

#### API Key ID:
```
rh-api-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

#### Private Key (PEM format):
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
(many lines of base64-encoded text)
...
-----END PRIVATE KEY-----
```

**COPY BOTH** to a secure location immediately!

**Options to save**:
1. Download the file if a download button is provided
2. Copy-paste into a text editor
3. Take a screenshot (but delete after copying)

---

## 💾 INSTALL KEYS ON YOUR SERVER:

Once you have copied both keys, SSH to your r510 server and run:

```bash
# Create secure directory
mkdir -p ~/.robinhood
chmod 700 ~/.robinhood

# Create the private key file
nano ~/.robinhood/trading_key.pem
```

**In nano editor**:
1. Paste the ENTIRE private key (including BEGIN/END lines)
2. Press `Ctrl+X`
3. Press `Y` to confirm
4. Press `Enter` to save

```bash
# Secure the file (IMPORTANT!)
chmod 600 ~/.robinhood/trading_key.pem

# Verify it looks correct
head -1 ~/.robinhood/trading_key.pem
# Should show: -----BEGIN PRIVATE KEY-----

# Add to environment
cat >> ~/.bashrc << 'EOF'

# Robinhood Crypto Trading API
export ROBINHOOD_API_KEY="rh-api-paste-your-key-id-here"
export ROBINHOOD_PRIVATE_KEY_PATH="$HOME/.robinhood/trading_key.pem"
EOF

# Edit to add your actual API key ID
nano ~/.bashrc
# Find the ROBINHOOD_API_KEY line and replace with your actual key
# Save: Ctrl+X, Y, Enter

# Load new environment
source ~/.bashrc
```

---

## ✅ TEST YOUR KEYS:

```bash
# Verify environment variables are set
echo $ROBINHOOD_API_KEY
echo $ROBINHOOD_PRIVATE_KEY_PATH

# Test the API
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

---

## 🚀 ENABLE AUTO-TRADING:

```bash
cd ~/Mattys-Robinhood-MCP
./run_trading_loop.sh
```

**Expected output:**
```
🤖 Agentic Trading Bot
============================================================
Status: active  ← (NOT "monitoring_only"!)
Portfolio Value: $0.26
Buying Power: $0.00
```

---

## 🔧 TROUBLESHOOTING:

### "Can't find API Keys section"

Try these direct URLs:
- https://robinhood.com/account/crypto
- https://robinhood.com/account/settings
- https://robinhood.com/crypto/settings

Or contact support:
- In app: Settings → Help → Contact Us
- Ask: "Where do I find API key settings?"

### "No 'Add key' button"

Possible reasons:
- Account not verified
- Crypto not enabled
- Not a US customer
- Try different browser (Chrome/Firefox)
- Clear cache and try again

### "Private key doesn't look right"

Correct format:
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAo...
(20-30 lines of letters/numbers/symbols)
...
-----END PRIVATE KEY-----
```

Wrong format:
- Just random text
- Missing BEGIN/END lines
- HTML code mixed in

### "Authentication failed"

```bash
# Check file permissions
ls -la ~/.robinhood/trading_key.pem
# Should show: -rw------- (600)

# Check file contents
cat ~/.robinhood/trading_key.pem | head -1
# Should show: -----BEGIN PRIVATE KEY-----

# Verify environment
env | grep ROBINHOOD

# Test connection
curl -H "x-api-key: $ROBINHOOD_API_KEY" \
     https://api.robinhood.com/api/v2/crypto/accounts/
```

---

## 📱 MOBILE APP ALTERNATIVE:

If you can't find it on web, try:

1. Open Robinhood mobile app
2. Tap profile icon
3. Settings → Crypto
4. Look for "API Access" or "Developer"

(But web is usually easier)

---

## 📚 OFFICIAL RESOURCES:

- **Support Article**: https://robinhood.com/us/en/support/articles/crypto-api/
- **API Documentation**: https://docs.robinhood.com/crypto/trading/
- **Help Center**: https://robinhood.com/support

---

## ⚠️ SECURITY REMINDERS:

1. ✅ Never share your private key
2. ✅ Keep file permissions at 600
3. ✅ Don't commit keys to git
4. ✅ Enable 2FA on your account
5. ✅ Review API key permissions regularly
6. ✅ Rotate keys if compromised

---

## 🎉 Once Done:

Your automated trading bot will:
- Trade every 15 minutes
- Manage risk automatically
- Take profits/cut losses
- Log everything

Check status:
```bash
tail -f /tmp/trading_loop.log
```

---

**Need help?** Let me know which step you're stuck on!
