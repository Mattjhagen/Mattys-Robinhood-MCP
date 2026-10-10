# 🎯 P3 ATM Auto-Start Service

Your Robinhood ATM can now automatically start when the computer boots!

---

## 🚀 Installation

**Run this ONE TIME to install the service:**

```bash
cd ~/Mattys-Robinhood-MCP/p3_atm
sudo bash install-service.sh
```

You'll be prompted for your sudo password. This:
- ✅ Installs the systemd service
- ✅ Enables auto-start on boot
- ✅ Starts the ATM immediately
- ✅ Verifies it's working

---

## 📋 Service Management

### **Check Status:**
```bash
sudo systemctl status p3-atm
```

### **Restart Service:**
```bash
sudo systemctl restart p3-atm
```

### **Stop Service:**
```bash
sudo systemctl stop p3-atm
```

### **Start Service:**
```bash
sudo systemctl start p3-atm
```

### **Disable Auto-Start:**
```bash
sudo systemctl disable p3-atm
```
(Service won't start on boot, but can still be started manually)

### **Enable Auto-Start Again:**
```bash
sudo systemctl enable p3-atm
```

---

## 📊 Viewing Logs

### **Live Logs (follow mode):**
```bash
sudo journalctl -u p3-atm -f
```
Press `Ctrl+C` to stop following

### **Recent Logs:**
```bash
sudo journalctl -u p3-atm -n 50
```

### **Today's Logs:**
```bash
sudo journalctl -u p3-atm --since today
```

### **Alternative Log File:**
```bash
tail -f /tmp/atm.log
```

---

## 🌐 Accessing Your ATM

**Locally:**
```
http://localhost:5050
```

**From Network:**
```
http://100.103.3.35:5050
```

**PIN:** `0213`

---

## 🔧 Technical Details

**Service File:** `/etc/systemd/system/p3-atm.service`

**What Happens on Boot:**
1. ⏰ System boots up
2. 📡 Network becomes available
3. 🚀 ATM service starts automatically
4. ✅ MCP bridge connects to Robinhood
5. 💰 Live data is ready

**Automatic Restart:**
- If the server crashes, it automatically restarts after 5 seconds
- Infinite restart attempts (until you stop it)

---

## 🛡️ Service Features

✅ **Runs as user `matt`** (not root - safer)  
✅ **Auto-starts on boot**  
✅ **Auto-restarts on failure**  
✅ **Logs to `/tmp/atm.log` and journald**  
✅ **Network-accessible**  
✅ **Security hardened** (NoNewPrivileges, PrivateTmp)  

---

## 🧪 Testing After Reboot

After rebooting your computer:

1. **Wait 30 seconds for boot to complete**
2. **Check if it's running:**
   ```bash
   sudo systemctl status p3-atm
   ```
3. **Test the endpoint:**
   ```bash
   curl http://localhost:5050/health
   ```
4. **Open in browser:**
   ```
   http://localhost:5050
   ```

---

## ⚠️ Troubleshooting

### **Service won't start:**
```bash
sudo journalctl -u p3-atm -n 100
```
Check for Python errors or port conflicts

### **Port 5050 already in use:**
```bash
lsof -i:5050
sudo systemctl stop p3-atm
lsof -ti:5050 | xargs -r sudo kill -9
sudo systemctl start p3-atm
```

### **MCP bridge issues:**
```bash
sudo journalctl -u p3-atm | grep -i mcp
```
Check if npm and `npx robinhood-mcp` are accessible

### **Update ATM code:**
After making changes to `atm_server.py` or `robinhood_api.py`:
```bash
sudo systemctl restart p3-atm
```

---

## 🔥 Uninstall Service

If you want to remove the auto-start service:

```bash
sudo systemctl stop p3-atm
sudo systemctl disable p3-atm
sudo rm /etc/systemd/system/p3-atm.service
sudo systemctl daemon-reload
```

---

## ✅ Quick Reference

| Task | Command |
|---|---|
| **Install** | `sudo bash install-service.sh` |
| **Status** | `sudo systemctl status p3-atm` |
| **Restart** | `sudo systemctl restart p3-atm` |
| **Stop** | `sudo systemctl stop p3-atm` |
| **Start** | `sudo systemctl start p3-atm` |
| **Logs** | `sudo journalctl -u p3-atm -f` |
| **Disable Boot** | `sudo systemctl disable p3-atm` |
| **Enable Boot** | `sudo systemctl enable p3-atm` |

---

**Your ATM will now survive reboots!** 🎉
