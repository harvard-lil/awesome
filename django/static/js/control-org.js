$(document).ready(function() {
    $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], .help_cover_user_id, .help_cover_service').hide();
    var cover_service = $('#id_cover_service').val();
    if(cover_service === 'syndetic' || cover_service === 'tlc') {
        $('#id_cover_user_id, label[for="id_cover_user_id"], .help_cover_user_id, .help_cover_service').show();
    }
    else if (cover_service === 'contentcafe') {
        $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], .help_cover_user_id, .help_cover_service').show();
    }
    
  $('#id_cover_service').on('change', function() {
    cover_service = $(this).val();
    $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], .help_cover_user_id, .help_cover_service').fadeOut();
    if(cover_service === 'syndetic' || cover_service === 'tlc') { console.log('here')
        $('#id_cover_user_id, label[for="id_cover_user_id"], .help_cover_user_id, .help_cover_service').fadeIn();
    }
    else if (cover_service === 'contentcafe') {
        $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], .help_cover_user_id, .help_cover_service').fadeIn();
    }
  });
  if(catalog_query === "notset") {
    $('#id_catalog_base_url').css('margin-bottom', '35px');
      $('#id_catalog_base_url').popover({'title': 'Put your catalog search URL here', 'content': "Don't know what this is? Send us an email and we'll take care of it.", 'trigger': 'manual'});
      $('#id_catalog_query').popover({'title': 'Choose what to search by here', 'content': 'ISBN, Title, or Title and Author', 'trigger': 'manual'});
      $('#id_catalog_base_url, #id_catalog_query').popover('show');
  }
});