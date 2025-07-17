// Configuration settings for eCFR Analysis Dashboard
const CONFIG = {
    // API Configuration - automatically detect environment
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? "http://127.0.0.1:8001/api"
        : "/api", // Use relative path for combined deployment
    
    // UI Configuration
    STATUS_DISPLAY_DURATION: 3000, // milliseconds
    
    // Pagination Configuration
    CORRECTIONS_PER_PAGE: 100,
    
    // Display Configuration
    CORRECTIVE_ACTION_MAX_LENGTH: 80,
    CHECKSUM_DISPLAY_LENGTH: 8,
    
    // Lexical Diversity Thresholds
    LEXICAL_DIVERSITY: {
        HIGH_THRESHOLD: 0.7,
        MEDIUM_THRESHOLD: 0.4
    }
};

// Make config available globally
window.CONFIG = CONFIG; 