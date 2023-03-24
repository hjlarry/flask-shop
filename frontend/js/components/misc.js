import 'lazysizes';
import SVGInjector from 'svg-injector-2';

export const csrftoken = $('meta[name=csrf-token]').attr('content');

export default $(() => {
  function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  new SVGInjector().inject(document.querySelectorAll('svg[data-src]'));

  $.ajaxSetup({
    beforeSend(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    },
  });

  // Open tab from the link

  const { hash } = window.location;
  $(`.nav-tabs a[href="${hash}"]`).tab('show');

  // Preload all images
  window.lazySizesConfig = window.lazySizesConfig || {};
  window.lazySizesConfig.preloadAfterLoad = true;
});
