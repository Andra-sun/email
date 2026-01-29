/**
 * Handlers para envio de emails e arquivos
 */

import { classifyEmail, classifyEmailFile } from "../api/emailService.js";
import { getQuillContent, clearQuill } from "./quillConfig.js";
import { clearFileInput, getSelectedFile } from "./fileUpload.js";
import { showError, setButtonLoading } from "../utils/ui.js";
import { showResult } from "./results.js";
import { toggleTab } from "./tabs.js";
import { saveToHistory } from "./history.js";

export async function handleSendEmail() {
    const fromInput = document.getElementById("from-input").value.trim();
    const subjectInput = document.getElementById("subject-input").value.trim();
    const emailText = getQuillContent();

    console.log("\n========== ENVIO DE EMAIL ==========");
    console.log("De:", fromInput || "[ VAZIO ]");
    console.log("Assunto:", subjectInput || "[ VAZIO ]");
    console.log("Tamanho do texto:", emailText.length, "caracteres");
    console.log("Texto do email:", emailText);
    console.log("======================================\n");

    if (!emailText) {
        showError("Por favor, escreva algo no email");
        console.warn("❌ Erro: Email vazio");
        return;
    }

    const sendBtn = document.getElementById("send-btn");
    setButtonLoading(sendBtn, true);

    console.log("📤 Enviando para o backend...");
    try {
        const result = await classifyEmail(
            emailText,
            fromInput || null,
            subjectInput || null,
        );
        
        console.log("✅ Resposta recebida do backend:", result);
        
        saveToHistory({
            sender: fromInput || 'Desconhecido',
            subject: subjectInput || 'Sem assunto'
        }, result);
        
        showResult(result);

        document.getElementById("from-input").value = "";
        document.getElementById("subject-input").value = "";
        clearQuill();
    } catch (error) {
        console.error("✗ Erro ao enviar email:", error);
        console.error("Detalhes do erro:", {
            message: error.message,
            stack: error.stack
        });
        showError("Erro ao processar o email. Tente novamente.");
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
        
        saveToHistory({
            sender: file.name || 'Arquivo',
            subject: file.name || 'Arquivo enviado'
        }, result);
        
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
