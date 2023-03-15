const {createEditor, createToolbar} = window.wangEditor

const rawTextarea = document.getElementById('content')
const editorConfig = {
    placeholder: 'Type here...',
    onChange(editor) {
        const html = editor.getHtml()
        rawTextarea.innerText = html
    }
}

const editor = createEditor({
    selector: '#text-editor',
    html: rawTextarea.innerText || '<p><br></p>',
    config: editorConfig,
    mode: 'default', // or 'simple'
})

const toolbarConfig = {}

const toolbar = createToolbar({
    editor,
    selector: '#toolbar-container',
    config: toolbarConfig,
    mode: 'default', // or 'simple'
})