//Stored Variables of scout tracks, scout positions, MIT campus polygon, and MIT lobby 7 marker.
//This file is acting as a temporary model breakout.

//Icon for waypoints
var waypointIcon = L.icon({
  iconUrl: 'icons/waypoint-icon-red.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

var pastPosIcon = L.icon({
  iconUrl: 'icons/black-dot.png',
  iconSize: [5, 5],
  iconAnchor: [2, 2],
  popupAnchor: [0, -28]
});

var currentPosIcon = L.icon({
  iconUrl: 'icons/waypoint-icon-blue.png',
  iconSize: [37, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});


//Manually inputted scoutTracks TODO: make these dynamically determined based off of scout positions.
var scoutTracks = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-71.094907, 42.358393],
                    [-71.094311, 42.358320]
                ]
            },
            "properties": {
                "popupContent": "Manually inputted track -- Scout Position 1 to 2",
            },
            "id": 1
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-71.094311, 42.358320],
                    [-71.094740, 42.358060]
                ]
            },
            "properties": {
                "popupContent": "Manually inputted track -- Scout Position 2 to 3",
            },
            "id": 2
        }
    ]
};

//Manually Inputted Scout Positions.
var scoutPositions = {
    "type": "FeatureCollection",
    "features": [
        {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -71.094907,
                    42.358393
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": "Scout Position 1",
                "isCurrentPos": true,
                // "icon": pastPosIcon //commented out because it's now determined dynamically by isCurrentPos
            },
            "id": 51
        },
        {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -71.094311,
                    42.358320
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": "Scout Position 2",
                "isCurrentPos": false,
                // "icon": pastPosIcon //commented out because it's now determined dynamically by isCurrentPos
            },
            "id": 54
        },
        {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -71.094740,
                    42.358060
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": "Scout Position 3",
                "isCurrentPos": false,
                // "icon": pastPosIcon //commented out because it's now determined dynamically by isCurrentPos
            },
            "id": 52
        }
    ]
};

//Manually defined polygon around campus. Could be useful if we want to draw a bounding box of area covered at any point.
var campus = {
    "type": "Feature",
    "properties": {
        "popupContent": "This is the MIT Campus",
        "style": {
            weight: 2,
            color: "#999",
            opacity: 1,
            fillColor: "#B0DE5C",
            fillOpacity: 0.8
        }
    },
    "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [-71.094878, 42.360148],
                    [-71.092711, 42.357492],
                    [-71.080040, 42.36126],
                    [-71.084675, 42.362308],
                    [-71.090018, 42.362689]
                ]
            ]
        ]
    }
};

//Manually defined waypoint at Lobby 7ish.
var lobby7mit = {
    "type": "Feature",
    "icon": waypointIcon,
    "properties": {
        "popupContent": "77 Mass Ave, Lobby 7 at MIT!"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [-71.093389, 42.359083]
    }
};
