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

    $('#escrutar').on("focus", function(){
        $(this).addClass("escrutar-focus")
    });

    $('#escrutar').on("blur", function(){
       $(this).removeClass("escrutar-focus") 
    });
    
    $("#cargarPlanilla").keypress(function(e) {
        if (e.keyCode == 27) { 
            $('#cancelar').click();
        }
    });
    $(".voto").keypress(function(e) {
        //var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
        if(e.keyCode == 13) {
            e.preventDefault();
            console.log(e.keyCode);
            var inputs = $(this).closest('form').find(':input:visible');
            inputs.eq( inputs.index(this)+ 1 ).focus();
            return false;
        }
    });

    $(".voto").on("focus", function(){;
        $(this).select();
    });

    $(".voto").first().focus();

});