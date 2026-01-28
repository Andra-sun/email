/**
 * Gerenciamento de exibição de resultados
 */

import {
    initializeResponseQuill,
    setResponseQuillContent,
} from "./quillConfig.js";

let responseQuillInitialized = false;

export function showResult(data) {
    const resultContainer = document.getElementById("result-container");
    const resultContent = document.getElementById("result-content");
    const responseEditorSection = document.getElementById(
        "response-editor-section",
    );
    const resultActions = document.getElementById("result-actions");
    const sendSection = document.getElementById("send-section");

    let html = '<div class="space-y-4">';

    if (data.classification) {
        const classification = data.classification;
        const bgColor =
            classification === "Produtivo" ? "bg-green-900" : "bg-red-900";
        const textColor =
            classification === "Produtivo" ? "text-green-300" : "text-red-300";

        html += `
            <div class="p-4 rounded-lg ${bgColor}">
                <p class="text-sm text-slate-300 mb-1">Classificação</p>
                <p class="text-2xl font-bold ${textColor}">${classification}</p>
            </div>
        `;
    }

    if (data.confidence) {
        html += `
            <div class="p-4 rounded-lg bg-blue-900">
                <p class="text-sm text-slate-300 mb-1">Confiança</p>
                <p class="text-xl font-bold text-blue-300">${(data.confidence * 100).toFixed(2)}%</p>
            </div>
        `;
    }

    if (data.summary) {
        html += `
            <div class="p-4 rounded-lg bg-slate-800 border border-slate-700">
                <p class="text-sm text-slate-300 mb-2">Resumo</p>
                <p class="text-slate-100">${data.summary}</p>
            </div>
        `;
    }

    if (data.recommendations) {
        html += `
            <div class="p-4 rounded-lg bg-slate-800 border border-slate-700">
                <p class="text-sm text-slate-300 mb-2">Recomendações</p>
                <p class="text-slate-100">${data.recommendations}</p>
            </div>
        `;
    }

    if (Object.keys(data).length > 0 && !data.classification) {
        html += `
            <div class="p-4 rounded-lg bg-slate-800 border border-slate-700">
                <p class="text-sm text-slate-300 mb-2">Dados</p>
                <pre class="text-xs text-slate-100 overflow-auto max-h-48">
${JSON.stringify(data, null, 2)}
                </pre>
            </div>
        `;
    }

    html += "</div>";

    resultContent.innerHTML = html;


    if (sendSection) {
        sendSection.classList.add("hidden");
    }

    if (data.suggested_response) {
        if (!responseQuillInitialized) {
            initializeResponseQuill();
            responseQuillInitialized = true;
        }

        setResponseQuillContent(data.suggested_response);

        responseEditorSection.classList.remove("hidden");
        resultActions.classList.add("hidden");

        const copyBtn = document.getElementById("copy-response-btn");
        if (copyBtn) {
            copyBtn.onclick = copyResponseToClipboard;
        }
    } else {
        responseEditorSection.classList.add("hidden");
        resultActions.classList.remove("hidden");
    }

    resultContainer.classList.remove("hidden");
    resultContainer.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function clearResult() {
    document.getElementById("result-container").classList.add("hidden");
    document.getElementById("result-content").innerHTML = "";
    document.getElementById("response-editor-section").classList.add("hidden");
    document.getElementById("send-section").classList.remove("hidden");
}

function copyResponseToClipboard() {
    const responseEditor = document.getElementById("response-editor");
    if (!responseEditor) {
        alert("Erro ao copiar resposta");
        return;
    }

    const quillContent = responseEditor.querySelector(".ql-editor")?.innerText;

    if (!quillContent) {
        alert("Nenhuma resposta para copiar");
        return;
    }

    navigator.clipboard
        .writeText(quillContent)
        .then(() => {
            const btn = document.getElementById("copy-response-btn");
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fi fi-rr-check"></i> Copiado!';
            btn.classList.add("bg-green-700");

            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.classList.remove("bg-green-700");
            }, 2000);
        })
        .catch(() => {
            alert("Erro ao copiar para clipboard");
        });
}
