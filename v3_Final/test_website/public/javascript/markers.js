// vars for icons
var waypointIcon = L.icon({
  iconUrl: 'icons/waypoint-icon-red.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var selectedWaypointIcon = L.icon({
  iconUrl: 'icons/waypoint-icon-red.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var pastPosIcon = L.icon({
  iconUrl: 'images/black-dot.png',
  iconSize: [5, 5],
  iconAnchor: [2, 2],
  popupAnchor: [0, -28]
});

var currentScoutPosIcon = L.icon({
  iconUrl: 'images/waypoint-icon-blue.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var currentQueenPosIcon = L.icon({
  iconUrl: 'images/waypoint-icon-blue.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var selected_marker = "";
var currentMarkers = {};
var waypointMarkers = {};
var processAllPoints = function(allPoints) {
    for (var i = 0; i < allPoints.length; i++) {
        var p = allPoints[i];
        console.log(p);
        if (p.isWaypoint) {
            var waypoint = L.marker([p.latitude, p.longitude], {icon: waypointIcon}).addTo(mymap);
            waypoint._icon.id = p._id;
            waypoint._icon.classList.add('waypoint-marker');
            waypointMarkers[p._id] = waypoint;
        } else {
            if (p.isCurrent) {
                helperCurrent(p);              
            } else {
                var pastPos = L.marker([p.latitude, p.longitude], {icon: pastPosIcon}).addTo(mymap);
            }
        }
    }
}

var updateCurrentLocation = function(scoutid, newPoint) {
    var old = currentMarkers[scoutid];
    old.setIcon(pastPosIcon);
    helperCurrent(newPoint);
}

var helperCurrent = function(p) {
    if (p.queen.length > 0) {
        var queenMarker = L.marker([p.latitude, p.longitude], {icon: currentQueenPosIcon}).addTo(mymap);
        queenMarker._icon.id = p.queen;
        queenMarker._icon.classList.add('queen-marker');
        currentMarkers[p.queen] = queenMarker;                    
    } else if (p.scout.length > 0){
        var scoutMarker = L.marker([p.latitude, p.longitude], {icon: currentScoutPosIcon}).addTo(mymap);
        scoutMarker._icon.id = p.scout;
        scoutMarker._icon.classList.add('scout-marker');
        currentMarkers[p.scout] = scoutMarker;
    } 
}

var fillQueenMenu = function(listQueens) {
    var queenDivs;
    for (var i = 0; i < listQueens.length; i++) {
        var queen = listQueens[i];
        var queenDiv = "<div></div>";
//        <div class = > 
    }
    $("#leaflet-menu-contents").append(queenDivs);
}

var selectMarker = function(markerid) {
    $('menu' + markerid).css("color", "white");
    currentMarkers[markerid].setIcon(selectedWaypointIcon);
    selected_marker = markerid;
}

var deselectMarker = function() {
    if (selected_marker.length > 0) {
        $('menu' + selected_marker).css("color", "yellow");
        currentMarkers[selected_marker].setIcon(waypointIcon);
        selected_marker = "";        
    }
}

var dummydata = '[{ "scout":"scout1", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.509, "longitude":-0.08, "description":"", "time":13, "needsTransmit":false },{ "scout":"scout2", "queen":"", "isWaypoint":false, "isCurrent":false, "latitude":51.508, "longitude":-0.09, "description":"", "time":13, "needsTransmit":false },{ "scout":"scout3", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.507, "longitude":-0.10, "description":"", "time":13, "needsTransmit":false }]';

var dp = '{ "scout":"scout3", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.506, "longitude":-0.11, "description":"", "time":13, "needsTransmit":false }';

processAllPoints(JSON.parse(dummydata));
updateCurrentLocation("scout1", JSON.parse(dp));
console.log("finsih parsing");


