/*  Controller controls the interactions between the board and the user
 *  contains functions for rerendering the board and regisering clicks
 */

var Controller = function (board) {
    that = Object.create(Controller.prototype);
    

    /*  
     *  looking at the stored cells, modifies the view 
     */
    that.reRender = function () {
        var allCells = board.getAllCells();
        allCells.forEach(function (cell) {
            if (board.statusCell(cell)) {
                $("#" + cell).css('background-color', 'aqua');
            } else {
                $("#" + cell).css('background-color', 'darkgray');
            }
        });
    };

    /*  @param: takes in the item that was just clicked
     *  modifies the item so that it is either killed or revived and updates view
     */
    that.clicked = function (item) {
        var itemID = $(item).attr("id");
        if (board.statusCell(itemID)) {
            board.killCell(itemID);
        } else {
            board.reviveCell(itemID);
        }
//        console.log(reRender());
//        console.log(this.reRender());
//        that.reRender();
    };
    
    Object.freeze(that);
    return that;
};


