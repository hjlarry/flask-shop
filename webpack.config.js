var BundleTracker = require('webpack-bundle-tracker');
var MiniCssExtractPlugin = require('mini-css-extract-plugin');
var path = require('path');
var webpack = require('webpack');
var autoprefixer = require('autoprefixer');
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var resolve = path.resolve.bind(path, __dirname);

var extractCssPlugin;
var manifestRevisionPlugin;
var fileLoaderPath;
var output;

// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');

// Development asset host (webpack dev server)
const publicHost = debug ? 'http://localhost:2992' : '';
const rootAssetPath = path.join(__dirname, 'flaskshop', 'assets');

output = {
    path: resolve('flaskshop/static/build/'),
    filename: '[name].[hash].js',
    chunkFilename: '[name].[hash].js',
    publicPath: `${publicHost}/static/build/`,
};
fileLoaderPath = 'file-loader?name=[name].[ext]';
extractCssPlugin = new MiniCssExtractPlugin({
    filename: '[name].[hash].css',
    chunkFilename: '[name].[hash].css',
});
manifestRevisionPlugin = new ManifestRevisionPlugin(path.join(__dirname, 'flaskshop', 'webpack', 'manifest.json'), {
    rootAssetPath,
    ignorePaths: ['/js', '/scss', '/css', '/fonts', '/images'],
});

var bundleTrackerPlugin = new BundleTracker({
    filename: 'webpack-bundle.json'
});

var providePlugin = new webpack.ProvidePlugin({
    $: 'jquery',
    jQuery: 'jquery',
    'window.jQuery': 'jquery',
    'Popper': 'popper.js',
    'query-string': 'query-string'
});

var config = {
    entry: {
        storefront: './flaskshop/assets/js/storefront.js'
    },
    output: output,
    devServer: {
        headers: {'Access-Control-Allow-Origin': '*'},
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            'sourceMap': true
                        }
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            'sourceMap': true,
                            'plugins': function () {
                                return [autoprefixer];
                            }
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            'sourceMap': true
                        }
                    }
                ]
            },
            {
                test: /\.(eot|otf|png|svg|jpg|ttf|woff|woff2)(\?v=[0-9.]+)?$/,
                loader: fileLoaderPath,
                include: [
                    resolve('node_modules'),
                    resolve('flaskshop/assets/fonts'),
                    resolve('flaskshop/assets/images'),
                ]
            }
        ]
    },
    plugins: [
        bundleTrackerPlugin,
        extractCssPlugin,
        providePlugin,
        manifestRevisionPlugin
    ],
    resolve: {
        alias: {
            'jquery': resolve('node_modules/jquery/dist/jquery.js'),
        }
    }
};

module.exports = config;
