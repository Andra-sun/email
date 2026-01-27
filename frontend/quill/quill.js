var quill = new Quill('#editor', {
    theme: 'snow',
    modules: {
        toolbar: [
            ['bold', 'italic', 'underline', 'strike'],
            ['link', 'image'],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'header': [1, 2, 3, false] }],
            ['blockquote', 'code-block'],
            [{"align": []}],
            ['clean']
        ]
    },
    placeholder: 'Escreva seu email aqui...'
});

quill.on('text-change', function() {
    const text = quill.getText();
    document.getElementById('char-count').innerText = text.length + ' caracteres';
});


function clearEditor() {
    quill.setContents([]);
    document.getElementById('char-count').innerText = '0 caracteres';
}