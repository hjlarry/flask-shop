export default $(function () {
    let styleGuideMenu = $('.styleguide__nav');
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 100) {
            styleGuideMenu.addClass('fixed');
        } else {
            styleGuideMenu.removeClass('fixed');
        }
    });
});
