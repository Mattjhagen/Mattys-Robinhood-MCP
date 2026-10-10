# Step 3: Enable 15-Minute Trading Loop (EASY WAY!)

## 🚀 Just Run This One Command:

```bash
cd ~/Mattys-Robinhood-MCP
./setup_cron.sh
```

**That's it!** The script does everything automatically.

---

## 📺 What You'll See:

```
🤖 Setting up automated trading loop...

✅ Cron job installed!

📋 Your crontab now has:
*/15 * * * * /home/matt/Mattys-Robinhood-MCP/run_trading_loop.sh

⏰ The bot will run every 15 minutes:
   - :00, :15, :30, :45 of every hour
   - 24/7, automatically
   - Logs to /tmp/trading_loop.log

🎉 Auto-trading is LIVE!
```

---

## ✅ How to Know It's Working:

### Watch it run:
```bash
tail -f /tmp/trading_loop.log
```

You'll see output like:
```
========================================
Sat Oct 10 19:15:01 UTC 2026: Starting trading cycle
🤖 Agentic Trading Bot
============================================================
Portfolio value: $0.26
Buying power: $0.00
Sat Oct 10 19:15:05 UTC 2026: Cycle complete ✅
```

### Test it immediately (don't wait 15 minutes):
```bash
./run_trading_loop.sh
```

---

## 📅 When Does It Run?

**Every 15 minutes:**
- 12:00, 12:15, 12:30, 12:45
- 1:00, 1:15, 1:30, 1:45
- 2:00, 2:15, 2:30, 2:45
- ... and so on, 24/7!

---

## 🛑 How to Stop It:

If you ever want to stop the auto-trading:

```bash
crontab -e
# Delete the line with "run_trading_loop.sh"
# Save and exit
```

Or just run:
```bash
crontab -l | grep -v "run_trading_loop.sh" | crontab -
```

---

## 🔧 Troubleshooting:

### "command not found"
```bash
# Make sure you're in the right directory:
cd ~/Mattys-Robinhood-MCP
./setup_cron.sh
```

### "Permission denied"
```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

### Check if it's running:
```bash
crontab -l
# You should see a line with "run_trading_loop.sh"
```

---

## 🎉 That's It!

Once you run `./setup_cron.sh`, your bot is LIVE and will trade automatically every 15 minutes!

**Next**: Monitor it with `tail -f /tmp/trading_loop.log`
