var User = require('../models/user');

module.exports = function (app) {
    app.get('/', function (req, res) {
        // already logged in
        if (req.session.userId !== undefined) {
            return res.redirect('/allTweets');
               
        // not logged in, render homepage
        }
        return res.render('login', {name: "express"});
    });
    
    app.get('/addDescription', function(req, res) {
        var error = req.query.error;
        var name = req.session.name;

        if (name === undefined) {
            return res.render('error', {message: "Please log in"});
        }

        User.findOne({ name: name }, function (err, user) {
            if (err || user === null) {
                console.error(err);
                res.render('error', {message: "Please try again"});
            } else {
                User.getAllTweets(function (err, tweets) {
                    if (err) {
                        console.error(err);
                        res.render('error', {message: "Please try again"});
                    } else {
                        res.render('index', {user: name, tweetsList: tweets});
                    }
                });   
            }
        });
    });
        
    app.get('/allQueens', function(req, res) {
        UserController.getTweets(req, res, true);
    });

    app.post('/allQueenWaypoints', function(req, res) {
        FritterController.addTweet(req, res);
    });

};
             