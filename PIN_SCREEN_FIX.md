# PIN Screen Bypass Fix

## Problem Summary

The ATM was **skipping the PIN entry screen** and logging directly into the account when pressing Enter on the welcome screen.

## Root Causes Found and Fixed

### Issue #1: Server Session Not Cleared (Fixed in 5e137e4)

**Problem:**
- Page load only cleared client-side `authenticated = false`
- Server-side `session.authenticated` remained `true` from previous session
- Server still thought user was authenticated

**Fix:**
```javascript
// Now calls server logout on page load
await fetch('/api/logout', { method: 'POST' });
authenticated = false;
```

**Verification:**
```bash
# Server logs now show:
POST /api/logout HTTP/1.1" 200
```

### Issue #2: Keyboard Navigation Clicking Hidden Elements (Fixed in 6303c82)

**Problem:**
- Arrow key navigation included **hidden** sidebar nav-items in focusable elements
- First nav-item has `onclick="showScreen('home-screen')"`
- When user pressed Enter on welcome screen, it clicked the **hidden nav-item**
- This bypassed PIN screen entirely

**Why It Happened:**
```javascript
// OLD CODE - BROKEN
focusableElements = [...navItems, ...screenElements].filter(el => {
    const style = window.getComputedStyle(el);
    return style.display !== "none" && style.visibility !== "hidden";
});
```

The problem: `getComputedStyle()` on a child element returns **the child's own display value**, even when parent has `display: none`. 

Example:
```html
<div id="side-nav" style="display: none;">  <!-- Parent hidden -->
    <div class="nav-item" onclick="showScreen('home-screen')">  <!-- Child thinks it's visible -->
        Investing
    </div>
</div>
```

`getComputedStyle()` on the nav-item returns its own `display: block`, not the parent's `display: none`.

**Fix:**
```javascript
// NEW CODE - FIXED
focusableElements = [...navItems, ...screenElements].filter(el => {
    // offsetParent is null for elements hidden by themselves OR parent
    if (el.offsetParent === null) return false;
    const style = window.getComputedStyle(el);
    return style.display !== "none" && style.visibility !== "hidden";
});
```

**Why `offsetParent` works:**
- Returns `null` for hidden elements (including those hidden by parent)
- Returns the nearest positioned ancestor for visible elements
- Standard DOM property, works cross-browser

## The Complete Flow Now

### Before Fixes (BROKEN):
1. Page loads
2. Client: `authenticated = false` ❌ Server: `session.authenticated = true`
3. User presses Enter
4. Clicks hidden nav-item: `showScreen('home-screen')` ❌
5. Bypasses PIN screen entirely

### After Fixes (WORKING):
1. Page loads
2. Calls `/api/logout` → Server: `session.authenticated = false` ✅
3. Client: `authenticated = false` ✅
4. Focus on visible welcome button only ✅
5. User presses Enter
6. Clicks welcome button: `showScreen('pin-screen')` ✅
7. PIN screen appears ✅
8. User enters PIN: `0213`
9. Quick balance screen shows ✅
10. Continue to home screen ✅

## Testing the Fix

### Expected Behavior:
1. Look at screen → See "Robinhood ATM Trading Terminal"
2. Press **Enter** or **Space** → PIN screen appears
3. Enter digits: **0-2-1-3**
4. Press **Enter** → Quick balance receipt shows
5. Shows balance, P&L, positions
6. Press **Enter** → Main menu appears

### Verification Commands:
```bash
# Restart ATM
~/Mattys-Robinhood-MCP/restart-web-atm.sh

# Check server logs for logout call
journalctl --user -u robinhood-atm-server.service -n 5 | grep logout

# Check what's focused on welcome screen (in browser console)
focusableElements.map(el => el.textContent || el.className)
# Should only show: ["Enter PIN to Continue"]
```

## Files Changed

| Commit | File | Change |
|--------|------|--------|
| 5e137e4 | `p3_atm/atm_templates/atm.html` | Add `/api/logout` call on page load |
| 6303c82 | `p3_atm/atm_templates/atm.html` | Fix `updateFocusableElements()` filter |

## Related Commits

- 65e8b96: Added quick balance receipt to terminal ATM (not related to web ATM)
- 57b4fcc: Added documentation explaining dual interfaces
- 5e137e4: Fixed server session bypass ✅
- 6303c82: Fixed keyboard navigation bypass ✅

## PIN Details

- **PIN:** `0213`
- **Storage:** SHA-256 hash in `ATM_PIN_HASH` environment variable
- **Hash:** `f020272c938ba0a213d31613fd5a1a8b053c693d489551f8b24e900db43d6873`
- **Max Attempts:** 3 (then 30-minute lockout)
- **Lockout File:** `~/.atm-lockout.json`

## Security Notes

✅ PIN is hashed with SHA-256  
✅ Server session cleared on page load  
✅ Authentication required for all endpoints  
✅ Lockout system prevents brute force  
✅ Auto-logout on inactivity  

## Status: FIXED ✅

Both issues have been identified, fixed, tested, and committed.
The ATM now requires PIN entry on every page load.
