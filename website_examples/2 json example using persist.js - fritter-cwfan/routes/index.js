var express = require('express');
var router = express.Router();
var Fritter = require('../fritter.js');


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('login', { user: 'Express' });
});


/* log in */
router.post('/loggedin', function(req, res, next) {
    var newUser = req.body.userLogin;
    Fritter.switchUser(newUser);
    var allTweetTuples = Fritter.getAllTweetTuples();
    var tweetsList = [];
    for (var i = 0; i < allTweetTuples.length; i++) {
        var tuple = allTweetTuples[i];
        var isCurrent = Fritter.getUser() === tuple[1] ? true : false;
        tweetsList.push({
            tweetID: tuple[0],
            tweetAuthor: tuple[1],
            tweet: tuple[2],
            isCurrentUser: isCurrent
        });
    }
    res.render('index', {user: newUser, tweetsList: tweetsList});
});

/* log out */
router.post('/logout', function(req, res, next) {
    res.render('login', {user: 'Express'});
});

module.exports = router;
