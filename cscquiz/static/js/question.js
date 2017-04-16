$('#submit-answer-btn').on('click', function(event){
    event.preventDefault();
    create_post();
});

function create_post(){
	var options = document.querySelectorAll('fieldset input');
	var choice = 0;
	[].forEach.call(options, function(option) {
		if (option.checked){
			choice = option.value
		}
	})

    $.ajax({
        url : urlSubmit, // the endpoint
        type : "POST", // http method
        data : { id:qnid ,choice:choice, csrfmiddlewaretoken:_token }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            if ('correct' == json.result){
            	document.querySelectorAll('input')[choice-1].parentElement.parentElement.parentElement.className+= " bg-success text-white"
                $('#scoring-modal').modal('show')
            } else {
            	document.querySelectorAll('input')[choice-1].parentElement.parentElement.parentElement.className+= " bg-danger text-white"
            }
            //console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}



$('#scoring-btn').on('click', function(event){
    event.preventDefault();
    //console.log("score btn clicked");
    score_post();
});

function score_post(){
    var options = document.querySelectorAll('#scoring-modal input');
    var choice = 0;
    [].forEach.call(options, function(option) {
        if (option.checked){
            choice = option.value
        }
    })
    //console.log(choice)

    $.ajax({
        url : urlScore, // the endpoint
        type : "POST", // http method
        data : { id:qnid ,choice:choice, csrfmiddlewaretoken:_token }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //console.log("success"); // another sanity check
            window.location.href = '/';
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
