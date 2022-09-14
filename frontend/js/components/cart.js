export default $(function () {
    let $cartLine = $('.cart__line');
    let $total = $('.cart-total span');
    let $cartBadge = $('.navbar__brand__cart .badge');
    let $closeMsg = $('.close-msg');
    let $removeProductSuccess = $('.remove-product-alert');
    $closeMsg.on('click', (e) => {
        $removeProductSuccess.addClass('d-none');
    });
    $cartLine.each(function () {
        let $quantityInput = $(this).find('#id_quantity');
        let cartFormUrl = $(this).find('.form-cart').attr('action');
        let $subtotal = $(this).find('.cart-item-price p');
        let $deleteIcon = $(this).find('.cart-item-delete');
        $(this).on('change', $quantityInput, (e) => {
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
                }
            });
        });
        $deleteIcon.on('click', (e) => {
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
                        location.reload();
                    }
                }
            });
        });
    });


    if ($.cookie('alert') === 'true') {
        $removeProductSuccess.removeClass('d-none');
        $.cookie('alert', 'false', { path: '/cart' });
    }
});
