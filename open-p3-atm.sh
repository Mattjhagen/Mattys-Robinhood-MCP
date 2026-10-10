#!/bin/bash
# Open P3 ATM in browser from any machine
echo "Opening P3 Lending Inc ATM..."
echo "URL: http://100.103.3.35:5050"
echo "PIN: 0213"
echo ""

# Try to open in default browser
if command -v xdg-open &> /dev/null; then
    xdg-open "http://100.103.3.35:5050"
elif command -v open &> /dev/null; then
    open "http://100.103.3.35:5050"
else
    echo "Please open this URL in your browser:"
    echo "http://100.103.3.35:5050"
fi
