function expander(arrow,content) {
  if (arrow.hasClass('glyphicon-chevron-down')) {
  content.slideDown();
  arrow.removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
}
  else {
  content.slideUp();
  arrow.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
  }
}

$(document).ready(function() {
  $('#title-arrow').click(function() {
    expander($(this),$('#about-content'));
  });

  $('#mp-arrow').click(function () {
    expander($(this),$('#mp-content'));
  });

  $('#upcoming-arrow').click(function () {
    expander($(this),$('#upcoming-content'));
  });

  $('#consultations-arrow').click(function () {
    expander($(this),$('#consultations-content'));
  });

  $('#petitions-arrow').click(function () {
    expander($(this),$('#petitions-content'));
  });
});
