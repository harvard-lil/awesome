var val = 10;
var timer;

$(document).ready(function() {
	$('#barcode').focus();
	
	
	
	function getURLParameter(name) {
        return decodeURI(
            (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
        );
    }

    var branch = getURLParameter('branch');
    
    if (branch) {
        $("select option").each(function(){
        if ($(this).val() == branch)
            $(this).attr("selected","selected");
        });
    }

    
	
	$('#lookup').submit(function() {
		$('.alert').hide();
		$('.progress').show();
	
	    var val = 0;
	
		function updateProgress() {
			val += 10;
			$('.bar').css('width', val + '%');
			if (val < 100) {
				timer = setTimeout(updateProgress, 500);
			}
		}
		updateProgress();
		var barcode = $('#barcode').val();
		var scanning_lib = $('#scanning_library option:selected').val();
		
		$.post('/services/new-item/', {barcode: barcode, branch: scanning_lib, csrfmiddlewaretoken: CSRF_TOKEN}).done(function(data) {
			$('.alert-success').show();
			$('.progress').hide();
			$('.added-title').html(data);
		}).fail(function(data) {
    			$('.progress').hide();
    			$('.alert-error').text('The barcode lookup failed - no data').fadeIn();
    		});
		
		return false;
	});
});