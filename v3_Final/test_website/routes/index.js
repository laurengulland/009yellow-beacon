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
    
    app.get('/test', function(req, res) {
        console.log("got routed to test");
        Point.testAll(function(err, data) {
            if (err) {
                console.log("fooked up reading from mongo");
                console.log(err);
            } else {
                console.log("successfully read from mongo");
                console.log(data);
                res.send(data);    
            }
        });
    });

};
             