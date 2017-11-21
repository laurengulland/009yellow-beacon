var Frit = require('../models/fritter');

/*
 * helper function that checks for errors and redirects the page
 * @param req the request the user sends
 * @param res the response that the user recieves
*/
var callback = function (res, err) {
    if (err) {
        console.log(err);
    } else {
        res.redirect('back');
    }
};

/*
 * the module that represents the tweets controller/routing
 * handles the req and res by calling our model methods
*/
module.exports = {
    

    /*
     * adds a tweet to the db
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    addTweet: function (req, res) {
        var nameID = req.session.userID;
        var content = req.body.tweetInput;
        var tweet = new Frit({ content: content, author: nameID });
        tweet.save(function(err) {
            return callback(res, err);
        });
    },

    /*
     * deletes a tweet from the db
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    deleteTweet: function (req, res) {
        var tweetID = req.headers.tweetid;
        Frit.remove({ _id: tweetID }, function(err) {
            if (err) {
                return console.log(err);
            }
            return res.redirect('back');
        });
    },

    /*
     * retweets, which essentially adds a tweet to the db
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    retweet: function (req, res) {
        var currentTweeterID = req.session.userID;
        var tweeter = req.body.tweetAuthor;
        var tweetText = req.body.tweet;
        Frit.retweet(currentTweeterID, tweeter, tweetText, function(err) {
            return callback(res, err);
        });
    }

};