export const $cartDropdown = $('.cart-dropdown');
export const $cartIcon = $('.cart__icon');

export default $(() => {
  // Cart dropdown
  $('.navbar__brand__cart').on('mouseenter', () => {
    $cartDropdown.addClass('show');
    $cartIcon.addClass('hover');
  }).on('mouseleave', () => {
    $cartDropdown.removeClass('show');
    $cartIcon.removeClass('hover');
  });
});
