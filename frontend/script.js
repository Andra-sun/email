function toggleTab(tab) {
    const writeTab = document.getElementById("write-tab");
    const fileTab = document.getElementById("file-tab");
    const writeSection = document.getElementById("write-section");
    const fileSection = document.getElementById("file-section");

    if (tab === "file") {
        writeSection.classList.add("hidden");
        fileSection.classList.remove("hidden");
        writeTab.classList.remove("border-blue-500", "text-blue-400");
        writeTab.classList.add(
            "border-transparent",
            "text-slate-400",
            "hover:text-slate-300"
        );
        fileTab.classList.remove(
            "border-transparent",
            "text-slate-400",
            "hover:text-slate-300"
        );
        fileTab.classList.add("border-blue-500", "text-blue-400");
    } else {
        writeSection.classList.remove("hidden");
        fileSection.classList.add("hidden");
        writeTab.classList.remove(
            "border-transparent",
            "text-slate-400",
            "hover:text-slate-300"
        );
        writeTab.classList.add("border-blue-500", "text-blue-400");
        fileTab.classList.remove("border-blue-500", "text-blue-400");
        fileTab.classList.add(
            "border-transparent",
            "text-slate-400",
            "hover:text-slate-300"
        );
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById("file-text").textContent = file.name;
        document.getElementById("file-name").classList.remove("hidden");
        document.getElementById("send-file-btn").disabled = false;
    }
}

document.getElementById("send-btn").addEventListener("click", () => {
    const content = quill.getContents();
    const text = quill.getText();

    if (text.trim().length === 0) {
        alert("Por favor, escreva algo no email");
        return;
    }

    console.log("Email enviado:", content);
    alert("Email enviado com sucesso!");
    clearEditor();
});

document.getElementById("send-file-btn").addEventListener("click", () => {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Selecione um arquivo");
        return;
    }

    console.log("Arquivo enviado:", file.name);
    alert(`Arquivo "${file.name}" enviado com sucesso!`);
    fileInput.value = "";
    document.getElementById("file-name").classList.add("hidden");
    document.getElementById("send-file-btn").disabled = true;
    toggleTab("write");
});