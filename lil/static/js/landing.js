$(document).ready(function() {
  $('#learn-how').submit(function() {
    var email = $('#email').val();
	  $.post('/services/learn-how/', {csrfmiddlewaretoken: CSRF_TOKEN, email: email}, function(data) {
      $('#signed-up').text("Thanks, we'll be in touch").fadeIn();
    });
  return false;
  });
});