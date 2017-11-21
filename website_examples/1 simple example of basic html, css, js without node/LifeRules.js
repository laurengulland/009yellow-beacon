/*  class that encompasses the logic of Conway's game of life
 *  performs the logic for one round of propagation
 */

var LifeRules = function (board) {
    that = Object.create(Controller.prototype);
    
    /*  
     *  mutate the board for one round of Conway's game of life
     */   
    that.OneRound = function () {
        var killCells = [];
        var reviveCells = [];
        board.getAliveCells().forEach(function (cell) {
            var neighbors = board.getNeighbors(cell);
            var aliveNeighbors = neighbors.filter(function (neighbor) {
                return board.statusCell(neighbor);
            });
            if (aliveNeighbors.length < 2 || aliveNeighbors.length > 3) {
                killCells.push(cell);
            }
            neighbors.forEach(function (neighbor) {
                var aliveNextNeighbors = board.getNeighbors(neighbor).filter(function (nextNeighbor) {
                    return board.statusCell(nextNeighbor);
                });
                if (aliveNextNeighbors.length === 3) {
                    reviveCells.push(neighbor);
                }
            });
        });
        killCells.forEach(function (cell) {
            board.killCell(cell);
        });
        reviveCells.forEach(function (cell) {
            board.reviveCell(cell);
        });
    };
    Object.freeze(that);
    return that;
};