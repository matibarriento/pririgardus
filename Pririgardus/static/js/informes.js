var cantInformes = 2;
var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='cerrar'><button>X</button></span></li>";
var tabs;
$(function() {
    tabs = $( "#divInformes" ).tabs();

    $( "#agregarInforme" ).button().click(function() {
        nuevoInforme();
    });
    // close icon: removing the tab on click
    tabs.delegate( "span.cerrar", "click", function() {
        var panelId = $( this ).closest( "li" ).remove().attr( "aria-controls" );
        $( "#" + panelId ).remove();
        tabs.tabs( "refresh" );
    });

});
function nuevoInforme() {
    var label = "Tab " + cantInformes,
    id = "informe-" + cantInformes,
    li = $( tabTemplate.replace( /#\{href\}/g, "#" + id ).replace( /#\{label\}/g, label ) ),
    tabContentHtml = "Tab " + cantInformes + " content.";
    tabs.find( ".ui-tabs-nav" ).append( li );
    tabs.append( "<div id='" + id + "'><p>" + tabContentHtml + "</p></div>" );
    tabs.tabs( "refresh" );
    cantInformes++;
}