# 🏦 P3 ATM × Clover POS Integration

Professional ATM interface meets secure card reader hardware.

## What This Is

Your **P3 Lending ATM** (black/green Matrix theme, trading features, professional UI) now works with **Clover POS devices** (touchscreen + secure card reader).

## Quick Start (5 Minutes)

### Option 1: Test It Now (Browser Mode)

**Easiest way to see if it works:**

```bash
# 1. On r510, make server accessible:
cd /home/matt/Mattys-Robinhood-MCP/p3_atm
sed -i 's/127.0.0.1/0.0.0.0/' atm_server.py
sudo systemctl restart p3-atm-web

# 2. On Clover device:
# Open Chrome → http://100.103.3.35:5050
```

That's it! Your ATM now works on Clover's touchscreen.

---

### Option 2: Full Integration (Secure PIN Pad)

**Use Clover's physical keypad for PIN entry:**

```bash
cd /home/matt/Mattys-Robinhood-MCP/clover_integration
./install_clover_option2.sh
```

This enables:
- ✅ Secure PIN entry on physical keypad (not touchscreen)
- ✅ Card reader integration
- ✅ Encrypted PIN transmission
- ✅ PCI-DSS compliant authentication

---

## Files in This Directory

```
clover_integration/
├── README.md                         ← You are here
├── CLOVER_INTEGRATION_GUIDE.md       ← Complete documentation
├── atm_server_with_clover.py         ← Enhanced Flask server
├── clover_bridge.html                ← Web bridge for PIN pad
├── CloverATMActivity.java            ← Native Android app
├── install_clover_option2.sh         ← Automated installer
└── test_clover.sh                    ← Test connectivity
```

## Three Integration Levels

| Option | What It Does | Setup Time | Security |
|--------|-------------|------------|----------|
| **1. Browser** | Clover as display only | 2 minutes | Basic |
| **2. PIN Pad** | Secure keypad + cards | 15 minutes | PCI-compliant |
| **3. Native App** | Full hardware control | 2-4 hours | Bank-grade |

**Start with Option 1**, upgrade to Option 2 when ready for customers.

## Requirements

**Hardware:**
- ✅ Clover Mini, Flex, Station, or Mobile
- ✅ R510 server (already set up)
- ✅ Same network connectivity

**Software:**
- ✅ P3 ATM already installed
- ✅ Flask server already running
- For Option 2+: Clover merchant account

## Test Your Setup

```bash
cd /home/matt/Mattys-Robinhood-MCP/clover_integration
./test_clover.sh
```

This checks:
1. Server is accessible from network
2. API endpoints are responding
3. Clover integration is configured
4. Authentication endpoints work

## URLs to Know

**From r510:**
- Main ATM: http://localhost:5050
- Health check: http://localhost:5050/health
- Clover bridge: http://localhost:5050/clover

**From Clover device:**
- Main ATM: http://100.103.3.35:5050
- Clover bridge: http://100.103.3.35:5050/clover

## Clover Device Setup

### For All Options:

1. **Connect to network:**
   - Clover must reach 100.103.3.35:5050
   - Same network as r510 server

2. **Open browser on Clover:**
   - Built-in Chrome browser
   - Navigate to ATM URL

3. **Bookmark for easy access:**
   - Add to home screen
   - Launch in fullscreen

### For Option 2 (PIN Pad):

4. **Get Clover credentials:**
   - Log in to https://dashboard.clover.com
   - Navigate to API Tokens
   - Copy: Merchant ID, API Key, Encryption Key

5. **Run installer:**
   ```bash
   ./install_clover_option2.sh
   ```
   Enter credentials when prompted

6. **Test PIN pad:**
   - Open http://100.103.3.35:5050/clover on Clover
   - Tap "Swipe Card & Enter PIN"
   - Enter PIN on physical keypad
   - Should authenticate and redirect to ATM

## How It Works

### Option 1 (Browser):
```
User → Clover Touchscreen → Chrome → Flask Server → Portfolio Data
```

### Option 2 (PIN Pad):
```
User → Card Reader → Encrypted PIN → Bridge → Flask Server → Auth → ATM
```

### Option 3 (Native App):
```
User → Card Reader → Secure Element → Native App → Flask API → ATM
        ↓
    PIN Pad (hardware encrypted)
```

## Security Notes

**Option 1:**
- 🔴 PIN visible on touchscreen
- 🟡 Use only for testing
- 🟡 Consider HTTPS

**Option 2:**
- 🟢 Encrypted PIN entry
- 🟢 Hardware security
- 🟢 PCI-DSS ready
- 🟡 Requires Clover account

**Option 3:**
- 🟢 Bank-grade security
- 🟢 Secure element
- 🟢 Production-ready
- 🟢 Full PCI compliance

## Troubleshooting

### Clover can't reach server

```bash
# Check server is listening:
ss -tlnp | grep 5050

# Should show: 0.0.0.0:5050

# Check firewall:
sudo ufw allow 5050/tcp

# Test from Clover:
# Browser → http://100.103.3.35:5050/health
# Should see: {"status": "ok"}
```

### PIN pad not working

```bash
# Check Clover credentials:
cat ~/.clover_atm_env

# Should have MERCHANT_ID, API_KEY, ENCRYPTION_KEY

# Check service loaded environment:
sudo systemctl show p3-atm-web | grep Environment

# Restart if needed:
sudo systemctl restart p3-atm-web
```

### Server not starting

```bash
# Check status:
sudo systemctl status p3-atm-web

# View logs:
sudo journalctl -u p3-atm-web -f

# Test manually:
cd /home/matt/Mattys-Robinhood-MCP/p3_atm
python3 atm_server.py
```

## What Clover Models Work?

All of them:
- ✅ **Clover Mini** - Counter-top touchscreen
- ✅ **Clover Flex** - Handheld mobile
- ✅ **Clover Station** - Full POS system
- ✅ **Clover Mobile** - Smartphone form factor

Each has:
- Android OS (runs web browser or native app)
- Touchscreen
- Secure card reader
- EMV chip + NFC support
- PIN pad (physical or on-screen)

## Next Steps

1. **Try Option 1** (2 minutes)
   - Test basic connectivity
   - Verify touchscreen works
   - See the interface on Clover

2. **Run tests** (2 minutes)
   ```bash
   ./test_clover.sh
   ```

3. **Set up Option 2** if you want secure PIN (15 minutes)
   ```bash
   ./install_clover_option2.sh
   ```

4. **Read full docs** when ready for production
   - See `CLOVER_INTEGRATION_GUIDE.md`
   - Covers all three options in detail
   - Includes security considerations

## Support

**For Clover issues:**
- https://docs.clover.com
- https://community.clover.com
- Your Clover merchant dashboard

**For P3 ATM issues:**
- Check `README_P3_WEB.md` in parent directory
- Check service status: `sudo systemctl status p3-atm-web`
- View logs: `sudo journalctl -u p3-atm-web -f`

**For integration issues:**
- Run `./test_clover.sh` first
- Check `CLOVER_INTEGRATION_GUIDE.md`
- Verify network connectivity
- Check Clover credentials are correct

## Quick Reference

```bash
# Start/Stop ATM
sudo systemctl start p3-atm-web
sudo systemctl stop p3-atm-web
sudo systemctl restart p3-atm-web

# View status
sudo systemctl status p3-atm-web

# View logs
sudo journalctl -u p3-atm-web -f

# Test connectivity
./test_clover.sh

# Install Clover integration
./install_clover_option2.sh

# Check Clover config
cat ~/.clover_atm_env

# Revert to original server
cp ../p3_atm/atm_server.py.backup ../p3_atm/atm_server.py
sudo systemctl restart p3-atm-web
```

---

**Built by:** P3 Lending Inc  
**ATM Software:** Flask + Python  
**Hardware:** Clover POS Systems  
**Integration:** REST API + Secure Card Reader
