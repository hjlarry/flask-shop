/*
 * Main Javascript file for flaskshop.
 *
 * This file bundles all of your javascript together using webpack.
 */

// JavaScript modules
window.$ = window.jQuery = require('jquery');
require('font-awesome-webpack');
require('bootstrap');
require('sweetalert');
window.axios = require('axios');
window.axios.defaults.headers.common = {
    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
    'X-Requested-With': 'XMLHttpRequest'
};

// Your own code
require('./plugins.js');
require('./script.js');
