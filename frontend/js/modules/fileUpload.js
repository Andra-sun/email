/**
 * Gerenciamento de upload de arquivos
 */

import { showError } from "../utils/ui.js";

export function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const isValidType =
            file.type === "application/pdf" || file.type === "text/plain";

        if (!isValidType) {
            showError("Apenas arquivos PDF e TXT são aceitos");
            document.getElementById("file-input").value = "";
            return;
        }

        document.getElementById("file-text").textContent = file.name;
        document.getElementById("file-name").classList.remove("hidden");
        document.getElementById("send-file-btn").disabled = false;
    }
}

export function clearFileInput() {
    const fileInput = document.getElementById("file-input");
    fileInput.value = "";
    document.getElementById("file-name").classList.add("hidden");
    document.getElementById("send-file-btn").disabled = true;
}

export function getSelectedFile() {
    return document.getElementById("file-input").files[0];
}
