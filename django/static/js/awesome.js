$(document).ready(function() {
	
	//////
	// Start of recent items logic
	//////
	
	var recentUrl = "/api/v1/item/";
	
	var recent_url_params = {
		'format': 'json',
		'order_by': '-latest_checkin',
		'branch__organization__slug': organization,
		'limit': limit,
		'offset': 0
	}
	
	if (branch) {
	    recent_url_params.branch__slug = branch;
	}

	// Draw the recent items on load
	draw_recent_items(recentUrl, recent_url_params);
	
	// Pagination buttons
	$('.newer, .older').live('click', function(event) {
		var start = $(this).attr('data-start');
		
		recent_url_params.offset = start;
		if(start >= 0) {
			draw_recent_items(recentUrl, recent_url_params);	
		    $('.newer').attr('data-start', start*1 - limit);
        	$('.older').attr('data-start', start*1 + limit);
	  }
		event.preventDefault();
	});
	
	
	$('.filter').live('click', function(event) {
		filter = $(this).attr('data-filter');
	  
	  
		if($(this).hasClass('selected')) {
	    	$('.selected').removeClass('selected');
	    	delete recent_url_params['physical_format'];
	  	}
	  	else { 
	    	$('.selected').removeClass('selected');
		  	$(this).addClass('selected');
		  	recent_url_params.physical_format = filter;
		}
		
		draw_recent_items(recentUrl, recent_url_params);
	});
	
	
	//////
	// End of recent items logic
	//////
	
	var mostUrl = "/api/v1/item/?format=json&order_by=-number_checkins&limit=" + limit + "&branch__organization__slug=" + organization;
	
	if (branch) {
	    mostUrl = mostUrl + "&branch__slug=" + branch;
	}

	$.get(mostUrl, function(data) {
	  var source = $("#items-template").html();
	  var template = Handlebars.compile(source);
      $('#most').html(template(data));
      $(".item-title").dotdotdot();
	});

	$('.item').live('click', function(event) {
		var link = $(this).find('a').attr('href');
		window.open(link);
		event.preventDefault();
	});
	
	$('#search-awesome').submit(function() {
		var query = $("#query").val();
		$.get("api/item/search?limit=45&filter=_all:" + query, function(data) {
		  showResults(data);
		});
		return false;
	});
	
	redrawDotNav();
	
	/* Scroll event handler */
    $(window).bind('scroll',function(e){
    	parallaxScroll();
		redrawDotNav();
    });
    
	/* Next/prev and primary nav btn click handlers */
	$('a.recently-awesome').click(function(){
    	$('html, body').animate({
    		scrollTop:0
    	}, 1000, function() {
	    	parallaxScroll(); // Callback is required for iOS
		});
    	return false;
	});
    $('a.most-awesome').click(function(){
    	$('html, body').animate({
    		scrollTop:$('#most-awesome').offset().top
    	}, 1000, function() {
	    	parallaxScroll(); // Callback is required for iOS
		});
    	return false;
    });
    $('a.search').click(function(){
    	$('html, body').animate({
    		scrollTop:$('#search').offset().top
    	}, 1000, function() {
	    	parallaxScroll(); // Callback is required for iOS
		});
    	return false;
    });
	$('a.about').click(function(){
    	$('html, body').animate({
    		scrollTop:$('#about').offset().top
    	}, 1000, function() {
	    	parallaxScroll(); // Callback is required for iOS
		});
    	return false;
    });
    
    /* Show/hide dot lav labels on hover */
    $('nav#primary a').hover(
    	function () {
			$(this).prev('h1').show();
		},
		function () {
			$(this).prev('h1').hide();
		}
    );	
    
    Handlebars.registerHelper('catalogQuery', function(object) {
      if(object.branch.organization.catalog_query == 'isbn')
        return object.catalog_id;
      else if(object.branch.organization.catalog_query == 'title')
        return object.title;
      else if(object.branch.organization.catalog_query == 'titleauthor')
        return object.title + "+" + object.creator;
      else if(object.branch.organization.catalog_query == 'landing' || object.branch.organization.catalog_query == 'notset')
        return '';
  });
  
  Handlebars.registerHelper('coverURL', function(object) {
    if(object.isbn == '' && object.isbn != null)
        return "http://" + object.branch.organization.slug + ".awesomebox.io/static/images/grey-cover.png";
    else if(object.branch.organization.cover_service == 'openlibrary' || object.branch.organization.cover_service == 'notset')
        return "http://covers.openlibrary.org/b/isbn/" + object.isbn + "-M.jpg";
    else if(object.branch.organization.cover_service == 'syndetic')
        return "http://www.syndetics.com/index.php?isbn=" + object.isbn + "/mc.gif&client=" + object.branch.organization.cover_user_id;
    else if(object.branch.organization.cover_service == 'tlc')
        return "http://content.tlcdelivers.com/tlccontent?customerid=" + object.branch.organization.cover_user_id + "&requesttype=bookjacket-md&isbn=" + object.isbn;
    else if(object.branch.organization.cover_service == 'contentcafe')
        return "http://contentcafe2.btol.com/ContentCafe/Jacket.aspx?&userID=" + object.branch.organization.cover_user_id + "&password=" + object.branch.organization.cover_password + "&Value=" + object.isbn + "&content=M&Return=1&Type=M";
  });
});

function showResults(data){ 
  var source = $("#most-template").html();
	var template = Handlebars.compile(source);
	Handlebars.registerPartial("items", $("#items-template").html());
  $('#most-results').html(template(data));
  $(".item-title").dotdotdot();
  $("#most-results").jCarouselLite({
    btnNext: ".right",
    btnPrev: ".left",
    speed: 600,
    circular: false,
    visible: 3
  });
}

/* Scroll the background layers */
function parallaxScroll(){
	var scrolled = $(window).scrollTop();
	$('#parallax-bg1').css('top',(0-(scrolled*.25))+'px');
	$('#parallax-bg2').css('top',(0-(scrolled*.5))+'px');
	$('#parallax-bg3').css('top',(0-(scrolled*.75))+'px');
}

/* Set navigation dots to an active state as the user scrolls */
function redrawDotNav(){
	// The top of each section is offset by half the distance to the previous section.
	var section1Top =  0;
	var section2Top =  $('#most-awesome').offset().top - (($('#about').offset().top - $('#most-awesome').offset().top) / 2);
	var section3Top =  $('#about').offset().top - (($(document).height() - $('#about').offset().top) / 2);;
	
	$('nav#primary a').removeClass('active');
	if($(document).scrollTop() >= section1Top && $(document).scrollTop() < section2Top){
		$('nav#primary a.recently-awesome').addClass('active');
	} else if ($(document).scrollTop() >= section2Top && $(document).scrollTop() < section3Top){
		$('nav#primary a.most-awesome').addClass('active');
	} else if ($(document).scrollTop() >= section3Top){
		$('nav#primary a.about').addClass('active');
	}
	
}

function draw_recent_items(recentUrl, recent_url_params) {
	/* Get data using our URL and URL params. Send it to Handlebars to draw to the DOM. */
	$.get(recentUrl, recent_url_params).done( function(data) {
		var source = $("#items-template").html();
		var template = Handlebars.compile(source);
		$('#recent').html(template(data));
		$(".item-title").dotdotdot();
	});
}