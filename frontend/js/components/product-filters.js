// $('.filters-menu').on('click', () => {
//   const menuContainer = $('.filters-menu__body');
//   if (menuContainer.hasClass('d-none')) {
//     menuContainer.removeClass('d-none');
//   } else {
//     menuContainer.addClass('d-none');
//   }
// });
//
// $('.filter-section__header').on('click', (event) => {
//   const $target = $(event.currentTarget).parent();
//   if ($target.attr('aria-expanded') === 'true') {
//     $target.attr('aria-expanded', 'false').addClass('filter-section--closed');
//   } else {
//     $target.attr('aria-expanded', 'true').removeClass('filter-section--closed');
//   }
// });
//
// $('.filters-toggle').on('click', () => {
//   $('.filters-menu__body').toggleClass('d-none');
// });

document.querySelectorAll('.filter-section__header').forEach((header) => {
  header.addEventListener('click', (event) => {
    const target = event.currentTarget.parentElement;
    if (target.getAttribute('aria-expanded') === 'true') {
      target.setAttribute('aria-expanded', 'false');
      target.classList.add('filter-section--closed');
    } else {
      target.setAttribute('aria-expanded', 'true');
      target.classList.remove('filter-section--closed');
    }
  });
});

const filterToggle = document.querySelector('.filters-toggle');
if (filterToggle !== null) {
  filterToggle.addEventListener('click', () => {
    const menuContainer = document.querySelector('.filters-menu__body');
    menuContainer.classList.toggle('d-none');
  });
}
