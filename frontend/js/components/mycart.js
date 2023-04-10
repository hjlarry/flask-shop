const cartDropdown = document.querySelector('.cart-dropdown');
const cartIcon = document.querySelector('.cart__icon');
const navBarCart = document.querySelector('.navbar__brand__cart');

if (navBarCart !== null) {
  navBarCart.addEventListener('mouseenter', () => {
    cartDropdown.classList.add('show');
    cartIcon.classList.add('hover');
  });
  navBarCart.addEventListener('mouseleave', () => {
    cartDropdown.classList.remove('show');
    cartIcon.classList.remove('hover');
  });
}
