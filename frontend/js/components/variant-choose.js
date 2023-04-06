document.querySelectorAll('.variant-picker__option').forEach((option) => {
  option.addEventListener('click', function () {
    const variantId = this.getAttribute('value');
    fetch(`api/variant_price/${variantId}`)
      .then((response) => response.json())
      .then((result) => {
        document.querySelector('.text-info').innerHTML = `$ ${result.price}`;
        document.querySelector('.stock').innerHTML = `Stock: ${result.stock}`;
      })
      .catch((error) => console.error(error));
  });
});
