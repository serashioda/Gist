$(document).ready(function(){
    var deleters = $(".delete");
    deleters.on("click", function(){
        // send ajax request to delete this expense
        $.ajax({
            url: 'delete/' + $(this).attr("data"),
            data: {
                "name": "some name",
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
