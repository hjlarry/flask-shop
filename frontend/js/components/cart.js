const csrftoken = document.querySelector('meta[name=csrf-token]').getAttribute('content');
const cartLine = document.querySelectorAll('.cart__line');
const total = document.querySelector('.cart-total span');
const cartBadge = document.querySelector('.navbar__brand__cart .badge');
const removeProductSuccess = document.querySelector('.remove-product-alert');

function onQuantityInputChanged(event) {
  const $quantityInput = event.target;
  if ($quantityInput.value > $quantityInput.getAttribute('max')) {
    $quantityInput.value = $quantityInput.getAttribute('max');
  }
  if ($quantityInput.value < $quantityInput.getAttribute('min')) {
    $quantityInput.value = $quantityInput.getAttribute('min');
  }

  const cartFormUrl = this.querySelector('.form-cart').getAttribute('action');
  const $subtotal = this.querySelector('.cart-item-price p');

  const formData = new URLSearchParams();
  formData.append('quantity', $quantityInput.value);
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
      $subtotal.innerHTML = response.subtotal;
      total.innerHTML = response.total;
      cartBadge.innerHTML = response.cart.numItems;
    })
    .catch((error) => console.error(error));
}

function onRemoveIconClicked() {
  const cartFormUrl = this.closest('.cart__line').querySelector('.form-cart').getAttribute('action');
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
        this.closest('.cart__line').style.display = 'none';
        total.innerHTML = response.total;
        cartBadge.innerHTML = response.cart.numItems;
        removeProductSuccess.classList.remove('d-none');
      } else {
        window.location.reload();
      }
    })
    .catch((error) => console.error(error));
}

const closeMsg = document.querySelector('.close-msg');
if (closeMsg !== null) {
  closeMsg.addEventListener('click', () => {
    removeProductSuccess.classList.add('d-none');
  });
}

cartLine.forEach((line) => {
  const quantityInput = line.querySelector('#id_quantity');
  const deleteIcon = line.querySelector('.cart-item-delete');

  quantityInput.addEventListener('change', onQuantityInputChanged.bind(line));
  deleteIcon.addEventListener('click', onRemoveIconClicked);
});
