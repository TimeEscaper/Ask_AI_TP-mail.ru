$(document).ready(function() {
    
    $(".like-answer-button").on('click', function(){
        var $par = $(this).parents('.likes-dislikes');
        var $input = $par.find('.answer_id');
        var $answer_id = $input.val();
        
        $.ajax({
            url: '/like_answer/',
            type: 'POST',
            data: { answer_id: $answer_id },
        }).success(function(data){
            
            });
        
    });
    
    $(".dislike-answer-button").on('click', function(){
        alert('Hi!');
    });
    
});
