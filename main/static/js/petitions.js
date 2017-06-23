function petitions() {
  $('#petitions-loading').fadeIn();
jQuery.ajax({
    url: 'https://petition.parliament.uk/petitions.json?state=open',
    type:"GET",
    dataType: "json",
    success: function(data) {
      data = data.data
      if (!data.length>0) {
        $none = $('<p>')
        $none.text('There are no open petitions right now.')
        $('#petitions-content').append($none);
      }
      else {
      for (i=0; i < data.length ; i++) {
        $petition = $("<div>", {"class": "petition"});
        url = data[i].links.self.replace('.json', '');
        $a = $("<a>", {"href": url});
        title = data[i].attributes.action;
        $title = $("<h3>").text(title);
        $title.appendTo($a);
        $a.appendTo($petition);
        $background = $("<p>");
        $background.text(data[i].attributes.background);
        $background.appendTo($petition);
        $signatures = $("<p>");
        $signatures.text('Signatures: ' + data[i].attributes.signature_count);
        $signatures.appendTo($petition);
        $date = $("<p>");
        $date.text(data[i].attributes.created_at);
        $date.appendTo($petition);
        $petition.appendTo('#petitions-content');
      }
    }
    }
});
$('#petitions-loading').fadeOut();
}

$(document).ready(function () {
  $('#petitions-arrow').click(function() {
    petitions();
  });
});
