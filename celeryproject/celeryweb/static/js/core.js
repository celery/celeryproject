//common js functions

function getStackOverflowQuestions(selector){
	$(selector).html('<div style="text-align: center; width: 100%; padding-top: 10px;">'+
					 '<img src="'+STATIC_URL+'img/ajax-loader.gif"/>'+
					 '</div>');
	$.ajax({
	    url: '/ajax/stackoverflowquestions/10/1/',
	    context: $(selector),
	    success: function(data){
	        $(this).html(data);
	    },
	    error: function(){
	  	    $(this).html('Error');
	    }
	});
}