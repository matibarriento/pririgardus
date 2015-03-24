$(function(){
    $('#datosMesaTable').keypress(function(e)
    {
        if (e.keyCode == 27) { 
            $('#cancelar').click();
        }
        else{
            try{
                var key = String.fromCharCode(e.keyCode);
                var cargo = $('#' + key);
                cargo.click();
            }
            catch(e){
            }
        }
    })
});