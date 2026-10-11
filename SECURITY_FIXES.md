# Critical Security Fixes Required for Robinhood ATM

## Issues Found (2026-10-11)

### 1. Multiple Server Processes Running
**Problem:** 3 instances of atm_server.py detected, consuming excessive CPU
```
matt 1964     - Running since 03:28
matt 1342084  - 74.5% CPU (spawned 13:51)
matt 1342087  - 82.1% CPU (spawned 13:51)
```

**Fix:** Kill duplicate processes and add PID file locking
```bash
# Immediate fix:
pkill -f "atm_server.py"
# Restart properly via systemd
systemctl --user restart trading-agent-keeper
```

### 2. Hardcoded PINs
**Problem:** PIN "0213" hardcoded in source files
- `trading_atm.py` line 29
- `atm_server.py` line 29

**Fix:** Use environment variables and password hashing
```python
# In both files, replace:
CORRECT_PIN = "0213"

# With:
import os
import hashlib

CORRECT_PIN_HASH = os.getenv('ATM_PIN_HASH')
if not CORRECT_PIN_HASH:
    raise ValueError("ATM_PIN_HASH environment variable required")

def verify_pin(input_pin):
    """Verify PIN against stored hash"""
    pin_hash = hashlib.sha256(input_pin.encode()).hexdigest()
    return pin_hash == CORRECT_PIN_HASH
```

Generate hash:
```bash
echo -n "0213" | sha256sum
# Add to ~/.bashrc:
export ATM_PIN_HASH="<hash_result>"
```

### 3. Unauthenticated Balance Exposure
**Problem:** `/api/quick-balance` returns sensitive financial data without auth

**Fix:** Remove or require authentication
```python
@app.route('/api/quick-balance', methods=['GET'])
def quick_balance():
    """Quick balance preview - REQUIRES AUTHENTICATION"""
    if not session.authenticated:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401
    
    # Rest of implementation...
```

### 4. Fake Clover Decryption
**Problem:** `decrypt_clover_pin()` always returns correct PIN (line 112)

**Fix:** Either implement real decryption or disable feature
```python
def decrypt_clover_pin(encrypted_pin):
    """Decrypt PIN from Clover's secure element"""
    if not CLOVER_ENCRYPTION_KEY:
        raise ValueError("Clover integration not properly configured")
    
    # For now, fail closed instead of returning fake success
    raise NotImplementedError(
        "Clover decryption not implemented. "
        "Use touchscreen PIN entry only."
    )
```

### 5. Session Bypass Via Restart
**Problem:** PIN attempt counter resets on service restart

**Fix:** Persist lockout state to disk
```python
LOCKOUT_FILE = Path.home() / ".atm-lockout.json"

def check_lockout():
    """Check if PIN entry is locked out"""
    if not LOCKOUT_FILE.exists():
        return False
    
    with open(LOCKOUT_FILE) as f:
        data = json.load(f)
        lockout_until = datetime.fromisoformat(data['lockout_until'])
        if datetime.now() < lockout_until:
            return True
    
    # Lockout expired, remove file
    LOCKOUT_FILE.unlink()
    return False

def apply_lockout():
    """Lock out PIN entry for 30 minutes"""
    lockout_until = datetime.now() + timedelta(minutes=30)
    with open(LOCKOUT_FILE, 'w') as f:
        json.dump({
            'lockout_until': lockout_until.isoformat(),
            'reason': 'Max PIN attempts exceeded'
        }, f)
```

### 6. Remove Useless Keeper Script
**Problem:** `trading_agent_keeper.sh` does nothing useful

**Fix:** Remove or replace with real monitoring
```bash
# Disable the service:
systemctl --user disable --now trading-agent-keeper

# If monitoring is needed, implement proper health checks instead
```

## Priority Order

1. **IMMEDIATE** - Kill duplicate processes
2. **HIGH** - Remove unauthenticated balance endpoint
3. **HIGH** - Fix hardcoded PINs
4. **MEDIUM** - Implement persistent lockout
5. **MEDIUM** - Remove/fix fake Clover decrypt
6. **LOW** - Clean up keeper script

## Testing After Fixes

```bash
# 1. Verify only one process running
ps aux | grep atm_server.py | grep -v grep

# 2. Test PIN lockout persists across restarts
curl -X POST localhost:5000/api/authenticate \
  -H "Content-Type: application/json" \
  -d '{"pin":"9999"}' # Try 3x, then restart, verify still locked

# 3. Verify balance requires auth
curl localhost:5000/api/quick-balance  # Should return 401

# 4. Test with correct hashed PIN
curl -X POST localhost:5000/api/authenticate \
  -H "Content-Type: application/json" \
  -d '{"pin":"0213"}'  # Should work with hash verification
```
