//Broken out js file -- creates layers, maps, icons, and features. Called by geojson_test.html.
//Modified from Leaflet's geojson example geojson_test.html

var map = L.map('map').setView([42.358393, -71.094907], 17);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.light'
}).addTo(map);

var baseballIcon = L.icon({
  iconUrl: 'baseball-marker.png',
  iconSize: [32, 37],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
});

function onEachFeature(feature, layer) {
  var popupContent = "<p>I started out as a GeoJSON " +
      feature.geometry.type + ", but now I'm a Leaflet vector!</p>";

  if (feature.properties && feature.properties.popupContent) {
    popupContent += feature.properties.popupContent;
  }

  layer.bindPopup(popupContent);
}

L.geoJSON([scoutPositions, campus], {

  style: function (feature) {
    return feature.properties && feature.properties.style;
  },

  onEachFeature: onEachFeature,

  pointToLayer: function (feature, latlng) {
    return L.circleMarker(latlng, {
      radius: 8,
      fillColor: "#ff7800",
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8
    });
  }
}).addTo(map);

L.geoJSON(scoutTracks, {

  filter: function (feature, layer) {
    if (feature.properties) {
      // If the property "underConstruction" exists and is true, return false (don't render features under construction)
      return feature.properties.underConstruction !== undefined ? !feature.properties.underConstruction : true;
    }
    return false;
  },

  onEachFeature: onEachFeature
}).addTo(map);

var mitLayer = L.geoJSON(lobby7mit, {

  pointToLayer: function (feature, latlng) {
    return L.marker(latlng, {icon: baseballIcon});
  },

  onEachFeature: onEachFeature
}).addTo(map);
