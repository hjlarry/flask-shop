export default $(() => {
  const navbarHeight = $('.navbar').outerHeight(true);
  const footerHeight = $('.footer').outerHeight(true);
  const windowHeight = $(window).height();
  $('.maincontent').css('min-height', windowHeight - navbarHeight - footerHeight);
  $('#carousel-example-generic').carousel('cycle');
});
