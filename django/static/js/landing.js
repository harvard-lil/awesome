$(document).ready(function() {
  $('#hard-results li.item').on('click', function(event) {
    if (!$(event.target).is(".item-amazon-link")) {
		var link = $(this).find('a.item-worldcat-link').attr('href');
		window.open(link);
		return false;
		}
	});
    
    $('#hard-results').slick({
          infinite: false,
          slidesToShow: 5,
          slidesToScroll: 5,
          slide: 'li',
          responsive: [
            {
              breakpoint: 1200,
              settings: {
                slidesToShow: 2,
                slidesToScroll: 2,
                slide: 'li'
              }
            },
            {
              breakpoint: 1000,
              settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
                slide: 'li'
              }
            },
            {
              breakpoint: 700,
              settings: {
                slidesToShow: 2,
                slidesToScroll: 2,
                slide: 'li',
                arrows: false
              }
            },
            {
              breakpoint: 570,
              settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
                slide: 'li',
                arrows:false
              }
            }
          ]
        });
});