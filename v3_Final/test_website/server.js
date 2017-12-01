var express = require('express');
var path = require('path');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');


// database
mongoose.connect('mongodb://localhost/db_name');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function (callback) {
  console.log("database connected");
});

// view engine setup
var app = express();
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');
app.use(express.static(path.join(__dirname, '/public')));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
require('./routes/index')(app);


// catch 404 and forward to error page
//app.use(function(req, res, next) {
//    res.render('error', {message: 'This is not a valid page.'});
//});

module.exports = app;