$(function() {
    $('#escrutar').click(function() {
        $.ajax({
            url: urlPlanilla,
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});