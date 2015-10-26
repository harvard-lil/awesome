$(document).ready(function() {
	$('#barcode').focus(); 
	
	getItems();
	
	$('#lookup').submit(function() {
		var barcode = $('#barcode').val();
		
		$.post('/services/new-shelf-item/', {barcode: barcode, shelf: shelf, csrfmiddlewaretoken: CSRF_TOKEN}).done(function(data) {
			$('#barcode').val('').focus();
			getItems()
			$('.status').text('');
		}).fail(function(data) {
    			$('.status').text('The barcode lookup failed - no data');
    		});
		
		return false;
	});
	
	function getItems() {
		$.getJSON( "/api/v1/shelf-item/?format=json&shelf=" + shelf, function( data ) {
  			var source = $("#items-template").html();
	  		var template = Handlebars.compile(source);
      		$('#shelf-items').html(template(data));
		});
	}
});