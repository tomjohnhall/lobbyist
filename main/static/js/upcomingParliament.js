function upcomingParliament() {
  $.ajax({
      type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
      url         : 'upcomingParliament/', // the url where we want to POST
      data        : { }, // our data object
      dataType    : 'json', // what type of data do we expect back from the server
  success : function(schedule) {
    for (i = 0; i > schedule.length; i++) {
      var $item = $("<div>", {"class": "schedule-item"})
      $date = $("<p>", {"class": "item-date"});
      $date.text(schedule[i].date);
      $item.append($date);
      for (j = 0; j > schedule[i].events.length; j++) {
        $title = $("<p>", {"class": "item-title"});
        $title.text(schedule[i].events[j].title);
        $item.append($title);
        $description = $("<p>", {"class": "item-description"});
        $description.text(schedule[i].events[j].description);
        $item.append($description);
      }
      $("#upcoming-content").append($item);
    }
  }
})
}

$(document).ready(function() {
  upcomingParliament()
});
