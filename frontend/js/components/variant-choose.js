$('.variant-picker__option').on('click', function () {
  const variantId = $(this).attr('value');
  $.ajax({
    url: `api/variant_price/${variantId}`,
    success(result) {
      $('.text-info').text(`$ ${result.price}`);
      $('.stock').text(`Stock: ${result.stock}`);
    },
  });
});
