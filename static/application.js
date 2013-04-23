$(document).ready(function() {
  $('#login-dropdown').click(function() {
    $('#login-form-dropdown').toggle();
    $('#signup-form-dropdown').hide();
  });
  $('#signup-dropdown').click(function() {
    $('#signup-form-dropdown').toggle();
    $('#login-form-dropdown').hide();
  });
});
