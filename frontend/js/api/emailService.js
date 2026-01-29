/**
 * Serviço de API para classificação de emails
 */

import { BACKEND_URL } from "../config.js";

/**
 * Classifica um email enviando o texto
 * @param {string} emailText - Texto do email a ser classificado
 * @param {string} sender - Remetente do email
 * @param {string} subject - Assunto do email
 * @returns {Promise<Object>} Resposta do servidor
 */
export async function classifyEmail(emailText, sender, subject) {
    try {
        const payload = {
            sender: sender,
            subject: subject,
            message: emailText,
        };

        console.log("📤 classifyEmail - Enviando payload:", payload);
        console.log("📤 classifyEmail - URL:", `${BACKEND_URL}/api/v1/email/classify`);

        const response = await fetch(`${BACKEND_URL}/api/v1/email/classify`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        console.log("📥 classifyEmail - Status da resposta:", response.status, response.statusText);

        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("📥 classifyEmail - Dados recebidos:", data);
        return data;
    } catch (error) {
        console.error("❌ classifyEmail - Erro:", error);
        throw error;
    }
}

/**
 * Classifica um email enviando um arquivo
 * @param {File} file - Arquivo a ser enviado para classificação
 * @returns {Promise<Object>} Resposta do servidor
 */
export async function classifyEmailFile(file) {
    try {
        const formData = new FormData();
        formData.append("file", file);

        console.log("📤 classifyEmailFile - Enviando arquivo:", {
            name: file.name,
            size: file.size,
            type: file.type
        });
        console.log("📤 classifyEmailFile - URL:", `${BACKEND_URL}/api/v1/email/classify-file`);

        const response = await fetch(
            `${BACKEND_URL}/api/v1/email/classify-file`,
            {
                method: "POST",
                body: formData,
            }
        );

        console.log("📥 classifyEmailFile - Status da resposta:", response.status, response.statusText);

        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("📥 classifyEmailFile - Dados recebidos:", data);
        return data;
    } catch (error) {
        console.error("❌ classifyEmailFile - Erro:", error);
        throw error;
    }
}
