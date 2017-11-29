$(document).ready(function () {

  // On submit button click, create the activity and display it.
  $('.delete-button').click(function () {
    // Create activity with POST request.apparently not right
    console.log("clicked buttom");
    $.ajax({
        url: '/allQueenWaypoints',
        type: 'GET',
        headers: {"queenid": this.class},
        success: function(data) {
          console.log(data);
          console.log('process sucess');
        var polygon = L.polygon([
    		[51.509, -0.08],
    		[51.503, -0.06],
    		[51.51, -0.047],
            [51.50, -0.048]
		]).addTo(mymap);
       },
    });
  });
});