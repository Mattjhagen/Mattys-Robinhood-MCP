// ============================================================================
// ARROW KEY NAVIGATION - Navigate with keyboard arrows!
// ============================================================================

let focusIndex = 0;
let focusableElements = [];

function updateFocusableElements() {
    const activeScreen = document.querySelector('.screen.active');
    if (!activeScreen) return;

    // Get all focusable elements in active screen
    focusableElements = Array.from(activeScreen.querySelectorAll(
        'button:not([disabled]), input:not([disabled]), .holding-item, .menu-btn, .pin-btn, .action-btn, .wf-btn, .trade-tab'
    )).filter(el => {
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden';
    });

    // Add focus styles
    focusableElements.forEach((el, index) => {
        el.setAttribute('data-focus-index', index);
        el.style.transition = 'all 0.2s';
    });
}

function focusElement(index) {
    if (focusableElements.length === 0) return;

    // Wrap around
    focusIndex = ((index % focusableElements.length) + focusableElements.length) % focusableElements.length;

    // Remove old focus
    focusableElements.forEach(el => {
        el.style.outline = 'none';
        el.style.boxShadow = '';
        el.style.transform = '';
    });

    // Add new focus
    const element = focusableElements[focusIndex];
    if (element) {
        element.style.outline = '3px solid #00C805';
        element.style.boxShadow = '0 0 20px rgba(0, 200, 5, 0.5)';
        element.style.transform = 'scale(1.05)';
        element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function activateFocusedElement() {
    if (focusableElements.length === 0) return;

    const element = focusableElements[focusIndex];
    if (!element) return;

    if (element.tagName === 'INPUT') {
        element.focus();
    } else if (element.onclick) {
        element.click();
    } else if (element.tagName === 'BUTTON') {
        element.click();
    }
}

// Arrow key handler
document.addEventListener('keydown', (e) => {
    const activeScreen = document.querySelector('.screen.active');
    if (!activeScreen) return;

    // Don't interfere with input fields (except arrow keys)
    if (e.target.matches('input') && !['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
        return;
    }

    switch(e.key) {
        case 'ArrowDown':
        case 'ArrowRight':
            e.preventDefault();
            updateFocusableElements();
            focusElement(focusIndex + 1);
            break;

        case 'ArrowUp':
        case 'ArrowLeft':
            e.preventDefault();
            updateFocusableElements();
            focusElement(focusIndex - 1);
            break;

        case 'Enter':
            if (!e.target.matches('input')) {
                e.preventDefault();
                activateFocusedElement();
            }
            break;

        case 'Home':
            e.preventDefault();
            updateFocusableElements();
            focusElement(0);
            break;

        case 'End':
            e.preventDefault();
            updateFocusableElements();
            focusElement(focusableElements.length - 1);
            break;
    }
});

// Update focusable elements when screen changes
const originalShowScreen = window.showScreen;
window.showScreen = function(screenId) {
    if (originalShowScreen) {
        originalShowScreen(screenId);
    }
    setTimeout(() => {
        focusIndex = 0;
        updateFocusableElements();
        focusElement(0);
    }, 100);
};

// Initialize
setTimeout(() => {
    updateFocusableElements();
    focusElement(0);
}, 500);

console.log('⬆️⬇️⬅️➡️ Arrow key navigation enabled!');
console.log('Use arrow keys to navigate, ENTER to select');
