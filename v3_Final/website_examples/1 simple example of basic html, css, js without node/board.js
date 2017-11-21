/*  Board class, an adt to represent the game
 *  defines the fields and methods of the board and containing cells
 */

var Board = function (height, width) {
    var that = Object.create(Board.prototype),
        cells = {};
    /*  
     *  @return: list of all cell ids
     */
    that.getAllCells = function () {
        return Object.keys(cells);
    };
    
    /*  
     *  mutates the board, sets all cells to false
     */
    that.killAllCells = function () {
        Object.keys(cells).forEach(function (cell) {
            that.killCell(cell);
        });
    };
    
    /*  
     *  @return: boolean of whether cell is alive or not
     */
    that.statusCell = function (key) {
        return cells[key];
    };
    
    /*  
     *  mutates the board, set cell to false
     */
    that.killCell = function (key) {
        cells[key] = false;
    };
    
    /*  
     *  mutates the board, set cell to true
     */
    that.reviveCell = function (key) {
        cells[key] = true;
    };
    
    /*  
     *  @return: list of all alive cells
     */
    that.getAliveCells = function () {
        var aliveCells = that.getAllCells().filter(function (cellName) {
            return cells[cellName];
        });
        return aliveCells;
    };
    
    /*  @param: cell oh which to get neighbors for
     *  @return: returns list of immediate neighbors of particular cell
     */
    that.getNeighbors = function (cell) {
        var index = cell.indexOf("-");
        var x = parseInt(cell.substr(0, index));
        var y = parseInt(cell.substr(index + 1));
        var neighbors = [];
        var i;
        var j;
        for (i = -1; i < 2; i++) {
            for (j = -1; j < 2; j++) {
                var currentX = x + i,
                    currentY = y + j;
                if (currentX > -1 && currentY > -1 && currentX < width && currentY < height) {
                    if (currentX === x && currentY === y) {                   
                    } else {
                        var key = currentX.toString() + "-" + currentY.toString();
                        neighbors.push(key);   
                    }
                }
            }
        }
        return neighbors;
    };
    
    /*  
     *  intializes the board with the named divs set to false
     */
    that.boardInit = function () {
        var i,
            j;
        for (i = 0; i < width; i++) {
            for (j = 0; j < height; j++) {
                var key = i.toString() + "-" + j.toString();
                cells[key] = false;
            }
        }
    };
    
    Object.freeze(that);
    return that;
};