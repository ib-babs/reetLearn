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

  // $("#sign-in-form").on("submit", function (e) {
  //   var formArray = $(this).serializeArray(),
  //     formData = {};
  //   $.each(formArray, function () {
  //     formData[this.name] = this.value;
  //   });
  //   var jsonData = JSON.stringify(formData);

  //   $.ajax({
  //     type: "POST",
  //     url: "http://localhost:5001/api/v1/login",
  //     data: jsonData,
  //     contentType: "application/json",
  //     success: function (response) {
  //       $(".message").text("Login successful!");
  //       $(".message").css("color", "green");
  //       localStorage.setItem("access_token", response["access_token"]);
  //       localStorage.setItem("id", response["user"]["id"]);
  //     },
  //     error: function (xhr) {
  //       localStorage.setItem("access_token", "");
  //       localStorage.setItem("id", "");
  //       $(".message").text(xhr.responseJSON["msg"]);
  //     },
  //   });
  // });


  $('.auth-btn-facebook, .auth-btn-apple, .auth-btn-google').click(()=>{
    alert('Coming soon...')
  })
});
