var assert = require("assert");
var mongoose = require("mongoose");
var User = require("../models/user");
var Fritter = require("../models/fritter");

describe("App", function() {
  // The mongoose connection object.
  var con;

  // Before running any test, connect to the database.
  before(function(done) {
    con = mongoose.connect("mongodb://localhost/geditables", function() {
      done();
    });
  });

  // Delete the database before each test.
  beforeEach(function(done) {
    con.connection.db.dropDatabase(function() { done(); });
  });

  describe("User", function() {
    it("should have a password field", function(done) {
      User.create({
        "name": "testuser",
          "password": "123",
          "following": []   
      }, function() {
        User.findOne({"name": "testuser"}, function(err, doc) {
          assert.strictEqual(doc.password, "123");
          done();
        });
      });
    }); // End it should have a password field.

    it("should not have empty username", function(done) {
      User.create({"name": "", "password": "123"}, function(err, doc) {
        assert.throws(function() {
          assert.ifError(err);
        });
        done();
      });
    });
    it("check password", function(done) {
      User.create({
        "name": "testuser",
          "password": "123",
          "following": []   
      }, function() {
        User.findOne({"name": "testuser"}, function(err, user) {
          user.checkPassword("123", function(passwordBool) {
              assert.strictEqual(true, passwordBool, "passwords should validate");
          });
          done();
        });
      });
    });
    it("get not following users", function(done) {
      User.create({
        "name": "testuser",
          "password": "123",
          "following": []   
      }, function() {
        User.findOne({"name": "testuser"}, function(err, user) {
          user.getNotFollowing(function(err, users) {
              assert.strictEqual(users.length, 0);
          });
          done();
        });
      });
    });
    it("testing follow mechaniscm", function(done) {
      User.create({
        "name": "testuser",
          "password": "123",
          "following": []   
      }, function() {
        User.follow("testuser", "123", true, function(err) {
          User.findOne({"name": "testuser", function(err, user) {
              assert.strictEqual(users.following, ["123"]);
          }});
          done();
        });
      });
    });
      
  it("should get all tweets", function(done) {
      var newUser = new User({ "name": "testuser", "password": "123" });
      newUser.save(function(err) {
        if (err) {
          console.log(err);
        }
      });

      var tweet = new Fritter({ "content": "a", "author": newUser._id });
      tweet.save(function (err) {
        if (err) {
          console.log(err);
        } else {
          User.getAllTweets(function(err, tweets) {
            assert.strictEqual(tweets.length, 1);
            done();
          });
        }
      });
    });
            

    it("get all following tweets", function(done) {
      User.create({
        "name": "testuser",
          "password": "123",
          "following": ["12"]   
      }, function() {
        User.getFollowingTweets("testuser", function(err, tweets) {
            assert.strictEqual(tweets.length, 0);
        })
          done();
        });
    });
  }); // End describe User.

  describe("Fritter", function() {
      
    it("should tweet text", function(done) {
      var newUser = new User({ "name": "testuser", "password": "123" });
      newUser.save(function(err) {
        if (err) {
          console.log(err);
        }
      });

      var tweet = new Fritter({ "content": "a", "author": newUser._id });
      tweet.save(function (err) {
        if (err) {
          console.log(err);
        } else {
          Fritter.findOne({"author": newUser._id}, function(err, tweet) {
            assert.strictEqual(tweet.content, "a");
            done();
          });
        }
      });
    }); // end should tweet correctly
      
    it("should retweet", function(done) {

      var newUser = new User({ name: "testuser", password: "123" });
      newUser.save(function(err) {
        if (err) {
          console.log(err);
        }
      });

      var tweet = new Fritter({ "content": "a", "author": newUser._id });
      tweet.save(function (err) {
        if (err) {
          console.log(err);
        } else {
          Fritter.retweet(newUser._id, tweet.text, newUser._id, function(err) {
            User.getAllTweets(function(err, tweets) {
              assert.strictEqual(tweets.length, 2);
              done();
            });     
          });
        }
      });      
    }); // End should retweet correctly
      
  }); // End describe Fritter.
}); // End describe App.
