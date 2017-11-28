//Stored Variables of scout tracks, scout positions, MIT campus polygon, and MIT lobby 7 marker.

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
                "underConstruction": false
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
                "underConstruction": false
            },
            "id": 2
        }
    ]
};

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
                "popupContent": "Scout Position 1"
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
                "popupContent": "Scout Position 2"
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
                "popupContent": "Scout Position 3"
            },
            "id": 52
        }
    ]
};

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

var lobby7mit = {
    "type": "Feature",
    "properties": {
        "popupContent": "77 Mass Ave, Lobby 7 at MIT!"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [-71.093389, 42.359083]
    }
};
