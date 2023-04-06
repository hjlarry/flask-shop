const toogleIcon = document.querySelector('.navbar__brand__menu-toggle');
const mobileNav = document.querySelector('nav');

const renderNavbar = () => {
  const desktopLinkBar = document.querySelector('.navbar__login');
  const desktopLinks = [...desktopLinkBar.querySelectorAll('a:not(.dropdown-link)')];
  if (desktopLinks.length) {
    const mobileLinks = document.createElement('ul');
    mobileLinks.classList.add('nav', 'navbar-nav', 'navbar__menu__login');
    desktopLinks.forEach((link) => {
      const loginItem = document.createElement('li');
      const navLink = document.createElement('a');
      navLink.innerHTML = link.innerHTML;
      navLink.classList.add('nav-link');
      loginItem.classList.add('nav-item', 'login-item');
      loginItem.appendChild(navLink);
      mobileLinks.appendChild(loginItem);
    });
    desktopLinkBar.innerHTML = '';
    mobileNav.appendChild(mobileLinks);
  }
};

if (mobileNav !== null && window.innerWidth < 768) {
  renderNavbar();
  toogleIcon.addEventListener('click', (e) => {
    mobileNav.classList.toggle('open');
    e.stopPropagation();
  });
  document.addEventListener('click', () => mobileNav.classList.remove('open'));
  window.addEventListener('resize', renderNavbar);
} else if (toogleIcon !== null) {
  toogleIcon.classList.add('d-none');
}

const searchIcon = document.querySelector('.mobile-search-icon');
const searchForm = document.querySelector('.search-form');
const closeSearchIcon = document.querySelector('.mobile-close-search');
if (searchIcon !== null) {
  searchIcon.addEventListener('click', () => searchForm.classList.remove('search-form--hidden'));
  closeSearchIcon.addEventListener('click', () => searchForm.classList.add('search-form--hidden'));
  if (window.innerWidth < 768) {
    searchForm.classList.add('search-form--hidden');
  }
}
