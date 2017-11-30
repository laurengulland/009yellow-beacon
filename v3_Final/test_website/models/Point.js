var mongoose = require('mongoose');
var Schema = mongoose.Schema;

/*
 * Point is the model class that represents tweets
 * content field: the text of the tweet
 * author field: the author of the tweet
*/
var PointSchema = new Schema({
    scout: { type: String }, // for Scout locations and waypoints
    queen: { type: String }, // for Queen locations and waypoints
    isWaypoint: { type: Boolean, required: true },
    isCurrent: {type: Boolean, required: true },
    latitude: { type: Number, required: true }, // 10**6
    longitude: { type: Number, required: true }, // 10**6
    description: { type: String },
    time: { type: Number, required: true },
    needsTransmit: { type: Boolean},
});

//{ scout:"scout1", queen:"", isWaypoint:false, isCurrent:true, latitude:51.509, longitude:-0.08, description:"", time:13, needsTransmit:false }

PointSchema.statics.addDescription = function (inp_description, callback) {
    Point.findOne({ '_id': waypoint_id, 'isWaypoint': true }, function (err, point_to_add) {
        this.model('Point').update({ "_id": this.id}, {description: inp_description}, function (err) {
            return callback(err);
        });
    });
};

PointSchema.statics.getAllCurrentScoutLocations = function (callback) {
    Point.find({ 'isCurrent': true , 'scout': {$exists:true} }, function (err, docs) {
        return callback(err, docs);
    });
};

PointSchema.statics.getAllCurrentQueenLocations = function (callback) {
    Point.find({ 'isCurrent': true , 'queen': {$exists:true} }, function (err, docs) {
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

PointSchema.statics.testAll = function (callback) {
    Point.findOne({}, function (err, docs) {
        return callback(err, docs);
    });
};

var Point = mongoose.model('Point', PointSchema);
module.exports = Point;