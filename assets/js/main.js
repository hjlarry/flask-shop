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

// Your own code
require('./plugins.js');
require('./script.js');
