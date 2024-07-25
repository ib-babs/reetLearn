window.addEventListener("load", () => {
  if (window.outerWidth < 620) {
    $(".aside-detail").css("display", "none");
    $(".sidebar").css("display", "block");
  }
  window.addEventListener("resize", () => {
    if (window.outerWidth < 620) {
      $(".aside-detail").css("display", "none");
      $(".sidebar").css("display", "block");
    }
    if (window.outerWidth >= 620) {
      $(".aside-detail").css("display", "block");
      $(".sidebar").css("display", "block");
    }
  });
  // $("#settings").click(() => {
  //   // showHideAsideDetail(
  //   //   "#information-detail",
  //   //   "#password-detail",
  //   //   "#delete-account-detail"
  //   // );
  // });
  $("#profile-modal-visibility-btn").click(() => {
    $(".profile-modal").toggle();
  });



  const currPwd = $("#show-hide-password"),
    newPwd = $("#new-hide-password");
  $(currPwd).click(() => showHidePassword(currPwd, "#current-password"));
  $(newPwd).click(() => showHidePassword(newPwd, "#new-password"));
  function showHidePassword(el, pwdElID) {
    if ($(el).text() == "Show") {
      $(el).text("Hide");
      $(pwdElID).attr("type", "text");
    } else {
      $(el).text("Show");
      $(pwdElID).attr("type", "password");
    }
  }

  function showHideAsideDetail(detailToShow, detailToHide1, detailToHide2) {
    $(detailToShow).removeAttr("hidden");
    $(detailToHide1).attr("hidden", "hidden");
    $(detailToHide2).attr("hidden", "hidden");
    resizeProfileModal();
  }
  function resizeProfileModal() {
    const asideLi = document.querySelectorAll(".aside-li");
    asideLi.forEach((val) => {
      if (val.classList.contains("aside-profile-item"))
        val.classList.remove("aside-profile-item");
      $(val).click(() => {
        $(val).addClass("aside-profile-item");
      });
    });
    if (window.outerWidth < 620) {
      $(".aside-detail").css("display", "block");
      $(".sidebar").css("display", "none");
      $(".aside-header").click(() => {
        $(".sidebar").css("display", "block");
        $(".aside-detail").css("display", "none");
      });
    }
    if (window.outerWidth >= 620) {
      $(".aside-detail").css("display", "block");
      $("#informatiosn-detail").removeAttr("hidden");
    }
  }

  $("#info-li").click(() =>
    showHideAsideDetail(
      "#information-detail",
      "#password-detail",
      "#delete-account-detail"
    )
  );
  $("#password-li").click(() =>
    showHideAsideDetail(
      "#password-detail",
      "#information-detail",
      "#delete-account-detail"
    )
  );
  $("#account-deletion-li").click(() =>
    showHideAsideDetail(
      "#delete-account-detail",
      "#information-detail",
      "#password-detail"
    )
  );

  const countries = [
    { code: "af", name: "Afghanistan" },
    { code: "ax", name: "Aland Islands" },
    { code: "al", name: "Albania" },
    { code: "dz", name: "Algeria" },
    { code: "as", name: "American Samoa" },
    { code: "ad", name: "Andorra" },
    { code: "ao", name: "Angola" },
    { code: "ai", name: "Anguilla" },
    { code: "aq", name: "Antarctica" },
    { code: "ag", name: "Antigua and Barbuda" },
    { code: "ar", name: "Argentina" },
    { code: "am", name: "Armenia" },
    { code: "aw", name: "Aruba" },
    { code: "sh-ac", name: "Ascension Island" },
    { code: "au", name: "Australia" },
    { code: "at", name: "Austria" },
    { code: "az", name: "Azerbaijan" },
    { code: "bs", name: "Bahamas" },
    { code: "bh", name: "Bahrain" },
    { code: "bd", name: "Bangladesh" },
    { code: "bb", name: "Barbados" },
    { code: "es-pv", name: "Basque Country" },
    { code: "by", name: "Belarus" },
    { code: "be", name: "Belgium" },
    { code: "bz", name: "Belize" },
    { code: "bj", name: "Benin" },
    { code: "bw", name: "Botswana" },
    { code: "br", name: "Brazil" },
    { code: "bg", name: "Bulgaria" },
    { code: "bf", name: "Burkina Faso" },
    { code: "bi", name: "Burundi" },
    { code: "kh", name: "Cambodia" },
    { code: "cm", name: "Cameroon" },
    { code: "ca", name: "Canada" },
    { code: "cf", name: "Central African Republic" },
    { code: "cl", name: "Chile" },
    { code: "cn", name: "China" },
    { code: "co", name: "Colombia" },
    { code: "cr", name: "Costa Rica" },
    { code: "hr", name: "Croatia" },
    { code: "cu", name: "Cuba" },
    { code: "cy", name: "Cyprus" },
    { code: "cz", name: "Czech Republic" },
    { code: "ci", name: "Côte d'Ivoire" },
    { code: "cd", name: "Democratic Republic of the Congo" },
    { code: "dk", name: "Denmark" },
    { code: "dg", name: "Diego Garcia" },
    { code: "dj", name: "Djibouti" },
    { code: "dm", name: "Dominica" },
    { code: "do", name: "Dominican Republic" },
    { code: "eac", name: "East African Community" },
    { code: "ec", name: "Ecuador" },
    { code: "eg", name: "Egypt" },
    { code: "sv", name: "El Salvador" },
    { code: "gb-eng", name: "England" },
    { code: "gq", name: "Equatorial Guinea" },
    { code: "er", name: "Eritrea" },
    { code: "ee", name: "Estonia" },
    { code: "sz", name: "Eswatini" },
    { code: "et", name: "Ethiopia" },
    { code: "eu", name: "Europe" },
    { code: "fk", name: "Falkland Islands" },
    { code: "fo", name: "Faroe Islands" },
    { code: "fm", name: "Federated States of Micronesia" },
    { code: "fj", name: "Fiji" },
    { code: "fi", name: "Finland" },
    { code: "fr", name: "France" },
    { code: "gf", name: "French Guiana" },
    { code: "pf", name: "French Polynesia" },
    { code: "tf", name: "French Southern Territories" },
    { code: "ga", name: "Gabon" },
    { code: "es-ga", name: "Galicia" },
    { code: "gm", name: "Gambia" },
    { code: "ge", name: "Georgia" },
    { code: "de", name: "Germany" },
    { code: "gh", name: "Ghana" },
    { code: "gi", name: "Gibraltar" },
    { code: "gr", name: "Greece" },
    { code: "gl", name: "Greenland" },
    { code: "gd", name: "Grenada" },
    { code: "gp", name: "Guadeloupe" },
    { code: "gu", name: "Guam" },
    { code: "gt", name: "Guatemala" },
    { code: "gg", name: "Guernsey" },
    { code: "gn", name: "Guinea" },
    { code: "gw", name: "Guinea-Bissau" },
    { code: "gy", name: "Guyana" },
    { code: "ht", name: "Haiti" },
    { code: "hk", name: "Hong Kong" },
    { code: "hu", name: "Hungary" },
    { code: "is", name: "Iceland" },
    { code: "in", name: "India" },
    { code: "id", name: "Indonesia" },
    { code: "ir", name: "Iran" },
    { code: "iq", name: "Iraq" },
    { code: "ie", name: "Ireland" },
    { code: "im", name: "Isle of Man" },
    { code: "il", name: "Israel" },
    { code: "it", name: "Italy" },
    { code: "jm", name: "Jamaica" },
    { code: "jp", name: "Japan" },
    { code: "je", name: "Jersey" },
    { code: "jo", name: "Jordan" },
    { code: "kz", name: "Kazakhstan" },
    { code: "ke", name: "Kenya" },
    { code: "ki", name: "Kiribati" },
    { code: "xk", name: "Kosovo" },
    { code: "kw", name: "Kuwait" },
    { code: "la", name: "Laos" },
    { code: "lv", name: "Latvia" },
    { code: "arab", name: "League of Arab States" },
    { code: "lb", name: "Lebanon" },
    { code: "ls", name: "Lesotho" },
    { code: "lr", name: "Liberia" },
    { code: "ly", name: "Libya" },
    { code: "li", name: "Liechtenstein" },
    { code: "lt", name: "Lithuania" },
    { code: "lu", name: "Luxembourg" },
    { code: "mo", name: "Macau" },
    { code: "mg", name: "Madagascar" },
    { code: "mw", name: "Malawi" },
    { code: "my", name: "Malaysia" },
    { code: "mv", name: "Maldives" },
    { code: "ml", name: "Mali" },
    { code: "mt", name: "Malta" },
    { code: "mh", name: "Marshall Islands" },
    { code: "mq", name: "Martinique" },
    { code: "mr", name: "Mauritania" },
    { code: "mu", name: "Mauritius" },
    { code: "yt", name: "Mayotte" },
    { code: "mx", name: "Mexico" },
    { code: "md", name: "Moldova" },
    { code: "mc", name: "Monaco" },
    { code: "mn", name: "Mongolia" },
    { code: "me", name: "Montenegro" },
    { code: "ms", name: "Montserrat" },
    { code: "ma", name: "Morocco" },
    { code: "mz", name: "Mozambique" },
    { code: "mm", name: "Myanmar" },
    { code: "na", name: "Namibia" },
    { code: "nr", name: "Nauru" },
    { code: "np", name: "Nepal" },
    { code: "nl", name: "Netherlands" },
    { code: "nc", name: "New Caledonia" },
    { code: "nz", name: "New Zealand" },
    { code: "ni", name: "Nicaragua" },
    { code: "ne", name: "Niger" },
    { code: "ng", name: "Nigeria" },
    { code: "nu", name: "Niue" },
    { code: "nf", name: "Norfolk Island" },
    { code: "kp", name: "North Korea" },
    { code: "mk", name: "North Macedonia" },
    { code: "gb-nir", name: "Northern Ireland" },
    { code: "mp", name: "Northern Mariana Islands" },
    { code: "no", name: "Norway" },
    { code: "om", name: "Oman" },
    { code: "pc", name: "Pacific Community" },
    { code: "pk", name: "Pakistan" },
    { code: "pw", name: "Palau" },
    { code: "pa", name: "Panama" },
    { code: "pg", name: "Papua New Guinea" },
    { code: "py", name: "Paraguay" },
    { code: "pe", name: "Peru" },
    { code: "ph", name: "Philippines" },
    { code: "pn", name: "Pitcairn" },
    { code: "pl", name: "Poland" },
    { code: "pt", name: "Portugal" },
    { code: "pr", name: "Puerto Rico" },
    { code: "qa", name: "Qatar" },
    { code: "cg", name: "Republic of the Congo" },
    { code: "ro", name: "Romania" },
    { code: "ru", name: "Russia" },
    { code: "rw", name: "Rwanda" },
    { code: "re", name: "Réunion" },
    { code: "bl", name: "Saint Barthélemy" },
    { code: "sh-hl", name: "Saint Helena" },
    { code: "sh", name: "Saint Helena, Ascension and Tristan da Cunha" },
    { code: "kn", name: "Saint Kitts and Nevis" },
    { code: "lc", name: "Saint Lucia" },
    { code: "mf", name: "Saint Martin" },
    { code: "pm", name: "Saint Pierre and Miquelon" },
    { code: "vc", name: "Saint Vincent and the Grenadines" },
    { code: "ws", name: "Samoa" },
    { code: "sm", name: "San Marino" },
    { code: "st", name: "Sao Tome and Principe" },
    { code: "sa", name: "Saudi Arabia" },
    { code: "gb-sct", name: "Scotland" },
    { code: "sn", name: "Senegal" },
    { code: "rs", name: "Serbia" },
    { code: "sc", name: "Seychelles" },
    { code: "sl", name: "Sierra Leone" },
    { code: "sg", name: "Singapore" },
    { code: "sx", name: "Sint Maarten" },
    { code: "sk", name: "Slovakia" },
    { code: "si", name: "Slovenia" },
    { code: "sb", name: "Solomon Islands" },
    { code: "so", name: "Somalia" },
    { code: "za", name: "South Africa" },
    { code: "gs", name: "South Georgia and the South Sandwich Islands" },
    { code: "kr", name: "South Korea" },
    { code: "ss", name: "South Sudan" },
    { code: "es", name: "Spain" },
    { code: "lk", name: "Sri Lanka" },
    { code: "ps", name: "State of Palestine" },
    { code: "sd", name: "Sudan" },
    { code: "sr", name: "Suriname" },
    { code: "sj", name: "Svalbard and Jan Mayen" },
    { code: "se", name: "Sweden" },
    { code: "ch", name: "Switzerland" },
    { code: "sy", name: "Syria" },
    { code: "tw", name: "Taiwan" },
    { code: "tj", name: "Tajikistan" },
    { code: "tz", name: "Tanzania" },
    { code: "th", name: "Thailand" },
    { code: "tl", name: "Timor-Leste" },
    { code: "tg", name: "Togo" },
    { code: "tk", name: "Tokelau" },
    { code: "to", name: "Tonga" },
    { code: "tt", name: "Trinidad and Tobago" },
    { code: "sh-ta", name: "Tristan da Cunha" },
    { code: "tn", name: "Tunisia" },
    { code: "tm", name: "Turkmenistan" },
    { code: "tc", name: "Turks and Caicos Islands" },
    { code: "tv", name: "Tuvalu" },
    { code: "tr", name: "Türkiye" },
    { code: "ug", name: "Uganda" },
    { code: "ua", name: "Ukraine" },
    { code: "ae", name: "United Arab Emirates" },
    { code: "gb", name: "United Kingdom" },
    { code: "un", name: "United Nations" },
    { code: "um", name: "United States Minor Outlying Islands" },
    { code: "us", name: "United States of America" },
    { code: "uy", name: "Uruguay" },
    { code: "uz", name: "Uzbekistan" },
    { code: "vu", name: "Vanuatu" },
    { code: "ve", name: "Venezuela" },
    { code: "vn", name: "Vietnam" },
    { code: "vg", name: "Virgin Islands (British)" },
    { code: "vi", name: "Virgin Islands (U.S.)" },
    { code: "gb-wls", name: "Wales" },
    { code: "wf", name: "Wallis and Futuna" },
    { code: "eh", name: "Western Sahara" },
    { code: "ye", name: "Yemen" },
    { code: "zm", name: "Zambia" },
    { code: "zw", name: "Zimbabwe" },
  ];
  $.each(countries, (idx, country) => {
    $("#country").append(
      `<button class='country-name-btn' type='button'><i class="fi fi-${country.code}" style="margin-right: 10px"></i><span>${country.name}</span></button><br>`
    );
  });
  $.each($("#country .country-name-btn"), (idx, btn) => {
    $(btn).click(() => {
      $('#country-input').val($(btn).text())
      $('#country-flag-input').val(countries[idx].code)
      $("#country-name #country-flag-name").text($(btn).text());
      $("#country-name #country-flag").removeAttr('class');
      $("#country-name #country-flag").html(`<span class='fi fi-${countries[idx].code}' id="country-flag"></span>`);
$('#country').toggle()
    });
    $('#country-name').click(()=>{
      $('#country').toggle()

    })
  });
});
