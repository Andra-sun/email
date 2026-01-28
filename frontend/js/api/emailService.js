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
        const response = await fetch(`${BACKEND_URL}/api/v1/email/classify`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                sender: sender,
                subject: subject,
                message: emailText,
            }),
        });

        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erro ao classificar email:", error);
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

        const response = await fetch(
            `${BACKEND_URL}/api/v1/email/classify-file`,
            {
                method: "POST",
                body: formData,
            }
        );

        if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erro ao classificar arquivo de email:", error);
        throw error;
    }
}
