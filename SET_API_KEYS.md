# 🔐 How to Set Your Robinhood API Keys

Your ATM is currently running in **MOCK MODE** with demo data.

To connect your **real Robinhood account**, you need to set your API credentials as environment variables.

---

## Quick Setup (Temporary - This Session Only)

```bash
# Set your keys (replace with your actual keys)
export ROBINHOOD_API_KEY="your_actual_api_key_here"
export ROBINHOOD_PRIVATE_KEY="your_actual_private_key_here"

# Restart the ATM server
cd ~/Mattys-Robinhood-MCP/p3_atm
pkill -f atm_server
python3 atm_server.py &

# Test it's working
curl http://localhost:5050/health
```

---

## Permanent Setup (Survives Reboots)

Add the keys to your shell profile so they load automatically:

```bash
# Edit your shell profile
nano ~/.bashrc

# Add these lines at the end:
export ROBINHOOD_API_KEY="your_actual_api_key_here"
export ROBINHOOD_PRIVATE_KEY="your_actual_private_key_here"

# Save (Ctrl+O, Enter, Ctrl+X)

# Reload your profile
source ~/.bashrc

# Restart the server
cd ~/Mattys-Robinhood-MCP/p3_atm
pkill -f atm_server
python3 atm_server.py &
```

---

## Where to Get Your API Keys

1. Visit: https://robinhood.com/us/en/support/articles/trading-api/
2. Sign in to your Robinhood account
3. Go to **Settings → API & Trading**
4. Click **Generate API Credentials**
5. Copy:
   - **API Key** (public key)
   - **Private Key** (keep this secret!)

---

## Check If Keys Are Set

```bash
# This will show the length if set, or error if not
echo "API Key: ${#ROBINHOOD_API_KEY} characters"
echo "Private Key: ${#ROBINHOOD_PRIVATE_KEY} characters"
```

---

## Test If Live Mode Is Active

```bash
cd ~/Mattys-Robinhood-MCP/p3_atm
python3 robinhood_api.py
```

You should see:
- ✅ `Mode: LIVE` if keys are working
- ⚠️ `Mode: MOCK` if keys are not set

---

## Security Notes ⚠️

1. **Never commit your keys to git!** (They're in .gitignore)
2. **Never share your private key** with anyone
3. Your keys are stored in your shell environment, not in files
4. The ATM server reads them on startup from `os.getenv()`

---

## What Changes When You Go Live?

### **MOCK MODE (Current):**
- ❌ Fake demo balances ($10,214.48)
- ❌ Sample accounts (crypto, individual, Roth IRA)
- ✅ All UI features work
- ✅ Safe for testing

### **LIVE MODE (After Setting Keys):**
- ✅ **Real account balances**
- ✅ **Real buying power**
- ✅ **Actual trade execution**
- ⚠️ **Real money at risk!**

---

## Need Help?

If you get errors:
1. Check the log: `tail -f /tmp/atm.log`
2. Verify keys are set: `echo $ROBINHOOD_API_KEY`
3. Test API: `python3 robinhood_api.py`
4. Restart server: `pkill -f atm_server && python3 atm_server.py &`

---

## Ready to Go Live?

Once you've set your keys and restarted the server:

1. Open http://localhost:5050
2. Enter your PIN: **0213**
3. You'll see your **REAL balance** on the ATM receipt screen!

🎉 Your Robinhood ATM is now connected to your actual account!
