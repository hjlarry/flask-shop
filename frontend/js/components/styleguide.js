// export default $(() => {
//   const styleGuideMenu = $('.styleguide__nav');
//   $(window).on('scroll', function () {
//     if ($(this).scrollTop() > 100) {
//       styleGuideMenu.addClass('fixed');
//     } else {
//       styleGuideMenu.removeClass('fixed');
//     }
//   });
// });
const styleGuideMenu = document.querySelector('.styleguide__nav');
window.addEventListener('scroll', () => {
  if (styleGuideMenu === null) {
    return;
  }
  if (window.scrollY > 100) {
    styleGuideMenu.classList.add('fixed');
  } else {
    styleGuideMenu.classList.remove('fixed');
  }
});
