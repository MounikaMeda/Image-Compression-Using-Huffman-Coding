// Enhanced script.js for Secure Image Compressor

document.addEventListener('DOMContentLoaded', function() {
    initializeFileInputs();
    initializePasswordStrength();
    initializeFormSubmissions();
});

// File input handling
function initializeFileInputs() {
    const imageInput = document.getElementById('imageInput');
    const fileInput = document.getElementById('fileInput');
    
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            handleFileSelection(e, 'imageFileName', ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']);
        });
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            handleFileSelection(e, 'fileFileName', ['.huffimg']);
        });
    }
}

function handleFileSelection(event, displayElementId, allowedTypes) {
    const file = event.target.files[0];
    const displayElement = document.getElementById(displayElementId);
    const label = event.target.closest('.file-label');
    
    if (file) {
        // Validate file type
        const isValid = allowedTypes.some(type => {
            if (type.startsWith('.')) {
                return file.name.toLowerCase().endsWith(type);
            } else {
                return file.type === type;
            }
        });
        
        if (!isValid) {
            alert('Please select a valid file type.');
            event.target.value = '';
            return;
        }
        
        // Display file name and size
        const fileSize = formatFileSize(file.size);
        displayElement.textContent = `${file.name} (${fileSize})`;
        label.classList.add('has-file');
        
        // Show preview for images
        if (file.type.startsWith('image/') && displayElementId === 'imageFileName') {
            showImagePreview(file);
        }
    } else {
        displayElement.textContent = '';
        label.classList.remove('has-file');
    }
}

function showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // You can add image preview functionality here if needed
        console.log('Image loaded for preview');
    };
    reader.readAsDataURL(file);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Password visibility toggle
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const button = input.nextElementSibling;
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Password strength indicator
function initializePasswordStrength() {
    const compressPassword = document.getElementById('compressPassword');
    const strengthIndicator = document.getElementById('passwordStrength');
    
    if (compressPassword && strengthIndicator) {
        compressPassword.addEventListener('input', function() {
            const strength = calculatePasswordStrength(this.value);
            updatePasswordStrength(strengthIndicator, strength);
        });
    }
}

function calculatePasswordStrength(password) {
    let score = 0;
    
    // Length check
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    
    // Character variety checks
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    
    if (score <= 2) return 'weak';
    if (score <= 4) return 'medium';
    return 'strong';
}

function updatePasswordStrength(element, strength) {
    element.className = 'password-strength ' + strength;
    
    const widths = {
        'weak': '33%',
        'medium': '66%',
        'strong': '100%'
    };
    
    element.style.width = widths[strength] || '0%';
}

// Form submission handling
function initializeFormSubmissions() {
    const compressForm = document.getElementById('compressForm');
    const decompressForm = document.getElementById('decompressForm');
    
    if (compressForm) {
        compressForm.addEventListener('submit', function(e) {
            handleFormSubmission(e, 'compressBtn', 'Compressing...');
        });
    }
    
    if (decompressForm) {
        decompressForm.addEventListener('submit', function(e) {
            handleFormSubmission(e, 'decompressBtn', 'Decrypting...');
        });
    }
}

function handleFormSubmission(event, buttonId, loadingText) {
    const button = document.getElementById(buttonId);
    const form = event.target;
    
    // Validate form
    if (!validateForm(form)) {
        event.preventDefault();
        return;
    }
    
    // Show loading state
    button.classList.add('loading');
    button.disabled = true;
    
    // Set a timeout to reset button state in case of long processing
    setTimeout(() => {
        if (button.classList.contains('loading')) {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }, 30000); // 30 seconds timeout
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#ef4444';
            isValid = false;
            
            // Reset border color after 3 seconds
            setTimeout(() => {
                input.style.borderColor = '';
            }, 3000);
        }
    });
    
    if (!isValid) {
        showNotification('Please fill in all required fields.', 'error');
    }
    
    return isValid;
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button class="close-notification" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    return icons[type] || icons.info;
}

function getNotificationColor(type) {
    const colors = {
        'success': '#10b981',
        'error': '#ef4444',
        'warning': '#f59e0b',
        'info': '#3b82f6'
    };
    return colors[type] || colors.info;
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .close-notification {
        background: none;
        border: none;
        color: rgba(255,255,255,0.8);
        cursor: pointer;
        padding: 2px;
        border-radius: 2px;
    }
    
    .close-notification:hover {
        color: white;
        background: rgba(255,255,255,0.1);
    }
`;
document.head.appendChild(style);

// Handle page visibility for form reset
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Reset loading states when page becomes visible again
        const loadingButtons = document.querySelectorAll('.btn.loading');
        loadingButtons.forEach(button => {
            button.classList.remove('loading');
            button.disabled = false;
        });
    }
});

// Legacy function for backwards compatibility (if needed)
function uploadImage() {
    console.warn('uploadImage() function is deprecated. Use the enhanced form submission instead.');
}