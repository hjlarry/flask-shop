var E = require('wangeditor')
var editor = new E('#text-editor')
var $text1 = $('#content')
$text1.hide()
editor.customConfig.onchange = function (html) {
    $text1.val(html)
}
editor.create()
$text1.val(editor.txt.html())