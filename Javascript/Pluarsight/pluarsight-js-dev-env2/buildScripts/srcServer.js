var express = require( 'express');
var path = require('path');
var open = require('open');

// added for webpack
// import webpack from 'webpack';
// import config from '../webpack.config.dev';

/* eslint-disable no-console */

const port = 3000;
const app = express();

// added for webpack
// const compiler = webpack(config);

// added for webpack
// app.use(require('webpack-dev-middleware')(compiler, {
//     noInfo: true,
//     publicPath: config.output.publicPath
// }));

// routing
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '../src/index.html'));
});

// app.get('/users', function(req, res) {
//     res.json([
//         {"id": 1, "firstName":"Bob", "lastName":"Smith","email":"s@gmail.com"},
//         {"id": 1, "firstName":"Tammy", "lastName":"Notron","email":"n@gmail.com"},
//         {"id": 1, "firstName":"Tina", "lastName":"Lee","email":"l@gmail.com"}
//     ]);
// });

// listening
app.listen(port, function(err) {
    if (err) {
        console.log(err);
    } else {
        open('http://localhost:' + port);
    }
});
