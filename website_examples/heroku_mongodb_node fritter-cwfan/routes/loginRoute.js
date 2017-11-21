var UserController = require('./userControl');

module.exports = function (app) {

    app.post('/register', function(req, res) {
        UserController.register(req, res);
    });

    app.post('/login', function(req, res) {
        UserController.login(req, res);
    });

    app.post('/logout', function(req, res) {
        UserController.logout(req, res);
    });
};