window.addEventListener("load", () => {
  $(".lives").text(10);
  function shuffleArray(array) {
    for (let index = array.length - 1; index > 0; index--) {
      const j = Math.floor(Math.random() * (index + 1));
      [array[index], array[j]] = [array[j], array[index]];
    }
    return array;
  }
  $(".delete-lesson-link").click(function (e) {
    confirm("Are your sure about deleting this lesson?")
      ? true
      : e.preventDefault();
  });

  $.each($(".hide-lesson-div"), (idx, val) => {
    $(val).click(() => {
      $(".lives").text(10);
      $(".quiz-cards").css("display", "none");
      $($(".lesson-div")[idx]).toggle(400);
    });
  });

  $.each($(".lesson-cards"), (idx, card) => {
    $(card).click(() => {
      $($(".quiz-range")[idx]).attr("max", $(".inner-lesson-div").length);
      $($(".lesson-div")[idx]).toggle(400);
      let lives = $(
        $(
          $($($(".lesson-div")[idx]).children(".inner-quiz-div")).children(
            ".quiz-header"
          )
        ).children(".lives-div")
      ).children(".lives");

      const quizCards = $(
        $($(".quiz-div")[idx]).children(".inner-quiz-div")
      ).children(".quiz-cards");
      $.each(quizCards, (idx3, qCard) => {
        $(quizCards[0]).css("display", "block");

        const quizCorrectAnswer = $($(qCard).children(".answers"))
          .children(".correct-answer")
          .text();
        const quizAnswersDiv = $($(qCard).children(".answers"));
        const quizAnswers = $($(qCard).children(".answers")).children(
          ".answer"
        );

        //  Answers button - Check correct answer
        var randomAnswers = shuffleArray([
          $(quizAnswers[0]).text(),
          $(quizAnswers[1]).text(),
          $(quizAnswers[2]).text(),
        ]);

        $($(".quiz-range")).attr("value", 0);
        $.each(quizAnswersDiv, (idx2, div) => {
          var cards = 1,
            nextQuiz = 1,
            preventMultiLoading = 10;
          $(".quiz-length").text(`${cards}/${$(quizCards).length}`);
          
          /**
           * Answers button
          */
         $.each($($(div).children(".answer")), (idxx, answer) => {
           $(answer).text(randomAnswers[idxx]);
            $(answer).click(() => {
              cards < $(quizCards).length && cards++;
              if ($(answer).text() === quizCorrectAnswer) {
                $($(".quiz-range")[idxx]).attr("value", nextQuiz);
                $(".quiz-length").text(`${cards}/${$(quizCards).length}`);
                $(".checked-div-alert").css("display", "grid");
                setTimeout(() => {
                  $(".checked-div-alert").css("display", "none");
                }, 1000);
                if (
                  $(quizCards).length > 1 &&
                  nextQuiz <= $(quizCards).length - 1
                ) {
                  $(quizCards).css("display", "none");
                  $($(quizCards)[nextQuiz]).css("display", "block");
                  nextQuiz++;
                }
              } else {
                $(".wrong-div-alert").css("display", "grid");
                setTimeout(() => {
                  $(".wrong-div-alert").css("display", "none");
                }, 1000);
                preventMultiLoading--;
                $(lives).text(preventMultiLoading);
                if (preventMultiLoading === 0) {
                  alert("You are out of lives💗!");
                  $(".quiz-cards").css("display", "none");
                  $($(".lesson-div")).css("display", "none");
                  $(".lives").text(10);
                  nextQuiz = 1;
                  preventMultiLoading = 0;
                }
              }
            });
          });
        });
        // End verification
      });
    });
  });

  $.each($(".fa-ellipsis-v"), (idx, val) => {
    $(val).click(() => {
      $($(".lesson-options")[idx]).toggle(400);
    });
  });
  $.each($(".lesson-options"), (idx, val) => {
    $($(val).children(".edit-lesson-link")).click(() => {
      $($(".edit-lesson-main")[idx]).toggle(500);
    });
  });
  $.each($(".close-edit-modal"), (idx, val) => {
    $(val).click(() => {
      $($(".edit-lesson-main")[idx]).toggle(500);
    });
  });
});
