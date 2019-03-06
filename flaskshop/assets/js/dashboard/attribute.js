import './select';

var add_btn = $("#add_entry");
var index = add_btn.data('index');
var field = add_btn.data('field');
add_btn.click(function () {
    var index_field = field + '-' + index;
    var html = '<div class="input-group input-group-sm field-list-item"><input type="text" class="form-control" id="' + index_field + '" name="' + index_field + '" ><span class="input-group-append"><button type="button" class="btn btn-info btn-flat" id="item_del">Remove Entry</button></span></div>';
    $('#field_list').append(html);
    index += 1;
});
$('#field_list').on('click', '#item_del', function () {
    $(this).parent().parent().remove();
});