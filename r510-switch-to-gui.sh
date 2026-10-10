#!/bin/bash
# Switch R510 display back to GUI (TTY1)
ssh matt@100.103.3.35 'sudo chvt 1'
echo "✓ R510 display switched to GUI (TTY1)"
