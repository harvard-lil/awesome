$(document).ready(function() {
  $('#id_b-slug').on('propertychange keyup input paste', function() {
    var slug = $(this).val();
    $('#id_b-slug').next('span').text(slug + '.awesomebox.io');
  });
});