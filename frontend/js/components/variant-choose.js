$('.variant-picker__option').on('click', function () {
  const variantId = $(this).attr('value');
  fetch(`api/variant_price/${variantId}`)
    .then((response) => response.json())
    .then((result) => {
      $('.text-info').text(`$ ${result.price}`);
      $('.stock').text(`Stock: ${result.stock}`);
    })
    .catch((error) => console.error(error));
});
