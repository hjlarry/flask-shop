// const $toogleIcon = $('.navbar__brand__menu-toggle');
// const $mobileNav = $('nav');
// const $searchIcon = $('.mobile-search-icon');
// const $closeSearchIcon = $('.mobile-close-search');
// const $searchForm = $('.search-form');
//
// const renderNavbar = () => {
//   const $desktopLinkBar = $('.navbar__login');
//   const $mobileLinkBar = $('.navbar__menu__login');
//   const windowWidth = window.innerWidth;
//
//   if (windowWidth < 768) {
//     const $desktopLinks = $desktopLinkBar.find('a').not('.dropdown-link');
//     if ($desktopLinks.length) {
//       $searchForm.addClass('search-form--hidden');
//       $mobileNav.append('<ul class="nav navbar-nav navbar__menu__login"></ul>');
//       $desktopLinks
//         .appendTo('.navbar__menu__login')
//         .wrap('<li class="nav-item login-item"></li>')
//         .addClass('nav-link');
//       $desktopLinkBar
//         .find('li')
//         .remove();
//     }
//   } else {
//     const $mobileLinks = $mobileLinkBar.find('a').not('.dropdown-link');
//     if ($mobileLinks.length) {
//       $searchForm.removeClass('search-form--hidden');
//       $mobileLinks
//         .appendTo('.navbar__login ul')
//         .wrap('<li></li>')
//         .removeClass('nav-link');
//       $mobileLinkBar.remove();
//     }
//   }
// };
//
// renderNavbar();
// $toogleIcon
//   .on('click', (e) => {
//     $mobileNav.toggleClass('open');
//     e.stopPropagation();
//   });
// $(document)
//   .on('click', () => $mobileNav.removeClass('open'));
// $(window)
//   .on('resize', renderNavbar);
// $searchIcon
//   .on('click', () => $searchForm.removeClass('search-form--hidden'));
// $closeSearchIcon
//   .on('click', () => $searchForm.addClass('search-form--hidden'));

const toogleIcon = document.querySelector('.navbar__brand__menu-toggle');
const mobileNav = document.querySelector('nav');
const searchIcon = document.querySelector('.mobile-search-icon');
const closeSearchIcon = document.querySelector('.mobile-close-search');
const searchForm = document.querySelector('.search-form');

const renderNavbar = () => {
  const desktopLinkBar = document.querySelector('.navbar__login');
  const windowWidth = window.innerWidth;

  if (windowWidth < 768) {
    const desktopLinks = [...desktopLinkBar.querySelectorAll('a:not(.dropdown-link)')];
    if (desktopLinks.length) {
      searchForm.classList.add('search-form--hidden');
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
  }
};

if (mobileNav !== null) {
  renderNavbar();
  toogleIcon.addEventListener('click', (e) => {
    mobileNav.classList.toggle('open');
    e.stopPropagation();
  });
  document.addEventListener('click', () => mobileNav.classList.remove('open'));
  window.addEventListener('resize', renderNavbar);
}

if (searchIcon !== null) {
  searchIcon.addEventListener('click', () => searchForm.classList.remove('search-form--hidden'));
  closeSearchIcon.addEventListener('click', () => searchForm.classList.add('search-form--hidden'));
}
