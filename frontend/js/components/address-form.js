export default $(function () {
    let $deleteAdressIcons = $('.icons');
    let $deleteAdressIcon = $('.delete-icon');
    let $deleteAddress = $('.address-delete');

    $deleteAdressIcon.on('click', function () {
        if ($deleteAddress.hasClass('none')) {
            $deleteAddress.removeClass('none');
            $deleteAdressIcons.addClass('none');
        } else {
            $deleteAddress.addClass('none');
        }
    });

    $deleteAddress.find('.cancel').on('click', function () {
        $deleteAddress.addClass('none');
        $deleteAdressIcons.removeClass('none');
    });

    // New address dropdown

    let $addressShow = $('.address_show label');
    let $addressHide = $('.address_hide label');
    let $addressForm = $('.checkout__new-address');
    let $initialValue = $('#address_new').prop('checked');
    $addressShow.on('click', function () {
        $addressForm.slideDown('slow');
    });
    $addressHide.on('click', function () {
        $addressForm.slideUp('slow');
    });
    if ($initialValue) {
        $addressForm.slideDown(0);
    } else {
        $addressForm.slideUp(0);
    }
});
