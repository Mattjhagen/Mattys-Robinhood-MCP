#!/bin/bash
export DISPLAY=:3
export HOME=/home/matt

# Start X server on VT3
xinit /home/matt/Mattys-Robinhood-MCP/p3_atm/launch_p3_atm.sh -- :3 vt3 -nocursor
