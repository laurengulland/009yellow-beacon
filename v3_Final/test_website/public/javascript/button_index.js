/////////////////////////////////////////////////////////
/////  Initializes map with all markers from mongo
/////////////////////////////////////////////////////////

// for debugging, set both to true
var isQueen = true;
var isHive = true;

////////////////// renders markers on map ///////////////////
//// runs once to initialize markers upon querying all data from mongo
$.ajax({
    url: '/all',
    type: 'GET',
    success: function(data) {
        processAllPoints(data, true);
        drawAllTracks();
        if (isHive) {
            $.ajax({
                url: '/allQueens',
                type: 'GET',
                success: function(queendata) {
                    fillQueenMenu(queendata);
               },
            }); 
        } else {
            $.ajax({
                url: '/allWaypoints',
                type: 'GET',
                success: function(data) {
                    fillWaypointMenu(data);
               },
            });            
        }
   },
});


/////////////////////////////////////////////////////////
/////  Button functionality
/////////////////////////////////////////////////////////
$(document).ready(function () {
    button_functions();
});

var button_functions = function() {

    // if click on current queen, show list of POI
    $('.queen-marker').click(function () {
        var id = this.id.replace("menu", "");
        $.ajax({
            url: '/allQueenWaypoints',
            type: 'GET',
            headers: {"queenid": id},
            success: function(data) {
                fillWaypointMenu(data);
                selectQueenMarker(id);
           },
        });
    });
    
    // if click on poi, show list of POI with poi highlights
    $('.waypoint-marker').click(function() {
        var id = this.id.replace("menu", "");
        $.ajax({
            url: '/allQueenWaypointsFromWaypoint',
            type: 'GET',
            headers: {"waypointid": id},
            success: function(data) {
                fillWaypointMenu(data);
                selectWaypointMarker(id);
           },
        });        
    });

    // when you click back on submenu
    $('.submenuBack').click(function () {
        $.ajax({
            url: '/allQueens',
            type: 'GET',
            success: function(data) {
                fillQueenMenu(data);
            },
        });
    });
    
    $('.form-inline').on("click", function(e) {
        e.stopPropagation();
    });
    
    $('form').on("submit", function(e) {
        e.preventDefault();
        var descriptionInput = $(this).serializeArray()[0].value.toString();
        var waypoint_id = $(this).serializeArray()[1].value;
        $.ajax({
            url: '/addDescription',
            type: 'POST',
            headers: {"des": descriptionInput,
                     "waypoint_id": waypoint_id},
            success: function(data) {
                $.ajax({
                    url: '/allQueenWaypointsFromWaypoint',
                    type: 'GET',
                    headers: {"waypointid": waypoint_id},
                    success: function(data) {
                        fillWaypointMenu(data);
                   },
                });
           },
        }); 
    });
};