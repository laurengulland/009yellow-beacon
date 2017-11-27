const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');


// database
mongoose.connect('mongodb://localhost/db_name');
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function (callback) {
  console.log("database connected");
});

// view engine setup
const app = express();
app.set('views', path.join(__dirname, 'views'));
//app.set('view engine', 'hbs');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
require('./routes/index')(app);


// catch 404 and forward to error page
app.use(function(req, res, next) {
    res.render('error', {message: 'This is not a valid page.'});
});


module.exports = app;