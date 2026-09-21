# Installation Guide

## Prerequisites

- Claude Code installed (CLI, desktop, or web)
- Robinhood account with agentic trading enabled
- Basic familiarity with JSON configuration files

## Step-by-Step Setup

### 1. Install Claude Code

If you haven't already, install Claude Code:

**macOS/Linux:**
```bash
curl -fsSL https://claude.com/install.sh | sh
```

**Or download from:**
- [Claude Code Desktop](https://claude.com/download)
- Use the web version at [claude.ai/code](https://claude.ai/code)

### 2. Locate Your Claude Configuration

Claude's configuration is stored in:
- **Linux/macOS**: `~/.claude.json`
- **Windows**: `%USERPROFILE%\.claude.json`

### 3. Add Robinhood MCP Server

Edit your `~/.claude.json` file and add the Robinhood MCP server to the `mcpServers` section:

```json
{
  "mcpServers": {
    "robinhood-trading": {
      "type": "http",
      "url": "https://agent.robinhood.com/mcp/trading"
    }
  }
}
```

If you already have other MCP servers configured, add the Robinhood configuration alongside them:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp"
    },
    "robinhood-trading": {
      "type": "http",
      "url": "https://agent.robinhood.com/mcp/trading"
    }
  }
}
```

### 4. Restart Claude Code

After modifying the configuration:
- CLI: Exit and restart `claude`
- Desktop: Quit and reopen the application
- Web: Refresh the page

### 5. Authenticate with Robinhood

In Claude Code, run:
```
/mcp
```

This will:
1. Show you available MCP servers
2. Allow you to authenticate with Robinhood
3. Grant Claude access to your account

Follow the authentication prompts to log in with your Robinhood credentials.

### 6. Enable Agentic Trading

**Important**: You must explicitly enable agentic trading on your Robinhood account:

1. Log into [robinhood.com](https://robinhood.com)
2. Go to **Account** → **Settings**
3. Find **Agentic Trading** section
4. Enable it for the account you want to use
5. Review and accept the terms
6. Set any trading limits or restrictions

### 7. Verify Setup

Test your configuration by asking Claude:

```
Check my Robinhood account status
```

You should see your account details, portfolio value, and buying power.

## Alternative Setup: Read-Only Mode

If you want Claude to only read data (no trading), use the npm package instead:

### Install the Package

```bash
npm install -g robinhood-mcp
```

### Configure in Claude

```json
{
  "mcpServers": {
    "robinhood-mcp-readonly": {
      "type": "stdio",
      "command": "npx",
      "args": ["robinhood-mcp"],
      "env": {}
    }
  }
}
```

This provides read-only access to:
- Portfolio data
- Market quotes
- Historical data
- News and research

But does NOT allow:
- Placing trades
- Creating/modifying alerts
- Managing watchlists

## Troubleshooting

### MCP Server Not Showing Up

**Check your JSON syntax:**
```bash
# Validate your config file
cat ~/.claude.json | python3 -m json.tool
```

If you see errors, fix the JSON syntax and restart Claude Code.

### Authentication Failing

1. **Check Robinhood service status**: Visit [status.robinhood.com](https://status.robinhood.com)
2. **Clear authentication cache**: 
   ```bash
   rm ~/.claude/mcp-needs-auth-cache.json
   ```
3. **Try authenticating again**: Run `/mcp` in Claude Code

### "Account not agentic-enabled" Error

This means your account doesn't have agentic trading enabled:

1. Log into Robinhood on web/mobile
2. Navigate to Account Settings → Agentic Trading
3. Enable agentic trading
4. Wait a few minutes for the change to propagate
5. Try again in Claude Code

### Permission Denied for Trading

Your account might have trading restrictions:

1. **Check account type**: Some account types don't support certain trades
2. **Verify buying power**: Run `get_portfolio` to check available funds
3. **Review trading limits**: Check your agentic trading settings
4. **Pattern day trader status**: If flagged as PDT, you may have limitations

### MCP Connection Timeout

1. **Check internet connection**
2. **Verify URL is correct**: `https://agent.robinhood.com/mcp/trading`
3. **Check firewall settings**: Ensure Claude can make outbound HTTPS connections
4. **Try alternative configuration**: Use the stdio/npm version if HTTP isn't working

## Configuration Options

### Setting Trading Limits

In your Robinhood agentic trading settings, you can set:

- **Max order size**: Maximum dollar amount per trade
- **Daily trade limit**: Maximum number of trades per day
- **Allowed asset classes**: Stocks, crypto, options, etc.
- **Restricted symbols**: Symbols that cannot be traded
- **Time restrictions**: Trading hours limitations

### Claude Code Permissions

You can configure Claude Code to require approval for certain actions:

Edit `~/.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [],
    "deny": [],
    "prompt": [
      "mcp__robinhood-trading__place_*"
    ]
  }
}
```

This will make Claude ask for permission before placing any trades.

## Security Best Practices

1. ✅ **Enable 2FA** on your Robinhood account
2. ✅ **Set conservative trading limits** initially
3. ✅ **Monitor trades** in the Robinhood app
4. ✅ **Review agentic trading logs** regularly
5. ✅ **Start with paper trading** if available
6. ✅ **Use a separate account** for agentic trading
7. ❌ **Never share your authentication tokens**
8. ❌ **Don't commit credentials to git**

## Next Steps

After installation:

1. **Review the main [README.md](README.md)** for usage examples
2. **Check [current-config-snapshot.json](current-config-snapshot.json)** for the current setup
3. **Explore available MCP tools** by asking Claude "What Robinhood tools are available?"
4. **Set up alerts and watchlists** for assets you want to monitor

## Support

For issues:
- **Claude Code**: [github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues)
- **Robinhood MCP**: Check Robinhood's agent documentation
- **This Config**: Open an issue in this repository

## Updates

This repository will be updated as:
- New features are added to the Robinhood MCP
- Configuration best practices evolve
- Issues and fixes are discovered

Watch this repo for updates!
