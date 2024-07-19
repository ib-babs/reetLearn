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
  $(collapseDesktopMenu).click(function () {
    $(menu).toggleClass("show-desktop-navbar");
    $(collapseDesktopMenu).toggleClass("fa-close");
    $(".profile-nav-menu").css("display", "none");
  });

  /**
   * Goto user account navbar
   */
  $("#user-account-nav-item").click(() => {
    if ($(".profile-nav-menu").css("display") === "none") {
      $(".profile-nav-menu").css("display", "block");
    } else {
      $(".profile-nav-menu").css("display", "none");
    }
  });

  /**
   * Hide user account navbar.
   * Changes menu icon
   * Hides desktop navbar
   */
  $(
    "#goto-desktop-navbar, #profile-modal-closer, #profile-modal-visibility-btn, #x-close-setting-modal"
  ).click(() => {
    $(".profile-nav-menu").css("display", "none");
    $(collapseDesktopMenu).removeClass("fa-close");
    $(menu).removeClass("show-desktop-navbar");
  });
  window.addEventListener("resize", () => {
    if (window.screen.width >= 768) $(menu).removeClass("show-desktop-navbar");
    else if (window.screen.width <= 320)
      $(collapseDesktopMenu).removeClass("fa-close");
  });

  $(".update-success").fadeOut(5000);
  $("#message").fadeOut(3000);
  $(".message-container").fadeOut(3000);
});
