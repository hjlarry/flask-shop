import { csrftoken } from './misc';

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
    const currentLine = $(this);
    $(this).on('change', $quantityInput, () => {
      if ($quantityInput.val() > $quantityInput.attr('max')) {
        $quantityInput.val($quantityInput.attr('max'));
      }
      if ($quantityInput.val() < $quantityInput.attr('min')) {
        $quantityInput.val($quantityInput.attr('min'));
      }
      const formData = new URLSearchParams();
      formData.append('quantity', $quantityInput.val());
      fetch(cartFormUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRF-Token': csrftoken,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          $subtotal.html(response.subtotal);
          $total.html(response.total);
          $cartBadge.html(response.cart.numItems);
        })
        .catch((error) => console.error(error));
    });
    $deleteIcon.on('click', () => {
      const formData = new URLSearchParams();
      formData.append('quantity', 0);
      fetch(cartFormUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRF-Token': csrftoken,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          if (response.cart.numLines >= 1) {
            currentLine.fadeOut();
            $total.html(response.total);
            $cartBadge.html(response.cart.numItems);
            $removeProductSuccess.removeClass('d-none');
          } else {
            window.location.reload();
          }
        })
        .catch((error) => console.error(error));
    });
  });
});
