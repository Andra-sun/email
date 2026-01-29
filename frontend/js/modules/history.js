/**
 * Gerenciamento do histórico de respostas
 */

const HISTORY_KEY = 'emailHistory';
const MAX_HISTORY = 5;

export function saveToHistory(emailData, responseData) {
    const history = getHistory();
    
    const entry = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        sender: emailData.sender || 'Desconhecido',
        subject: emailData.subject || 'Sem assunto',
        classification: responseData.classification || 'N/A',
        confidence: responseData.confidence || 0,
        summary: responseData.summary || '',
        recommendations: responseData.recommendations || '',
        suggested_response: responseData.suggested_response || '',
        fullData: responseData
    };
    
    history.unshift(entry);
    
    if (history.length > MAX_HISTORY) {
        history.pop();
    }
    
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    updateHistorySidebar();
    
    return entry;
}

export function getHistory() {
    const stored = localStorage.getItem(HISTORY_KEY);
    return stored ? JSON.parse(stored) : [];
}

export function getHistoryEntry(id) {
    const history = getHistory();
    return history.find(entry => entry.id === id);
}

export function clearHistory() {
    localStorage.removeItem(HISTORY_KEY);
    updateHistorySidebar();
}

export function updateHistorySidebar() {
    const history = getHistory();
    const sidebar = document.getElementById('history-sidebar');
    
    if (!sidebar) return;
    
    const cardsContainer = sidebar.querySelector('#history-cards');
    
    if (history.length === 0) {
        cardsContainer.innerHTML = `
            <div class="text-center text-slate-400 text-sm p-4">
                <p>Nenhuma análise realizada ainda</p>
            </div>
        `;
        return;
    }
    
    cardsContainer.innerHTML = history.map(entry => `
        <button
            class="w-full text-left p-3 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-blue-500 transition-colors cursor-pointer group"
            onclick="loadHistoryEntry(${entry.id})"
        >
            <p class="text-xs text-slate-400 mb-1">
                ${formatDate(entry.timestamp)}
            </p>
            <p class="text-sm font-medium text-slate-100 truncate group-hover:text-blue-300">
                ${entry.subject}
            </p>
            <p class="text-xs text-slate-500 truncate">
                De: ${entry.sender}
            </p>
            <div class="mt-2 flex gap-1">
                <span class="inline-block px-2 py-0.5 text-xs rounded ${
                    entry.classification === 'Produtivo' 
                        ? 'bg-green-900/50 text-green-300' 
                        : 'bg-red-900/50 text-red-300'
                }">
                    ${entry.classification}
                </span>
                <span class="inline-block px-2 py-0.5 text-xs rounded bg-blue-900/50 text-blue-300">
                    ${(entry.confidence * 100).toFixed(0)}%
                </span>
            </div>
        </button>
    `).join('');
}

export function loadHistoryEntry(id) {
    const entry = getHistoryEntry(id);
    if (!entry) return;
    
    import('./results.js').then(module => {
        module.showResult(entry.fullData);
    });
    
    const sidebar = document.getElementById('history-sidebar');
    if (sidebar && window.innerWidth < 768) {
        sidebar.classList.add('hidden');
    }
}

function formatDate(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Agora';
    if (diffMins < 60) return `${diffMins}m atrás`;
    if (diffHours < 24) return `${diffHours}h atrás`;
    if (diffDays < 7) return `${diffDays}d atrás`;
    
    return date.toLocaleDateString('pt-BR');
}

export function toggleHistorySidebar() {
    const sidebar = document.getElementById('history-sidebar');
    if (sidebar) {
        sidebar.classList.toggle('hidden');
    }
}

export function initializeHistory() {
    updateHistorySidebar();
    window.loadHistoryEntry = loadHistoryEntry;
    window.toggleHistorySidebar = toggleHistorySidebar;
}
