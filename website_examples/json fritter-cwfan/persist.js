var fs = require("fs");

var DEFAULT_FILENAME = "fritter.json";

var Persister = function(filename) {
  var that = Object.create(Persister);

  /**
   * Write the given JavaScript object to a file.
   * @param {Object} object - The object to write to a file.
   * @param {Function} callback - The function to execute after the object
   *  has been written to a file. It is executed as callback(err), where 
   *  err is the error object and null if there is no error.
   */
  that.persist = function(object, callback) {
    fs.writeFile(filename, JSON.stringify(object), callback);
  };

  /**
   * Read the file and parse the result as a JavaScript object.
   * @param {Function} callback - The function to execute after the object
   *  has been read. It is executed as callback(err, object), where 
   *  err is the error object and null if there is no error and where object
   *  is the object read from the file. It is undefined if err is not null.
   */
  that.load = function(callback) {
    fs.readFile(filename, function(err, data) {
      if (err) {
        callback(err);
      } else {
        console.log(data.toString());
        callback(null, JSON.parse(data.toString()));
      }
    });
  };

  Object.freeze(that);
  return that;
};

module.exports = Persister(DEFAULT_FILENAME);
