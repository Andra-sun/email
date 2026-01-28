/**
 * Arquivo principal - Inicialização e setup de event listeners
 */

import { initializeQuill } from "./modules/quillConfig.js";
import { toggleTab } from "./modules/tabs.js";
import { handleFileSelect } from "./modules/fileUpload.js";
import { handleSendEmail, handleSendFile } from "./modules/forms.js";
import { clearResult } from "./modules/results.js";
import { clearQuill } from "./modules/quillConfig.js";

document.addEventListener("DOMContentLoaded", () => {
    initializeQuill();
    setupEventListeners();
});

function setupEventListeners() {
    // Abas
    document
        .getElementById("write-tab")
        .addEventListener("click", () => toggleTab("write"));
    document
        .getElementById("file-tab")
        .addEventListener("click", () => toggleTab("file"));

    // Upload de arquivo
    document
        .getElementById("file-input")
        .addEventListener("change", handleFileSelect);

    // Botões de envio
    document
        .getElementById("send-btn")
        .addEventListener("click", handleSendEmail);
    document
        .getElementById("send-file-btn")
        .addEventListener("click", handleSendFile);

    // Botão limpar
    document
        .getElementById("clear-btn")
        ?.addEventListener("click", clearEditor);
}

function clearEditor() {
    clearQuill();
    clearResult();
}

window.toggleTab = toggleTab;
window.handleFileSelect = handleFileSelect;
window.clearEditor = clearEditor;
window.clearResult = clearResult;
