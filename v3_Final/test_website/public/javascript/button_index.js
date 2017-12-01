$(document).ready(function () {

  // when clicking on queen on map or side menu, get POI from backend
    $('#mapid').click(function () {
//        //todo
    });
    
    $('.test-button').click(function () {
    // Create activity with POST request.apparently not right
    $.ajax({
        url: '/test',
        type: 'GET',
        success: function(data) {
          console.log("success after getting button");
          console.log(data);
       },
    });
  });
    
    // if click on current queen, show list of POI
    $('.queen-marker').click(function(){
        $.ajax({
            url: '/allQueenWaypoints',
            type: 'GET',
            headers: {"queenid": this.id},
            success: function(data) {
              console.log(data);
              fillQueenMenu(data);
           },
        });
    });
    
    // if click on poi, show list of POI with poi highlights
    $('.waypoint-marker').click(function() {
        var id = this.id;
        $.ajax({
            url: '/allQueenWaypoints',
            type: 'GET',
            headers: {"queenid": this.id},
            success: function(data) {
                console.log(data);
                fillQueenMenu(data);
                selectMarker(id);
           },
        });        
    });
    
  $('.queen-button').click(function () {
    // Create activity with POST request.apparently not right
    $.ajax({
        url: '/allQueenWaypoints',
        type: 'GET',
        headers: {"queenid": this.id},
        success: function(data) {
          console.log(data);
          var polygon = L.polygon([
      		  [51.509, -0.08],
    		  [51.503, -0.06],
      		  [51.51, -0.047],
              [51.50, -0.048]
		  ]).addTo(mymap);
       },
    });
  });

  $('.queens-list-button').click(function () {
    // Create activity with POST request.apparently not right
    $.ajax({
        url: '/allQueens',
        type: 'GET',
        success: function(data) {
          console.log(data);
          var polygon = L.polygon([
      		  [51.509, -0.08],
    		  [51.503, -0.06],
      		  [51.51, -0.047],
              [51.50, -0.048]
		  ]).addTo(mymap);
       },
    });
  });

//  $('.keyboard-button').click(function () {
//    // Create activity with POST request.apparently not right
//    // var keyboard = $('#keyboard').keyboard();
//    // keyboard.reveal();
//    $('#keyboard').keyboard();
//    console.log('hai')
//  });

  $('.keyboard').keyboard({
//    accepted : function(event, keyboard, el) {
////        var that = this;
//        console.log('The content "' + el.value + '" was accepted!');
//
//    }
  });
    $('.keyboard').bind('accepted', function(e, keyboard, el){
        console.log(el.value);
        $.ajax({
            url: '/addDescription',
            type: 'GET',
            headers: {"description": el.value, "waypoint_id": keyboard.id},
            success: function() {
              var polygon = L.polygon([
                  [51.509, -0.08],
                  [51.503, -0.06],
                  [51.51, -0.047],
                  [51.50, -0.048]
              ]).addTo(mymap);
           },
        });    
    });

//  $('.keyboard-submit-button').click(function () {
//    // Create activity with POST request.apparently not right
//    $.ajax({
//        url: '/addDescription',
//        type: 'GET',
//        headers: {"queenid": this.id},
//        success: function(data) {
//          console.log(data);
//          var polygon = L.polygon([
//      		  [51.509, -0.08],
//    		  [51.503, -0.06],
//      		  [51.51, -0.047],
//              [51.50, -0.048]
//		  ]).addTo(mymap);
//       },
//    });
//  });
});
