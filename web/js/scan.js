var title = '',
creator = '',
hollis = '',
isbn = '',
library = '',
val = 10,
timer;
$(document).ready(function() {
	$('#barcode').focus();
    $('#lookup').submit(function() {
      $('.alert').hide();
      $('.progress').show();
      function updateProgress() {
        val += 10;
        $('.bar').css('width', val + '%');
        if(val < 100)
          timer = setTimeout(updateProgress, 500);
      }
      updateProgress();
    	var barcode = $('#barcode').val();
    	$.getJSON('api/services/' + barcode_method + '-lookup', {barcode: barcode},
    	//$.getJSON('api/services/isbn-lookup', {barcode: barcode},
    	//$.getJSON('api/services/wc-lookup', {barcode: barcode},
			function (item) {
			  $('.bar').css('width', '100%');
			  $('.progress').hide();
			  clearTimeout(timer);
			  if(item && item.hollis) {
			    title = '',
          creator = '',
          hollis = '',
          isbn = '',
          library = '';
          hollis = item.hollis;
          title = item.title;
          library = item.library;
          
          var isbn = -1;
          if(item.isbn instanceof Array)
            isbn = item.isbn[0] + '';
          else
            isbn = item.isbn + '';
  
          if (isbn.indexOf(" ") != -1) {
            isbn = isbn.split(' ')[0];
          }
          if(item.creator) {
            creator = item.creator;
          }
          else if(item.authors) {
            if(item.authors.authorName) {
              var authorName = item.authors.authorName;
              if(authorName instanceof Array)
                authorName = authorName[0];
              if(authorName.authorFirst.length > 0)
                creator = authorName.authorFirst.replace(/\.$/, "") + ' ' + authorName.authorLast;
              else
                creator = authorName.authorLast;
            }
          }
  
          $('#barcode').val('').focus();
          $('.bar').css('width', '10%');
          val = 10;
          
          var url = "api/item";
      
          $.post(url, {hollis_id: hollis, title: title, creator: creator, isbn: isbn, library: library, format: item.format, poster: item.poster}, function(data) {
              $('.alert-success').show();
              $('.added-title').html(title)
          });

          $.post('api/services/tweet', {hollis_id: hollis, title: title, creator: creator, isbn: isbn});
				}
				else {
				console.log(item);
				  $('.alert-error').text('The barcode lookup failed - no data').fadeIn();
				}
			})
			.error(function() { 
			  $('.alert-error').text('The barcode lookup failed - cannot connect').fadeIn(); 
			  $('.bar').css('width', '100%');
			  $('.progress').hide();
			  clearTimeout(timer);
			});
		return false;	
	});
});
