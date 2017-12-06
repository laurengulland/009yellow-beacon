var mongoose = require('mongoose');
var Schema = mongoose.Schema;

/*
 * Point is the model class that represents points
*/
var PointSchema = new Schema({
    scout: { type: String }, // for Scout locations and waypoints
    queen: { type: String }, // for Queen locations and waypoints
    isWaypoint: { type: Boolean, required: true },
    isCurrent: {type: Boolean },
    latitude: { type: Number, required: true },
    longitude: { type: Number, required: true },
    description: { type: String },
    time: { type: Number, required: true },
    needsTransmit: { type: Boolean},
}, {
    capped: 1000000,
});

PointSchema.statics.addDescription = function (waypoint_id, waypoint_description, callback) {
    Point.findOneAndUpdate({'_id': waypoint_id, 'isWaypoint': true},{description: waypoint_description}, function(err, doc) {
        console.log("found waypoint");
        console.log(waypoint_description);
        console.log(doc);
        return callback(err);
    });
};

PointSchema.statics.getAllCurrentScoutLocations = function (callback) {
    Point.find({ 'isCurrent': true , 'scout': {$nin: ["", null]} }, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getAllCurrentQueenLocations = function (callback) {
    Point.find({ 'isCurrent': true , 'queen': {$nin: ["", null]}, 'isWaypoint': false}, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getScoutTracks = function (scout_id, callback) {
    Point.find({ 'scout': scout_id, 'isCurrent': false , 'isWaypoint': false }, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getQueenTracks = function (queen_id, callback) {
    Point.find({ 'queen': queen_id, 'isCurrent': false , 'isWaypoint': false }, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getWaypoints = function (callback) {
    Point.find({ 'isWaypoint': true }, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getSingleWaypoint = function (waypoint_id, callback) {
    Point.findOne({ '_id': waypoint_id, 'isWaypoint': true }, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getWaypointsFromQueen = function (queen_id, callback) {
    Point.find({ 'queen': queen_id, 'isWaypoint': true }, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getWaypointsFromWaypoint = function (waypoint_id, callback) {
    Point.findOne({ '_id': waypoint_id, 'isWaypoint': true }, function (err, waypoint) {
        Point.find({ 'queen': waypoint.queen, 'isWaypoint': true }, function (err, docs) {
            return callback(err, docs);
        });        
    });
};

PointSchema.statics.getAll = function (callback) {
    Point.find({}, function (err, docs) {
        return callback(err, docs);
    });
};

var Point = mongoose.model('Point', PointSchema);
module.exports = Point;