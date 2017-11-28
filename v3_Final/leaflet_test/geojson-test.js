//Broken out js file -- creates layers, maps, icons, and features. Called by geojson_test.html.
//Modified from Leaflet's geojson example geojson_test.html

//Set Map default view
var map = L.map('map').setView([42.358393, -71.094907], 17);

//Add map tiles to background
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.light'
}).addTo(map);


function onEachFeature(feature, layer) {
  var popupContent = "<p></p>";

  if (feature.properties && feature.properties.popupContent) {
    popupContent += feature.properties.popupContent;
  }

  layer.bindPopup(popupContent);
}

L.geoJSON(campus, {
  style: function (feature) {
    return feature.properties && feature.properties.style;
  },
  onEachFeature: onEachFeature,
}).addTo(map);

var positionLayer = L.geoJSON(scoutPositions,{
  filter: function (feature, layer) {
    if (feature.properties.isCurrentPos == undefined) {
      // if the position doesn't have a value for "isCurrentPos", assume it's not a current position
      feature.properties.icon = pastPosIcon
    } else if (feature.properties.isCurrentPos) {
      // If the property "isCurrentPos" exists and is true, render with a different symbol.
      feature.properties.icon = currentPosIcon
    } else {
      // if the position is not current position, render it with the past position icon.
      feature.properties.icon = pastPosIcon
    }
    return true; //render all
  },
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, {icon: feature.properties.icon});
  },
  onEachFeature: onEachFeature //TODO: this allows you to click on past points, but that's probably not necessary.
  // pointToLayer: function (feature, latlng) {
  //   return L.circleMarker(latlng, {
  //     radius: 8,
  //     fillColor: "#ff7800",
  //     color: "#000",
  //     weight: 1,
  //     opacity: 1,
  //     fillOpacity: 0.8
  //   })
  // }
}).addTo(map);

L.geoJSON(scoutTracks, {
  onEachFeature: onEachFeature,
}).addTo(map);

var mitWaypointLayer = L.geoJSON(lobby7mit, {
  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, {icon: feature.icon});
  },
  onEachFeature: onEachFeature
}).addTo(map);
