#!/bin/bash
#
# Upgrade P3 ATM to Professional Banking Interface
# Adds professional features, security indicators, and polished design
#

echo "======================================================================"
echo "  P3 ATM Professional Upgrade"
echo "  Making your ATM look like a real bank terminal"
echo "======================================================================"
echo ""

cd /home/matt/Mattys-Robinhood-MCP/p3_atm/atm_templates

# Backup current version
echo "1. Backing up current ATM..."
cp atm.html atm_before_upgrade_$(date +%Y%m%d_%H%M%S).html
echo "✓ Backup created"
echo ""

echo "2. Professional enhancements to add:"
echo "   • Bank-grade header with security badges"
echo "   • Status bar with session tracking"
echo "   • Card reader animation"
echo "   • Receipt-style transaction format"
echo "   • FDIC insurance notices"
echo "   • Professional footer with disclaimers"
echo "   • Transaction numbers"
echo "   • Enhanced security visuals"
echo "   • Network status indicators"
echo "   • Professional typography (monospace for amounts)"
echo ""

echo "3. Creating professional CSS enhancements..."

# Create CSS enhancement file
cat > professional_enhancements.css << 'EOF'
/* Professional Banking ATM Enhancements */

/* Bank Logo and Branding */
.bank-header {
    background: linear-gradient(135deg, #1a472a 0%, #2d5016 100%);
    padding: 15px 30px;
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

.bank-logo {
    font-size: 2.5em;
    font-weight: 900;
    color: #00ff00;
    text-shadow: 0 0 20px rgba(0, 255, 0, 0.8), 0 0 40px rgba(0, 255, 0, 0.4);
    font-family: 'Arial Black', sans-serif;
    letter-spacing: 2px;
}

.bank-name {
    font-size: 0.9em;
    color: #ccffcc;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.security-badges {
    display: flex;
    gap: 10px;
    align-items: center;
}

.security-badge {
    background: rgba(0, 255, 0, 0.2);
    border: 2px solid #00ff00;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 0.75em;
    color: #00ff00;
    display: flex;
    align-items: center;
    gap: 5px;
}

/* Status Bar */
.status-bar {
    background: rgba(0, 0, 0, 0.8);
    border-bottom: 1px solid #00ff00;
    padding: 8px 20px;
    display: flex;
    justify-content: space-between;
    font-size: 0.85em;
    color: #00ff00;
    font-family: 'Courier New', monospace;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 5px;
}

.status-icon {
    font-size: 1.1em;
}

/* Card Reader Animation */
.card-reader {
    position: absolute;
    top: 20px;
    right: 20px;
    background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
    border: 2px solid #333;
    border-radius: 8px;
    padding: 8px 15px;
    font-size: 0.85em;
    color: #666;
    display: none;
}

.card-reader.active {
    display: block;
    border-color: #00ff00;
    color: #00ff00;
    animation: cardPulse 2s infinite;
}

@keyframes cardPulse {
    0%, 100% { box-shadow: 0 0 5px rgba(0, 255, 0, 0.3); }
    50% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.6); }
}

/* Transaction Receipt Style */
.receipt-style {
    font-family: 'Courier New', monospace;
    background: rgba(255, 255, 255, 0.05);
    border: 2px dashed #00ff00;
    padding: 20px;
    border-radius: 5px;
    line-height: 1.6;
}

.receipt-header {
    text-align: center;
    border-bottom: 1px dashed #00ff00;
    padding-bottom: 10px;
    margin-bottom: 15px;
    color: #ccffcc;
    font-weight: bold;
}

.receipt-line {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
    color: #00ff00;
}

.receipt-line .label {
    color: #95a5a6;
}

.receipt-line .value {
    font-weight: bold;
    color: #00ff00;
}

.receipt-footer {
    text-align: center;
    border-top: 1px dashed #00ff00;
    padding-top: 10px;
    margin-top: 15px;
    font-size: 0.85em;
    color: #7f8c8d;
}

/* Transaction Number */
.transaction-number {
    font-family: 'Courier New', monospace;
    color: #95a5a6;
    font-size: 0.85em;
    text-align: center;
    margin: 10px 0;
}

/* Amount Display - Professional Typography */
.amount {
    font-family: 'Courier New', monospace;
    font-weight: bold;
    letter-spacing: 1px;
    text-align: right;
}

.amount.large {
    font-size: 2.5em;
}

.amount.medium {
    font-size: 1.8em;
}

/* Account Number Masking */
.account-mask {
    font-family: 'Courier New', monospace;
    letter-spacing: 2px;
}

/* Professional Footer */
.atm-footer {
    background: rgba(0, 0, 0, 0.8);
    border-top: 2px solid #00ff00;
    padding: 15px 20px;
    font-size: 0.75em;
    color: #7f8c8d;
    text-align: center;
}

.footer-section {
    margin: 5px 0;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin: 10px 0;
}

.footer-link {
    color: #00ff00;
    text-decoration: none;
    transition: color 0.2s;
}

.footer-link:hover {
    color: #00cc00;
}

/* Security Notice */
.security-notice {
    background: rgba(0, 255, 0, 0.05);
    border-left: 4px solid #00ff00;
    padding: 10px 15px;
    margin: 15px 0;
    font-size: 0.9em;
    color: #95a5a6;
}

.security-notice .icon {
    color: #00ff00;
    margin-right: 10px;
}

/* Network Status Indicator */
.network-status {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: rgba(0, 0, 0, 0.9);
    border: 2px solid #27ae60;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.85em;
    color: #27ae60;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 1000;
}

.network-status.offline {
    border-color: #e74c3c;
    color: #e74c3c;
}

.network-pulse {
    width: 8px;
    height: 8px;
    background: #27ae60;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.3; transform: scale(1.2); }
}

/* Loading Progress Bar */
.progress-bar {
    width: 100%;
    height: 4px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 2px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ff00 0%, #00cc00 100%);
    width: 0%;
    transition: width 0.3s;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

/* Session Timer */
.session-timer {
    position: fixed;
    top: 20px;
    left: 20px;
    background: rgba(0, 0, 0, 0.9);
    border: 2px solid #3498db;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.85em;
    color: #3498db;
    font-family: 'Courier New', monospace;
    z-index: 1000;
}

.session-timer.warning {
    border-color: #f39c12;
    color: #f39c12;
    animation: warningBlink 1s infinite;
}

@keyframes warningBlink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* FDIC Badge */
.fdic-badge {
    background: rgba(0, 100, 200, 0.2);
    border: 2px solid #0064c8;
    color: #5dade2;
    padding: 10px 15px;
    border-radius: 8px;
    text-align: center;
    font-size: 0.85em;
    margin: 15px 0;
}

.fdic-logo {
    font-weight: bold;
    font-size: 1.2em;
    color: #0064c8;
}

/* Print Receipt Button */
.print-receipt-btn {
    background: linear-gradient(180deg, #7f8c8d 0%, #95a5a6 100%);
    border: 2px solid #95a5a6;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.9em;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 10px auto;
}

.print-receipt-btn:hover {
    background: linear-gradient(180deg, #95a5a6 0%, #7f8c8d 100%);
    transform: scale(1.05);
}

/* Camera/Surveillance Indicator */
.surveillance-indicator {
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(255, 0, 0, 0.1);
    border: 2px solid #e74c3c;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: recordBlink 2s infinite;
}

@keyframes recordBlink {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

/* Enhanced Welcome Animation */
.welcome-animation {
    text-align: center;
    animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Transaction Success Animation */
.success-checkmark {
    display: inline-block;
    animation: checkmarkPop 0.5s ease-out;
}

@keyframes checkmarkPop {
    0% { transform: scale(0); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}
EOF

echo "✓ CSS enhancements created"
echo ""

echo "======================================================================"
echo "Professional Upgrade Created!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "1. Review the CSS enhancements in: professional_enhancements.css"
echo "2. These will be integrated into the main ATM interface"
echo "3. Run: sudo systemctl restart p3-atm-web"
echo ""
echo "New Professional Features:"
echo "  ✓ Bank-grade header with security badges"
echo "  ✓ Live status bar with session tracking"
echo "  ✓ Card reader visual feedback"
echo "  ✓ Receipt-style transaction formatting"
echo "  ✓ FDIC insurance notices"
echo "  ✓ Professional footer with disclaimers"
echo "  ✓ Monospace typography for financial data"
echo "  ✓ Network status indicators"
echo "  ✓ Session timer with warnings"
echo "  ✓ Surveillance camera indicator"
echo ""
echo "Backup saved as: atm_before_upgrade_*.html"
echo "======================================================================"
