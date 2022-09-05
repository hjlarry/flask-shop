export default $(document).ready((e) => {
    let $deleteAdressIcons = $('.icons');
    let $deleteAdressIcon = $('.delete-icon');
    let $deleteAddress = $('.address-delete');

    $deleteAdressIcon.on('click', (e) => {
        if ($deleteAddress.hasClass('none')) {
            $deleteAddress.removeClass('none');
            $deleteAdressIcons.addClass('none');
        } else {
            $deleteAddress.addClass('none');
        }
    });

    $deleteAddress.find('.cancel').on('click', (e) => {
        $deleteAddress.addClass('none');
        $deleteAdressIcons.removeClass('none');
    });

    // New address dropdown

    let $addressShow = $('.address_show label');
    let $addressHide = $('.address_hide label');
    let $addressForm = $('.checkout__new-address');
    let $initialValue = $('#address_new').prop('checked');
    $addressShow.click((e) => {
        $addressForm.slideDown('slow');
    });
    $addressHide.click((e) => {
        $addressForm.slideUp('slow');
    });
    if ($initialValue) {
        $addressForm.slideDown(0);
    } else {
        $addressForm.slideUp(0);
    }
});
