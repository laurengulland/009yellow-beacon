/*  boardinit file intializes the board
 *  also intializes the listeners on the board and buttons
 *  also has the rendering
 */

(function () {
    var width = 30;
    var height = 30;
    var gameBoard = Board(height, width);
    var controller = Controller(gameBoard);
    var rules = LifeRules(gameBoard);
    var playGame = false;
    
    /*  @param: width, height, controller 
     *  @return: nothing, mutates the html to make the divs for the grid
     */
    var createBoard = function(width, height, controller) {
        var i,
            j;
        for (j = 0; j < height; j++) {
            var stripe = $("<div class = 'stripe'></div>");
            stripe.attr("id", "stripe" + j);
            $(".gameBoard").append(stripe);
            for (i = 0; i < width; i++) {
                var cell = $("<div class = 'cell'></div>");
                $(cell).click(function () {
                    controller.clicked(this);
                });
                cell.attr("id", i + "-" + j);
                $("#stripe" + j).append(cell);
            }
        }        
    };
    createBoard(width, height, controller);
    gameBoard.boardInit();

    $(".playButton").click(function() {
        playGame = true;
    });
    $(".pauseButton").click(function() {
        playGame = false;
    });
    $(".preset1").click(function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("10-10");
        gameBoard.reviveCell("11-11");
        controller.reRender();
    });
    $(".preset3").click(function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("3-13");
        gameBoard.reviveCell("4-13");
        gameBoard.reviveCell("5-13");
        gameBoard.reviveCell("5-14");
        gameBoard.reviveCell("4-15");
        controller.reRender();
    });
    $(".preset2").click(function() {
        gameBoard.killAllCells();
        gameBoard.reviveCell("5-7");
        gameBoard.reviveCell("6-8");
        gameBoard.reviveCell("6-6");
        gameBoard.reviveCell("7-9");
        gameBoard.reviveCell("7-5");
        controller.reRender();
    });
    
    (function () {
        var intervalID;
        var callback = function() {
            if (playGame) {
                rules.OneRound();
            }
            controller.reRender();
        }
        intervalID = window.setInterval(callback, 500)        
        
    })();
    

    
    
})();


