function getMP(postcode) {
  $.ajax({
      type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
      url         : 'postcode/', // the url where we want to POST
      data        : { postcode }, // our data object
      dataType    : 'json', // what type of data do we expect back from the server
  success : function(mp) {
    if (mp.error) {
      error = mp.error + '. Please try again.';
      $('#postcode-error').fadeOut(400, function() {
        $('#postcode-error').text(error);
        $('#postcode-error').fadeIn(400);
      });
    }
    else {
    $('#postcode-error').fadeOut(400);
    $('#postcode-form').fadeOut(400, function() {

      $('#mp-image').attr('src', mp.details.image );
      $('#party-image').attr('src', mp.party.image );
      $('#party-text').text(mp.party.name);
      $('#mp-name').text(mp.details.full_name);
      $('#mp-constituency').text(mp.details.constituency);
      if (mp.details.office) {
        $('#mp-position').text(mp.details.office[0].position);
      }
      link = 'https://www.theyworkforyou.com' + mp.details.url;
      $('#twfy').attr('href', link);
      if (mp.contact.email) {
        email = mp.contact.email;
        $('#unconfirmed-email').hide();
      }
      else {
        email = mp.details.full_name.replace(' ','.') + '.mp@parliament.uk';
        $('#unconfirmed-email').show();
      }
      $('.mp-mailto').attr('href', 'mailto:' + email);
      $('#mp-email').text(email);
      if (mp.contact.twitter) {
        twitter = 'https://twitter.com/' + mp.contact.twitter;
      }
      else {
        twitter = 'https://twitter.com/search?f=users&q=' + mp.details.full_name;
      }
      $('#mp-twitter').attr('href', twitter);
      if (mp.contact.facebook) {
        facebook = 'https://www.facebook.com/' + mp.contact.facebook;
      }
      else {
        facebook = 'https://www.facebook.com/search/pages/?q=' + mp.details.full_name;
      }
      $('#mp-facebook').attr('href', facebook);
      $('#mp-result').fadeIn(400);
    });

  }
  }
});
}


$(document).ready(function() {
  try {
    if (postcode != false) {
    getMP(postcode);
    }
  }
  catch(err) {}
  // process the form
  $('form').submit(function(event) {

      // get the form data
      // there are many ways to get this data using jQuery (you can use the class or id also)
      postcode = $('input[name=postcode]').val();
      getMP(postcode);
      $('input[name=postcode]').val('');
      // stop the form from submitting the normal way and refreshing the page
      event.preventDefault();
    });

  $('#clear-mp').click(function() {
    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        url         : 'clearPostcode/', // the url where we want to POST
        data        : { }, // our data object
        dataType    : 'json', // what type of data do we expect back from the server
    success : function(clear) {
      $('#mp-result').fadeOut(400, function() {
        $('#unconfirmed-email').hide();
        $('#postcode-error').hide();
        $('#mp-name,#mp-consituency,#mp-position,#mp-email,#party-text').text('');
        $('#twfy,.mp-mailto,#mp-twitter,#mp-facebook').attr('href', '');
        $('#mp-image,#party-image').attr('src', '');
        $('#postcode-form').fadeIn(400);
      });
      }
    });
  });
});
