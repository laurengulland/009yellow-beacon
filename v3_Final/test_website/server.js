var express = require('express');
var path = require('path');
var mongoose = require('mongoose');
var mubsub = require('mubsub');
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


// mubsub
var client = mubsub(url);
var channel = client.channel('test');
client.on('error', console.error);
channel.on('error', console.error);
//subscription = channel.subscribe(function(doc) {
//   app.get()
//});


// catch 404 and forward to error page
//app.use(function(req, res, next) {
//    res.render('error', {message: 'This is not a valid page.'});
//});

module.exports = app;