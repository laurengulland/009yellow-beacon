var Point = require('../models/Point');

module.exports = function (app) {
    app.get('/', function (req, res) {
        return res.render('index', {message: "teehee"});
    });

    app.get('/addDescription', function(req, res) {
        var description = req.headers.description;
        var waypoint_id = req.headers.waypointid;
        Point.addDescription(waypoint_id, description, handle_err);
    });

    app.get('/allQueens', function(req, res) {
        Point.getAllCurrentQueenLocations(function(err, data) {
            handle_err(err);
            return res.send(data);
        });
    });

    app.get('/allQueenWaypoints', function(req, res) {
        console.log("got to waypoint");
        var queenid = req.headers.queenid;
        console.log(queenid);
        Point.getWaypointsFromQueen(function(err, data) {
            handle_err(err);
            return res.send(data);
        })
        //res.send({blah:"gee"});
        //var allQueens = Point.getAll
    });

    app.get('/addDescription', function(req, res) {
        console.log("keyboard initialized");
        })
        //res.send({blah:"gee"});
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

//    app.get('/keyboard', function(req, res) {
//        console.log("keyboard initialize");
//        var queenid = req.headers.queenid;
//        console.log(queenid);
//        res.type('json');
//        res.send({blah:"gee"});
//        //var allQueens = Point.getAll
//    });

};

var handle_err = function(err) {
    if (err) {
         return console.log(err);
    }
};
