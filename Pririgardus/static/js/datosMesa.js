$(function(){
    $('#datosMesa').keypress(function(e)
    {
        try{
            var key = String.fromCharCode(e.keyCode);
            var cargo = $('#' + key);
            cargo.click();
        }catch(e){
        }
    })
});