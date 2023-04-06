import 'lazysizes';
import SVGInjector from 'svg-injector-2';

export const csrftoken = document.querySelector('meta[name=csrf-token]').getAttribute('content');

new SVGInjector().inject(document.querySelectorAll('svg[data-src]'));
