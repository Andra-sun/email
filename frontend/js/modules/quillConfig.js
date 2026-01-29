/**
 * Configuração e inicialização do editor Quill
 */

let quill;
let responseQuill;

export function initializeQuill() {
    // Aguarda o Quill estar disponível globalmente
    if (typeof Quill === "undefined") {
        console.error(
            "Quill não foi carregado. Verifique se o script do Quill está no HTML.",
        );
        return;
    }

    quill = new Quill("#editor", {
        theme: "snow",
        modules: {
            toolbar: [
                [{ header: [1, 2, false] }],
                ["bold", "italic", "underline"],
                ["link", "code-block"],
            ],
        },
        placeholder: "Escreva a mensagem do email aqui...",
    });

    quill.on("text-change", () => {
        const charCount = quill.getLength() - 1;
        document.getElementById("char-count").textContent =
            `${charCount} caracteres`;
    });
}

export function initializeResponseQuill() {
    if (typeof Quill === "undefined") {
        console.error("Quill não foi carregado.");
        return;
    }

    responseQuill = new Quill("#response-editor", {
        theme: "snow",
        modules: {
            toolbar: [
                [{ header: [1, 2, false] }],
                ["bold", "italic", "underline"],
                ["link", "code-block"],
            ],
        },
        placeholder: "Resposta será exibida aqui...",
    });
    return responseQuill;
}

export function getQuillContent() {
    const text = quill.getText().trim();
    console.log("[getQuillContent] Conteúdo obtido do Quill:");
    console.log("  - Tamanho:", text.length, "caracteres");
    console.log("  - Conteúdo:", text);
    console.log("  - Vazio?", text.length === 0 ? "SIM ⚠️" : "NÃO ✓");
    return text;
}

export function getResponseQuillContent() {
    return responseQuill ? responseQuill.getContents() : null;
}

export function setResponseQuillContent(text) {
    if (responseQuill) {
        responseQuill.setContents([{ insert: text }]);
    }
}

export function clearQuill() {
    quill.setContents([]);
    document.getElementById("char-count").textContent = "0 caracteres";
}
