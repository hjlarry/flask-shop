import './select';


$('.custom-file-input').on('click', function () {
    $('.custom-file-input').on('change', function () {
        var filename = $('.custom-file-input').val();
        $('.custom-file-label').html(filename);
    });
});
