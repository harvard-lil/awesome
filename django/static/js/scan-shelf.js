$(document).ready(function() {
	//$('#build-shelf-message').fadeOut(1725);
	setTimeout("$('#build-shelf-message').fadeOut(1725)", 750);
	$('#barcode').focus(); 
	
	//getItems();
	
	$('#lookup').submit(function() {
		var barcode = $('#barcode').val();
		var sort = 10;
		var last_sort = $('.order_item:last').find('.order input').val();
		if(last_sort)
			sort = parseInt(last_sort) + 10;
		
		$.post('/services/new-shelf-item/', {barcode: barcode, shelf: shelf, csrfmiddlewaretoken: CSRF_TOKEN, sort: sort}).done(function(data) {
			$('#barcode').val('').focus();
			$('.success, .error').hide();
			//getItems()
			var total = $('#id_form-TOTAL_FORMS').val();
			data.form_num = total;
   		 	total++;
   		 	data.item_num = total;
   		 	data.sort = sort;
    		$('#id_form-TOTAL_FORMS').val(total);
    		$('#id_form-INITIAL_FORMS').val(total);
			var source = $("#items-template2").html();
	  		var template = Handlebars.compile(source);
      		$('.order_list').append(template(data));
			$('.success').text('Got it!').fadeIn();
		}).fail(function(data) {
    			$('.error').text('The barcode lookup failed - no data').fadeIn();
    		});
		
		return false;
	});
	
	$('#new-blank-item').on("click", function(event) {
		var sort = 10;
		var last_sort = $('.order_item:last').find('.order input').val();
		if(last_sort)
			sort = parseInt(last_sort) + 10;
		$.post('/services/new-blank-shelf-item/', {shelf: shelf, csrfmiddlewaretoken: CSRF_TOKEN, sort: sort}).done(function(data) {
			var total = $('#id_form-TOTAL_FORMS').val();
			data.form_num = total;
   			total++;
   			data.item_num = total;
   			data.sort = sort;
    		$('#id_form-TOTAL_FORMS').val(total);
    		$('#id_form-INITIAL_FORMS').val(total);
			var source = $("#items-template2").html();
	  		var template = Handlebars.compile(source);
      		$('.order_list').append(template(data));
		});
		
      	event.preventDefault();
	});
	
	$( ".order_list" ).on( "click", "input:checkbox", function() {
  		$(this).closest('.order_item').addClass('deleted-item');
	});
	
	// hide order fields 
    $('span.order').addClass('hidden');

    // turns the list into a sortable one 
    $('div.order_list').sortable({
        update: function(event, ui) {
            var item_order =  $(this).sortable('toArray');
            
            // redo all of the order numbers in multiples of 10
            for( i = 0; i < item_order.length; i++ ) {
                var item = item_order[i];
                var new_order = (i + 1) * 10;
                var selector = '#'+item+' span.order input';
                $(selector).val(new_order);
            }
            
        },
    });
	
	function getItems() {
		$.getJSON( "/api/v1/shelf-item/?format=json&order_by=-date_created&shelf=" + shelf, function( data ) {
  			var source = $("#items-template").html();
	  		var template = Handlebars.compile(source);
      		$('#shelf-items').html(template(data));
		});
	}
});