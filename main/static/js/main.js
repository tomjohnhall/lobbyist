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

  if($('.future').length == 0) {
    $('.date:nth-of-type(-n+3)').addClass('importance');
    $('#recent-events').hide();
  }

  $('#mp-title').click(function () {
    expander($('#mp-arrow'),$('#mp-content'));
  });

  $('#upcoming-title').click(function () {
    expander($('#upcoming-arrow'),$('#upcoming-content'));
  });

  $('#consultations-title').click(function () {
    expander($('#consultations-arrow'),$('#consultations-content'));
  });

  $('#petitions-title').click(function () {
    expander($('#petitions-arrow'),$('#petitions-content'));
  });

  function sticky_relocate(anchor,sticky) {
    var window_top = $(window).scrollTop();
    var div_top = anchor.offset().top;
    if (window_top > div_top) {
        $('h2').removeClass('stick');
        sticky.addClass('stick');
        anchor.height(sticky.outerHeight());
    } else {
        sticky.removeClass('stick');
        anchor.height(0);
    }
}

$(window).scroll(function () {
  sticky_relocate($('#mp-anchor'),$('#mp-title'));
  sticky_relocate($('#upcoming-anchor'),$('#upcoming-title'));
  sticky_relocate($('#consultations-anchor'),$('#consultations-title'));
  sticky_relocate($('#petitions-anchor'),$('#petitions-title'));
    });

$('#recent-events').click( function() {
  $('.past').slideDown();
  $(this).fadeOut();
});

$('#more-events').click( function() {
  $('.date:nth-child(n+5)').slideDown();
  $(this).fadeOut();
});

});
