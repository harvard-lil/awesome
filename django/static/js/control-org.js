$(document).ready(function() {
    $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], #div_id_cover_service .help-block, #div_id_cover_user_id .help-block').hide();
    var cover_service = $('#id_cover_service').val();
    if(cover_service === 'syndetic' || cover_service === 'tlc') {
        $('#id_cover_user_id, label[for="id_cover_user_id"], #div_id_cover_service .help-block, #div_id_cover_user_id .help-block').show();
    }
    else if (cover_service === 'contentcafe') {
        $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], .help_cover_user_id, .help_cover_service').show();
    }
    
  $('#id_cover_service').on('change', function() {
    cover_service = $(this).val();
    $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], #div_id_cover_user_id .help-block, #div_id_cover_service .help-block').fadeOut();
    if(cover_service === 'syndetic' || cover_service === 'tlc') { console.log('here')
        $('#id_cover_user_id, label[for="id_cover_user_id"], #div_id_cover_user_id .help-block, #div_id_cover_service .help-block').fadeIn();
    }
    else if (cover_service === 'contentcafe') {
        $('#id_cover_user_id, label[for="id_cover_user_id"], #id_cover_password, label[for="id_cover_password"], #div_id_cover_service .help-block, #div_id_cover_user_id .help-block').fadeIn();
    }
  });
  if(catalog_query === "notset") {
    $('#id_catalog_base_url').css('margin-bottom', '35px');
    $('#id_catalog_base_url').popover({'title': 'Put your catalog search URL here', 'content': "Don't know what this is? Send us an email and we'll take care of it.", 'trigger': 'manual'});
    $('#id_catalog_query').popover({'title': 'Choose what to search by here', 'content': 'ISBN, Title, or Title and Author', 'trigger': 'manual'});
    $('#id_catalog_base_url, #id_catalog_query').popover('show');
  }
  if(cover_service === "notset") {
    $('#div_id_cover_service').css('margin-bottom', '35px').css('margin-top', '35px');
    $('#id_cover_service').popover({'title': 'Change your cover images here', 'content': "Don't know if your library has an account? Send us an email and we can help you check.", 'trigger': 'manual'});
    $('#id_cover_service').popover('show');
  }
});