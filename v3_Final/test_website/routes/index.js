var Point = require('../models/Point');

module.exports = function (app) {
    app.get('/', function (req, res) {
        res.render('index', {message: "teehee"});
    });

//    app.get('/addDescription', function(req, res) {
//        var error = req.query.error;
//        var name = req.session.name;
//
//        if (name === undefined) {
//            return res.render('error', {message: "Please log in"});
//        }
//
//        Point.findOne({ name: name }, function (err, user) {
//            if (err || user === null) {
//                console.error(err);
//                res.render('error', {message: "Please try again"});
//            } else {
//                Point.getAllTweets(function (err, tweets) {
//                    if (err) {
//                        console.error(err);
//                        res.render('error', {message: "Please try again"});
//                    } else {
//                        res.render('index', {user: name, tweetsList: tweets});
//                    }
//                });
//            }
//        });
//    });

    app.get('/allQueens', function(req, res) {
        res.render('index', {message: "muahah"});
    });

    app.get('/allQueenWaypoints', function(req, res) {
        console.log("got to waypoint");
        var queenid = req.headers.queenid;
        console.log(queenid);
        res.type('json');
        res.send({blah:"gee"});
        //var allQueens = Point.getAll
    });

    app.get('/addDescription', function(req, res) {
        console.log("keyboard initialize");
        res.type('json');
        res.send({blah:"hai"});
        //var allQueens = Point.getAll
    });

};
