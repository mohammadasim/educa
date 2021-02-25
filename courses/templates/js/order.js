/*
In the following code the main trick is done by the sortable function
that is part of jquery-ui. This function allows for items to be dragged
and dropped. However the remaining code is there to update the order field
of both the content and module in the database.
So once the sortable function is executed, we define the stop function that
is executed immediately after it. In this we get the index of each module or
content add 1 to it because index starts at 0.
And then a post request is made to update the database.
**/


$('#modules').sortable({
    stop:function(event, ui){
        let modules_order = {};
        $('#modules').children().each(function(){
            // update the order field
            $(this).find('.order').text($(this).index() + 1);
            // associate the module's id with its order
            modules_order[$(this).data('id')] = $(this).index();
        });
        $.ajax({
            type:'POST',
            url: '{% url "module_order" %}',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: JSON.stringify(modules_order)
        });
    }
});
$('#module-contents').sortable({
    stop:function(event, ui){
        let contents_order = {};
        $('#module-contents').children().each(function(){
            // associate the module's id with its order
            contents_order[$(this).data('id')] = $(this).index()
        });
        $.ajax({
            type:'POST',
            url: '{% url "content_order" %}',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(contents_order),
            dataType: 'json'
        });
    }
});