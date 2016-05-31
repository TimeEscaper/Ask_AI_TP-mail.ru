$(document).ready(function() {
    
    $(".like-answer-button").on('click', function(){
        var $par = $(this).parents('.likes-dislikes');
        var $input = $par.find('.answer_id');
        var $answer_id = $input.val();
        $.ajax({
            url: '/like_answer/',
            type: 'POST',
            data: { answer_id: $answer_id, value: '1', csrfmiddlewaretoken: $.cookie('csrftoken')},
        }).success(function(data){
            var count_field = $par.find(".like-count");
            count_field.html(data);
            $(this).toggleClass(function() { return "like-answer-liked" });
        }).error(function(){
            alert('Ajax error!');
            });
    });
    
    $(".dislike-answer-button").on('click', function(){
        var $par = $(this).parents('.likes-dislikes');
        var $input = $par.find('.answer_id');
        var $answer_id = $input.val();
        $.ajax({
            url: '/like_answer/',
            type: 'POST',
            data: { answer_id: $answer_id, value: '0', csrfmiddlewaretoken: $.cookie('csrftoken')},
        }).success(function(data){
            var count_field = $par.find(".dislike-count");
            count_field.html(data);
            $(this).toggleClass(function() { return "dislike-answer-disliked" });
        }).error(function(){
            alert('Ajax error!');
            });
    });
    
});
