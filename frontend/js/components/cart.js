export default $(() => {
  const $cartLine = $('.cart__line');
  const $total = $('.cart-total span');
  const $cartBadge = $('.navbar__brand__cart .badge');
  const $closeMsg = $('.close-msg');
  const $removeProductSuccess = $('.remove-product-alert');
  $closeMsg.on('click', () => {
    $removeProductSuccess.addClass('d-none');
  });
  $cartLine.each(function () {
    const $quantityInput = $(this).find('#id_quantity');
    const cartFormUrl = $(this).find('.form-cart').attr('action');
    const $subtotal = $(this).find('.cart-item-price p');
    const $deleteIcon = $(this).find('.cart-item-delete');
    $(this).on('change', $quantityInput, () => {
      if ($quantityInput.val() > $quantityInput.attr('max')) {
        $quantityInput.val($quantityInput.attr('max'));
      }
      if ($quantityInput.val() < $quantityInput.attr('min')) {
        $quantityInput.val($quantityInput.attr('min'));
      }
      $.ajax({
        url: cartFormUrl,
        method: 'POST',
        data: { quantity: $quantityInput.val() },
        success: (response) => {
          $subtotal.html(response.subtotal);
          $total.html(response.total);
          $cartBadge.html(response.cart.numItems);
        },
        error: (response) => {
          console.log(response, 9876);
        },
      });
    });
    $deleteIcon.on('click', function () {
      $.ajax({
        url: cartFormUrl,
        method: 'POST',
        data: { quantity: 0 },
        success: (response) => {
          if (response.cart.numLines >= 1) {
            $(this).fadeOut();
            $total.html(response.total);
            $cartBadge.html(response.cart.numItems);
            $removeProductSuccess.removeClass('d-none');
          } else {
            $.cookie('alert', 'true', { path: '/cart' });
            window.location.reload();
          }
        },
      });
    });
  });

  if ($.cookie('alert') === 'true') {
    $removeProductSuccess.removeClass('d-none');
    $.cookie('alert', 'false', { path: '/cart' });
  }
});
