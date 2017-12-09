///////// stored vars for markers ////////////////////
var waypointIcon = L.icon({
  iconUrl: 'images/waypoint.png',
  iconSize: [37, 50],
  iconAnchor: [16, 37],
});

var selectedWaypointIcon = L.icon({
  iconUrl: 'images/selectedWaypoint.png',
  iconSize: [37, 50],
  iconAnchor: [16, 37],
});

var pastPosIcon = L.icon({
  iconUrl: 'images/black-dot.png',
  iconSize: [5, 5],
  iconAnchor: [2, 2],
});

var scoutIcon = L.icon({
  iconUrl: 'images/scout.png',
  iconSize: [20, 20],
  iconAnchor: [10, 10],
});

var selectedWaypointMarker = "";
var selectedQueenMarker = "";
var allMarkers = {};
var waypointOpen = false; //TODO: should be isQueen

///////////// Point socket to our site //////////////////////
const socket = io('http://localhost:3001');
socket.on('connect', () => {
    console.log("connected on client");
});

socket.on('mongo_update', msg => {
    console.log("mongo_update from server: ", msg);
    processAllPoints([msg], false);
    updateMenu(msg);
});


////////// All the map related functions //////////////////////
var processAllPoints = function (allPoints, isInitialize) {
    for (var i = 0; i < allPoints.length; i++) {
        var p = allPoints[i];
        if (p.dummy) {
            continue;
        }
        if (p.isWaypoint) {
            var waypoint = L.marker([p.latitude, p.longitude], {icon: waypointIcon}).addTo(mymap);
            waypoint._icon.id = p._id;
            waypoint._icon.classList.add('waypoint-marker');
            allMarkers[p._id] = waypoint;
            console.log("added waypoint");
        } else {
            if (p.isCurrent) {
                var isStored = p.scout in allMarkers || p.queen in allMarkers;
                if (isInitialize || !isStored) {
                    helperCurrent(p);
                } else {
                    updateCurrentLocation(p);
                }
            } else {
                var pastPos = L.marker([p.latitude, p.longitude], {icon: pastPosIcon}).addTo(mymap);
                console.log("add past point");
            }
        }
    }
}

var drawAllTracks = function() {
    for (var moduleID in allMarkers) {
        if (moduleID.includes("leader")) {
            $.ajax({
                url: '/queenTrack',
                type: 'GET',
                headers: {"queenid": moduleID},
                success: function(data) {
                    drawTracksHelper(data);
                },
            });            
        } else if (moduleID.includes("scout")) {
            $.ajax({
                url: '/scoutTrack',
                type: 'GET',
                headers: {"scoutid": moduleID},
                success: function(data) {
                    drawTracksHelper(data);
                },
            });
        }
    }
}

// draws tracks between each of the scouts
var drawTracksHelper = function(pastPoints){
    console.log("drawing tracks")
    var pathCoords = [];
    for (var i = 0; i < pastPoints.length; i++) {
      x = pastPoints[i].latitude;
      y = pastPoints[i].longitude;
      pathCoords.push([x,y]);
    }
   var pathLine = L.polyline(pathCoords, {
        color: 'grey',
        weight: 2,
        smoothFactor: 3,       
   }).addTo(mymap);
//   pathLine.setStyle({color: 'grey'});
   console.log("drew tracks");
}


// runs to replace the current location of queens or scouts
var updateCurrentLocation = function(newPoint) {
    var previousPoint;
    if (newPoint.queen) {
        previousPoint = allMarkers[newPoint.queen];
    } else {
        previousPoint = allMarkers[newPoint.scout];
    }
    if (previousPoint) {
        previousPoint.setIcon(pastPosIcon);
        var prevCoord = previousPoint.getLatLng();
        var pathline = L.polyline(
            [[prevCoord.lat, prevCoord.lng], [newPoint.latitude, newPoint.longitude]], {
            color: 'grey',
            weight: 2,
            smoothFactor: 3,
        }).addTo(mymap);
    }

    helperCurrent(newPoint);
}

var updateMenu = function(newPoint) {
    if (newPoint.isWaypoint && waypointOpen) {
        // add waypoint menu
        var newWaypoint = createWaypointSubmenu(newPoint);
        $("queenmenublock"+ ":last-child").append(newWaypoint);
    } else if (newPoint.queen && !waypointOpen) {
        if ($('#menu' + newPoint.queen)) { // queen menu already exists
             $('#menu' + newPoint.queen + ' > .submenuTime')[0].innerHTML = newPoint.time;
        } else {
            // create queen menu
            $.ajax({
                url: '/allQueens',
                type: 'GET',
                success: function(queendata) {
                    fillQueenMenu(queendata);
               },
            }); 
        }
    }
}

var helperCurrent = function(p) {
    if (p.queen) {
        var queenIcon = getQueenIcon(p.queen, false);
        var queenMarker = L.marker([p.latitude, p.longitude], {icon: queenIcon}).addTo(mymap);
        queenMarker._icon.id = p.queen;
        queenMarker._icon.classList.add('queen-marker');
        console.log("added queen");
        allMarkers[p.queen] = queenMarker;
    } else if (p.scout){
        var scoutMarker = L.marker([p.latitude, p.longitude], {icon: scoutIcon}).addTo(mymap);
        scoutMarker._icon.id = p.scout;
        scoutMarker._icon.classList.add('scout-marker');
        allMarkers[p.scout] = scoutMarker;
        console.log("added scout");
    }
}

// populates side menu with all waypoints associated with a given queen
var fillWaypointMenu = function(listWaypoints) {
    waypointOpen = true;
    $("#leafletSideMenuContent").remove();
    var menuContent = "<div id='leafletSideMenuContent'>";
    if (listWaypoints) {
        menuContent += "<div class='menuContainer'>";
        if (isHive) {
            menuContent += "<i class='fa fa-chevron-left fa-2 submenuBack'></i>";
        }
        menuContent += "<div class='menuTitle'>" + listWaypoints[0].queen + "</div></div>";
        for (var i = 0; i < listWaypoints.length; i++) {
            menuContent += createWaypointSubmenu(listWaypoints[i]);
        }
    }
    menuContent += "</div>";
    $(".leaflet-menu-contents").append(menuContent);
    $('#menu' + selectedWaypointMarker).css("background-color", "white");
    button_functions();
}

// populates sidemenu with all queens in database
var fillQueenMenu = function(listQueens) {
    waypointOpen = true;
    $("#leafletSideMenuContent").remove();
    var menuContent = "<div id='leafletSideMenuContent'>";
    if (listQueens) {
        menuContent += "<div class='menuContainer'><div class='menuTitle'>List of Leaders</div></div>";
        for (var i = 0; i < listQueens.length; i++) {
            var queen = listQueens[i];
            var time = new Date(queen.time).toTimeString().split(' ')[0].substring(0, 5);
            var queenContent = "<div class = 'queenmenublock queen-marker' id = 'menu" + queen.queen +"'>";
            queenContent += "<div class = 'submenuName'>" + queen.queen + "</div>";
            queenContent += "<div class = 'submenuContent submenuCoord'>" + queen.latitude + "°N, " +  queen.longitude + "°W</div>";
            queenContent += "<div class ='submenuContent submenuTime'>Last received: " + time + "</div>";
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
    var selectedQueenIcon = getQueenIcon(markerid, true);
    allMarkers[markerid].setIcon(selectedQueenIcon);
    selectedQueenMarker = markerid;
}

var deselectMarker = function() {
    if (selectedWaypointMarker.length > 0) {
        $('#menu' + selectedWaypointMarker).css("background-color", "#fbe104");
        allMarkers[selectedWaypointMarker].setIcon(waypointIcon);
        selectedWaypointMarker = "";
    } else if (selectedQueenMarker.length > 0) {
        $('#menu' + selectedQueenMarker).css("background-color", "#fbe104");
        var queenIcon = getQueenIcon(selectedQueenMarker, false);
        allMarkers[selectedQueenMarker].setIcon(queenIcon);
        selectedQueenMarker = "";
    }
}
var createWaypointSubmenu = function(waypoint) {
    var time = new Date(waypoint.time).toTimeString().split(' ')[0].substring(0, 5);
    var description = waypoint.description.replace(new RegExp('9', 'g'), '');
    var waypointContent = "<div class = 'queenmenublock waypoint-marker' id = 'menu" + waypoint._id +"'>";
    waypointContent += "<div class = 'submenuName'>POI: " + waypoint.scout + "</div>";
    waypointContent += "<div class = 'submenuContent submenuCoord'>" + waypoint.latitude + "°N, " +  waypoint.longitude + "°W</div>";
    waypointContent += "<div class ='submenuContent submenuTime'>Time marked: " + time + "</div>";
    if (description || !isQueen) {
        waypointContent += "<div class ='submenuContent submenuText'>" + description + "</div>";
    } else {
        waypointContent += '<form class="form-inline">';
        waypointContent += "<input class='form-control descriptionInput' type='text' name='descriptionInput' placeholder='Enter description'>";
        waypointContent += "<input type='hidden' name='waypoint_id' value='" + waypoint._id + "'>";
        waypointContent +='<button type="submit" class="fa fa-check-square btn descriptionButton"></button>';
        waypointContent += "</form>";
    }
    return waypointContent + "</div>";
}


var getQueenIcon = function(queenid, isSelected) {
    var markerLabel = queenid.replace(/\D/g,'');
    if (isSelected) {
        return L.divIcon({
          className: 'queenMapIcon',
          html: '<div class="selectedQueenMarker"><div class="queenMarkerLabel">' + markerLabel + '</div></div>',
          iconSize: [37, 37],
          iconAnchor: [16, 37],
          popupAnchor: [0, -28]
        });
    }
    return L.divIcon({
      className: 'queenMapIcon',
      html: '<div class="queenMarker"><div class="queenMarkerLabel">' + markerLabel + '</div></div>',
      iconSize: [37, 37],
      iconAnchor: [16, 37],
      popupAnchor: [0, -28]
    });
}
