//common js functions

function getHTMLBlock(selector, url){
	$(selector).html('<div style="text-align: center; width: 100%; padding-top: 10px;">'+
					 '<img src="'+STATIC_URL+'img/ajax-loader.gif"/>'+
					 '</div>');
	$.ajax({
	    url: url,
	    context: $(selector),
	    success: function(data){
	        $(this).html(data);
	    },
	    error: function(){
	  	    $(this).html('Error');
	    }
	});
}