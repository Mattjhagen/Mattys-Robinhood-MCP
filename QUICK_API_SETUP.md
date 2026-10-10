# 🚀 Quick API Key Setup

You have 2 options to add your keys:

## Option A: Interactive Script (Recommended)

```bash
cd ~/Mattys-Robinhood-MCP
./setup_api_keys.sh
```

The script will:
- ✅ Check for existing keys
- ✅ Prompt you to paste your keys securely
- ✅ Add them to ~/.bashrc
- ✅ Load them immediately
- ✅ Verify they're working

---

## Option B: Manual Edit

1. **Edit your .bashrc:**
   ```bash
   nano ~/.bashrc
   ```

2. **Add these lines at the end** (replace with your actual keys):
   ```bash
   # Robinhood API Keys
   export ROBINHOOD_API_KEY="paste_your_api_key_here"
   export ROBINHOOD_PRIVATE_KEY="paste_your_private_key_here"
   ```

3. **Save and load:**
   ```bash
   # Save: Ctrl+O, Enter, Ctrl+X
   source ~/.bashrc
   ```

4. **Verify:**
   ```bash
   echo "API Key: ${#ROBINHOOD_API_KEY} characters"
   echo "Private Key: ${#ROBINHOOD_PRIVATE_KEY} characters"
   ```

---

## After Adding Keys

**Start the live ATM server:**
```bash
cd ~/Mattys-Robinhood-MCP/p3_atm
./start_atm_live.sh
```

**Access your real account:**
- 🌐 Web: http://localhost:5050
- 🔑 PIN: 0213
- 💰 Shows your ACTUAL balance!

---

## Verify It's Working

```bash
# Quick test
cd ~/Mattys-Robinhood-MCP/p3_atm
python3 << 'EOF'
from robinhood_api import get_robinhood_api
api = get_robinhood_api()
print('Mode:', 'LIVE ✅' if api.is_live() else 'MOCK ⚠️')
EOF
```

Should show: `Mode: LIVE ✅`

---

## Security Reminder 🔐

- ✅ Keys are in ~/.bashrc (private file)
- ✅ .env files are gitignored
- ⚠️ NEVER commit keys to git
- ⚠️ NEVER share your private key
