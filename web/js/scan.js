var title = '',
creator = '',
hollis = '',
isbn = '',
val = 10,
timer;
$(document).ready(function() {
	$('#barcode').focus();
    $('#lookup').submit(function() {
      $('.alert').hide();
      function updateProgress() {
        val += 10;
        $('.bar').css('width', val + '%');
        if(val < 100)
          timer = setTimeout(updateProgress, 500);
      }
      $('.bar').css('width', '10%')
      $('.progress').show();
      updateProgress();
    	var barcode = $('#barcode').val();
    	$.getJSON('lookup.php?barcode=' + barcode,
			function (data) {
			  $('.bar').css('width', '100%');
			  $('.progress').hide();
			  clearTimeout(timer);
			  if(data) {
          var item = data.rlistFormat.hollis;
          hollis = item.hollisId.substr(0, 9);
          title = item.title;
          
          var isbn = -1;
          if(item.isbn instanceof Array)
            isbn = item.isbn[0] + '';
          else
            isbn = item.isbn + '';
  
          if (isbn.indexOf(" ") != -1) {
            isbn = isbn.split(' ')[0];
          }
          
          $.ajax({
              url: 'convert.php?isbn=' + isbn,
              async: false,
              success: function(isbn10){
                        isbn = isbn10;
                    }
          });
          
          if(item.authors.authorName) {
            var authorName = item.authors.authorName;
            if(authorName instanceof Array)
              authorName = authorName[0];
            creator = authorName.authorFirst.replace(/\.$/, "") + ' ' + authorName.authorLast;
          }
  
          $('#barcode').val('').focus();
          $('.bar').css('width', '10%')
          
          var url = "services/awesome-service.php";
      
          $.post(url, {id: hollis, title: title, creator: creator, isbn: isbn}, function(data) {
              $('.alert-success').show();
              $('.added-title').html(title)
          });
          
          $.post('tweet.php', {id: hollis, title: title, creator: creator, isbn: isbn});
				}
				else {
				  $('.alert-error').text('The barcode lookup failed').fadeIn();;
				}
			});
		return false;	
	});
});
