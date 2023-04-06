// import 'lazysizes';
// import SVGInjector from 'svg-injector-2';
//
// export const csrftoken = $('meta[name=csrf-token]').attr('content');
//
// export default $(() => {
//   new SVGInjector().inject(document.querySelectorAll('svg[data-src]'));
//
//   // Open tab from the link
//   const { hash } = window.location;
//   $(`.nav-tabs a[href="${hash}"]`).tab('show');
//
//   // Preload all images
//   window.lazySizesConfig = window.lazySizesConfig || {};
//   window.lazySizesConfig.preloadAfterLoad = true;
// });
import 'lazysizes';
import SVGInjector from 'svg-injector-2';

export const csrftoken = document.querySelector('meta[name=csrf-token]').getAttribute('content');

new SVGInjector().inject(document.querySelectorAll('svg[data-src]'));
