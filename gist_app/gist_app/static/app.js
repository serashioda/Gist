$(document).ready(function(){
    var deleters = $(".delete");
    deleters.on("click", function(){
        // send ajax request to delete this expense
        $.ajax({
            url: 'delete/' + $(this).attr("data"),
            data: {
                "user_name": "some name",
                "f_name": "some name",
                "l_name": "some name",
                "email": "email",
                "favorite_food": "some food"
            }
            success: function(){
                console.log("deleted");
            }
        });        
        // fade out expense
        this_row = $(this.parentNode.parentNode);
        // delete the containing row
        this_row.animate({
            opacity: 0
        }, 500, function(){
            $(this).remove();
        })
    });
});
