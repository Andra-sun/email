/**
 * Gerenciamento de abas (Escrever vs Arquivo)
 */

export function toggleTab(tab) {
    const writeTab = document.getElementById("write-tab");
    const fileTab = document.getElementById("file-tab");
    const writeSection = document.getElementById("write-section");
    const fileSection = document.getElementById("file-section");

    const isWriteTab = tab === "write";

    writeSection.classList.toggle("hidden", !isWriteTab);
    fileSection.classList.toggle("hidden", isWriteTab);

    writeTab.classList.toggle("border-blue-500", isWriteTab);
    writeTab.classList.toggle("text-blue-400", isWriteTab);
    writeTab.classList.toggle("border-transparent", !isWriteTab);
    writeTab.classList.toggle("text-slate-400", !isWriteTab);
    writeTab.classList.toggle("hover:text-slate-300", !isWriteTab);

    fileTab.classList.toggle("border-blue-500", !isWriteTab);
    fileTab.classList.toggle("text-blue-400", !isWriteTab);
    fileTab.classList.toggle("border-transparent", isWriteTab);
    fileTab.classList.toggle("text-slate-400", isWriteTab);
    fileTab.classList.toggle("hover:text-slate-300", isWriteTab);
}
