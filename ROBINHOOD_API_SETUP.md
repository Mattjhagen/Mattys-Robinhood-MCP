# 🏦 Robinhood API Integration Setup

Your ATM now supports **real Robinhood trading** via their official API!

## ✅ What's Integrated

### **Real-Time Features:**
- ✅ Live cryptocurrency prices (BTC, ETH, DOGE, SOL, ADA, MATIC)
- ✅ Real-time portfolio balances
- ✅ Actual position data
- ✅ Live order execution
- ✅ Trading history

### **Trading Features:**
- ✅ Market buy orders (USD amount)
- ✅ Market sell orders (crypto quantity)
- ✅ Order status tracking
- ✅ Real-time quotes

### **Keyboard Navigation:**
- ✅ Full keyboard support - **NO MOUSE NEEDED!**
- ✅ Number keys for PIN entry
- ✅ Shortcuts for all actions (B=Buy, S=Sell, P=Positions)
- ✅ Press **H** for help overlay

---

## 🔐 Get Robinhood API Credentials

### Step 1: Create API Keys

1. **Visit:** https://robinhood.com/us/en/support/articles/trading-api/
2. **Sign in** to your Robinhood account
3. **Navigate to:** Settings → API & Trading
4. **Generate** new API credentials
5. **Save** these values:
   - API Key
   - Private Key (PEM format)

### Step 2: Set Environment Variables

**On R510 Server:**

```bash
# Edit your shell profile
nano ~/.bashrc

# Add these lines at the end:
export ROBINHOOD_API_KEY="your_api_key_here"
export ROBINHOOD_PRIVATE_KEY="your_private_key_here"

# Save and reload
source ~/.bashrc
```

### Step 3: Restart ATM Service

```bash
sudo systemctl restart p3-atm-web
```

---

## 📡 API Endpoints

### **Account**
- `GET /api/balance` - Get account balance
- `GET /api/portfolio` - Get full portfolio
- `GET /api/positions` - Get crypto positions

### **Market Data**
- `GET /api/quote/<symbol>` - Get real-time quote
- `GET /api/tickers` - Get multiple ticker prices

### **Trading**
- `POST /api/trade/buy` - Buy cryptocurrency
  ```json
  {
    "symbol": "BTC",
    "amount": 100.00
  }
  ```

- `POST /api/trade/sell` - Sell cryptocurrency
  ```json
  {
    "symbol": "BTC",
    "quantity": 0.001
  }
  ```

---

## ⌨️ Keyboard Shortcuts

**You don't need a mouse!** Full keyboard navigation:

### **Welcome Screen:**
- `ENTER` - Enter PIN screen

### **PIN Entry:**
- `0-9` - Enter digits
- `ENTER` - Submit PIN
- `BACKSPACE` - Delete digit
- `ESC` - Cancel

### **Home Screen:**
- `1` or `B` - Buy crypto
- `2` or `S` - Sell crypto
- `3` - View balance
- `4` or `P` - View positions
- `ESC` or `Q` - Exit/Logout

### **Trade Screen:**
- `B` - Switch to Buy tab
- `S` - Switch to Sell tab
- `ENTER` - Submit order
- `ESC` - Back to home

### **Any Screen:**
- `ESC` - Go back
- `H` - Show keyboard shortcuts
- `TAB` - Next field
- `SHIFT+TAB` - Previous field

**Keyboard hint in bottom-right corner** - Click or press H anytime!

---

## 🧪 Testing Modes

### **Mock Mode (Default)**
If no API credentials are set, the ATM runs in **MOCK MODE**:
- ✅ Full UI works
- ✅ All features functional
- ✅ Uses sample data
- ✅ Safe for testing
- ⚠️ No real trades execute

### **Live Mode**
Once you set `ROBINHOOD_API_KEY` and `ROBINHOOD_PRIVATE_KEY`:
- ✅ Real account data
- ✅ Live prices
- ✅ Actual trade execution
- ⚠️ **Real money!**

Check current mode:
```bash
cd /home/matt/Mattys-Robinhood-MCP/p3_atm
python3 robinhood_api.py
```

---

## 🔧 Configuration

### **API Settings**

Location: `/home/matt/Mattys-Robinhood-MCP/p3_atm/robinhood_api.py`

**Base URL:** `https://trading.robinhood.com`

**Authentication:** HMAC-SHA256 signature

**Supported Symbols:**
- BTC-USD (Bitcoin)
- ETH-USD (Ethereum)
- DOGE-USD (Dogecoin)
- SOL-USD (Solana)
- ADA-USD (Cardano)
- MATIC-USD (Polygon)

### **Server Settings**

Location: `/home/matt/Mattys-Robinhood-MCP/p3_atm/atm_server.py`

**PIN:** `0213` (change in code)
**Port:** `5050`
**Host:** `0.0.0.0` (accessible from network)

---

## 📊 Live Data Flow

```
┌─────────────┐
│   Robinhood │
│   ATM UI    │
└──────┬──────┘
       │
       │ User enters PIN
       ▼
┌──────────────┐
│  Flask API   │ ◄── Connects to
│  atm_server  │     robinhood_api.py
└──────┬───────┘
       │
       │ API Calls
       ▼
┌──────────────────┐
│  Robinhood API   │
│  trading.        │
│  robinhood.com   │
└──────────────────┘
       │
       │ Real-time data
       ▼
┌──────────────────┐
│  Your Account    │
│  Balances        │
│  Positions       │
│  Orders          │
└──────────────────┘
```

---

## 🚀 Quick Start

### **1. Test in Mock Mode (No Setup)**

```bash
# Just open in browser:
http://localhost:5050

# Or from network:
http://100.103.3.35:5050
```

**Works immediately with sample data!**

### **2. Enable Live Trading**

```bash
# Set credentials
export ROBINHOOD_API_KEY="your_key"
export ROBINHOOD_PRIVATE_KEY="your_private_key"

# Restart
sudo systemctl restart p3-atm-web

# Test
curl http://localhost:5050/api/balance
```

### **3. Use From Clover**

```bash
# On Clover device browser:
http://100.103.3.35:5050

# Full keyboard support - no touch needed!
```

---

## 🔍 Troubleshooting

### **API Key Issues:**

```bash
# Check if keys are set:
echo $ROBINHOOD_API_KEY
echo $ROBINHOOD_PRIVATE_KEY

# Test API connection:
cd /home/matt/Mattys-Robinhood-MCP/p3_atm
python3 robinhood_api.py
```

### **Service Not Starting:**

```bash
# Check logs:
sudo journalctl -u p3-atm-web -f

# Check if port is in use:
ss -tlnp | grep 5050

# Restart manually:
pkill -f atm_server
cd /home/matt/Mattys-Robinhood-MCP/p3_atm
python3 atm_server.py
```

### **Keyboard Not Working:**

- Press `F5` to reload page
- Try pressing `H` for shortcuts
- Check browser console (F12) for errors
- Make sure JavaScript is enabled

---

## 📚 Resources

**Official Docs:**
- https://docs.robinhood.com/crypto/trading/
- https://robinhood.com/us/en/support/articles/trading-api/

**Code Files:**
- `p3_atm/robinhood_api.py` - API client
- `p3_atm/atm_server.py` - Flask server
- `p3_atm/atm_templates/atm.html` - UI with keyboard support

**Help:**
- View logs: `sudo journalctl -u p3-atm-web -f`
- Check status: `sudo systemctl status p3-atm-web`
- Test API: `python3 p3_atm/robinhood_api.py`

---

## ⚠️ Security Notes

1. **Never commit** API keys to git
2. **Use environment variables** only
3. **Keep private key secure** (PEM file)
4. **Monitor trades** regularly
5. **Test in mock mode** first
6. **PIN protect** the ATM (already set to 0213)
7. **Network security** - restrict access if public

---

## ✅ You're Ready!

**Without API keys:**
- ✅ Full UI works
- ✅ Keyboard navigation
- ✅ Mock data for testing

**With API keys:**
- ✅ Real account balances
- ✅ Live cryptocurrency prices
- ✅ Actual trade execution
- ✅ Real-time portfolio

**Start using it:**
```bash
# Open browser:
http://localhost:5050

# Press H for keyboard shortcuts
# No mouse needed!
```

**🎉 Your Robinhood ATM is ready!**
