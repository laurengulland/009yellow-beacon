$(document).ready(function () {

  // On submit button click, create the activity and display it.
  $('.delete-button').click(function () {
    // Create activity with POST request.apparently not right
    $.ajax({
        url: '/deleteTweet',
        type: 'DELETE',
        headers: {"tweetid": this.id},
        success: window.location.replace('/profile')
    });
  });
});