$(document).ready(function() {
	//$('#build-shelf-message').fadeOut(1725);
	setTimeout("$('#build-shelf-message').fadeOut(1725)", 750);
	$('#barcode').focus(); 
	
	//getItems();
	
	$('#lookup').submit(function() {
		var barcode = $('#barcode').val();
		var sort = 10;
		var last_sort = $('.order_item:first').find('.order input').val();
		if(last_sort)
			sort = parseInt(last_sort) + 10;
		
		$.post('/services/new-shelf-item/', {barcode: barcode, shelf: shelf, csrfmiddlewaretoken: CSRF_TOKEN, sort: sort}).done(function(data) {
			$('#barcode').val('').focus();
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
      		$('.order_list').prepend(template(data));
			$('.alert').html('<span class="success">Got it!</span>');
		}).fail(function(data) {
    			$('.alert').html('<span class="error">The barcode lookup failed - no data</span>');
    		});
		
		return false;
	});
	
	$('#new-blank-item').on("click", function(event) { console.log(shelf)
		var sort = 10;
		var last_sort = $('.order_item:first').find('.order input').val();
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
      		$('.order_list').prepend(template(data));
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
            
            var j = 0;
            // redo all of the order numbers in multiples of 10
            for( i = item_order.length - 1; i >= 0; i-- ) {
                var item = item_order[i];
                var new_order = (j + 1) * 10;
                j++;
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