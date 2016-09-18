function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    // Check if the XMLHttpRequest object has a "withCredentials" property.
    // "withCredentials" only exists on XMLHTTPRequest2 objects.
    xhr.open(method, url, true);
  } 
  else if (typeof XDomainRequest != "undefined") {
    // Otherwise, check if XDomainRequest.
    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
    xhr = new XDomainRequest();
    xhr.open(method, url);
  } 
  else {
    // Otherwise, CORS is not supported by the browser.
    xhr = null;
  }
  return xhr;
}

function getBody(text) {
  return text.match('<body>(.*)?</body>')[1];
}


var Gimmie = {
    $content: $('.content'),
    $form: $('form'),
	toggleLoading: function(){
        // Toggle loading indicator
        this.$content.toggleClass('content--loading');
         
        // Toggle the submit button so we don't get double submissions
        // http://stackoverflow.com/questions/4702000/toggle-input-disabled-attribute-using-jquery
        this.$form.find('button').prop('disabled', function(i, v) { return !v; });
    },
	userInput: '',
    userInputIsValid: false,
    appId: '',
    validate: function(input) {
        // Use regex to test if input is valid. It's valid if:
        // 1. It begins with 'http://itunes'
        // 2. It has '/id' followed by digits in the string somewhere
        var regUrl = /^(http|https):\/\/itunes/;
        var regId = /\/id(\d+)/i;
        if ( regUrl.test(this.userInput) && regId.test(this.userInput) ) {
            this.userInputIsValid = true;
            var id = regId.exec(this.userInput);
            this.appId = id[1];
        } else {
            this.userInputIsValid = false;
            this.appId = '';
        }
    },
	throwError: function(header, text){
        // Remove animation class
        this.$content.removeClass('content--error-pop');
 
        // Trigger reflow
        // https://css-tricks.com/restart-css-animation/
        this.$content[0].offsetWidth = this.$content[0].offsetWidth;
 
        // Add classes and content
        this.$content
            .html('<p><strong>' + header + '</strong> ' + text + '</p>')
            .addClass('content--error content--error-pop');
 
        this.toggleLoading();
    },
	render: function(response){
        var icon = new Image();
        icon.src = response.artworkUrl512;
        icon.onload = function() {
            Gimmie.$content
                .html(this)
                .append('<p><strong>' + response.trackName + '</strong></p>')
                .removeClass('content--error');
            Gimmie.toggleLoading();
        }
    }
};
 
$(document).ready(function(){
    Gimmie.$form.on('submit', function(e){
        e.preventDefault();
        //Gimmie.toggleLoading(); // call the loading function
		Gimmie.userInput = $(this).find('input').val();
		
		/*
		var xhr = createCORSRequest('GET', "http://127.0.0.1:5000/");
		if (!xhr) {
		  throw new Error('CORS not supported');
		}
		console.log(xhr);
		xhr.onload = function() {
			var responseText = xhr.responseText;
			console.log(responseText);
			// process the response.
		};
		xhr.onerror = function() {
			console.log('There was an error!');
		};
		*/
		/*
		$.ajax({
			type: "GET",
			url: "http://127.0.0.1:5000/",
			data: $('form').serialize(),
			dataType: "html"
		})
		.done(function(response) {
			// Get the first response and log it
			var response = response.results[0];
			console.log(response);
		 
			// Check to see if request is valid & contains the info we want
			// If it does, render it. Otherwise throw an error
			if(response && response.artworkUrl512 != null){
				Gimmie.render(response);
			} else {
				Gimmie.throwError(
					'Invalid Response',
					'The request you made appears to not have an associated icon. <br> Try a different URL.'
				);
			}
		})
		.fail(function(data) {
			Gimmie.throwError(
				'iTunes API Error',
				'There was an error retrieving the info. Check the iTunes URL or try again later.'
			);
		});
		*/
		$.getJSON("http://127.0.0.1:5000" + '/_add_numbers', {
			a: $('input[name="a"]').val(),
			b: $('input[name="b"]').val()
		}, function(data) {
			$("#result").text(data.result);
			console.log($("#result").text(data.result))
		});
		return false;
    });	
});

$(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON("http://127.0.0.1:5000" + '/_add_numbers', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $("#year").text(data.year);
		$("#desc").text(data.desc);
		$("#wiki").text(data.wiki);
      });
      return false;
    });
  });