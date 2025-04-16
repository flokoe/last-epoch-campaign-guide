// Load saved state on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCheckboxState();
    loadCollapseState();
    
    // Add event listeners to all checkboxes
    const checkboxes = document.querySelectorAll('.zone-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const zoneId = this.getAttribute('data-zone-id');
            const zoneElement = document.getElementById(zoneId);
            
            if (this.checked) {
                zoneElement.classList.add('completed');
            } else {
                zoneElement.classList.remove('completed');
            }
            
            saveCheckboxState();
        });
    });
    
    // Add event listeners to chapter headers for collapsible functionality
    const chapterHeaders = document.querySelectorAll('.chapter-header');
    chapterHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const contentId = this.getAttribute('data-target');
            const contentElement = document.getElementById(contentId);
            
            this.classList.toggle('collapsed');
            contentElement.classList.toggle('collapsed');
            
            saveCollapseState();
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
            const zoneElement = document.getElementById(zoneId);
            
            if (checkbox && state[zoneId]) {
                checkbox.checked = true;
                zoneElement.classList.add('completed');
            }
        }
    }
}

// Save collapse state to localStorage
function saveCollapseState() {
    const chapterHeaders = document.querySelectorAll('.chapter-header');
    const state = {};
    
    chapterHeaders.forEach(header => {
        const contentId = header.getAttribute('data-target');
        state[contentId] = header.classList.contains('collapsed');
    });
    
    localStorage.setItem('leGuideCollapseState', JSON.stringify(state));
}

// Load collapse state from localStorage
function loadCollapseState() {
    const savedState = localStorage.getItem('leGuideCollapseState');
    
    if (savedState) {
        const state = JSON.parse(savedState);
        
        for (const contentId in state) {
            const header = document.querySelector(`.chapter-header[data-target="${contentId}"]`);
            const contentElement = document.getElementById(contentId);
            
            if (header && contentElement && state[contentId]) {
                header.classList.add('collapsed');
                contentElement.classList.add('collapsed');
            }
        }
    }
} 