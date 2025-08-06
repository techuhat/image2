/**
 * Library Loader - Enhanced loading and verification for critical JavaScript libraries
 * Helps ensure libraries like jsPDF are properly loaded before use
 */

class LibraryLoader {
    constructor() {
        this.loadedLibraries = new Set();
        this.loadPromises = new Map();
        this.retryAttempts = 3;
        this.retryDelay = 1000; // 1 second
    }

    /**
     * Check if jsPDF library is properly loaded and functional
     */
    checkJsPDF() {
        try {
            // Check multiple ways jsPDF might be available
            if (typeof window.jsPDF !== 'undefined') {
                console.log('✅ jsPDF found at window.jsPDF');
                return { available: true, source: 'window.jsPDF', version: window.jsPDF.version || 'unknown' };
            }
            
            if (typeof window.jspdf !== 'undefined' && window.jspdf.jsPDF) {
                console.log('✅ jsPDF found at window.jspdf.jsPDF');
                return { available: true, source: 'window.jspdf.jsPDF', version: window.jspdf.version || 'unknown' };
            }

            if (typeof jsPDF !== 'undefined') {
                console.log('✅ jsPDF found in global scope');
                return { available: true, source: 'global', version: jsPDF.version || 'unknown' };
            }

            console.warn('❌ jsPDF not found in any expected location');
            return { available: false, source: null };
        } catch (error) {
            console.error('❌ Error checking jsPDF availability:', error);
            return { available: false, source: null, error: error.message };
        }
    }

    /**
     * Wait for a library to be available with timeout and retries
     */
    async waitForLibrary(libraryName, checkFunction, timeout = 10000) {
        const startTime = Date.now();
        let attempts = 0;

        while (Date.now() - startTime < timeout && attempts < this.retryAttempts) {
            attempts++;
            console.log(`🔍 Checking for ${libraryName} (attempt ${attempts}/${this.retryAttempts})`);
            
            const result = checkFunction();
            if (result.available) {
                console.log(`✅ ${libraryName} is ready!`, result);
                this.loadedLibraries.add(libraryName);
                return result;
            }

            // Wait before retry
            if (attempts < this.retryAttempts) {
                console.log(`⏳ ${libraryName} not ready, retrying in ${this.retryDelay}ms...`);
                await new Promise(resolve => setTimeout(resolve, this.retryDelay));
            }
        }

        const error = `❌ ${libraryName} failed to load after ${attempts} attempts in ${timeout}ms`;
        console.error(error);
        throw new Error(error);
    }

    /**
     * Load and verify jsPDF library
     */
    async loadJsPDF() {
        const cacheKey = 'jsPDF';
        
        if (this.loadPromises.has(cacheKey)) {
            return this.loadPromises.get(cacheKey);
        }

        const promise = this.waitForLibrary('jsPDF', () => this.checkJsPDF());
        this.loadPromises.set(cacheKey, promise);
        
        return promise;
    }

    /**
     * Force reload a script with cache busting
     */
    async forceReloadScript(src, id = null) {
        console.log(`🔄 Force reloading script: ${src}`);
        
        // Remove existing script if it exists
        if (id) {
            const existingScript = document.getElementById(id);
            if (existingScript) {
                existingScript.remove();
            }
        }

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = `${src}?t=${Date.now()}`; // Cache busting
            if (id) script.id = id;
            
            script.onload = () => {
                console.log(`✅ Script loaded successfully: ${src}`);
                resolve();
            };
            
            script.onerror = (error) => {
                console.error(`❌ Script failed to load: ${src}`, error);
                reject(new Error(`Failed to load script: ${src}`));
            };
            
            document.head.appendChild(script);
        });
    }

    /**
     * Get diagnostic information about the current state
     */
    getDiagnosticInfo() {
        const info = {
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            loadedLibraries: Array.from(this.loadedLibraries),
            jsPDF: this.checkJsPDF(),
            serviceWorker: {
                supported: 'serviceWorker' in navigator,
                controller: navigator.serviceWorker ? !!navigator.serviceWorker.controller : false
            },
            scripts: Array.from(document.scripts).map(script => ({
                src: script.src,
                loaded: script.readyState === 'complete' || !script.readyState
            }))
        };

        console.log('📊 Library Loader Diagnostic Info:', info);
        return info;
    }

    /**
     * Check service worker cache for a specific file
     */
    async checkServiceWorkerCache(url) {
        if (!navigator.serviceWorker || !navigator.serviceWorker.controller) {
            return { cached: false, reason: 'No service worker controller' };
        }

        return new Promise((resolve) => {
            const messageChannel = new MessageChannel();
            messageChannel.port1.onmessage = (event) => {
                resolve(event.data);
            };

            navigator.serviceWorker.controller.postMessage(
                { type: 'CHECK_CACHE', url: url },
                [messageChannel.port2]
            );

            // Timeout after 5 seconds
            setTimeout(() => {
                resolve({ cached: false, reason: 'Timeout' });
            }, 5000);
        });
    }

    /**
     * Force refresh a file in service worker cache
     */
    async forceRefreshCache(url) {
        if (!navigator.serviceWorker || !navigator.serviceWorker.controller) {
            throw new Error('No service worker controller available');
        }

        return new Promise((resolve, reject) => {
            const messageChannel = new MessageChannel();
            messageChannel.port1.onmessage = (event) => {
                if (event.data.type === 'CACHE_REFRESHED') {
                    resolve(event.data);
                } else if (event.data.type === 'CACHE_REFRESH_ERROR') {
                    reject(new Error(event.data.error));
                }
            };

            navigator.serviceWorker.controller.postMessage(
                { type: 'FORCE_CACHE_REFRESH', url: url },
                [messageChannel.port2]
            );

            // Timeout after 10 seconds
            setTimeout(() => {
                reject(new Error('Cache refresh timeout'));
            }, 10000);
        });
    }
}

// Create global instance
window.LibraryLoader = new LibraryLoader();

// Auto-diagnostic on load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Library Loader initialized');
    
    // Run diagnostic after a short delay to let other scripts load
    setTimeout(() => {
        window.LibraryLoader.getDiagnosticInfo();
    }, 2000);
});
