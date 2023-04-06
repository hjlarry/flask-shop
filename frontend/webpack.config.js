const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const path = require('path');

const resolve = path.resolve.bind(path, __dirname);
// take debug mode from the environment
const debug = process.env.NODE_ENV === 'production' ? 'production' : 'development';

const extractCssPlugin = new MiniCssExtractPlugin({
    filename: '[name].css',
    chunkFilename: '[name].css',
});

const output = {
    path: resolve('../flaskshop/static/build/'),
    filename: '[name].js',
    chunkFilename: '[name].js'
};

const entry_items = {'storefront': './js/storefront.js'}

const config = {
    mode: debug,
    entry: entry_items,
    output,
    devServer: {
        headers: {'Access-Control-Allow-Origin': '*'},
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
                            postcssOptions: {
                                plugins: [require('autoprefixer')({})]
                            }
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
                type: "javascript/auto",
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            esModule: false,
                            name: '[name].[ext]'
                        },
                    },
                ],
                include: [
                    resolve('node_modules'),
                    resolve('fonts'),
                    resolve('images'),
                ],
            },
        ],
    },
    plugins: [
        extractCssPlugin,
    ],
    optimization: {
        minimizer: [new TerserPlugin({
            extractComments: false,
            terserOptions: {
                format: {
                    comments: false,
                },
            },
        })],
    },
    performance: {
        hints: false,
        maxEntrypointSize: 512000,
        maxAssetSize: 512000
    },
};

module.exports = config;
