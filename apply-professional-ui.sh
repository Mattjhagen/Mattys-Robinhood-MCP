#!/bin/bash
#
# Apply Professional UI Changes to P3 ATM
# This actually modifies the HTML file with professional enhancements
#

set -e

echo "======================================================================"
echo "  Applying Professional UI to P3 ATM"
echo "======================================================================"
echo ""

cd /home/matt/Mattys-Robinhood-MCP/p3_atm/atm_templates

# Backup first
echo "Creating backup..."
cp atm.html atm_before_professional_$(date +%Y%m%d_%H%M%S).html
echo "✓ Backup created"
echo ""

echo "Applying professional enhancements..."

# Add professional CSS right after the opening <style> tag
# This will insert our professional styling
sed -i '/<style>/r /dev/stdin' atm.html << 'CSSEOF'

        /* Professional ATM Enhancements */

        .atm-container {
            height: 100vh !important;
            max-width: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
        }

        .bank-header-pro {
            background: linear-gradient(135deg, #1a472a 0%, #2d5016 100%);
            padding: 20px 40px;
            border-bottom: 3px solid #00ff00;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0, 255, 0, 0.3);
        }

        .bank-logo-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .atm-logo {
            font-size: 3em !important;
            font-weight: 900 !important;
            font-family: 'Arial Black', sans-serif !important;
            letter-spacing: 3px !important;
        }

        .atm-institution {
            font-size: 0.9em !important;
            letter-spacing: 4px !important;
        }

        .security-badges {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .security-badge {
            background: rgba(0, 255, 0, 0.2);
            border: 2px solid #00ff00;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.75em;
            color: #00ff00;
            white-space: nowrap;
        }

        .status-bar {
            background: rgba(0, 0, 0, 0.8);
            border-bottom: 1px solid #00ff00;
            padding: 10px 30px;
            display: flex;
            justify-content: space-between;
            font-size: 0.85em;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            flex-wrap: wrap;
            gap: 15px;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .atm-screen {
            margin: 0 !important;
            border-radius: 0 !important;
            flex: 1;
        }

        .atm-footer {
            background: rgba(0, 0, 0, 0.9);
            border-top: 2px solid #00ff00;
            padding: 20px 30px;
            font-size: 0.75em;
            color: #7f8c8d;
            text-align: center;
        }

        .footer-section {
            margin: 8px 0;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 10px 0;
            flex-wrap: wrap;
        }

        .footer-link {
            color: #00ff00;
            text-decoration: none;
        }

        .fdic-badge {
            background: rgba(0, 100, 200, 0.15);
            border: 2px solid #0064c8;
            color: #5dade2;
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 0.9em;
            margin: 20px auto;
            max-width: 500px;
        }

        .transaction-id {
            font-family: 'Courier New', monospace;
            color: #95a5a6;
            font-size: 0.85em;
            text-align: center;
            margin: 15px 0;
        }

        .surveillance-indicator {
            position: fixed;
            top: 30px;
            right: 30px;
            background: rgba(255, 0, 0, 0.15);
            border: 2px solid #e74c3c;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: recordBlink 2s infinite;
            font-size: 1.2em;
        }

        @keyframes recordBlink {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }

        .session-timer {
            position: fixed;
            top: 30px;
            left: 30px;
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 0.9em;
            color: #3498db;
            font-family: 'Courier New', monospace;
            z-index: 10000;
        }

        .network-status {
            position: fixed;
            bottom: 30px;
            left: 30px;
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid #27ae60;
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 0.85em;
            color: #27ae60;
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 10000;
        }

        .network-pulse {
            width: 10px;
            height: 10px;
            background: #27ae60;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(1.3); }
        }

        @media (max-width: 768px) {
            .bank-header-pro {
                flex-direction: column;
                gap: 15px;
                padding: 15px 20px;
            }

            .security-badges {
                justify-content: center;
            }

            .status-bar {
                font-size: 0.75em;
                padding: 8px 15px;
            }

            .surveillance-indicator,
            .session-timer {
                width: 35px;
                height: 35px;
                font-size: 0.8em;
            }
        }
CSSEOF

# Now replace the header section
sed -i '/<div class="atm-header">/,/<\/div>/c\
        <div class="bank-header-pro">\
            <div class="bank-logo-container">\
                <div>\
                    <div class="atm-logo">P3</div>\
                    <div class="atm-institution">LENDING INC</div>\
                </div>\
            </div>\
            <div class="security-badges">\
                <div class="security-badge">🔒 256-bit Encryption</div>\
                <div class="security-badge">✓ FDIC Insured</div>\
                <div class="security-badge">🛡️ Secure</div>\
            </div>\
        </div>\
        \
        <div class="status-bar">\
            <div class="status-item">\
                <span>📅</span>\
                <span id="status-datetime">Loading...</span>\
            </div>\
            <div class="status-item">\
                <span>Session:</span>\
                <span id="status-session">#ATM-2024-000000</span>\
            </div>\
            <div class="status-item">\
                <span>📍</span>\
                <span>Main Terminal</span>\
            </div>\
            <div class="status-item">\
                <span>🟢</span>\
                <span>Network: Online</span>\
            </div>\
        </div>' atm.html

# Add indicators before closing body tag
sed -i 's|</body>|\
    <!-- Professional Indicators -->\
    <div class="surveillance-indicator" title="This ATM is monitored for your security">🔴</div>\
    <div class="session-timer" id="session-timer">⏱️ 60:00</div>\
    <div class="network-status">\
        <div class="network-pulse"></div>\
        <span>Online</span>\
    </div>\
\
    <script>\
        // Update status bar time\
        function updateStatusBar() {\
            const now = new Date();\
            const dateStr = now.toLocaleDateString();\
            const timeStr = now.toLocaleTimeString();\
            const el = document.getElementById("status-datetime");\
            if (el) el.textContent = dateStr + " " + timeStr;\
            \
            // Generate session ID\
            const sessionEl = document.getElementById("status-session");\
            if (sessionEl && sessionEl.textContent.includes("000000")) {\
                const sessionId = Math.floor(Math.random() * 999999).toString().padStart(6, "0");\
                sessionEl.textContent = "#ATM-2024-" + sessionId;\
            }\
        }\
        setInterval(updateStatusBar, 1000);\
        updateStatusBar();\
        \
        // Session timer countdown\
        let sessionSeconds = 3600; // 60 minutes\
        function updateSessionTimer() {\
            const el = document.getElementById("session-timer");\
            if (el && authenticated) {\
                const mins = Math.floor(sessionSeconds / 60);\
                const secs = sessionSeconds % 60;\
                el.textContent = `⏱️ ${mins}:${secs.toString().padStart(2, "0")}`;\
                \
                if (sessionSeconds <= 300) {\
                    el.style.borderColor = "#f39c12";\
                    el.style.color = "#f39c12";\
                }\
                if (sessionSeconds <= 60) {\
                    el.style.borderColor = "#e74c3c";\
                    el.style.color = "#e74c3c";\
                }\
                \
                sessionSeconds--;\
                if (sessionSeconds <= 0) {\
                    securityLogout("Session timeout - 60 minutes");\
                }\
            }\
        }\
        setInterval(updateSessionTimer, 1000);\
    </script>\
\
</body>|' atm.html

# Add footer before </div> closing of atm-container
sed -i 's|</div><!--atm-container-->|\
        </div>\
        \
        <div class="atm-footer">\
            <div class="fdic-badge">\
                <div style="font-weight: bold; font-size: 1.2em; color: #0064c8; margin-bottom: 5px;">Member FDIC</div>\
                <div>Your deposits are insured up to $250,000 per account</div>\
                <div>by the Federal Deposit Insurance Corporation</div>\
            </div>\
            <div class="footer-section">\
                <strong>P3 Lending Inc</strong> | Member FDIC | Equal Housing Lender\
            </div>\
            <div class="footer-links">\
                <a href="#" class="footer-link">Terms of Service</a>\
                <a href="#" class="footer-link">Privacy Policy</a>\
                <a href="#" class="footer-link">Accessibility</a>\
                <a href="#" class="footer-link">Help</a>\
            </div>\
            <div class="footer-section">\
                Customer Service: <strong style="color: #00ff00;">1-800-P3-LEND</strong> (1-800-735-3637) | 24/7 Support\
            </div>\
            <div class="footer-section" style="margin-top: 10px; font-size: 0.9em;">\
                © 2026 P3 Lending Inc. All rights reserved. | This ATM is monitored for your security 📹\
            </div>\
        </div>\
    </div><!--atm-container-->|' atm.html

echo "✓ Professional UI applied"
echo ""

echo "======================================================================"
echo "✓ Professional ATM Interface Applied!"
echo "======================================================================"
echo ""
echo "Changes made:"
echo "  • Bank-grade header with security badges"
echo "  • Live status bar with date/time/session"
echo "  • Surveillance camera indicator (top-right)"
echo "  • Session timer (top-left)"
echo "  • Network status (bottom-left)"
echo "  • FDIC insurance notice in footer"
echo "  • Professional legal footer"
echo "  • Customer service contact (1-800-P3-LEND)"
echo ""
echo "Restart service to see changes:"
echo "  sudo systemctl restart p3-atm-web"
echo ""
echo "Then open: http://localhost:5050"
echo "======================================================================"
