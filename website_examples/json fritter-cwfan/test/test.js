var assert = require("assert");
var fritter = require("../fritter.js");


describe('Fritter', function() {
    

  describe('addUser', function() {
    it('adds a tweeter to the database if they did not already exist', function() {
      fritter.clearDictionaries();
      fritter.addUser("dumbledore");
      fritter.addUser("yourmom");
      assert.deepEqual(2, fritter.getAllUsers().length);
    });
  });
    
  describe('getUser', function() {
    it('return the current user', function() {
      fritter.switchUser("yourmom");
      assert.equal("yourmom", fritter.getUser());
    });
  });
    
  describe('switchUser', function() {
    it('switch the current user from one to another', function() {
      fritter.switchUser("dumbledore");
      assert.equal("dumbledore", fritter.getUser());
    });
  });
    
  describe('clearDictionaries', function() {
    it('clears the dictionaries', function() {
      fritter.addUser("waddip");
      fritter.clearDictionaries();
      assert.equal(0, fritter.getAllUsers().length);
    });
  });
    
    
  describe('getAllTweetTuples', function() {
    it('get all tweet tuples of [tweetkey, author, tweet]', function() {
      fritter.clearDictionaries();
      fritter.addUser("Harry Potter");
      fritter.addUser("minion");
      fritter.addTweet("Harry Potter", "#yolo");
      fritter.addTweet("minion", "bello!");
      assert.equal(2, fritter.getAllTweetTuples().length);
    });
  });

  describe('getAllUserTweetKeys', function() {
    it('get all tweetkeys', function() {
      fritter.clearDictionaries();
      fritter.addUser("Harambe");
      fritter.addTweet("Harambe", "likes bananas");
      assert.equal(1, fritter.getAllUserTweetKeys("Harambe").length);
    });
  });
    
  describe('getAllUsers', function() {
    it('get all users in fritter', function() {
      fritter.clearDictionaries();
      fritter.addUser("thing1");
      fritter.addUser("thing2");
      var expected = ["thing1", "thing2"];
      assert.deepEqual(expected, fritter.getAllUsers());
    });
  });
    
  describe('getTweet', function() {
    it('get tweet from a tweetkey', function() {
      fritter.clearDictionaries();
      fritter.addUser("snow white");
      var key = fritter.addTweet("snow white", "I like red apples")[0];
      assert.equal("I like red apples", fritter.getTweet(key));
    });
  });

  describe('addTweet', function() {
    it('add tweet', function() {
      fritter.clearDictionaries();
      fritter.addUser("snow white");
      var key = fritter.addTweet("snow white", "I like red apples")[0];
      assert.equal("I like red apples", fritter.getTweet(key));
    });
  });

  describe('deleteTweet', function() {
    it('delete tweet', function() {
      fritter.clearDictionaries();
      fritter.addUser("snow white");
      var key = fritter.addTweet("snow white", "I like red apples")[0];
      assert.equal(1, fritter.getAllTweetTuples().length);
      fritter.deleteTweet("snow white", key);
      assert.equal(undefined, fritter.getTweet(key));
    });
  });
  
});

    