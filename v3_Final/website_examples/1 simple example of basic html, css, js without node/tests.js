(function() {
  mocha.setup("bdd");
  var assert = chai.assert;

//testing variables
var width = 16;
var height = 16;
var gameBoard = Board(height, width);
var controller = Controller(gameBoard);
var rules = LifeRules(gameBoard);
var playGame = false;
gameBoard.boardInit();

  describe("Game of Life", function() {
      
    describe("Board class", function() {
      it("getAllCells", function() {
        assert.equal(gameBoard.getAllCells().length, 256);
      });
      it("killAllCells", function() {
        gameBoard.reviveCell("1-1");
        gameBoard.killAllCells();
        assert.equal(gameBoard.getAliveCells().length, 0);
      });
      it("statusCell", function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("1-1");
        assert.equal(gameBoard.statusCell("1-2"), false);
        assert.equal(gameBoard.statusCell("1-1"), true);
      });
      it("killCell", function() {
        gameBoard.reviveCell("1-1");
        gameBoard.reviveCell("1-2");
        gameBoard.killCell("1-1");
        assert.equal(gameBoard.getAliveCells().length, 1);
      });
      it("reviveCell", function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("1-1");
        assert.equal(gameBoard.statusCell("1-1"), true);
      });
      it("getAliveCells", function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("1-1");
        assert.equal(gameBoard.getAliveCells().length, 1);
      });
      it("geNeighbors", function() {
        assert.equal(gameBoard.getNeighbors("0-0").length, 3);
        assert.equal(gameBoard.getNeighbors("1-1").length, 8);
        assert.equal(gameBoard.getNeighbors("0-1").length, 5);
      });
    });
      
    describe("LifeRules class methods", function() {
      it("OneRound too little", function() {
        gameBoard.reviveCell("1-1");
        rules.OneRound();
        assert.equal(gameBoard.getAliveCells(), "");
      });
       it("OneRound alive", function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("1-1");
        gameBoard.reviveCell("1-2");
        gameBoard.reviveCell("2-1");        
        rules.OneRound();
        assert.equal(gameBoard.getAliveCells().length, 4);
       });
       it("OneRound too many", function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("1-1");
        gameBoard.reviveCell("1-3");  
        gameBoard.reviveCell("2-2");
        gameBoard.reviveCell("3-1");
        gameBoard.reviveCell("3-3");  
        rules.OneRound();
        assert.equal(gameBoard.getAliveCells().length, 4);
       });
    });
      
    describe("Controller class methods", function() {
      it("clicked", function() {
        gameBoard.killAllCells();
        controller.clicked($("#1-1"));
        assert.equal(gameBoard.getAliveCells().length, 1);
      });
    });
    
  });

  mocha.run();
})()
