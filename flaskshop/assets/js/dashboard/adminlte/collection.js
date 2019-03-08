import './select';


$('.custom-file-input').click(function () {
    $('.custom-file-input').change(function () {
        var filename = $('.custom-file-input').val();
        $('.custom-file-label').html(filename);
    });
});