$(function() {
    $(".active").removeClass("active");
    $("#mesaLink").addClass("active");

    if(escrutada){
        $("#escrutar").remove();
        $("#cancelar").val("Salir");

    }
    $("#datosMesa").dialog({
        autoOpen: false,
        modal: true,
        closeOnEscape: false,
        draggable: false,
        dialogClass: "",
        resizable: false,
        title: "Próxima acción"
       });

    $('#escrutar').click(function(e) {
        e.preventDefault();
        $.ajax({
            url: urlPlanilla,
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('#datosMesa').html(response);
                $("#datosMesa").dialog( "open" );
                return false;
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#escrutar').on("focus", function(){
        $(this).addClass("escrutar-focus");
    });

    $('#escrutar').on("blur", function(){
       $(this).removeClass("escrutar-focus");
    });

    // $('#escrutar').keypress(function(e){
    //     if(e.keyCode == 13) {
    //         $(this).click();
    //     }
    // });
    
    $("#cargarPlanilla").keypress(function(e) {
        if (e.keyCode == 27) { 
            $('#cancelar').click();
        }
    });

    $(".voto").keypress(function(e) {
        //var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
        if(e.keyCode == 13) {
            e.preventDefault();
            var inputs = $(this).closest('form').find(':input:visible');
            inputs.eq( inputs.index(this)+ 1 ).focus();
            return false;
        }
    });

    $(".voto").autoNumeric('init', {
        aSep: '', aDec: ',', vMin: '0', mDec: '0', wEmpty: 'zero'});

    $(".voto").on("focus", function(){
        $(".votosFrente").removeClass("panel-primary");
        if ( $(this).hasClass("voto-lista") ){
            $($(this).closest(".votosFrente")).addClass("panel-primary");
        }
        $(this).select();
    });

    $(".voto").first().focus();

});