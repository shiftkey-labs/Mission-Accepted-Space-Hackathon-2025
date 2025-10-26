// AlgalWatch Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all dashboard components
    initializeDashboard();
});

function initializeDashboard() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize card animations
    initializeCardAnimations();
    
    // Initialize real-time updates
    initializeRealTimeUpdates();
    
    // Initialize interactive elements
    initializeInteractiveElements();

    // Fetch and display Lake Winnipeg plot on load
    fetchAndDisplayLakeWinnipegPlot();
}


// Fetch the Lake Winnipeg algae PNG from the backend and display it in the homepage
function fetchAndDisplayLakeWinnipegPlot() {
    const imgEl = document.getElementById('lakeWinnipegPlot');
    const loader = document.getElementById('plotLoader');

    if (!imgEl) return;

    const url = (window.__env && window.__env.baseUrl ? window.__env.baseUrl : '') + '/api/satellite/lake-winnipeg';

    fetch(url, { method: 'GET' })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.blob();
        })
        .then(blob => {
            const objectUrl = URL.createObjectURL(blob);
            imgEl.src = objectUrl;
            imgEl.style.display = 'block';
            if (loader) loader.style.display = 'none';
        })
        .catch(err => {
            console.error('Failed to load Lake Winnipeg plot:', err);
            if (loader) {
                loader.innerHTML = '<p class="text-muted small">Unable to load plot.</p>';
            }
            showNotification('Could not load Lake Winnipeg algae plot', 'warning');
        });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize card hover animations
function initializeCardAnimations() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Simulate real-time data updates
function initializeRealTimeUpdates() {
    // Update stats every 30 seconds
    setInterval(updateStats, 30000);
    
    // Update last updated time every minute
    setInterval(updateLastUpdateTime, 60000);
}

// Update dashboard statistics
function updateStats() {
    const statsElements = document.querySelectorAll('.stats-value');
    
    statsElements.forEach(element => {
        const currentValue = parseInt(element.textContent.replace(/[^\d]/g, ''));
        const variation = Math.floor(Math.random() * 10) - 5; // Random variation between -5 and +5
        const newValue = Math.max(0, currentValue + variation);
        
        // Animate the number change
        animateValue(element, currentValue, newValue, 1000);
    });
}

// Animate number changes
function animateValue(element, start, end, duration) {
    const isPercentage = element.textContent.includes('%');
    const suffix = isPercentage ? '%' : '';
    
    const startTimestamp = performance.now();
    
    const step = (timestamp) => {
        const elapsed = timestamp - startTimestamp;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    };
    
    requestAnimationFrame(step);
}

// Update last update time
function updateLastUpdateTime() {
    const timeElements = document.querySelectorAll('.text-muted:contains("ago")');
    
    timeElements.forEach(element => {
        if (element.textContent.includes('min ago')) {
            const minutes = parseInt(element.textContent.match(/\d+/)[0]);
            element.textContent = `${minutes + 1} min ago`;
        }
    });
}

// Initialize interactive elements
function initializeInteractiveElements() {
    // Add click handlers for quick action buttons
    const quickActionButtons = document.querySelectorAll('.card-body .btn');
    
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add loading state
            this.classList.add('loading');
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            
            // Simulate action
            setTimeout(() => {
                this.classList.remove('loading');
                this.innerHTML = originalText;
                
                // Show success message
                showNotification('Action completed successfully!', 'success');
            }, 2000);
        });
    });
    
    // Add handlers for chart period buttons
    const chartButtons = document.querySelectorAll('.btn-group .btn');
    
    chartButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            chartButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update chart (placeholder)
            updateChart(this.textContent);
        });
    });
}

// Update chart based on period selection
function updateChart(period) {
    // This would update the Chart.js chart with new data
    console.log(`Updating chart for period: ${period}`);
    
    // Show loading indicator
    const chartContainer = document.getElementById('bloomChart').parentElement;
    chartContainer.style.opacity = '0.6';
    
    // Simulate data loading
    setTimeout(() => {
        chartContainer.style.opacity = '1';
        showNotification(`Chart updated for ${period} period`, 'info');
    }, 1000);
}

// Show notification to user
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Utility function to format numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border: none;
        border-radius: 8px;
    }
`;
document.head.appendChild(style);

// Export functions for global use
window.AlgalWatch = {
    updateStats,
    showNotification,
    formatNumber
};
