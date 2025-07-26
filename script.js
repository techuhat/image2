// Global variables
let currentFiles = [];
let processedFiles = [];
let currentTool = '';
let currentSlideIndex = 0;
let imageDataUrls = [];

// File handling functions
function removeFile(index) {
    currentFiles.splice(index, 1);
    updateFileList(currentFiles);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getFileIcon(mimeType) {
    if (mimeType.startsWith('image/')) {
        return 'fa-image';
    } else if (mimeType === 'application/pdf') {
        return 'fa-file-pdf';
    } else {
        return 'fa-file';
    }
}

async function updateFileList(files) {
    currentFiles = files;
    const filePreview = document.getElementById('file-preview');
    const fileList = document.getElementById('file-list');
    const processBtn = document.getElementById('process-btn');
    const imagePreviewGrid = document.getElementById('image-preview-grid');
    
    if (files.length > 0) {
        filePreview.classList.remove('hidden');
        fileList.innerHTML = '';
        
        // Get image files
        const imageFiles = files.filter(file => file.type.startsWith('image/'));
        
        // Create file list with enhanced styling and animations
        files.forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item flex items-start justify-between bg-gray-50 dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 transition-all duration-200 hover:shadow-md hover:border-blue-300 dark:hover:border-blue-500';
            fileItem.style.opacity = '0';
            fileItem.style.transform = 'translateY(10px)';
            
            const fileIcon = getFileIcon(file.type);
            const fileTypeClass = file.type.startsWith('image/') ? 'text-green-600' : 
                               file.type === 'application/pdf' ? 'text-red-600' : 'text-blue-600';
            
            fileItem.innerHTML = `
                <div class="flex items-start flex-1 min-w-0">
                    <div class="flex-shrink-0 w-12 h-12 bg-white dark:bg-gray-600 rounded-lg flex items-center justify-center mr-4 shadow-sm">
                        <i class="fas ${fileIcon} text-lg ${fileTypeClass}"></i>
                    </div>
                    <div class="flex-1 min-w-0 overflow-hidden">
                        <div class="font-medium text-gray-900 dark:text-white break-words leading-tight">${file.name}</div>
                        <div class="text-sm text-gray-500 dark:text-gray-400 flex flex-wrap items-center mt-1 gap-1">
                            <span>${formatFileSize(file.size)}</span>
                            <span class="hidden sm:inline">•</span>
                            <span class="capitalize">${file.type.split('/')[1] || 'Unknown'}</span>
                            ${file.lastModified ? `<span class="hidden sm:inline">•</span><span>${new Date(file.lastModified).toLocaleDateString()}</span>` : ''}
                        </div>
                    </div>
                </div>
                <button onclick="removeFile(${index})" class="btn-enhanced flex-shrink-0 ml-4 p-2 text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all duration-200">
                    <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    </svg>
                </button>
            `;
            
            fileList.appendChild(fileItem);
            
            // Animate in
            setTimeout(() => {
                fileItem.style.opacity = '1';
                fileItem.style.transform = 'translateY(0)';
            }, index * 50);
        });
        
        processBtn.disabled = false;
        
        // Show image previews if there are image files
        if (imageFiles.length > 0) {
            imagePreviewGrid.innerHTML = '';
            imageDataUrls = [];
            
            // Generate image previews
            for (let i = 0; i < Math.min(imageFiles.length, 4); i++) {
                const file = imageFiles[i];
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const dataUrl = e.target.result;
                    imageDataUrls.push(dataUrl);
                    
                    const previewItem = document.createElement('div');
                    previewItem.className = 'image-preview-item';
                    previewItem.style.backgroundImage = `url(${dataUrl})`;
                    
                    imagePreviewGrid.appendChild(previewItem);
                };
                
                reader.readAsDataURL(file);
            }
            
            // Show "more" indicator if there are more than 4 images
            if (imageFiles.length > 4) {
                const moreItem = document.createElement('div');
                moreItem.className = 'image-preview-more';
                moreItem.innerHTML = `<span>+${imageFiles.length - 4}</span>`;
                imagePreviewGrid.appendChild(moreItem);
            }
            
            imagePreviewGrid.classList.remove('hidden');
        } else {
            imagePreviewGrid.classList.add('hidden');
        }
    } else {
        filePreview.classList.add('hidden');
        processBtn.disabled = true;
    }
}

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.classList.add('dark');
    }
}

function toggleTheme() {
    const isDark = document.documentElement.classList.contains('dark');
    
    if (isDark) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}

// Initialize theme on page load
initTheme();

// Theme toggle event listener and global initialization
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('dn');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        toggle.checked = savedTheme === 'dark';
        // Apply theme based on saved preference
        if (savedTheme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    } else {
        // Set toggle based on current theme
        toggle.checked = document.documentElement.classList.contains('dark');
    }
    
    // Listen for toggle changes
    toggle.addEventListener('change', function() {
        const theme = this.checked ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
        
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    });
    
    // Initialize global drag and drop functionality
    setupGlobalDragDrop();
});

// Utility Functions
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function showToast(message, type = 'success', duration = 3000) {
    // Determine which container to use based on whether the tool modal is open
    const isToolOpen = !document.getElementById('tool-modal').classList.contains('hidden');
    const containerId = isToolOpen ? 'tool-toast-container' : 'toast-container';
    const container = document.getElementById(containerId);
    
    const toast = document.createElement('div');
    const toastId = 'toast-' + Date.now();
    toast.id = toastId;
    toast.className = `toast bg-white dark:bg-gray-800 border-l-4 ${
        type === 'success' ? 'border-green-500' : 
        type === 'error' ? 'border-red-500' : 
        type === 'warning' ? 'border-yellow-500' :
        'border-blue-500'
    } p-4 rounded-lg shadow-lg transform translate-x-full opacity-0 transition-all duration-300 ease-out`;
    
    // Add additional styles for better visibility
    if (isToolOpen) {
        toast.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.2)';
        toast.style.fontWeight = '500';
        toast.style.zIndex = '9999';
    }
    
    const icon = type === 'success' ? '<svg class="w-6 h-6 text-green-500 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>' :
                    type === 'error' ? '<svg class="w-6 h-6 text-red-500 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>' :
                    type === 'warning' ? '<svg class="w-6 h-6 text-yellow-500 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>' :
                    '<svg class="w-6 h-6 text-blue-500 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>';
    
    toast.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center flex-1">
                ${icon}
                <span class="text-sm font-medium text-gray-900 dark:text-white">${message}</span>
            </div>
            <button onclick="dismissToast('${toastId}')" class="ml-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">
                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
            </button>
        </div>
        <div class="absolute bottom-0 left-0 h-1 bg-gradient-to-r ${
            type === 'success' ? 'from-green-500 to-green-400' :
            type === 'error' ? 'from-red-500 to-red-400' :
            type === 'warning' ? 'from-yellow-500 to-yellow-400' :
            'from-blue-500 to-blue-400'
        } rounded-bl-lg transition-all duration-${duration} ease-linear" style="width: 100%; animation: toast-progress ${duration}ms linear;"></div>
    `;
    
    container.appendChild(toast);
    
    // Show toast with animation
    requestAnimationFrame(() => {
        if (window.innerWidth <= 640) {
            // Mobile devices - use opacity animation instead of transform
            toast.classList.remove('opacity-0');
            toast.classList.add('opacity-100');
            // Ensure toast is properly positioned on mobile
            toast.style.transform = 'translateX(0)';
            toast.style.left = '0';
            toast.style.right = '0';
            toast.style.width = '100%';
            toast.style.maxWidth = '100%';
        } else {
            // Desktop devices - use transform animation but ensure proper positioning
            toast.classList.remove('translate-x-full', 'opacity-0');
            toast.classList.add('translate-x-0', 'opacity-100');
            // Ensure toast is properly positioned on desktop
            toast.style.transform = 'translateX(0)';
            toast.style.left = '0';
            toast.style.right = '0';
            toast.style.width = '100%';
            toast.style.maxWidth = '100%';
        }
    });
    
    // Auto-remove toast
    const timeoutId = setTimeout(() => {
        dismissToast(toastId);
    }, duration);
    
    // Store timeout ID for manual dismissal
    toast.dataset.timeoutId = timeoutId;
}

function dismissToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        // Clear timeout if manually dismissed
        if (toast.dataset.timeoutId) {
            clearTimeout(toast.dataset.timeoutId);
        }
        
        if (window.innerWidth <= 640) {
            // Mobile devices - use opacity animation
            toast.classList.remove('opacity-100');
            toast.classList.add('opacity-0');
            // Ensure toast stays in position during dismissal
            toast.style.transform = 'translateX(0)';
        } else {
            // Desktop devices - use opacity animation to prevent sliding off-screen
            toast.classList.remove('opacity-100');
            toast.classList.add('opacity-0');
            // Ensure toast stays in position during dismissal
            toast.style.transform = 'translateX(0)';
        }
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }
}

function showProgress(show = true, message = 'Processing...') {
    const container = document.getElementById('progress-container');
    const bar = document.getElementById('progress-bar');
    const text = container.querySelector('.progress-text');
    
    if (show) {
        container.classList.remove('hidden');
        bar.style.width = '0%';
        bar.style.transition = 'width 0.3s ease-out';
        if (text) text.textContent = message;
        
        // Add pulse animation to container
        container.classList.add('animate-pulse');
        setTimeout(() => container.classList.remove('animate-pulse'), 500);
    } else {
        // Smooth hide animation
        container.style.opacity = '0';
        setTimeout(() => {
            container.classList.add('hidden');
            container.style.opacity = '1';
        }, 300);
    }
}

function updateProgress(percentage, message = null) {
    const bar = document.getElementById('progress-bar');
    const container = document.getElementById('progress-container');
    const text = container.querySelector('.progress-text');
    
    const clampedPercentage = Math.min(100, Math.max(0, percentage));
    bar.style.width = `${clampedPercentage}%`;
    
    // Update message if provided
    if (message && text) {
        text.textContent = message;
    }
    
    // Add completion animation
    if (clampedPercentage === 100) {
        bar.classList.add('animate-pulse');
        setTimeout(() => {
            bar.classList.remove('animate-pulse');
            showProgress(false);
        }, 500);
    }
    
    // Update progress bar color based on percentage
    if (clampedPercentage < 30) {
        bar.className = bar.className.replace(/bg-\w+-\d+/g, '') + ' bg-red-500';
    } else if (clampedPercentage < 70) {
        bar.className = bar.className.replace(/bg-\w+-\d+/g, '') + ' bg-yellow-500';
    } else {
        bar.className = bar.className.replace(/bg-\w+-\d+/g, '') + ' bg-green-500';
    }
}

// Tool management functions
function openTool(toolName) {
    currentTool = toolName;
    const modal = document.getElementById('tool-modal');
    const title = document.getElementById('tool-title');
    const content = document.getElementById('tool-content');
    
    // Set title
    const titles = {
        'image-to-pdf': 'Image to PDF Converter',
        'pdf-to-images': 'PDF to Images Converter',
        'image-compressor': 'Image Compressor',
        'image-resizer': 'Image Resizer',
        'format-converter': 'Format Converter',
        'batch-processor': 'Batch Processor'
    };
    
    title.textContent = titles[toolName] || 'Tool Workspace';
    
    // Load tool content
    content.innerHTML = getToolContent(toolName);
    
    // Show modal
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Initialize tool
    setTimeout(() => initializeTool(toolName), 100);
    
    // Show success toast for better UX
    showToast(`Opening ${titles[toolName]}...`, 'success', 2000);
}

function closeTool() {
    const modal = document.getElementById('tool-modal');
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
    
    // Reset state
    currentFiles = [];
    processedFiles = [];
    currentTool = '';
    currentSlideIndex = 0;
    imageDataUrls = [];
}

function getToolContent(toolName) {
    const commonFileInput = `
        <div class="file-drop-zone rounded-xl p-8 text-center mb-6">
            <div class="file-input-wrapper">
                <svg class="w-12 h-12 text-gray-400 mb-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/></svg>
                <p class="text-lg font-medium mb-2">Drag & drop files here</p>
                <p class="text-gray-500 mb-4">or click to browse</p>
                <button type="button" onclick="document.getElementById('file-input').click()" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Choose Files
                </button>
                <input type="file" id="file-input" multiple accept="image/*,.pdf" class="hidden">
            </div>
        </div>
        <div id="file-preview" class="hidden mb-6">
            <h3 class="text-lg font-semibold mb-4">Selected Files</h3>
            <div id="file-list" class="space-y-2 mb-4"></div>
            <div id="image-preview-grid" class="image-preview-grid"></div>
        </div>
    `;
    
    const controls = {
        'batch-processor': `
            <div class="mb-6">
                <h3 class="text-lg font-semibold mb-4">Individual Image Settings</h3>
                <div id="batch-images" class="grid gap-6 md:grid-cols-2">
                    <!-- Individual image controls will be added here -->
                </div>
            </div>
        `,
        'pdf-to-images': `
            <div class="grid md:grid-cols-2 gap-4 mb-6">
                <div>
                    <label class="block text-sm font-medium mb-2">Output Format</label>
                    <select id="pdf-extract-format" class="w-full p-3 border dark:border-gray-600 rounded-lg dark:bg-gray-700">
                        <option value="jpeg">JPEG</option>
                        <option value="png">PNG</option>
                        <option value="webp">WebP</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Quality</label>
                    <input type="range" id="pdf-extract-quality" min="10" max="100" value="90" class="w-full">
                    <div class="text-center text-sm text-gray-500 mt-1">
                        <span id="pdf-extract-quality-value">90</span>%
                    </div>
                </div>
            </div>
            <div class="mb-6">
                <label class="block text-sm font-medium mb-2">DPI (Resolution)</label>
                <select id="pdf-extract-dpi" class="w-full p-3 border dark:border-gray-600 rounded-lg dark:bg-gray-700">
                    <option value="96">96 DPI (Screen Resolution)</option>
                    <option value="150">150 DPI (Medium Quality)</option>
                    <option value="300">300 DPI (High Quality)</option>
                </select>
            </div>
        `,
        'image-to-pdf': `
            <div class="grid md:grid-cols-2 gap-4 mb-6">
                <div>
                    <label class="block text-sm font-medium mb-2">Page Layout</label>
                    <select id="pdf-layout" class="w-full p-3 border dark:border-gray-600 rounded-lg dark:bg-gray-700">
                        <option value="portrait">Portrait</option>
                        <option value="landscape">Landscape</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Page Size</label>
                    <select id="pdf-size" class="w-full p-3 border dark:border-gray-600 rounded-lg dark:bg-gray-700">
                        <option value="a4">A4</option>
                        <option value="letter">Letter</option>
                        <option value="legal">Legal</option>
                    </select>
                </div>
            </div>
            <div class="mb-6">
                <label class="block text-sm font-medium mb-2">Margin (px)</label>
                <input type="range" id="pdf-margin" min="0" max="50" value="10" class="w-full">
                <div class="text-center text-sm text-gray-500 mt-1">
                    <span id="margin-value">10</span>px
                </div>
            </div>
        `,
        'image-compressor': `
            <div class="mb-6">
                <label class="block text-sm font-medium mb-2">Quality</label>
                <input type="range" id="quality-slider" min="10" max="100" value="80" class="w-full">
                <div class="text-center text-sm text-gray-500 mt-1">
                    <span id="quality-value">80</span>%
                </div>
            </div>
            <div id="compression-stats" class="hidden bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6">
                <div class="grid grid-cols-3 gap-4 text-center">
                    <div>
                        <div class="text-sm text-gray-500">Original</div>
                        <div id="original-size" class="font-bold">-</div>
                    </div>
                    <div>
                        <div class="text-sm text-gray-500">Compressed</div>
                        <div id="compressed-size" class="font-bold">-</div>
                    </div>
                    <div>
                        <div class="text-sm text-gray-500">Saved</div>
                        <div id="saved-percentage" class="font-bold text-green-600">-</div>
                    </div>
                </div>
            </div>
        `,
        'image-resizer': `
            <div class="grid md:grid-cols-2 gap-4 mb-6">
                <div>
                    <label class="block text-sm font-medium mb-2">Width (px)</label>
                    <input type="number" id="resize-width" placeholder="800" class="w-full p-3 border dark:border-gray-600 rounded-lg dark:bg-gray-700">
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Height (px)</label>
                    <input type="number" id="resize-height" placeholder="600" class="w-full p-3 border dark:border-gray-600 rounded-lg dark:bg-gray-700">
                </div>
            </div>
            <div class="mb-6">
                <label class="flex items-center">
                    <input type="checkbox" id="maintain-aspect" checked class="mr-2">
                    <span class="text-sm">Maintain aspect ratio</span>
                </label>
            </div>
        `,
        'format-converter': `
            <div class="mb-6">
                <label class="block text-sm font-medium mb-2">Output Format</label>
                <select id="output-format" class="w-full p-3 border dark:border-gray-600 rounded-lg dark:bg-gray-700">
                    <option value="jpeg">JPEG</option>
                    <option value="png">PNG</option>
                    <option value="webp">WebP</option>
                    <option value="avif">AVIF</option>
                    <option value="bmp">BMP</option>
                    <option value="tiff">TIFF</option>
                </select>
            </div>
            <div class="mb-6">
                <label class="block text-sm font-medium mb-2">Quality</label>
                <input type="range" id="convert-quality" min="10" max="100" value="90" class="w-full">
                <div class="text-center text-sm text-gray-500 mt-1">
                    <span id="convert-quality-value">90</span>%
                </div>
            </div>
        `
    };
    
    return `
        ${commonFileInput}
        ${controls[toolName] || ''}
        <div class="flex space-x-4">
            <button id="process-btn" class="flex items-center justify-center flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed" disabled>
                <svg class="w-5 h-5 mr-2 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>
                <span>Process Files</span>
            </button>
            <button id="download-btn" class="flex items-center justify-center flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed hidden" disabled>
                <svg class="w-5 h-5 mr-2 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
                <span>Download All</span>
            </button>
        </div>
        <div id="results" class="mt-6 hidden">
            <h3 class="text-lg font-semibold mb-4">Processed Files</h3>
            <div id="results-list" class="space-y-2"></div>
        </div>
    `;
}