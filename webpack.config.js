const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');
const glob = require('glob');

const resolve = path.resolve.bind(path, __dirname);
// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');


// Development asset host (webpack dev server)
const publicHost = debug ? 'http://localhost:2992' : '';
const fileLoaderPath = 'file-loader?name=[name].[ext]';

const extractCssPlugin = new MiniCssExtractPlugin({
  filename: '[name].css',
  chunkFilename: '[name].css',
});

const bundleTrackerPlugin = new BundleTracker({
  filename: 'webpack-bundle.json',
});

const providePlugin = new webpack.ProvidePlugin({
  $: 'jquery',
  jQuery: 'jquery',
  'window.jQuery': 'jquery',
  Popper: 'popper.js',
  'query-string': 'query-string',
});

const output = {
  path: resolve('flaskshop/static/build/'),
  filename: '[name].js',
  chunkFilename: '[name].js',
  publicPath: `${publicHost}/static/build/`,
};

const entry_items = glob.sync('./flaskshop/assets/js/dashboard/**/*.js').reduce(
  (entries, entry) => Object.assign(entries, { [entry.split('/').splice(-2, 2).join('/').replace('.js', '')]: entry }), {});
entry_items['storefront'] = './flaskshop/assets/js/storefront.js';

const config = {
  entry: entry_items,
  output,
  devServer: {
    headers: { 'Access-Control-Allow-Origin': '*' },
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              sourceMap: true,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              sourceMap: true,
              plugins() {
                return [autoprefixer];
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
            },
          },
        ],
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(eot|otf|png|svg|jpg|ttf|woff|woff2)(\?v=[0-9.]+)?$/,
        loader: fileLoaderPath,
        include: [
          resolve('node_modules'),
          resolve('flaskshop/assets/fonts'),
          resolve('flaskshop/assets/images'),
        ],
      },
    ],
  },
  plugins: [
    bundleTrackerPlugin,
    extractCssPlugin,
    providePlugin,
  ],
  resolve: {
    alias: {
      jquery: resolve('node_modules/jquery/dist/jquery.js'),
      'react': resolve('node_modules/react/dist/react.min.js'),
      'react-dom': resolve('node_modules/react-dom/dist/react-dom.min.js'),
    },
  },
};

module.exports = config;

