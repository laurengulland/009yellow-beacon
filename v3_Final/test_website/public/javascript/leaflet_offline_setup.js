//var leaflet = require('leaflet');
//var offlineLeafletMap = require('offline-leaflet-map');
//var button = require('./leaflet-button-control');

var myButtonOptions = {
			'text': 'MyButton',  // string
			'iconUrl': '/images/baseball-marker.png',  // string
			'onClick': my_button_onClick,  // callback function
			'hideText': true,  // bool
			'maxWidth': 30,  // number
			'toggle': false,  // bool
			'toggleStatus': false  // bool
		};

		function my_button_onClick(){
			console.log('LOL');
			return offlineLayer.saveTiles(15, (function(_this) {
				return function() {
					return null;
				};
			})(this), (function(_this) {
				return function() {
					//return _this._setIdleState();
				};
			})(this), (function(_this) {
				return function(error) {
					console.log(error);
					//return _this._setIdleState();
				};
			})(this));
		}

		onReady = function() {
			var cacheBtn, progressControls;
			console.log("The OfflineLayer is ready to be used");
			offlineLayer.addTo(mymap);
			cacheBtn = new L.Control.Button(myButtonOptions);
			mymap.addControl(cacheBtn);
			progressControls = new OfflineProgressControl();
			progressControls.setOfflineLayer(offlineLayer);
			return mymap.addControl(progressControls);
		};

		var mymap = L.map('mapid', {attributionControl: false}).setView([51.505, -0.09], 13);

		var offlineLayer = new OfflineLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiMDA5eWVsbG93MTciLCJhIjoiY2phZnkwOHlsMTk1bjJ3cnoxNG4yaGxuNCJ9.ICzaK-eMacI1DF_b9YJcrw', {
			maxZoom: 20,
			minZoom: 13,
			subdomains: 'abc',
			id: 'mapbox.satellite',//Alternatively, 'mapbox.satellite, mapbox.streets'
			accessToken: 'pk.eyJ1IjoiMDA5eWVsbG93MTciLCJhIjoiY2phZnkwOHlsMTk1bjJ3cnoxNG4yaGxuNCJ9.ICzaK-eMacI1DF_b9YJcrw',
			dbOption: "WebSQL",
			onReady: onReady
		})
		offlineLayer.addTo(mymap);
