/**
 * Configuração e inicialização do editor Quill
 */

let quill;
let responseQuill;

export function initializeQuill() {
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
    return quill.getText().trim();
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
