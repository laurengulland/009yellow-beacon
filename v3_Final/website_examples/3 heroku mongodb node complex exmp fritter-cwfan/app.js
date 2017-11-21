var express = require('express');
var path = require('path');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('express-session');


// database
var mongoose = require('mongoose');
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost/cwfan-fritter');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function (callback) {
  console.log("database connected");
});

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');


app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(session({ secret: 'dimsum', 
    saveUninitialized: true,
    resave: true }));

require('./routes/loginRoute')(app);
require('./routes/tweetRoute')(app);
require('./routes/userRoute')(app);

// catch 404 and forward to error page
app.use(function(req, res, next) {
    res.render('error', {message: 'This is not a valid page.'});
});


module.exports = app;
