$(document).ready(function () {
    button_functions();
});

// ensures all buttons have desired functionality
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
    
//  $('.keyboard').keyboard({
//  });
//    $('.keyboard').bind('accepted', function(e, keyboard, el){
//        console.log(el.value);
//        $.ajax({
//            url: '/addDescription',
//            type: 'GET',
//            headers: {"description": el.value, "waypoint_id": keyboard.id},
//            success: function() {
//              var polygon = L.polygon([
//                  [51.509, -0.08],
//                  [51.503, -0.06],
//                  [51.51, -0.047],
//                  [51.50, -0.048]
//              ]).addTo(mymap);
//           },
//        });    
//    });

};