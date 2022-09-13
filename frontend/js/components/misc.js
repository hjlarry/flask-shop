import 'lazysizes';
import SVGInjector from 'svg-injector-2';

export const getAjaxError = (response) => {
    let ajaxError = JSON.parse(response.responseText).error.quantity;
    return ajaxError;
};
export const csrftoken = $('meta[name=csrf-token]').attr('content');

export default $(function () {
    function csrfSafeMethod(method) {
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }

    new SVGInjector().inject(document.querySelectorAll('svg[data-src]'));

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    // Open tab from the link

    let hash = window.location.hash;
    $('.nav-tabs a[href="' + hash + '"]').tab('show');

    // // Preload all images
    // window.lazySizesConfig.preloadAfterLoad = true;
});
