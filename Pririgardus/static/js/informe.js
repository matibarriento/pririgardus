$(function() {
    $(".active").removeClass("active");
    $("#informesLink").addClass("active");
    crearAutocompletado($("#alcanceCargo"), $("#cargoID"), false);
    crearAutocompletado(("#frentes"), $("#frenteID"), true);
    crearAutocompletado(("#seccionales"), $("#seccionalNum"), true);

    $('#informe').click(function(e) {
            $("#graficoInforme").load(
                urlInforme +"/" + $("#tipoCargo").val() + "/" + $("#cargoID").val()+ "/"+ $("#seccionalNum").val() +"/" + $("#frenteID").val() + "/" + $("#tipoGrafico").val());
            e.preventDefault();
        });
    

    Anidado($("#tipoCargo"), $("#alcanceCargo"), $("#cargoID"), $("#informe"));
    Anidado($("#cargoID"), $("#frentes"), $("#frenteID"), $("#informe"));
    Anidado($("#cargoID"), $("#seccionales"), $("#seccionalNum"), $("#informe"));
    
    $("#tipoCargo").on("change", function()
    {
        //$("#alcanceCargo").autocomplete("option", "source", []);
        clearHijo(("#alcanceCargo"), $("#cargoID"), $("#informe"));
        var tieneValor = Anidado($("#tipoCargo"), $("#alcanceCargo"), $("#cargoID"), $("#informe"));
        if(tieneValor){
            getAlcanceCargos($("#tipoCargo").val());
        }
    });

    $("#alcanceCargo").on("change", function()
    {
        clearHijo($("#frentes"), $("#frenteID"), $("#informe"));
        var tieneValor = Anidado($("#cargoID"), $("#frentes"), $("#frenteID"), $("#informe"));
        if(tieneValor){
            getFrentes($("#cargoID").val());
        }

        clearHijo($("#seccionales"), $("#seccionalNum"), $("#informe"));
        var tieneValor = Anidado($("#cargoID"), $("#seccionales"), $("#seccionalNum"), $("#informe"));
        if(tieneValor){
            getSeccionales($("#cargoID").val());
        }
    });
    setInterval(function(){
        if(! $("#informe").prop("disabled")){
            $("#informe").click();
        }
    },60000); //milisegundos, 1 minuto


});

function Anidado(controlPadre, controlHijo, controlIDHijo, controlSubmit){
    var tieneValor = $.inArray($(controlPadre).val(), [0,'0', "0", '', "undefined"]) == -1;
    if(tieneValor){
        $(controlHijo).prop("disabled", false);
        $(controlSubmit).prop("disabled", false);
    }
    else{
        $(controlHijo).prop("disabled", true);
        $(controlHijo).val("");
        $(controlIDHijo)[0].value = '0';
        $(controlSubmit).prop("disabled", true);
    }
    $(controlHijo).trigger("change");
    return tieneValor;
}

function clearHijo(controlHijo, controlIDHijo, controlSubmit){
    $(controlHijo).prop("disabled", true);
        $(controlHijo).val("");
        $(controlIDHijo)[0].value = '0';
        $(controlSubmit).prop("disabled", true);
}

function getAlcanceCargos(tipo_cargo_id){
    $.getJSON(urlAlcances + "/" + tipo_cargo_id, function (data) {
        var alcanceCargos = $.map(data, function (value, key) {
            return {
                label: value,
                value: key
            };
        });
        $("#alcanceCargo").autocomplete("option", "source", alcanceCargos);
    });
}

function getSeccionales(cargo_id){
    $.getJSON(urlSeccionales + "/" + cargo_id, function (data) {
        var seccionales = $.map(data, function (value, key) {
            return {
                label: value,
                value: key
            };
        });
        $("#seccionales").autocomplete("option", "source", seccionales);
        valorDefault = findLabel(seccionales, 0);
        $("#seccionales").val(valorDefault);
        $("#seccionales").trigger("change");
    });
}

function getFrentes(cargo_id){
    $.getJSON(urlFrentes + "/" + cargo_id, function (data) {
        var frentes = $.map(data, function (value, key) {
            return {
                label: value,
                value: key
            };
        });
        $("#frentes").autocomplete("option", "source", frentes);
        valorDefault = findLabel(frentes, 0);
        $("#frentes").val(valorDefault);
        $("#frentes").trigger("change");
    });
}

function crearAutocompletado(controlPrincipal, controlID, tieneDefault){
    $(controlPrincipal).autocomplete({
        source: [],
        minChars:0,
        minLength:0,
        change: function (event, ui) {
            forAutocomplete($(controlPrincipal), $(controlID), event, ui, tieneDefault);
        },
        select: function (event, ui) {
            forAutocomplete($(controlPrincipal), $(controlID), event, ui, tieneDefault);
        },
        focus:function (event, ui) {
            forAutocomplete($(controlPrincipal), $(controlID), event, ui, tieneDefault);
        },
    }).on('focus', function(event) {
            $(this).autocomplete("search", "");
        });
}

function forAutocomplete(controlPrincipal, controlID, event, ui, tieneDefault){
    if (ui.item) {
        event.preventDefault();
        $(controlPrincipal).val(ui.item.label);
        $(controlID)[0].value = ui.item.value;
    }
    else {
        if(tieneDefault){
            valorDefault = findLabel($(controlPrincipal).autocomplete("option", "source"), 0);
            $(controlPrincipal).val(valorDefault);
        }
        else{
            $(controlPrincipal).val('');
            
        }
        $(controlID)[0].value = '0';
    }
    $(controlPrincipal).trigger("change");
}

function findLabel(lista, value) {
    var count = lista.length;
    for (var i = 0; i < count; i++) {
        if (lista[i].value == value) {
            return lista[i].label;
        }
    }
    return "";
}