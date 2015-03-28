$(function(){
    $('#datosMesaTable').keypress(function(e)
    {
        console.log(e.keyCode);
        if (e.keyCode == 27) { 
            $('#salir').click();
        }
        else{
            try{
                var key = String.fromCharCode(e.keyCode);
                var cargo = $('#' + key);
                console.log(cargo);
                cargo.click();
            }
            catch(ex){
                console.log(ex);
            }
        }
    });
});