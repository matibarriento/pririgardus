$(function() {
    var alcanceCargos = [];
    $("#alcanceCargo").autocomplete({
        source: alcanceCargos,
        minChars:0,
        change: function (event, ui) {
            if (ui.item) {
                event.preventDefault();
                $("#alcanceCargo").val(ui.item.label);
                $("#cargoID")[0].value = ui.item.value;
            }
            else {
                $("#alcanceCargo").val('');
                $("#cargoID")[0].value = '-1';
            }
            $(this).trigger("change");
        },
        select: function (event, ui) {
            if (ui.item) {
                event.preventDefault();
                $("#alcanceCargo").val(ui.item.label);
                $("#cargoID")[0].value = ui.item.value;
            }
            else {
                $("#alcanceCargo").val('');
                $("#cargoID")[0].value = '-1';
            }
            $(this).trigger("change");
        },
    });

    $('#exportar').click(function(e) {
            e.preventDefault();
            $.ajax({
                url: urlExportar + "/" + $("#cargoID").val(),
                type: 'POST',
                success: function(response) {
                    return false;
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });
    

    Anidado($("#tipoCargo"), ("#alcanceCargo"));

    $("#tipoCargo").on("change", function()
    {
        Anidado($("#tipoCargo"), ("#alcanceCargo"));
    });

});

function Anidado(controlPadre, controlHijo){
    if($(controlPadre).val() == '0'){
        $(controlHijo).prop("disabled", true);
        $(controlHijo).val("");
        $("#exportar").prop("disabled", true);
        $(controlHijo).trigger("change");
    }
    else{
        $(controlHijo).prop("disabled", false);
        $("#exportar").prop("disabled", false);
        getAlcanceCargos($("#tipoCargo").val());
        // $("#alcanceCargo").autocomplete({
        //         source: alcanceCargos.responseJSON,
        //         minLength:0,
        //     });
        // console.log(getAlcanceCargos($("#tipoCargo").val()));
    }
}

function getAlcanceCargos(tipo_cargo_id){
    $.getJSON(urlAlcances + "/" + tipo_cargo_id, function (data) {
        alcanceCargos = $.map(data, function (value, key) {
            return {
                label: value,
                value: key
            };
        });
        $("#alcanceCargo").autocomplete("option", "source", alcanceCargos);
    });
}