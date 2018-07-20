export const $cartDropdown = $('.cart-dropdown');
export const $cartIcon = $('.cart__icon');


export default $(document).ready((e) => {
  // Cart dropdown
  $('.navbar__brand__cart').hover((e) => {
    $cartDropdown.addClass('show');
    $cartIcon.addClass('hover');
  }, (e) => {
    $cartDropdown.removeClass('show');
    $cartIcon.removeClass('hover');
  });
});
