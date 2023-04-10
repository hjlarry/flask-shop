const addresses = document.querySelectorAll('.myaddress');
addresses.forEach((el) => {
  const deleteAdressIcon = el.querySelector('.delete-icon');
  const deleteAddress = el.querySelector('.address-delete');
  const deleteAdressIcons = el.querySelectorAll('.icons');
  deleteAdressIcon.addEventListener('click', () => {
    if (deleteAddress.classList.contains('none')) {
      deleteAddress.classList.remove('none');
      deleteAdressIcons.forEach((icon) => icon.classList.add('none'));
    } else {
      deleteAddress.classList.add('none');
    }
  });

  deleteAddress.querySelector('.cancel').addEventListener('click', () => {
    deleteAddress.classList.add('none');
    deleteAdressIcons.forEach((icon) => icon.classList.remove('none'));
  });
});

// New address dropdown
const addressShow = document.querySelector('.address_show label');
const addressHide = document.querySelectorAll('.address_hide label');
const addressForm = document.querySelector('.checkout__new-address');
const addressNew = document.querySelector('#address_new');

if (addressShow !== null) {
  addressShow.addEventListener('click', () => {
    addressForm.style.display = 'block';
  });
}

addressHide.forEach((el) => {
  el.addEventListener('click', () => {
    addressForm.style.display = 'none';
  });
});

if (addressNew !== null) {
  if (addressNew.checked) {
    addressForm.style.display = 'block';
  } else {
    addressForm.style.display = 'none';
  }
}
