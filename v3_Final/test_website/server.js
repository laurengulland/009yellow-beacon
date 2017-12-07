var express = require('express');
var path = require('path');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');

// database
var url = 'mongodb://localhost/coordinate';
mongoose.connect(url);
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


module.exports = app;