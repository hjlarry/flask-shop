/*
 * Main Javascript file for flaskshop.
 *
 * This file bundles all of your javascript together using webpack.
 */
import 'jquery';
import 'jquery.cookie';
import 'bootstrap';

import '../scss/storefront.scss';

import './components/navbar';
import './components/cart';
import './components/sorter';
import './components/variant-picker';
import './components/language-picker';
import './components/footer';
import './components/product-filters';
import './components/address-form';
import './components/password-input';
import './components/styleguide';
import './components/misc';
// JavaScript modules
// window.$ = window.jQuery = require('jquery');
// require('font-awesome-webpack');
// require('bootstrap');
// require('sweetalert');
window.axios = require('axios');
window.axios.defaults.headers.common = {
    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
    'X-Requested-With': 'XMLHttpRequest'
};

// Your own code
// require('./plugins.js');
// require('./script.js');
// require('./storefront.js');

