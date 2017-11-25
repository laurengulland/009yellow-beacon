var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var Frit = require('../models/fritter');

/*
 * User is the model class that represents a user/tweeter
 * name field: the string name of a tweeter, must be unique
 * password field: the password associated with said account
 * following field: a list of object ids of users they follow that ref user
*/
var UserSchema = new Schema({
    name: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    following: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }]
});

/*
 * checks inputted password with db
 * @param enteredPassword the user inputted password
 * @callback the callback function
 * returns the callback with the boolean argument
*/
UserSchema.methods.checkPassword = function (enteredPassword, callback) {
    return callback(this.password === enteredPassword);
};

/*
 * get the list of users they don't follow, not including themselves
 * @param callback the callback function
 * returns the callback with the arguments of err and docs, the list of users not followed
*/
UserSchema.methods.getNotFollowing = function (callback) {
    var following = this.following;
    following.push(this.id);
    User.find({ '_id': {$nin: following} }, function (err, docs) {
        return callback(err, docs);
    });
};

/*
 * gets the list of user's own tweets
 * @param callback the callback function
 * returns the callback with the arguments of err and docs, the list of own tweets
*/
UserSchema.methods.getOwnTweets = function (callback) {
    Frit.find({ author: this.id }, function (err, docs) {
        callback(err, docs);
    });
};

/*
 * calls follow on a user
 * @param name the user who wants to follow someone
 * @param idToFollow the id of the user we want to follow
 * @param follow the boolean of whether or not we want to follow someone vs unfollow
 * @param callback the callback function 
*/
UserSchema.statics.follow = function (name, idToFollow, follow, callback) {
    var that = this;
    if (follow) {
        that.update({ "name": name}, {$push: {following: idToFollow}}, function (err) {
            return callback(err);
        });
    } else {
        that.update({ "name": name}, {$pull: {following: idToFollow}}, function (err) {
            return callback(err);
        });
    }
};

/*
 * gets all the tweets
 * @param callback the callback function
 * @return the callback function with the arguments of err and a list of all the tweet objects
*/
UserSchema.statics.getAllTweets = function (callback) {
    Frit.find({}).populate('author').exec(function (err, tweets) {
       return callback(err, tweets);
    });
};

/*
 * gets the tweets of users that they follow
 * @param name the user who wants to view their following tweets
 * @param callback the callback function
 * @return the callback function with the arguments of err adnd the list of user objects that user follows
*/
UserSchema.statics.getFollowingTweets = function (name, callback) {   
    User.findOne({name: name}, function (err, user) {
        Frit.find({ author: {$in: user.following} }).populate('author').exec(function (err, tweets) {
           return callback(err, tweets);
        });
    });
    
};


var User = mongoose.model('User', UserSchema);
module.exports = User;