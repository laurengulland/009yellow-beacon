var mongoose = require('mongoose');
var Schema = mongoose.Schema;

/*
 * Point is the model class that represents tweets
 * content field: the text of the tweet
 * author field: the author of the tweet
*/
var PointSchema = new Schema({
    content: { type: String, required: true },
    author: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true }
});

/*
 * a static retweet method that retweets, saving into collection
 * @param currentTweeterID the person retweeting
 * @param tweeter the person who wrote the actual tweet
 * @tweetText the text of the tweet we want to retweet
 * @callback the callback function
*/
PointSchema.statics.retweet = function (currentTweeterID, tweeter, tweetText, callback) {
    var newTweet = new Point({
        content: tweeter + ":" + tweetText,
        author: currentTweeterID
    });
    newTweet.save(function (err, newTweet) {
        return callback(err);
    });
};

var Point = mongoose.model('Point', PointSchema);
module.exports = Point;