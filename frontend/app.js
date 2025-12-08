// Application State
let analysisResults = {};
let currentFile = null;

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupFileUpload();
    setupFormSubmission();
    setupResultsActions();
    setupTabs();
    setupHelpButton();
}

// File Upload Setup
function setupFileUpload() {
    const fileInput = document.getElementById('transcriptFile');
    const fileLabel = document.getElementById('fileLabel');
    const fileName = document.getElementById('fileName');
    const analyzeBtn = document.getElementById('analyzeBtn');

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            currentFile = e.target.files[0];

            // Validate file type
            if (!currentFile.name.endsWith('.txt')) {
                showNotification('Please select a .txt file', 'error');
                fileInput.value = '';
                return;
            }

            fileName.textContent = currentFile.name;
            fileLabel.classList.add('has-file');
            analyzeBtn.disabled = false;
        } else {
            resetFileUpload();
        }
    });
}

// Form Submission
function setupFormSubmission() {
    const form = document.getElementById('uploadForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!currentFile) {
            showNotification('Please select a file', 'error');
            return;
        }

        await analyzeTranscript();
    });
}

// Main Analysis Function
async function analyzeTranscript() {
    try {
        // Show loading state
        showSection('loading');
        animateProgressSteps();

        // Prepare form data
        const formData = new FormData();
        formData.append('file', currentFile);

        // Make API call
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }

        const data = await response.json();
        analysisResults = data.minutes || data;

        // Show results
        showSection('results');
        displayResults();

    } catch (error) {
        console.error('Analysis error:', error);
        showNotification(`Error: ${error.message}`, 'error');
        showSection('upload');
    }
}

// Progress Steps Animation
function animateProgressSteps() {
    const steps = document.querySelectorAll('.step');

    steps.forEach(step => step.classList.remove('active'));
    steps[0].classList.add('active');

    setTimeout(() => {
        steps[0].classList.remove('active');
        steps[1].classList.add('active');
    }, 2000);

    setTimeout(() => {
        steps[1].classList.remove('active');
        steps[2].classList.add('active');
    }, 4000);
}

// Display Results
function displayResults() {
    // Set timestamp
    const timestamp = document.getElementById('resultsTimestamp');
    timestamp.textContent = `Analyzed on ${new Date().toLocaleString()}`;

    // Show first tab by default
    switchTab('executive_summary');
}

// Tab Setup and Switching
function setupTabs() {
    const tabs = document.querySelectorAll('.tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update active tab
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add('active');

    // Display content
    displayTabContent(tabName);
}

function displayTabContent(tabName) {
    const tabContent = document.getElementById('tabContent');
    const content = analysisResults[tabName];

    if (!content || (Array.isArray(content) && content.length === 0)) {
        tabContent.innerHTML = `
            <div class="empty-state">
                <svg width="64" height="64" viewBox="0 0 64 64" fill="none" opacity="0.3">
                    <circle cx="32" cy="32" r="24" stroke="currentColor" stroke-width="2" fill="none"/>
                    <path d="M32 20V32M32 44H32.02" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <p>No ${tabName.replace(/_/g, ' ')} found in the transcript</p>
            </div>
        `;
        return;
    }

    let html = '';

    if (Array.isArray(content)) {
        if (content.length > 0 && typeof content[0] === 'object') {
            // Array of objects - format as cards
            content.forEach((item, index) => {
                html += formatContentItem(item, index + 1);
            });
        } else {
            // Array of strings - format as list
            html += '<div class="content-item">';
            html += '<div class="summary-text"><ul>';
            content.forEach(item => {
                html += `<li>${escapeHtml(item)}</li>`;
            });
            html += '</ul></div>';
            html += '</div>';
        }
    } else if (typeof content === 'object') {
        // Single object
        html += formatContentItem(content, null);
    } else {
        // Simple string value
        html += `<div class="content-item">`;
        html += `<div class="content-item-body">${escapeHtml(content)}</div>`;
        html += `</div>`;
    }

    tabContent.innerHTML = html;
}

function formatContentItem(item, number) {
    let html = '<div class="content-item">';

    if (number) {
        html += '<div class="content-item-header">';
        html += `<div class="content-item-number">${number}</div>`;
        html += '<div class="content-item-title">Item</div>';
        html += '</div>';
    }

    html += '<div class="content-item-body">';

    for (const [key, value] of Object.entries(item)) {
        if (value !== null && value !== undefined && value !== '') {
            const displayKey = key.replace(/_/g, ' ')
                .split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');

            html += `<p><strong>${displayKey}:</strong> ${escapeHtml(String(value))}</p>`;
        }
    }

    html += '</div>';
    html += '</div>';

    return html;
}

// Results Actions Setup
function setupResultsActions() {
    document.getElementById('copyJsonBtn').addEventListener('click', copyJsonToClipboard);
    document.getElementById('downloadJsonBtn').addEventListener('click', downloadJsonFile);
    document.getElementById('newAnalysisBtn').addEventListener('click', startNewAnalysis);
}

function copyJsonToClipboard() {
    if (!analysisResults || Object.keys(analysisResults).length === 0) {
        showNotification('No results to copy', 'error');
        return;
    }

    const jsonString = JSON.stringify(analysisResults, null, 2);

    navigator.clipboard.writeText(jsonString)
        .then(() => {
            showNotification('Results copied to clipboard', 'success');
        })
        .catch(err => {
            console.error('Copy failed:', err);
            showNotification('Failed to copy to clipboard', 'error');
        });
}

function downloadJsonFile() {
    if (!analysisResults || Object.keys(analysisResults).length === 0) {
        showNotification('No results to download', 'error');
        return;
    }

    const jsonString = JSON.stringify(analysisResults, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const filename = `meeting-analysis-${Date.now()}.json`;
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification(`Downloaded as ${filename}`, 'success');
}

function startNewAnalysis() {
    analysisResults = {};
    resetFileUpload();
    showSection('upload');
}

// Section Management
function showSection(sectionName) {
    // Hide all sections
    document.getElementById('uploadSection').classList.add('hidden');
    document.getElementById('loadingSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.add('hidden');

    // Show requested section
    const section = document.getElementById(`${sectionName}Section`);
    if (section) {
        section.classList.remove('hidden');
    }
}

// Reset File Upload
function resetFileUpload() {
    const fileInput = document.getElementById('transcriptFile');
    const fileLabel = document.getElementById('fileLabel');
    const fileName = document.getElementById('fileName');
    const analyzeBtn = document.getElementById('analyzeBtn');

    fileInput.value = '';
    currentFile = null;
    fileName.textContent = 'Choose File (.txt)';
    fileLabel.classList.remove('has-file');
    analyzeBtn.disabled = true;
}

// Help Button
function setupHelpButton() {
    document.getElementById('helpBtn').addEventListener('click', () => {
        showNotification(`
            <strong>How to use:</strong><br>
            1. Upload a meeting transcript (.txt file)<br>
            2. Click "Analyze Transcript"<br>
            3. Review AI-extracted insights in tabs<br>
            4. Copy or download results
        `, 'info');
    });
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = message;

    // Styles
    Object.assign(notification.style, {
        position: 'fixed',
        top: '90px',
        right: '32px',
        padding: '16px 24px',
        background: type === 'success' ? '#107C10' :
                    type === 'error' ? '#D13438' :
                    '#6264A7',
        color: 'white',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        zIndex: '1000',
        maxWidth: '400px',
        animation: 'slideInRight 0.3s ease-out',
        fontSize: '14px',
        lineHeight: '1.5'
    });

    document.body.appendChild(notification);

    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
