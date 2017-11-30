var Point = require('../models/Point');

module.exports = function (app) {
    app.get('/', function (req, res) {
        return res.render('index', {message: "teehee"});
    });

    app.get('/addDescription', function(req, res) {
        var description = req.headers.description;
        var waypoint_id = req.headers.waypointid;
        return Point.addDescription(waypoint_id, description, function(err) {
            if (err){
                return console.log(err);
            }
        });
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
    
    app.get('/dummydata', function(req, res) {
        console.log("got routed to dummydata");
        res.send({ scout:"scout1", queen:"", isWaypoint:false, isCurrent:true, latitude:51.509, longitude:-0.08, description:"", time:13, needsTransmit:false });

    });
};

var handle_err = function(err) {
    if (err) {
         return console.log(err);
    }
};
