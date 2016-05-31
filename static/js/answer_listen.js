$(document).ready(function(){
    var answer_request = function() {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:7777/sub',
        }).done(function(answer_response){
            

            var new_answer =    
                           '<div class="row answer-box">'+
                '<a name="'+answer_response['answer_id']+'"></a>'
				+'<div class="col-md-2">'
						+'<h4><a href="#">'+answer_response['answer_author']+'</a></h4>'
						+'<img src="http://lorempixel.com/60/60" class="img-circle" />'
				+'</div>'
				+'<div class="col-md-10">'
					+'<div class="text">'
                    +    answer_response['answer_text']+
					+'</div>'
                    +'<div class="likes-dislikes">'
                        
                        +' <input class="answer_id" type="hidden" value="'+answer_response['answer_id']+'" />'
            
                            '<span class="like-answer-button">'+
                                    '<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span>&nbsp;'+
                                '<span class="like-count">0</span> &nbsp;&nbsp;</span>'+
                                
                           +'<span class="dislike-answer-button">'
                              +  '<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span>&nbsp;'
                             +   '<span class="dislike-count">0</span> </span>'
                             
            $('#answer-list').prepend(new_answer);
            setTimeout(answer_request, 3000);
        });
    }
    
    answer_request();
});
