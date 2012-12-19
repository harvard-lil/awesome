$(document).ready(function() {
	
	var recentUrl = "api/item/recently-awesome";
		
	$.get(recentUrl, function(data) {
	  /*$.each(data.docs, function(key, value) { 
      if(value.format == 'videofilm') {       $.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=dte98e86zfhyvryb8r8epcp3&q=Toy+Story&page_limit=1&callback=?', function(data) {
        console.log(data.movies[0].posters.profile);
	        value.poster = data.movies[0].title;
	      });
      }
    });*/
    	var source = $("#items-template").html();
		  var template = Handlebars.compile(source);console.log(data);
      $('#recent').html(template(data));
      $(".item-title").dotdotdot();
	});
	
	$('.newer, .older').live('click', function(event) {
		var start = $(this).attr('data-start');
		if(start >= 0) {
      $.get(recentUrl + '?start=' + start, function(data) {
        var source = $("#items-template").html();
        var template = Handlebars.compile(source);
        $('#recent').html(template(data));
        $(".item-title").dotdotdot();
        $('.newer').attr('data-start', start*1 - 9);
        $('.older').attr('data-start', start*1 + 9);
      });
	  }
		event.preventDefault();
	});
	
	var mostUrl = "api/item/most-awesome";
	
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
});

function showResults(data){ 
  var source = $("#search-template").html();
	var template = Handlebars.compile(source);
	Handlebars.registerPartial("items", $("#items-template").html());
  $('#search-results').html(template(data));
  $(".item-title").dotdotdot();
  $("#search-results").jCarouselLite({
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
	var section1Top =  0;
	// The top of each section is offset by half the distance to the previous section.
	var section2Top =  $('#most-awesome').offset().top - (($('#search').offset().top - $('#most-awesome').offset().top) / 2);
	var section3Top =  $('#search').offset().top - (($('#about').offset().top - $('#search').offset().top) / 2);
	var section4Top =  $('#about').offset().top - (($(document).height() - $('#about').offset().top) / 2);;
	$('nav#primary a').removeClass('active');
	if($(document).scrollTop() >= section1Top && $(document).scrollTop() < section2Top){
		$('nav#primary a.recently-awesome').addClass('active');
	} else if ($(document).scrollTop() >= section2Top && $(document).scrollTop() < section3Top){
		$('nav#primary a.most-awesome').addClass('active');
	} else if ($(document).scrollTop() >= section3Top && $(document).scrollTop() < section4Top){
		$('nav#primary a.search').addClass('active');
	} else if ($(document).scrollTop() >= section4Top){
		$('nav#primary a.about').addClass('active');
	}
	
}