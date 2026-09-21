# Example Claude Prompts for Robinhood Trading

This document contains useful prompts you can use with Claude Code to interact with your Robinhood account.

## Portfolio & Account Management

### Check Account Status
```
What's my Robinhood account status?
```

### View Portfolio Value
```
Show me my portfolio breakdown
```

### Check Buying Power
```
How much buying power do I have?
```

### View All Positions
```
Show me all my positions across equities, options, and crypto
```

### Crypto Holdings
```
What crypto do I own and what's it worth?
```

## Market Data & Research

### Get Stock Quote
```
What's the current price of AAPL?
```

### Multiple Quotes
```
Give me quotes for TSLA, NVDA, and MSFT
```

### Crypto Prices
```
What's the current price of Bitcoin and Ethereum?
```

### Company Research
```
Give me a summary of Apple's fundamentals and recent news
```

### View Financials
```
Show me Tesla's latest financial statements
```

## Trading

### Buy Stock
```
Buy $100 worth of AAPL on my agentic account
```

### Buy Crypto
```
Buy $50 of Bitcoin
```

### Sell Position
```
Sell all my shares of TSLA
```

### Limit Order
```
Place a limit order to buy 10 shares of MSFT at $400
```

### Market Order with Shares
```
Buy 5 shares of NVDA at market price
```

### Preview Order Before Placing
```
Show me what it would cost to buy $1000 of Tesla stock
```

## Alerts & Monitoring

### Create Price Alert
```
Alert me when Bitcoin goes above $100,000
```

### Create Drop Alert
```
Alert me if Apple stock drops below $150
```

### View Current Alerts
```
What price alerts do I have set up?
```

### Delete Alert
```
Delete my Bitcoin price alert
```

### Update Alert
```
Change my Apple alert threshold to $160
```

## Watchlists

### View Watchlists
```
Show me all my watchlists
```

### Add to Watchlist
```
Add NVDA to my "Currently Trading" watchlist
```

### Create New Watchlist
```
Create a new watchlist called "AI Stocks" with NVDA, MSFT, and GOOGL
```

### Remove from Watchlist
```
Remove DOGE from my "Cryptos to Watch" list
```

## Orders & History

### View Open Orders
```
Show me my open orders
```

### View Recent Trades
```
What trades have I made in the last 7 days?
```

### Check Order Status
```
What's the status of my TSLA order?
```

### Cancel Order
```
Cancel my pending MSFT order
```

## Scanners & Screeners

### View Saved Scans
```
What scanners do I have saved?
```

### Run a Scan
```
Run my "High Volume Movers" scan
```

### Create Custom Scan
```
Create a scanner for stocks with RSI above 70 and volume over 1 million
```

## Portfolio Analysis

### Performance Summary
```
How has my portfolio performed this month?
```

### Asset Allocation
```
Show me my portfolio allocation by asset type
```

### Dividend Income
```
How much dividend income have I earned this year?
```

### Tax Lots
```
Show me the tax lots for my Apple shares
```

## Options Trading

### View Options Chains
```
Show me the options chain for AAPL expiring next month
```

### Options Positions
```
What options positions do I have?
```

### Buy Call Option
```
Buy 1 TSLA call option at $300 strike expiring next Friday
```

### Options Strategy
```
What would a covered call strategy look like for my NVDA shares?
```

## Advanced Strategies

### Dollar Cost Averaging
```
Set up a plan to buy $100 of Bitcoin every week
```

### Rebalancing
```
Analyze my portfolio and suggest rebalancing to 60/30/10 stocks/bonds/crypto
```

### Risk Assessment
```
What's my portfolio's beta and correlation to the S&P 500?
```

### Stop Loss Strategy
```
Set up stop losses for all my equity positions at 10% below current price
```

## Monitoring & Notifications

### Daily Summary
```
Give me a daily summary of my portfolio performance
```

### Unusual Activity
```
Alert me to any unusual price movements in my watchlist
```

### Earnings Calendar
```
Which of my holdings have earnings reports this week?
```

### Dividend Calendar
```
When are my next dividend payments?
```

## Research & Analysis

### Compare Stocks
```
Compare TSLA and RIVN fundamentals side by side
```

### Sector Analysis
```
How is the tech sector performing today?
```

### Analyst Ratings
```
What are analysts saying about Apple?
```

### News Summary
```
Give me the latest news on my portfolio holdings
```

## Complex Prompts

### Multi-Step Strategy
```
Check my buying power, then if it's over $1000, buy equal amounts of AAPL, MSFT, and GOOGL, 
and set up price alerts at 5% above and below purchase price for each
```

### Conditional Trading
```
If Bitcoin drops below $90,000, buy $500 worth, otherwise alert me when it hits $95,000
```

### Portfolio Optimization
```
Analyze my current holdings, identify any overconcentration risks, 
suggest rebalancing moves, and create a watchlist of diversification candidates
```

### Risk Management
```
Review all my positions, calculate my total portfolio risk, 
set up appropriate stop losses, and alert me if any position moves more than 5% in a day
```

## Debugging & Testing

### List Available Tools
```
What Robinhood MCP tools are available?
```

### Test Connection
```
Is my Robinhood MCP connection working?
```

### Verify Agentic Access
```
Which of my accounts can you trade on?
```

### Check Permissions
```
What trading permissions does my agentic account have?
```

## Tips for Better Prompts

1. **Be Specific**: Instead of "buy stock", say "buy 10 shares of AAPL"
2. **Specify Account**: If you have multiple accounts, specify which one
3. **Set Limits**: Use exact dollar amounts or share quantities
4. **Use Confirmations**: For large trades, ask Claude to confirm before executing
5. **Chain Commands**: You can ask Claude to do multiple things in sequence
6. **Ask for Explanations**: Add "and explain why" to understand Claude's reasoning

## Safety Prompts

### Always Start Small
```
Before we do any real trading, let's review my account settings and limits
```

### Test Mode
```
Show me what this trade would do without actually placing it
```

### Review Before Execution
```
Calculate the total cost of this trade and ask me to confirm before placing
```

### Set Guards
```
Never let me spend more than $100 in a single trade without explicit confirmation
```

## Common Workflows

### Morning Routine
```
Give me my portfolio summary, show overnight performance, 
list any alerts that fired, and highlight any news about my holdings
```

### Weekly Review
```
Summarize my trades this week, calculate P&L, show best and worst performers, 
and suggest any rebalancing moves
```

### Research New Investment
```
I'm thinking about buying COIN. Give me fundamentals, recent news, 
analyst ratings, and compare it to other crypto-related stocks
```

### Exit Strategy
```
I want to sell my TSLA position. Show me current value, 
calculate gains/losses, review tax implications, and execute if favorable
```

---

**Remember**: Always verify trades before they execute and start with small amounts when testing new strategies!
