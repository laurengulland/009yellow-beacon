var UserController = require('./userControl');
var FritterController = require('./fritterControl');

module.exports = function (app) {
    app.get('/', function (req, res) {
        // already logged in
        if (req.session.userId !== undefined) {
            return res.redirect('/allTweets');
               
        // not logged in, render homepage
        }
        return res.render('login', {name: "express"});
    });
    
    app.get('/allTweets', function(req, res) {
        UserController.getTweets(req, res, false);
    });
        
    app.get('/allFollowingTweets', function(req, res) {
        UserController.getTweets(req, res, true);
    });

    app.post('/addTweet', function(req, res) {
        FritterController.addTweet(req, res);
    });

    app.post('/retweet', function(req, res) {
        FritterController.retweet(req, res);
    }); 

};
             