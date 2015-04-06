var mesas;
$(function() {
    $(".active").removeClass("active");
    $("#mesaLink").addClass("active");
    $("#numero_mesa").focus();
    $("#numero_mesa").val('');
    $("#numero_mesa").autoNumeric('init', {
        aSep: '', aDec: ',', vMin: '0', mDec: '0'});
    $("#numero_mesa").autocomplete({
        source: function (request, response) {
            getNumerosMesa(request, response);
        },
        minLength:2,
        change: function (event, ui) {
            if (ui.item) {
                $("#numero_mesa").val(ui.item.label);
                getDatosMesa(ui.item.value, false)
                return false;
            }
            else {
                $("#numero_mesa").val('');
                $('#datosMesa').empty();
            }
            $(this).trigger("change");
        },
        select: function (event, ui) {
            if (ui.item) {
                $("#numero_mesa").val(ui.item.label);
                getDatosMesa(ui.item.value, true)
                $(this).trigger("change");
                //$(this).blur();
                return false;
            }
            else {
                    $("#numero_mesa").val('');
                    $('#datosMesa').empty();
            }
        },
        focus: function (event, ui) {
            if (ui.item) {
                $("#numero_mesa").val(ui.item.label);
                getDatosMesa(ui.item.value)
                return false;
            }
            else {
                    $("#numero_mesa").val('');
                    $('#datosMesa').empty();
            }

        },
    });
});
function getDatosMesa(numero_mesa, focus) {
    $('#datosMesa').load('getDatosMesa/' + numero_mesa);
    if(focus){
        $('#datosMesa').focus();
    }
}

function getNumerosMesa(request, response){
    $.getJSON(urlMesas, function (data) {
        response($.map(data, function (value, key) {
            if( value.startsWith(request.term)){
                return {
                    label: value,
                    value: key
                };
            }
            else{
                return null;
            }
        }));
    });
}