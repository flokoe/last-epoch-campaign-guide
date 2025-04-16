// Load saved state on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCheckboxState();
    loadDetailsState();
    
    // Add event listeners to all checkboxes
    const checkboxes = document.querySelectorAll('.zone-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            saveCheckboxState();
        });
    });
    
    // Add event listeners to details elements for persistence
    const chapters = document.querySelectorAll('details.chapter');
    chapters.forEach(details => {
        details.addEventListener('toggle', function() {
            saveDetailsState();
        });
    });
});

// Save checkbox state to localStorage
function saveCheckboxState() {
    const checkboxes = document.querySelectorAll('.zone-checkbox');
    const state = {};
    
    checkboxes.forEach(checkbox => {
        const zoneId = checkbox.getAttribute('data-zone-id');
        state[zoneId] = checkbox.checked;
    });
    
    localStorage.setItem('leGuideState', JSON.stringify(state));
}

// Load checkbox state from localStorage
function loadCheckboxState() {
    const savedState = localStorage.getItem('leGuideState');
    
    if (savedState) {
        const state = JSON.parse(savedState);
        
        for (const zoneId in state) {
            const checkbox = document.querySelector(`.zone-checkbox[data-zone-id="${zoneId}"]`);
            if (checkbox && state[zoneId]) {
                checkbox.checked = true;
            }
        }
    }
}

// Save details open/closed state to localStorage
function saveDetailsState() {
    const chapters = document.querySelectorAll('details.chapter');
    const state = {};
    
    chapters.forEach(details => {
        const chapterId = details.id;
        state[chapterId] = details.open;
    });
    
    localStorage.setItem('leGuideDetailsState', JSON.stringify(state));
}

// Load details open/closed state from localStorage
function loadDetailsState() {
    const savedState = localStorage.getItem('leGuideDetailsState');
    
    if (savedState) {
        const state = JSON.parse(savedState);
        
        for (const chapterId in state) {
            const details = document.getElementById(chapterId);
            if (details) {
                details.open = state[chapterId];
            }
        }
    }
} 