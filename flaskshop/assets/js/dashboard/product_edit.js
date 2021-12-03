import './select';

$('#field_list').on('click', '#item_del', function () {
    $(this).parent().remove();
});