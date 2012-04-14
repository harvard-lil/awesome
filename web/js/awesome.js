$(document).ready(function() {
		
	var url = "services/awesome-service.php";

	var awesomeList = '';
		
	$.get(url, function(data) {
  		$.each(data.docs, function(i,item){
			var creator_full = '';
			if (item.creator && item.creator.length > 0) {
				creator_full = item.creator;
			}
			var isbn = item.isbn;
			var row = '';
			if(i == 0 || i == 3 || i == 6)
				row = ' alpha';
			if(i == 2 || i == 5 || i == 8)
				row = ' omega';
            awesomeList += '<div class="grid_4 item' + row + '"><img class="faceUp-book-image" src="http://images.amazon.com/images/P/' + isbn + '.01.ZTZZZZZZ.jpg" alt="' + item.title + '" /><span class="faceUp-details"><p class="faceUp-title"><a href="http://hollis.harvard.edu/?itemid=|library/m/aleph|' + item.hollis_id + '" target="_blank">' + item.title + '</a></p><p class="faceUp-author">' + creator_full + '</p></div>';
  		});
  		$('#awesome').html(awesomeList);
	});

	$('.item').live('click', function() {
		var link = $(this).find('a').attr('href');
		window.open(link);
	});
});