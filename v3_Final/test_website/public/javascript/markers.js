// vars for icons
var waypointIcon = L.icon({
  iconUrl: 'images/waypoint-icon-red.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var selectedWaypointIcon = L.icon({
  iconUrl: 'images/emo.png',
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

var scoutIcon = L.icon({
  iconUrl: 'images/waypoint-icon-blue.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var queenIcon = L.icon({
  iconUrl: 'images/waypoint-icon-blue.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var selectedQueenIcon = L.icon({
  iconUrl: 'images/emo.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var selectedWaypointMarker = "";
var selectedQueenMarker = "";
var allMarkers = {};
var processAllPoints = function (allPoints) {
    for (var i = 0; i < allPoints.length; i++) {
        var p = allPoints[i];
        console.log(p);
        if (p.isWaypoint) {
            var waypoint = L.marker([p.latitude, p.longitude], {icon: waypointIcon}).addTo(mymap);
            waypoint._icon.id = p._id;
            waypoint._icon.classList.add('waypoint-marker');
            allMarkers[p._id] = waypoint;
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
    var old = allMarkers[scoutid];
    old.setIcon(pastPosIcon);
    helperCurrent(newPoint);
}

var helperCurrent = function(p) {
    if (p.queen.length > 0) {
        var queenMarker = L.marker([p.latitude, p.longitude], {icon: queenIcon}).addTo(mymap);
        queenMarker._icon.id = p.queen;
        queenMarker._icon.classList.add('queen-marker');
        allMarkers[p.queen] = queenMarker;                    
    } else if (p.scout.length > 0){
        var scoutMarker = L.marker([p.latitude, p.longitude], {icon: scoutIcon}).addTo(mymap);
        scoutMarker._icon.id = p.scout;
        scoutMarker._icon.classList.add('scout-marker');
        allMarkers[p.scout] = scoutMarker;
    } 
}

var fillQueenMenu = function(listQueens) {
    var queenDivs;
    for (var i = 0; i < listQueens.length; i++) {
        var queen = listQueens[i];
        var queenDiv = "<div></div>";
        queenDivs += queenDiv;
//        <div class = > 
    }
    $("#leaflet-menu-contents").append(queenDivs);
}

var selectWaypointMarker = function(markerid) {
    deselectMarker();
    mymap.panTo(allMarkers[markerid].getLatLng());
    $('menu' + markerid).css("color", "white");
    allMarkers[markerid].setIcon(selectedWaypointIcon);
    selectedWaypointMarker = markerid;
}

var selectQueenMarker = function(markerid) {
    deselectMarker();
    mymap.panTo(allMarkers[markerid].getLatLng());
    $('menu' + markerid).css("color", "white");
    allMarkers[markerid].setIcon(selectedQueenIcon);
    selectedQueenMarker = markerid;
}

var deselectMarker = function() {
    if (selectedWaypointMarker.length > 0) {
        $('menu' + selectedWaypointMarker).css("color", "yellow");
        allMarkers[selectedWaypointMarker].setIcon(waypointIcon);
        selectedWaypointMarker = "";        
    } else if (selectedQueenMarker.length > 0) {
        $('menu' + selectedQueenMarker).css("color", "yellow");
        allMarkers[selectedQueenMarker].setIcon(queenIcon);
        selectedQueenMarker = "";        
    }
}

var dummydata = '[{ "_id": "2837hf3", "scout":"scout1", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.509, "longitude":-0.08, "description":"", "time":13, "needsTransmit":false },{ "_id": "3837hf3","scout":"scout2", "queen":"", "isWaypoint":false, "isCurrent":false, "latitude":51.508, "longitude":-0.09, "description":"", "time":13, "needsTransmit":false },{ "_id": "4837hf3","scout":"scout3", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.507, "longitude":-0.10, "description":"", "time":13, "needsTransmit":false }, { "_id": "5837hf3", "scout":"scout5", "queen":"queen1", "isWaypoint":true, "isCurrent":false, "latitude":51.505, "longitude":-0.12, "description":"", "time":13, "needsTransmit":false }, {"_id": "7837hf3", "scout":"scout5", "queen":"queen1", "isWaypoint":true, "isCurrent":false, "latitude":51.504, "longitude":-0.13, "description":"", "time":13, "needsTransmit":false }, { "_id": "8837hf3", "scout":"", "queen":"queen5", "isWaypoint":false, "isCurrent":true, "latitude":51.503, "longitude":-0.014, "description":"", "time":13, "needsTransmit":false }]';

var dp = '{ "_id": "6837hf3", "scout":"scout3", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.506, "longitude":-0.11, "description":"", "time":13, "needsTransmit":false }';

processAllPoints(JSON.parse(dummydata));
updateCurrentLocation("scout1", JSON.parse(dp));
console.log("finsih parsing");


