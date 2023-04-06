// export const $cartDropdown = $('.cart-dropdown');
// export const $cartIcon = $('.cart__icon');
//
// export default $(() => {
//   // Cart dropdown
//   $('.navbar__brand__cart').on('mouseenter', () => {
//     $cartDropdown.addClass('show');
//     $cartIcon.addClass('hover');
//   }).on('mouseleave', () => {
//     $cartDropdown.removeClass('show');
//     $cartIcon.removeClass('hover');
//   });
// });

const cartDropdown = document.querySelector('.cart-dropdown');
const cartIcon = document.querySelector('.cart__icon');

// TODO 不需要foreach了  就这一个
document.querySelectorAll('.navbar__brand__cart').forEach((navBarCart) => {
  navBarCart.addEventListener('mouseenter', () => {
    cartDropdown.classList.add('show');
    cartIcon.classList.add('hover');
  });
  navBarCart.addEventListener('mouseleave', () => {
    cartDropdown.classList.remove('show');
    cartIcon.classList.remove('hover');
  });
});
