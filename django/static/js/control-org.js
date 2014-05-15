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
});