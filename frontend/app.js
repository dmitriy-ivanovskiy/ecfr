// Use configuration from config.js
const API_BASE = CONFIG.API_BASE_URL;

// Pagination state for historical corrections
let currentCorrectionsPage = 1;
let totalCorrectionsPages = 1;
let totalCorrectionsCount = 0;

function showStatus(message, type = 'success') {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `px-4 py-2 rounded-md ${type === 'success' ? 'bg-green-100 text-green-800 border border-green-200' : 'bg-red-100 text-red-800 border border-red-200'}`;
    status.classList.remove('hidden');
    setTimeout(() => {
        status.classList.add('hidden');
    }, CONFIG.STATUS_DISPLAY_DURATION);
}

function updatePaginationControls(pagination) {
    const paginationControls = document.getElementById('paginationControls');
    const paginationInfo = document.getElementById('paginationInfo');
    const currentPageSpan = document.getElementById('currentPage');
    const totalPagesSpan = document.getElementById('totalPages');
    
    const firstBtn = document.getElementById('firstPageBtn');
    const prevBtn = document.getElementById('prevPageBtn');
    const nextBtn = document.getElementById('nextPageBtn');
    const lastBtn = document.getElementById('lastPageBtn');
    
    if (pagination && pagination.total_available > 0) {
        // Update pagination info
        const startRecord = pagination.offset + 1;
        const endRecord = Math.min(pagination.offset + pagination.showing, pagination.total_available);
        paginationInfo.textContent = `Showing ${startRecord.toLocaleString()} to ${endRecord.toLocaleString()} of ${pagination.total_available.toLocaleString()} results`;
        
        // Update page numbers
        currentPageSpan.textContent = pagination.current_page;
        totalPagesSpan.textContent = pagination.total_pages;
        
        // Update global state
        currentCorrectionsPage = pagination.current_page;
        totalCorrectionsPages = pagination.total_pages;
        totalCorrectionsCount = pagination.total_available;
        
        // Enable/disable buttons
        firstBtn.disabled = !pagination.has_previous;
        prevBtn.disabled = !pagination.has_previous;
        nextBtn.disabled = !pagination.has_next;
        lastBtn.disabled = !pagination.has_next;
        
        // Update button styles
        [firstBtn, prevBtn, nextBtn, lastBtn].forEach(btn => {
            if (btn.disabled) {
                btn.classList.add('opacity-50', 'cursor-not-allowed');
                btn.classList.remove('hover:bg-gray-50', 'hover:text-gray-700');
            } else {
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
                btn.classList.add('hover:bg-gray-50', 'hover:text-gray-700');
            }
        });
        
        paginationControls.classList.remove('hidden');
    } else {
        paginationControls.classList.add('hidden');
    }
}

async function loadHistoricalCorrections(page = 1) {
    const offset = (page - 1) * CONFIG.CORRECTIONS_PER_PAGE;
    
    try {
        showStatus('Loading historical changes...', 'success');
        
        // Hide other sections and show historical section
        document.getElementById('summary').classList.add('hidden');
        document.querySelector('.content').classList.add('hidden');
        document.getElementById('historicalSection').classList.remove('hidden');
        
        // Only scroll on first load, not on pagination
        if (page === 1) {
            document.getElementById('historicalSection').scrollIntoView({ behavior: 'smooth' });
        }
        
        // Load corrections statistics (only on first load)
        if (page === 1) {
            const statsResponse = await fetch(`${API_BASE}/corrections/stats`);
            if (!statsResponse.ok) {
                throw new Error(`Stats API returned ${statsResponse.status}`);
            }
            
            const stats = await statsResponse.json();
            if (stats.error) {
                throw new Error(stats.error);
            }
            
            // Update statistics
            const totalCorrectionsElement = document.getElementById('totalCorrections');
            const dateRange = document.getElementById('dateRange');
            const activeYears = document.getElementById('activeYears');
            const mostCorrectedTitle = document.getElementById('mostCorrectedTitle');
            const historicalStats = document.getElementById('historicalStats');
            
            if (totalCorrectionsElement) totalCorrectionsElement.textContent = stats.total_corrections.toLocaleString();
            if (dateRange) dateRange.textContent = `${stats.date_range.earliest} to ${stats.date_range.latest}`;
            
            // Find most active year
            const mostActiveYear = Object.entries(stats.corrections_by_year)[0];
            if (activeYears) activeYears.textContent = `${mostActiveYear[0]} (${mostActiveYear[1]} corrections)`;
            
            // Find most corrected title
            const mostCorrectedTitleData = Object.entries(stats.corrections_by_title)[0];
            if (mostCorrectedTitle) mostCorrectedTitle.textContent = `Title ${mostCorrectedTitleData[0]} (${mostCorrectedTitleData[1]} corrections)`;
            
            if (historicalStats) historicalStats.classList.remove('hidden');
        }
        
        // Load corrections data with pagination
        const correctionsResponse = await fetch(`${API_BASE}/corrections?limit=${CONFIG.CORRECTIONS_PER_PAGE}&offset=${offset}`);
        if (!correctionsResponse.ok) {
            throw new Error(`Corrections API returned ${correctionsResponse.status}`);
        }
        
        const corrections = await correctionsResponse.json();
        if (corrections.error) {
            throw new Error(corrections.error);
        }
        
        const tbody = document.getElementById('correctionsTableBody');
        if (!tbody) {
            throw new Error('Could not find correctionsTableBody element');
        }
        
        tbody.innerHTML = '';
        
        if (!corrections.corrections || corrections.corrections.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-10 text-gray-500">No corrections data available</td></tr>';
            updatePaginationControls(null);
            return;
        }
        
        // Populate table with corrections data
        for (let correction of corrections.corrections) {
            const row = document.createElement('tr');
            row.className = 'border-b border-gray-100 hover:bg-gray-50 transition-colors';
            
            // Truncate long corrective actions
            const action = correction.corrective_action && correction.corrective_action.length > CONFIG.CORRECTIVE_ACTION_MAX_LENGTH 
                ? correction.corrective_action.substring(0, CONFIG.CORRECTIVE_ACTION_MAX_LENGTH) + '...'
                : correction.corrective_action || 'N/A';
            
            row.innerHTML = `
                <td class="px-4 py-3"><strong class="text-gray-900">${correction.cfr_reference || 'N/A'}</strong></td>
                <td class="px-4 py-3 text-gray-700">${action}</td>
                <td class="px-4 py-3 text-gray-700">${correction.error_occurred || 'N/A'}</td>
                <td class="px-4 py-3 text-gray-700">${correction.error_corrected || 'N/A'}</td>
                <td class="px-4 py-3"><code class="bg-gray-100 px-2 py-1 rounded text-sm">${correction.fr_citation || 'N/A'}</code></td>
                <td class="px-4 py-3 text-gray-700">Title ${correction.title || 'N/A'}</td>
            `;
            tbody.appendChild(row);
        }
        
        // Update pagination controls
        updatePaginationControls(corrections);
        
        showStatus(`Loaded ${corrections.showing} historical corrections (Page ${corrections.current_page} of ${corrections.total_pages})`, 'success');
        
    } catch (error) {
        showStatus('Error loading historical changes: ' + error.message, 'error');
        const tbody = document.getElementById('correctionsTableBody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-10 text-gray-500">Error loading historical data: ' + error.message + '</td></tr>';
        }
        updatePaginationControls(null);
    }
}

// Pagination functions
function loadFirstPage() {
    if (currentCorrectionsPage > 1) {
        loadHistoricalCorrections(1);
    }
}

function loadPreviousPage() {
    if (currentCorrectionsPage > 1) {
        loadHistoricalCorrections(currentCorrectionsPage - 1);
    }
}

function loadNextPage() {
    if (currentCorrectionsPage < totalCorrectionsPages) {
        loadHistoricalCorrections(currentCorrectionsPage + 1);
    }
}

function loadLastPage() {
    if (currentCorrectionsPage < totalCorrectionsPages) {
        loadHistoricalCorrections(totalCorrectionsPages);
    }
}

// Wrapper function for backward compatibility
function loadHistoricalChanges() {
    loadHistoricalCorrections(1);
}

async function loadDashboard() {
    try {
        showStatus('Loading dashboard...', 'success');
        
        // Show agency sections, hide historical section
        document.getElementById('historicalSection').classList.add('hidden');
        document.querySelector('.content').classList.remove('hidden');
        
        // Load summary data
        const summaryResponse = await fetch(`${API_BASE}/summary`);
        const summary = await summaryResponse.json();
        
        document.getElementById('totalAgencies').textContent = summary.total_agencies.toLocaleString();
        document.getElementById('totalWords').textContent = summary.total_words.toLocaleString();
        document.getElementById('avgLexical').textContent = summary.average_lexical_diversity.toFixed(3);
        document.getElementById('agenciesWithData').textContent = summary.agencies_with_data.toLocaleString();
        document.getElementById('summary').classList.remove('hidden');
        
        // Load agencies with metrics in one call
        const agenciesResponse = await fetch(`${API_BASE}/agencies/with-metrics`);
        const agencies = await agenciesResponse.json();
        
        const tbody = document.getElementById('agencyTableBody');
        tbody.innerHTML = '';
        
        for (let agency of agencies) {
            if (agency.metrics) {
                const row = document.createElement('tr');
                row.className = 'border-b border-gray-100 hover:bg-gray-50 transition-colors';
                
                const lexicalDiversity = agency.metrics.lexical_diversity;
                let lexicalClass = 'bg-red-100 text-red-800';
                if (lexicalDiversity > CONFIG.LEXICAL_DIVERSITY.HIGH_THRESHOLD) {
                    lexicalClass = 'bg-green-100 text-green-800';
                } else if (lexicalDiversity > CONFIG.LEXICAL_DIVERSITY.MEDIUM_THRESHOLD) {
                    lexicalClass = 'bg-yellow-100 text-yellow-800';
                }
                
                row.innerHTML = `
                    <td class="px-4 py-3"><strong class="text-gray-900">${agency.name}</strong></td>
                    <td class="px-4 py-3 text-gray-700">${agency.metrics.word_count.toLocaleString()}</td>
                    <td class="px-4 py-3 text-gray-700">${agency.metrics.unique_words.toLocaleString()}</td>
                    <td class="px-4 py-3"><span class="px-2 py-1 rounded text-xs font-medium ${lexicalClass}">${lexicalDiversity.toFixed(3)}</span></td>
                    <td class="px-4 py-3"><code class="bg-gray-100 px-2 py-1 rounded text-sm">${agency.metrics.checksum.substring(0, CONFIG.CHECKSUM_DISPLAY_LENGTH)}...</code></td>
                    <td class="px-4 py-3 text-gray-700">${agency.metrics.fetched_on}</td>
                `;
                tbody.appendChild(row);
            }
        }
        
        if (tbody.children.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-10 text-gray-500">No data available. Click "Refresh Dashboard" to reload data.</td></tr>';
        }
        
        showStatus('Dashboard loaded successfully!', 'success');
        
    } catch (error) {
        showStatus('Error loading dashboard: ' + error.message, 'error');
    }
}

// Load dashboard on page load
window.addEventListener('load', loadDashboard); 