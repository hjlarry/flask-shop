export default $(() => {
  const $deleteAdressIcons = $('.icons');
  const $deleteAdressIcon = $('.delete-icon');
  const $deleteAddress = $('.address-delete');

  $deleteAdressIcon.on('click', () => {
    if ($deleteAddress.hasClass('none')) {
      $deleteAddress.removeClass('none');
      $deleteAdressIcons.addClass('none');
    } else {
      $deleteAddress.addClass('none');
    }
  });

  $deleteAddress.find('.cancel').on('click', () => {
    $deleteAddress.addClass('none');
    $deleteAdressIcons.removeClass('none');
  });

  // New address dropdown
  const $addressShow = $('.address_show label');
  const $addressHide = $('.address_hide label');
  const $addressForm = $('.checkout__new-address');
  const $initialValue = $('#address_new').prop('checked');
  $addressShow.on('click', () => {
    $addressForm.slideDown('slow');
  });
  $addressHide.on('click', () => {
    $addressForm.slideUp('slow');
  });
  if ($initialValue) {
    $addressForm.slideDown(0);
  } else {
    $addressForm.slideUp(0);
  }
});
