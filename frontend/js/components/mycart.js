export const $cartDropdown = $('.cart-dropdown');
export const $cartIcon = $('.cart__icon');


export default $(function () {
  // Cart dropdown
  $('.navbar__brand__cart').on("mouseenter", function () {
    $cartDropdown.addClass('show');
    $cartIcon.addClass('hover');
  }).on("mouseleave", function () {
    $cartDropdown.removeClass('show');
    $cartIcon.removeClass('hover');
  });
});
