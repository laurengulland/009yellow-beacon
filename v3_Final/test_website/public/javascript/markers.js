// vars for icons
var waypointIcon = L.icon({
  iconUrl: 'images/waypoint.png',
  iconSize: [37, 50],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var selectedWaypointIcon = L.icon({
  iconUrl: 'images/selectedWaypoint.png',
  iconSize: [37, 50],
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
  iconUrl: 'images/scout.png',
  iconSize: [20, 20],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

//var queenIcon = L.divIcon({
//  className: 'queenMapIcon',
//  html: '<img src="images/waypoint-icon-blue.png">',
//  iconSize: [37, 37],
//  iconAnchor: [16, 37],
//  popupAnchor: [0, -28]
//});

var queenIcon = L.icon({
  iconUrl: 'images/queen.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var selectedQueenIcon = L.icon({
  iconUrl: 'images/selectedQueen.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

//var selectedQueenIcon = L.divIcon({
//  html: '<img src="images/emo.png"/>',
//  iconSize: [37, 37],
//  iconAnchor: [16, 37],
//  popupAnchor: [0, -28]
//});

var selectedWaypointMarker = "";
var selectedQueenMarker = "";
var allMarkers = {};

//////////////////////////////////
/////  Socket Stuff
//////////////////////////////////

// Point socket to our site
const socket = io('http://localhost:3001');
// This runs when it connects to the server-side library
socket.on('connect', () => {
    console.log("connected on client");
});

// Make a button here for a quick example
const base = document.getElementsByClassName('leaflet-menu-contents')[0];
const test_button = document.createElement('button');
test_button.id = 'test_button';
test_button.innerHTML = 'socket.io test';
base.appendChild(test_button);



test_button.addEventListener('click', () => {
    // On a given event (button click for example), emit a socket message
    // This name has to match the name on the client!
    // This shows sending a JSON object 
    let data = {val: 'hello from client'}
    socket.emit('socket_from_client', data)
}, false)

// Listen for our message from the server
// Remember, the names need to match!
socket.on('socket_from_server', msg => {
    console.log("message from server: ", msg)
});

//////////////////////////////////
/////  End of Socket Stuff
//////////////////////////////////




//////////////// renders markers on map ///////////////////
// runs once to initialize markers upon querying all data from mongo
$.ajax({
    url: '/all',
    type: 'GET',
    success: function(data) {
        processAllPoints(data);
        $.ajax({
            url: '/allQueens',
            type: 'GET',
            success: function(queendata) {
                fillQueenMenu(queendata);
           },
        });
   },
});

// runs every 5sec to read from entire db and draw all markers again
//setInterval(function(){
//    $.ajax({
//        url: '/all',
//        type: 'GET',
//        success: function(data) {
//            processAllPoints(data);
//            if ($(".menuTitle").length > 0) {
//                if ($('.submenuBack').length > 0) {
//                    var id = $('.menuTitle')[0].innerText;
//                    $.ajax({
//                        url: '/allQueenWaypoints',
//                        type: 'GET',
//                        headers: {"queenid": id},
//                        success: function(data) {
//                            fillWaypointMenu(data);
//                       },
//                    }); 
//                } else {
//                    $.ajax({
//                        url: '/allQueens',
//                        type: 'GET',
//                        success: function(queendata) {
//                            fillQueenMenu(queendata);
//                       },
//                    });   
//                }                
//            }
//       },
//    });    
//            
//},5000);


////////// All the map related functions //////////////////////

var processAllPoints = function (allPoints) {
    for (var i = 0; i < allPoints.length; i++) {
        var p = allPoints[i];
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

// runs to replace the current location of queens or scouts
var updateCurrentLocation = function(id, newPoint) {
    var old = allMarkers[id];
    old.setIcon(pastPosIcon);
    helperCurrent(newPoint);
}

var helperCurrent = function(p) {
    if (p.queen.length > 0) {
        var queenMarker = L.marker([p.latitude, p.longitude], {icon: queenIcon}).addTo(mymap);
        queenMarker._icon.id = p.queen;
        queenMarker._icon.classList.add('queen-marker');
//        queenMarker._icon.html = '<img src="images/emo.png">';
        allMarkers[p.queen] = queenMarker;                    
    } else if (p.scout.length > 0){
        var scoutMarker = L.marker([p.latitude, p.longitude], {icon: scoutIcon}).addTo(mymap);
        scoutMarker._icon.id = p.scout;
        scoutMarker._icon.classList.add('scout-marker');
        allMarkers[p.scout] = scoutMarker;
    } 
//    if (selectedQueenMarker) {
//        allMarkers[selectedQueenMarker].setIcon(selectedQueenIcon);        
//    } else if (selectedWaypointMarker) {
//        allMarkers[selectedWaypointMarker].setIcon(selectedQueenIcon);        
//    }
}

// populates side menu with all waypoints associated with a given queen
var fillWaypointMenu = function(listWaypoints) {
    $("#leafletSideMenuContent").remove();
    var menuContent = "<div id='leafletSideMenuContent'>";
    if (listWaypoints) {
        menuContent += "<i class='fa fa-chevron-left submenuBack'></i>";
        menuContent += "<div class='menuTitle'>" + listWaypoints[0].queen + "</div>";
        for (var i = 0; i < listWaypoints.length; i++) {
            var waypoint = listWaypoints[i];
            var time = new Date(waypoint.time).toTimeString().split(' ')[0].substring(0, 5);
            var waypointContent = "<div class = 'queenmenublock waypoint-marker' id = 'menu" + waypoint._id +"'>";
            waypointContent += "<div class = 'submenuName'>POI: " + waypoint.scout + "</div>";
            waypointContent += "<div class = 'submenuCoord'>" + waypoint.latitude + "°N, " +  waypoint.longitude + "°W</div>";
            waypointContent += "<div class ='submenuTime'>" + time + "</div>";
            if (waypoint.description) {
                waypointContent += "<div class ='submenuText'>" + waypoint.description + "</div>";
            } else {
                waypointContent += '<form class="form-inline" action="addDescription" method="post">';
                waypointContent += "<input class='form-control descriptionInput' type='text' name='descriptionInput' placeholder='Enter description'>";
                waypointContent += "<input type='hidden' name='waypoint_id' value='" + waypoint._id + "'>";
                waypointContent +='<button type="submit" class="btn-default descriptionButton">Save</button>';
                waypointContent += "</form>";
            }
            
            menuContent += waypointContent + "</div>";
        }        
    }
    menuContent += "</div>";
    $(".leaflet-menu-contents").append(menuContent);
    $('#menu' + selectedWaypointMarker).css("background-color", "white");
    button_functions();
}

// populates sidemenu with all queens in database
var fillQueenMenu = function(listQueens) {
    $("#leafletSideMenuContent").remove();
    var menuContent = "<div id='leafletSideMenuContent'>";
    if (listQueens) {
        menuContent += "<div class='menuTitle'>List of Queens</div>";
        for (var i = 0; i < listQueens.length; i++) {
            var queen = listQueens[i];
            var time = new Date(queen.time).toTimeString().split(' ')[0].substring(0, 5);
            var queenContent = "<div class = 'queenmenublock queen-marker' id = 'menu" + queen.queen +"'>";
            queenContent += "<div class = 'submenuName'>" + queen.queen + "</div>";
            queenContent += "<div class = 'submenuCoord'>" + queen.latitude + "°N, " +  queen.longitude + "°W</div>";
            queenContent += "<div class ='submenuTime'>Last received: " + time + "</div>";
            menuContent += queenContent + "</div>";
        }        
    }
    menuContent += "</div>";
    $(".leaflet-menu-contents").append(menuContent);
    $('#menu' + selectedQueenMarker).css("background-color", "white");
    button_functions();
}

var selectWaypointMarker = function(markerid) {
    if (markerid.length < 1) {
        return;
    }
    deselectMarker();
    mymap.panTo(allMarkers[markerid].getLatLng());
    $('#menu' + markerid).css("background-color", "white");
    allMarkers[markerid].setIcon(selectedWaypointIcon);
    selectedWaypointMarker = markerid;
}

var selectQueenMarker = function(markerid) {
    if (markerid.length < 1) {
        return;
    }
    deselectMarker();
    mymap.panTo(allMarkers[markerid].getLatLng());
    allMarkers[markerid].setIcon(selectedQueenIcon);
    selectedQueenMarker = markerid;
}

var deselectMarker = function() {
    if (selectedWaypointMarker.length > 0) {
        $('#menu' + selectedWaypointMarker).css("background-color", "yellow");
        allMarkers[selectedWaypointMarker].setIcon(waypointIcon);
        selectedWaypointMarker = "";        
    } else if (selectedQueenMarker.length > 0) {
        $('#menu' + selectedQueenMarker).css("background-color", "yellow");
        allMarkers[selectedQueenMarker].setIcon(queenIcon);
        selectedQueenMarker = "";        
    }
}

//var dummydata = '[{ "_id": "2837hf3", "scout":"", "queen":"queen10", "isWaypoint":false, "isCurrent":true, "latitude":51.509, "longitude":-0.08, "description":"", "time":13, "needsTransmit":false },{ "_id": "3837hf3","scout":"scout2", "queen":"", "isWaypoint":false, "isCurrent":false, "latitude":51.508, "longitude":-0.09, "description":"", "time":13, "needsTransmit":false },{ "_id": "4837hf3","scout":"scout3", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.507, "longitude":-0.10, "description":"", "time":13, "needsTransmit":false }, { "_id": "5837hf3", "scout":"scout5", "queen":"queen1", "isWaypoint":true, "isCurrent":false, "latitude":51.505, "longitude":-0.12, "description":"", "time":13, "needsTransmit":false }, {"_id": "7837hf3", "scout":"scout5", "queen":"queen1", "isWaypoint":true, "isCurrent":false, "latitude":51.504, "longitude":-0.13, "description":"", "time":13, "needsTransmit":false }, { "_id": "8837hf3", "scout":"", "queen":"queen5", "isWaypoint":false, "isCurrent":true, "latitude":51.503, "longitude":-0.014, "description":"", "time":13, "needsTransmit":false }]';
//
//var dp = '{ "_id": "6837hf3", "scout":"scout3", "queen":"", "isWaypoint":false, "isCurrent":true, "latitude":51.506, "longitude":-0.11, "description":"", "time":13, "needsTransmit":false }';
//
//var listq = '[{ "_id": "2837hf3", "scout":"", "queen":"QueenLatifah", "isWaypoint":false, "isCurrent":true, "latitude":51.509, "longitude":-0.08, "description":"", "time":13, "needsTransmit":false }]';
//
//processAllPoints(JSON.parse(dummydata));
////updateCurrentLocation("scout1", JSON.parse(dp));
//fillQueenMenu(JSON.parse(listq));
//fillQueenMenu(JSON.parse(dummydata));
//console.log("finsih parsing");