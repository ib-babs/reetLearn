window.addEventListener("load", function () {
  $('.message').fadeOut(2000);
  const showHidePassword = $("#show-hide-password");
  $(showHidePassword).click(function (e) {
    if ($(showHidePassword).text() == "Show") {
      $(showHidePassword).text("Hide");
      $("#user-password").attr("type", "text");
    } else {
      $(showHidePassword).text("Show");
      $("#user-password").attr("type", "password");
    }
  });
  
  $('.auth-btn-facebook, .auth-btn-apple, .auth-btn-google').click(()=>{
    alert('Coming soon...')
  })
});
