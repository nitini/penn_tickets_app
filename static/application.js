$(document).ready(function() {
  var loginShouldBeShowing = false;
  var signupShouldBeShowing = false;
  $('#login-dropdown').click(function() {
    loginShouldBeShowing = true;
    $('#login-form-dropdown').toggle();
    $('#signup-form-dropdown').hide();
  });
  $('#signup-dropdown').click(function() {
    signupShouldBeShowing = true;
    $('#signup-form-dropdown').toggle();
    $('#login-form-dropdown').hide();
  });
  $('.datepicker').datepicker();
  $('.timepicker').timepicker({
    minuteStep: 1,
    showInputs: false,
    disableFocus: true
  });
  $('body').click(function() {
    if(!loginShouldBeShowing)
      $('#login-form-dropdown').hide();
    if(!signupShouldBeShowing)
      $('#signup-form-dropdown').hide();
    loginShouldBeShowing = false;
    signupShouldBeShowing = false;
  });
  $('#login-form-dropdown').click(function() {
    loginShouldBeShowing = true;
  });
  $('#signup-form-dropdown').click(function() {
    signupShouldBeShowing = true;
  });
});
