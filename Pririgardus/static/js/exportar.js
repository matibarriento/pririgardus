$(function() {

    Anidado($("#tipoCargo"), ("#cargo"))
    Anidado($("#cargo"), ("#alcanceCargo"))

    $("#tipoCargo").on("change", function()
    {
        Anidado($("#tipoCargo"), ("#cargo"))
    });

    $("#cargo").on("change", function()
    {
        Anidado($("#cargo"), ("#alcanceCargo"))
    });

    $("#cargo").autocomplete({
        source: []
    });
});

function Anidado(controlPadre, controlHijo){
    if($(controlPadre).val() == 0){
        $(controlHijo).prop("disabled", true);
        $(controlHijo).val("0");
        $(controlHijo).trigger("change");
    }
    else{
        $(controlHijo).prop("disabled", false);
    }
}