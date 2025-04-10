const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './static/js/app/App.js',
  output: {
    path: path.resolve(__dirname, 'static/dist'),
    filename: 'app.bundle.js',
    publicPath: '/static/dist/',
        library: 'reactApp',
    libraryTarget: 'window'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './templates/index.html',
      filename: '../../templates/react_app.html'
    })
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, 'static/dist'),
    },
    compress: true,
    port: 3000,
    hot: true,
    devMiddleware: {
      writeToDisk: true, // Для сохранения файлов в Django static
    }
  }
};