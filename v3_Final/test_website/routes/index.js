var Point = require('../models/Point');

module.exports = function (app) {
    app.get('/', function (req, res) {
//        makeFakeData();
        return res.render('index', {message: "teehee"});
    });

    app.post('/addDescription', function(req, res) {
        var descriptionInput = req.headers.des;
        var waypoint_id = req.headers.waypoint_id;
        Point.addDescription(waypoint_id, descriptionInput, function(err) {
            handle_err();
            return res.send({
                "description": descriptionInput, 
                "waypoint_id": waypoint_id,
            });
        });
    });

    app.get('/allQueens', function(req, res) {
        Point.getAllCurrentQueenLocations(function(err, data) {
            handle_err(err);
            return res.send(data);
        });
    });
    
    app.get('/allWaypoints', function(req, res) {
        Point.getWaypoints(function(err, data) {
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
    
    app.get('/scoutTrack', function(req, res) {
        var scoutid = req.headers.scoutid;
        Point.getScoutTracks(scoutid, function(err, data) {
            handle_err(err);
            return res.send(data);
        });
    });
    
    app.get('/queenTrack', function(req, res) {
        var queenid = req.headers.queenid;
        Point.getQueenTracks(queenid, function(err, data) {
            handle_err(err);
            return res.send(data);
        });
    });

    app.get('/all', function(req, res) {
        Point.getAll(function(err, data) {
            if (err) {
                console.log(err);
            } else {
                res.send(data);
            }
        });
    });
};


// some helper and dummy data creation
var handle_err = function(err) {
    if (err) {
         return console.log(err);
    }
};

// makes scout1 current, past, past scout2 current
// leader1 current past, past, queen 2 current
// waypoint1, wpt2
//42.43615226140728, -71.1098070134176
var lat = -9.06584774;
var long = -71.099807;
var placeholder = "9".repeat(60);
var makeFakeData = function() {
        var point = new Point({ 
            scout: "scout1", 
            queen: "",
            isWaypoint: false,
            isCurrent:true, 
            latitude:51.502 + lat, 
            longitude:-0.015 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        });  
        point = new Point({ 
            scout: "scout1", 
            queen: "",
            isWaypoint: false,
            isCurrent:false, 
            latitude:51.503 + lat, 
            longitude:-0.014 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        });  
        point = new Point({ 
            scout: "scout1", 
            queen: "",
            isWaypoint: false,
            isCurrent:false, 
            latitude:51.504 + lat, 
            longitude:-0.013 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        });
    
        point = new Point({ 
            scout: "scout2", 
            queen: "",
            isWaypoint: false,
            isCurrent:true, 
            latitude:51.505 + lat, 
            longitude:-0.012 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        });
        point = new Point({ 
            scout: "", 
            queen: "leader1",
            isWaypoint: false,
            isCurrent:true, 
            latitude:51.506 + lat, 
            longitude:-0.011 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        }); 
        point = new Point({ 
            scout: "", 
            queen: "leader1",
            isWaypoint: false,
            isCurrent:false, 
            latitude:51.507 + lat, 
            longitude:-0.010 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        }); 
        point = new Point({ 
            scout: "", 
            queen: "leader1",
            isWaypoint: false,
            isCurrent:false, 
            latitude:51.508 + lat, 
            longitude:-0.009 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        }); 
        point = new Point({ 
            scout: "", 
            queen: "leader2",
            isWaypoint: false,
            isCurrent:true, 
            latitude:51.509 + lat, 
            longitude:-0.008 + long, 
            description:"", 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        });
        point = new Point({ 
            scout: "scout1", 
            queen: "leader1",
            isWaypoint: true,
            isCurrent:false, 
            latitude:51.510 + lat, 
            longitude:-0.007 + long, 
            description:placeholder, 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        }); 
        point = new Point({ 
            scout: "scout2", 
            queen: "leader2",
            isWaypoint: true,
            isCurrent:false, 
            latitude:51.511 + lat, 
            longitude:-0.006 + long, 
            description:placeholder, 
            time:13, 
            needsTransmit:false,
        });
        point.save(function(err) {
            console.log("saved");
        }); 
}
