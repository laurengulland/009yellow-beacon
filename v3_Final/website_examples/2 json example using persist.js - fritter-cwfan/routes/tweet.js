var express = require('express');
var router = express.Router();
var Fritter = require('../fritter.js');

var getAllTweetsJson = function() {

    return tweetsList;
}

/* gets all tweets */
router.get('/', function(req, res, next) {
    var allTweetTuples = Fritter.getAllTweetTuples();
    var tweetsList = [];
    var user = Fritter.getUser();
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
    res.render('index', {user: user, tweetsList: tweetsList});
});

/* post a tweet and author */
router.post('/post', function(req, res, next) {
    var currentAuthor = Fritter.getUser();
    var tweetBody = req.body.tweetInput;
    var tweetTuple = Fritter.addTweet(currentAuthor, tweetBody);
    res.redirect('back');
});


/* delete tweet */
router.post('/:tweetid', function(req, res, next) {
    var currentAuthor = Fritter.getUser();
    var tweetKey = req.body.tweetid;
    Fritter.deleteTweet(currentAuthor, tweetKey);
    res.redirect('back');
});
module.exports = router;
