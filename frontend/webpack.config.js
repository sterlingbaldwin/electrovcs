/* global __dirname */
var path = require("path");

module.exports = {
    entry: ["babel-polyfill", "./src/index.js"],
    devtool: 'source-map',
    mode: 'development',
    output: {
        path: __dirname + "/dist",
        filename: "Bundle.js"
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            presets: [
                                'react',
                                ['env', {
                                    "targets": {
                                        "uglify": false
                                    }
                                }]
                            ]
                        }
                    }
                ]
            },
            {
                test: /\.css$/,
                use: [
                    { loader: "style-loader" },
                    { loader: "css-loader" }
                ]
            },
            {
                test: /\.scss$/,
                use: [{
                    loader: "style-loader" // creates style nodes from JS strings 
                }, {
                    loader: "css-loader", // translates CSS into CommonJS 
                }, {
                    loader: "sass-loader", // compiles Sass to CSS 
                    options: {
                        includePaths: ["src"]
                    }
                }]
            }
        ]
    }
};
