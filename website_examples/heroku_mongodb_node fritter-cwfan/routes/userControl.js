var User = require('../models/user');

module.exports = {

    /*
     * logs in the user
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    login: function (req, res) {
        var name = req.body.name;
        var password = req.body.password;

        User.findOne({ name: name }, function (err, user) {
            if (err) {
                console.log(err);
                res.render('error', {message: "Please try again later."});
            } else if (user === null) {
                res.render('error', {message: "Username not found"});
            } else {
                user.checkPassword(password, function (match) {
                    if (!match) {
                        res.render('error', {message: "Invalid password"});
                    } else {
                        // save user cookie, show all tweets
                        req.session.name = user.name;
                        req.session.userID = user.id;
                        req.session.save(function (err) {
                            res.redirect('/allTweets');
                        });
                    }
                });
            }
        });
    },

    /*
     * registers new users
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    register: function (req, res) {
        var name = req.body.name;
        var password = req.body.password;
        
        if (name.length < 1 || password.length < 1) {
            res.render('error', {message: "Please do not leave any fields blank"});
        }

        var user = new User({ name: name, password: password});
        user.save(function (err, user) {
            if (err) {
                if (err.code === 11000) {
                    res.render('error', {message: "This name is taken"});
                } else {
                    console.log(err);
                    res.render('error', {message: "Please try again later"});
                }
            } else {
                // success! redirect to feed
                req.session.name = user.name;
                req.session.userID = user.id;
                req.session.save(function (err) {
                    res.redirect('/allTweets');
                });
            }
        });
    },

    /*
     * logs out logged in users
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    logout: function (req, res) {
        req.session.destroy(function (err) {
            if (err) {
                console.log(err);
                res.render('error', {message: "Can't currently log out, please try again"});
            } else {
                res.render('login', {user: "express"});
            }
        });
    },
    
    /*
     * gets the user profile that displays a list of their own tweets and users they don't follow
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    getProfile: function (req, res) {
        var name = req.session.name;
        User.findOne({ name: name }, function (err, user) {
            if (err) {
                return res.render('error', {message: "Can't access profile, please try again"});
            }
            user.getOwnTweets(function (err, ownTweets) {
                if (err) { console.log(err); return res.render('error', {message: "can't get own tweet"}); }
                user.getNotFollowing(function (err, notFollowed) {
                    if (err) { return res.render('error', {message: "can't get not following users"}); }
                    return res.render('profile', {user: name, tweetsList: ownTweets, tweeterList: notFollowed});
                });
            });
        });
    },

    /*
     * gets either all tweets or following tweets
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    getTweets: function (req, res, isFollowingOnly) {
        var error = req.query.error;
        var success = req.query.success;
        var name = req.session.name;

        if (name === undefined) {
            return res.render('error', {message: "Please log in"});
        }

        User.findOne({ name: name }, function (err, user) {
            if (err || user === null) {
                console.error(err);
                res.render('error', {message: "Please try again"});
            } else {
                if (isFollowingOnly) {
                    User.getFollowingTweets(name, function (err, tweets) {
                        if (err) {
                            console.error(err);
                            res.render('error', {message: "Please try again"});
                        } else {
                            res.render('index', {user: name, tweetsList: tweets});
                        }
                    });
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
            }
        });
    },

    /*
     * follows another user
     * @param req the request the user sends
     * @param res the response that the user recieves
    */
    follow: function (req, res) {
        var name = req.session.name;
        var userIDToFollow = req.body.tweetAuthorID;
        var follow = req.body.follow === "true"; // boolean- follow or unfollow      

        User.follow(name, userIDToFollow, follow, function (err) {
            if (err) {
                console.error(err);
                res.render('error', {message: "Please try again"});
            } else {
                res.redirect('back');
            }
        });
    }

};


