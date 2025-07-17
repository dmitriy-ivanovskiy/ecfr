// Configuration settings for eCFR Analysis Dashboard
const CONFIG = {
    // API Configuration
    API_BASE_URL: "http://127.0.0.1:8001",
    
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