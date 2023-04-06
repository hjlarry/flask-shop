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
