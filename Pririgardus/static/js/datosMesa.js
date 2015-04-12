$(function(){
    $('#datosMesa').on("keypress", function(e)
    {
        console.log(e.keyCode);
        var key = String.fromCharCode(e.keyCode);
        if (e.keyCode == 42 || e.keyCode == 45) { 
            $('#salir').click();
            //parent.location='/mesas';
        }
        else{
            try{
                var cargo = $('#' + key);
                cargo.click();
            }
            catch(ex){
                // console.log(ex);
            }
        }
    });
});