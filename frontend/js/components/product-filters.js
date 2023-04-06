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
