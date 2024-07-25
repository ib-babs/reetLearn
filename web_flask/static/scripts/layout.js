window.addEventListener("load", () => {

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        $(".header").css("background-color", "white");
      } else {
        $(".header").css("background-color", "#eeeeff");
      }
    });
  });

  const doc = document.querySelectorAll(".landing-page-section"),
    menu = $(".desktop-navbar")[0],
    collapseDesktopMenu = $(".mobile-navbar #collapse-menu");
  doc.forEach((el) => {
    observer.observe(el);
  });

  /**
   * Menu button =
   */
  $(collapseDesktopMenu).click(function (e) {

    if (window.outerWidth < 768) {
      if ($(".profile-nav-menu").css("display") === "block")
        $(".profile-nav-menu").css("display", "none");
      else $(menu).toggle();
      $(collapseDesktopMenu).toggleClass("fa-close");
    }
  });

  /**
   * Goto user account navbar
   */
  $("#user-account-nav-item").click(() => {
    $(".profile-nav-menu").toggle();

    if (window.outerWidth < 768) $(".desktop-navbar").toggle();
  });

  /**
   * Hide user account navbar.
   * Changes menu icon
   * Hides desktop navbar
   */
  $("#goto-desktop-navbar").click(() => {
    $(".profile-nav-menu").toggle();
    if (window.outerWidth < 768) $(".desktop-navbar").toggle();
  });
  window.addEventListener("resize", () => {

    if (window.outerWidth < 768) {
      $(collapseDesktopMenu).removeClass("fa-close");
      $(menu).css("display", "none");
    } 
    if (window.outerWidth >= 768){
      $(menu).css("display", "block");
    }
  });

  $(".update-success").fadeOut(5000);
  $("#message").fadeOut(3000);
  $(".message-container").fadeOut(3000);
});
