// Shared Backend Configuration for All Tools
// This file provides centralized backend configuration for all tools

window.SHARED_BACKEND_CONFIG = {
    // Backend Configuration - Production Azure URL
    baseUrl: 'https://imagetool-h4dmewahfmg4bkej.eastasia-01.azurewebsites.net',  // 🌐 AZURE BACKEND
    
    // For local testing, use:
    // baseUrl: 'http://localhost:5000',           // 🔧 LOCAL BACKEND (all endpoints)
    
    // API Endpoints for different tools
    endpoints: {
        // PDF Tools
        pdfToDocx: '/pdf-to-docx',
        docxToPdf: '/docx-to-pdf',
        compressPdf: '/compress-pdf',
        batchProcess: '/batch-process',
        
        // Advanced PDF Processing
        pdfOcr: '/pdf-ocr',
        pdfMerge: '/pdf-merge',
        pdfSplit: '/pdf-split',
        pdfRotate: '/pdf-rotate',
        pdfProtect: '/pdf-protect',
        pdfUnlock: '/pdf-unlock',
        
        // Image Processing
        compressImage: '/compress-image',
        imageToPdf: '/image-to-pdf',
        pdfToImages: '/pdf-to-images',
        
        // Utility endpoints
        health: '/health',
        ping: '/ping',
        clearCache: '/clear-cache'
    },
    
    // Configuration limits (updated for advanced processing)
    maxFileSize: 500 * 1024 * 1024, // 500MB for advanced processing
    timeout: 300000, // 5 minutes
    
    // Retry configuration
    retryAttempts: 3,
    retryDelay: 1000, // 1 second
    
    // Auto-detection settings
    autoDetectBackend: true,
    fallbackToClientSide: true,
    
    // Advanced features configuration
    features: {
        ocr: true,
        advancedCompression: true,
        batchProcessing: true,
        multiFormatSupport: true
    }
};

// Backend Status Management
window.BackendStatus = {
    status: 'unknown', // 'available', 'unavailable', 'checking', 'client-only'
    lastChecked: null,
    capabilities: null,
    
    // Check if backend is available
    async check() {
        try {
            this.status = 'checking';
            const response = await fetch(`${window.SHARED_BACKEND_CONFIG.baseUrl}/ping`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                },
                timeout: 10000
            });
            
            if (response.ok) {
                // Get detailed capabilities
                const healthResponse = await fetch(`${window.SHARED_BACKEND_CONFIG.baseUrl}/health`);
                if (healthResponse.ok) {
                    this.capabilities = await healthResponse.json();
                    console.log('Backend capabilities:', this.capabilities);
                }
                
                this.status = 'available';
                this.lastChecked = new Date();
                return true;
            } else {
                this.status = 'unavailable';
                return false;
            }
        } catch (error) {
            console.warn('Backend not available:', error.message);
            this.status = 'unavailable';
            return false;
        }
    },
    
    // Check if specific capability is available
    hasCapability(capability) {
        if (!this.capabilities || this.status !== 'available') {
            return false;
        }
        return this.capabilities.capabilities && this.capabilities.capabilities[capability];
    },
    
    // Check if advanced features are available
    hasAdvancedFeatures() {
        if (!this.capabilities || this.status !== 'available') {
            return false;
        }
        
        const advancedFeatures = [
            'pdf_ocr',
            'pdf_advanced_processing',
            'advanced_compression',
            'batch_processing'
        ];
        
        return advancedFeatures.some(feature => 
            this.capabilities.capabilities && this.capabilities.capabilities[feature]
        );
    },
    
    // Get status indicator HTML
    getStatusIndicator() {
        const indicators = {
            'available': '<span class="text-green-600">🟢 Advanced Backend Available</span>',
            'unavailable': '<span class="text-orange-600">🟡 Client-side Only</span>',
            'checking': '<span class="text-blue-600">🔵 Checking...</span>',
            'client-only': '<span class="text-gray-600">⚪ Client-side Mode</span>'
        };
        return indicators[this.status] || indicators['client-only'];
    },
    
    // Get detailed status information
    getDetailedStatus() {
        if (!this.capabilities) {
            return {
                status: this.status,
                features: [],
                version: 'unknown'
            };
        }
        
        const features = [];
        if (this.capabilities.capabilities) {
            if (this.capabilities.capabilities.pdf_to_docx) features.push('PDF→DOCX');
            if (this.capabilities.capabilities.pdf_ocr) features.push('OCR Processing');
            if (this.capabilities.capabilities.pdf_advanced_processing) features.push('Advanced PDF');
            if (this.capabilities.capabilities.advanced_compression) features.push('Advanced Compression');
            if (this.capabilities.capabilities.batch_processing) features.push('Batch Processing');
        }
        
        return {
            status: this.status,
            features: features,
            version: this.capabilities.version || 'unknown',
            maxFileSize: this.capabilities.limits?.max_file_size || '100MB'
        };
    }
};

// Utility Functions for Backend Integration
window.BackendUtils = {
    // Make API request with proper error handling
    async makeRequest(endpoint, options = {}) {
        const url = `${window.SHARED_BACKEND_CONFIG.baseUrl}${endpoint}`;
        const config = {
            timeout: window.SHARED_BACKEND_CONFIG.timeout,
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            return response;
        } catch (error) {
            console.error('Backend request failed:', error);
            throw error;
        }
    },
    
    // Upload file to backend
    async uploadFile(file, endpoint, additionalData = {}) {
        const formData = new FormData();
        formData.append('file', file);
        
        // Add additional form data
        Object.keys(additionalData).forEach(key => {
            formData.append(key, additionalData[key]);
        });
        
        return this.makeRequest(endpoint, {
            method: 'POST',
            body: formData
        });
    },
    
    // Check file size against backend limits
    isFileSizeValid(file) {
        return file.size <= window.SHARED_BACKEND_CONFIG.maxFileSize;
    },
    
    // Format file size for display
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
};

// Auto-initialize backend status check on page load
document.addEventListener('DOMContentLoaded', async () => {
    if (window.SHARED_BACKEND_CONFIG.autoDetectBackend) {
        await window.BackendStatus.check();
        console.log('Backend status:', window.BackendStatus.status);
        
        // Update any status indicators on the page
        const statusElements = document.querySelectorAll('[data-backend-status]');
        statusElements.forEach(element => {
            element.innerHTML = window.BackendStatus.getStatusIndicator();
        });
    }
});

// Periodic backend health check (every 5 minutes)
if (window.SHARED_BACKEND_CONFIG.autoDetectBackend) {
    setInterval(async () => {
        await window.BackendStatus.check();
    }, 5 * 60 * 1000);
}
