var UserController = require('./userControl');
var FritterController = require('./fritterControl');

module.exports = function (app) {
    
    app.get('/profile', function(req, res) {
        UserController.getProfile(req, res);
    });   

    app.delete('/deleteTweet', function(req, res) {
        FritterController.deleteTweet(req, res);
    });

    app.post('/follow', function(req, res) {
        UserController.follow(req, res);
    });
};
