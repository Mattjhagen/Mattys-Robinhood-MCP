# P3 ATM Manual Installation Guide

## Quick Install (Run these commands on r510)

```bash
# SSH into r510
ssh matt@100.103.3.35

# Install dependencies
sudo apt-get update
sudo apt-get install -y chromium-browser python3-flask xinit

# Create directory structure
mkdir -p ~/Mattys-Robinhood-MCP/p3_atm/{atm_static,atm_templates}

# Copy files from /tmp (already uploaded)
cd ~/Mattys-Robinhood-MCP/p3_atm
cp /tmp/atm_server.py .
cp /tmp/atm.html atm_templates/
cp /tmp/launch_p3_atm.sh .
chmod +x launch_p3_atm.sh

# Test the server manually first
python3 atm_server.py &
SERVER_PID=$!

# Wait a moment and test
sleep 3
curl http://localhost:5050/health

# If you see {"status":"ok"}, it's working!
# Kill the test server
kill $SERVER_PID

# Create X server wrapper script
cat > start_x_atm.sh << 'EOF'
#!/bin/bash
export DISPLAY=:1
export HOME=/home/matt

# Start X server on VT2
xinit /home/matt/Mattys-Robinhood-MCP/p3_atm/launch_p3_atm.sh -- :1 vt2 -nocursor
EOF

chmod +x start_x_atm.sh

# Create systemd service
sudo tee /etc/systemd/system/p3-atm-tty2.service > /dev/null << 'EOF'
[Unit]
Description=P3 Lending Inc ATM on TTY2
After=multi-user.target

[Service]
Type=simple
User=matt
TTYPath=/dev/tty2
StandardInput=tty
StandardOutput=tty
TTYReset=yes
TTYVHangup=yes
TTYVTDisallocate=yes
ExecStart=/home/matt/Mattys-Robinhood-MCP/p3_atm/start_x_atm.sh
Restart=always
RestartSec=5
Environment=HOME=/home/matt
Environment=XDG_RUNTIME_DIR=/run/user/1000

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable p3-atm-tty2
sudo systemctl start p3-atm-tty2

# Check status
sudo systemctl status p3-atm-tty2

# Switch to TTY2 to see it
sudo chvt 2

# Switch back to TTY1 (or press Ctrl+Alt+F1)
# sudo chvt 1
```

## Troubleshooting

### If the service fails to start:

```bash
# Check logs
sudo journalctl -u p3-atm-tty2 -n 50

# Check if Flask is working
python3 -c "import flask; print('Flask OK')"

# Check if Chromium is installed
which chromium-browser

# Test X server manually
xinit -- :1 vt2
```

### If you see a black screen:

```bash
# Check if the Flask server is running
ps aux | grep atm_server.py

# Check if it's listening on port 5050
sudo lsof -i :5050

# Check X server
ps aux | grep xinit
```

### Quick restart:

```bash
sudo systemctl restart p3-atm-tty2
```

## PIN

Default PIN: **0213**

## Done!

Once running, switch to TTY2 anytime with:
```bash
sudo chvt 2
```

Switch back:
```bash
sudo chvt 1
```
