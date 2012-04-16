$(document).ready(function() {
		
	var url = "services/awesome-service.php";
		
	$.get(url, function(data) {
    	var source = $("#awesome-template").html();
		  var template = Handlebars.compile(source);
      $('#recent').html(template(data));
	});

	$('.item').live('click', function(event) {
		var link = $(this).find('a').attr('href');
		window.open(link);
		event.preventDefault();
	});
});