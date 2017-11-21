var persist = require("./persist.js"); 

/*
 * Fritter is a class that is the abstract data representation of freets
 * the methods it contains are essentailly getting and setting tweets and tweeters
*/
var Fritter = function() {
     var that = Object.create(Fritter.prototype);
     var tweeters = {};
     var tweets = {};
     var currentUser;

     /* 
      * helper method to update dictionaries by loading from json
     */
     var updateDictionaries = function() {
         persist.load(function(err, data) {
          if (err) {
            console.log("err" + err);
          } else {
            tweeters = data[0];
            tweets = data[1];
          }
         });
     };
     /*
      * helper method to update the json from the dictionaries
     */
     var persistDictionaries = function() {
         persist.persist([tweeters, tweets], function(err, data){
             if (err) {
                 console.log("err" + err);
             }
         });
     };

     updateDictionaries();
     /*
      * method to add user onto database
      * @param user to add
     */
     that.addUser = function(user) {
         updateDictionaries();
         if (! (user in tweeters)) {
             tweeters[user] = [];
             persistDictionaries();
         }
     };
     /*
      * return the current user
      * @returns the currentUser
     */
     that.getUser = function() {
         return currentUser;
     };
     /*
      * switch user to another user
      * @param newUser to switch to
      * @return returns the newUser we just added
     */
     that.switchUser = function(newUser) {
         currentUser = newUser;
         that.addUser(newUser);
         return newUser;
     }
     /*
      * clear the dictionaries for easy testing
     */
     that.clearDictionaries = function() {
         tweeters = {};
         tweets = {};
         persistDictionaries();
     }
     /*
      * get all the tweet tuples of [tweetkey, author, tweet]
      * @return returns the tweet tuples
     */
     that.getAllTweetTuples = function() {
         updateDictionaries();
         if (tweeters === null) {
             return [];
         }
         var tweetTuples = [];
         for (var t in tweeters) {
             if (tweeters.hasOwnProperty(t)) {
                 var tweetKeyList = tweeters[t];
                 for (var i = 0; i < tweetKeyList.length; i++) {
                     var key = tweetKeyList[i];
                     tweetTuples.push([key, t, tweets[key]]);
                 }
              }
         }
         return tweetTuples;
     };
     /*
      * get all the user tweetkeys
      * @param author to search with
      * @return a list of tweetKeys associated with author
     */
     that.getAllUserTweetKeys = function(author) {
         updateDictionaries();
         var tweetKeys = tweeters[author];
         var tweetList = tweetKeys.map(function(tweetKey) {
             return tweets[tweetKey];
         });
         return tweetList;
     };
    /*
     * gets all the users
     * @return a list of all the users
    */
     that.getAllUsers = function() {
         updateDictionaries();
         return Object.keys(tweeters);
     };
    /*
     * get a tweet from a tweetkey
     * @param tweetKey of the tweet
     * @return the tweet associated with tweetKey
    */
     that.getTweet = function(tweetKey) {
         updateDictionaries();
         return tweets[tweetKey];
     };
    /*
     * adds a tweet
     * @param author the author of that tweet
     * @param tweet the tweet to add
     * @return the tweet tuple
    */
     that.addTweet = function(author, tweet) {
         updateDictionaries();
         var counter = Math.floor(Math.random() * 1000000).toString();
         if (tweeters[author].length > 0) {
             tweeters[author].push(counter);
         } else {
             tweeters[author] = [counter];
         }
         tweets[counter] = tweet;
         persistDictionaries();
         return [counter, author, tweet];
     };
    /*
     * deletes a tweet
     * @param author of the to be deleted tweet
     * @param tweetKey the key of the tweet to be deleted
     * @return the tweetkey of the deleted tweet
    */
     that.deleteTweet = function(author, tweetKey) {

         updateDictionaries();
         if (tweeters[author].length > 0) {
             tweetKey = tweetKey.slice(0, -1);
             delete tweets[tweetKey];
             var authortweetkeys = tweeters[author];
             var tweetIndex = authortweetkeys.indexOf(tweetKey);
             authortweetkeys.splice(tweetIndex, 1);
             tweeters[author] = authortweetkeys;

         } else {
             console.log("delete tweet doesn't exist");
         }
         persistDictionaries();
         return tweetKey;
     };
    Object.freeze(that);
    return that;
  };

module.exports = Fritter();