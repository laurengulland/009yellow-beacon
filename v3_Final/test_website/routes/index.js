var Point = require('../models/Point');

module.exports = function (app) {
    app.get('/', function (req, res) {
        return res.render('index', {message: "teehee"});
    });

    app.get('/addDescription', function(req, res) {
        console.log("keyboard initialized");
        var description = req.headers.description;
        var waypoint_id = req.headers.waypoint_id;
        Point.addDescription(waypoint_id, description, function(err) {
            handle_err();
        });
    });

    app.get('/allQueens', function(req, res) {
        Point.getAllCurrentQueenLocations(function(err, data) {
            handle_err(err);
            return res.send(data);
        });
    });

    app.get('/allQueenWaypoints', function(req, res) {
        var queenid = req.headers.queenid;
        Point.getWaypointsFromQueen(queenid, function(err, data) {
            handle_err(err);
            return res.send(data);
        });
    });
    
    app.get('/allQueenWaypointsFromWaypoint', function(req, res) {
        var waypointid = req.headers.waypointid;
        Point.getWaypointsFromWaypoint(waypointid, function(err, data) {
            handle_err(err);
            return res.send(data);
        });
    });

    app.get('/all', function(req, res) {
        Point.getAll(function(err, data) {
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
