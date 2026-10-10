# 🎴 Robinhood Agentic Credit Card Setup

This allows AI agents (like Claude Code) to make purchases on your behalf using a virtual credit card!

---

## What It Does

- 🤖 **AI agents control your credit card** to buy things automatically
- 💳 Virtual card within your Robinhood Gold Card
- 🔐 Safe: You set approval rules and spending limits
- 📊 Agents can view transactions and card details
- 🛒 Makes purchases with your permission

**Supported AI Platforms:**
- ✅ Claude Code (this!)
- ✅ Claude Desktop
- ✅ ChatGPT
- ✅ Cursor, Codex, OpenClaw

---

## Step 1: Add the Robinhood Banking MCP

Run this command in your terminal:

```bash
claude mcp add robinhood-banking --transport http https://banking-agent.robinhood.com/mcp/banking
```

This connects Claude Code to Robinhood's banking system.

---

## Step 2: Connect & Authenticate

1. **In Claude Code, type:** `/mcp`
2. **Select:** `robinhood-banking`
3. **Authenticate** with your Robinhood credentials

---

## Step 3: Configure Your Card

In the Robinhood Banking app:

### **Set Control Preferences:**

**Option A: Per-Purchase Approval**
- You approve each transaction manually
- Most secure option

**Option B: Monthly Spending Limit**
- Set automatic spending cap (e.g., $100/month)
- Agent can spend up to limit without asking

---

## Using the Agentic Card

Once connected, Claude Code can:

### **View Card Details:**
```
Show me my agentic card details
```

### **Check Transaction History:**
```
What purchases has my AI agent made?
```

### **Make Purchases:**
```
Buy a $10 book on Amazon using my agentic card
```

(Requires approval based on your settings)

---

## Important Notes

### ⚠️ **You Are Responsible**
- You're liable for all purchases your agent makes
- Review transactions regularly
- Set conservative limits at first

### 🔒 **Security Features**
- Agent can ONLY access agentic virtual cards
- No access to your main account or other cards
- FDIC insured through Coastal Community Bank
- MCP provides secure, sandboxed connection

### 📱 **Requirements**
- Desktop device for initial setup
- Robinhood Gold Card account
- Agent authentication required
- Must be done from computer (not mobile)

---

## Testing the Connection

After setup, test with:

```bash
# In Claude Code
/mcp

# Then ask:
"What agentic card tools do I have access to?"
```

You should see:
- `get_card_details`
- `get_transaction_history`
- `get_card_policies`

---

## Troubleshooting

### **MCP Not Showing Up:**
```bash
# List all MCP servers
claude mcp list

# Re-add if needed
claude mcp remove robinhood-banking
claude mcp add robinhood-banking --transport http https://banking-agent.robinhood.com/mcp/banking
```

### **Can't Authenticate:**
- Make sure you're on desktop (not mobile)
- Try refreshing the MCP menu (`/mcp` again)
- Check you have Robinhood Gold Card active

### **Agent Can't Make Purchases:**
- Verify card policies are set in Robinhood app
- Check if approval is required (approve manually)
- Ensure spending limit isn't exceeded

---

## Example Usage

**Simple Purchase:**
```
"Buy me a $15 USB cable on Amazon"
```

**With Research:**
```
"Find the best wireless mouse under $30 and buy it"
```

**Budget Tracking:**
```
"How much have I spent this month on my agentic card?"
```

---

## What Agents CAN Do:
✅ View card number, expiry, CVV  
✅ See transaction history  
✅ Check spending limits  
✅ Make purchases (with approval)  

## What Agents CANNOT Do:
❌ Access your main Robinhood account  
❌ View other cards or investments  
❌ Browse the internet independently  
❌ Make purchases without MCP authorization  

---

## Ready to Set Up?

1. Run the MCP add command above
2. Type `/mcp` in Claude Code
3. Authenticate with Robinhood
4. Configure your card policies
5. Start making AI-powered purchases!

🎉 **Your AI agent can now shop for you!**
