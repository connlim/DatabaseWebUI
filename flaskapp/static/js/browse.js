$(document).ready(function() 
    { 
        console.log("oink");
        $(".myTable").tablesorter(); 
        $(".myTable").each( function() {
            if ($(this).children().length == 0) {
                $(this).append("<tr><td>No items returned</td></tr>");
            }
        });
    } 
); 