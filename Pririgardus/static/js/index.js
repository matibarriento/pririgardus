var mesas;
$(function() {
    $("#numero_mesa").val('')
    $("#numero_mesa").autocomplete({
        source: function (request, response) {
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
        },
        minLength:2,
        change: function (event, ui) {
            if (ui.item) {
                $("#numero_mesa").val(ui.item.label);
                getDatosMesa(ui.item.value)
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
                getDatosMesa(ui.item.value)
                $(this).trigger("change");
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
function getDatosMesa(numero_mesa) {
    $('#datosMesa').load('getDatosMesa/' + numero_mesa);
}