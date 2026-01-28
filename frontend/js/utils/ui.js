/**
 * Funções utilitárias de UI
 */

export function showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.className =
        "fixed top-4 right-4 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 ";
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);

    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

export function setButtonLoading(button, isLoading) {
    button.disabled = isLoading;
    button.classList.toggle("loading", isLoading);

    if (isLoading) {
        button.innerHTML = `
            <i class="fi fi-rr-spinner-alt animate-spin"></i>
            Processando...
        `;
    } else {
        button.innerHTML = `
            <i class="fi fi-rr-paper-plane"></i>
            ${button.id === "send-btn" ? "Processar Email" : "Processar Arquivo"}
        `;
    }
}
