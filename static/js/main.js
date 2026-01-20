// Main JavaScript file

// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = 'red';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
    
    // Number input validation
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            const min = parseFloat(this.getAttribute('min'));
            const max = parseFloat(this.getAttribute('max'));
            const value = parseFloat(this.value);
            
            if (min !== null && value < min) {
                this.value = min;
            }
            if (max !== null && value > max) {
                this.value = max;
            }
        });
    });
    
    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const maxSize = 16 * 1024 * 1024; // 16MB
                if (file.size > maxSize) {
                    alert('File size exceeds 16MB limit');
                    this.value = '';
                    return;
                }
                
                // Show file name
                const fileName = file.name;
                let label = this.nextElementSibling;
                if (label && label.tagName === 'SMALL') {
                    label.textContent = `Selected: ${fileName} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
                }
            }
        });
    });
});

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functions for use in other scripts
window.MediDiagnosis = {
    formatDate,
    formatDateTime
};




