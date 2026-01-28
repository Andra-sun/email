/**
 * Handlers para envio de emails e arquivos
 */

import { classifyEmail, classifyEmailFile } from "../api/emailService.js";
import { getQuillContent, clearQuill } from "./quillConfig.js";
import { clearFileInput, getSelectedFile } from "./fileUpload.js";
import { showError, setButtonLoading } from "../utils/ui.js";
import { showResult } from "./results.js";
import { toggleTab } from "./tabs.js";

export async function handleSendEmail() {
    const fromInput = document.getElementById("from-input").value.trim();
    const subjectInput = document.getElementById("subject-input").value.trim();
    const emailText = getQuillContent();

    if (!emailText) {
        showError("Por favor, escreva algo no email");
        return;
    }

    const sendBtn = document.getElementById("send-btn");
    setButtonLoading(sendBtn, true);

    try {
        const result = await classifyEmail(
            emailText,
            fromInput || null,
            subjectInput || null,
        );
        showResult(result);

        document.getElementById("from-input").value = "";
        document.getElementById("subject-input").value = "";
        clearQuill();
    } catch (error) {
        showError("Erro ao processar o email. Tente novamente.");
        console.error(error);
    } finally {
        setButtonLoading(sendBtn, false);
    }
}

export async function handleSendFile() {
    const file = getSelectedFile();

    if (!file) {
        showError("Selecione um arquivo");
        return;
    }

    const sendFileBtn = document.getElementById("send-file-btn");
    setButtonLoading(sendFileBtn, true);

    try {
        const result = await classifyEmailFile(file);
        showResult(result);

        clearFileInput();
        toggleTab("write");
    } catch (error) {
        showError("Erro ao processar o arquivo. Tente novamente.");
        console.error(error);
    } finally {
        setButtonLoading(sendFileBtn, false);
    }
}
