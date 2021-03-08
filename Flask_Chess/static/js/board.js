//"use strict";

function drag( ev ) {
    try {
        if ( ev === undefined ) {
            throw "ev is undefined in drag_function";
        }
        ev.dataTransfer.setData( "text", ev.target.id );
    } catch ( err ) {
        alert( "drag_function:" + err.name + err.message );
    }
}

function allowDrop( ev ) {
    try {
        if ( ev === undefined ) {
            throw "ev is undefined in allowDrop_function";
        }
        ev.preventDefault( );
    } catch ( err ) {
        alert( "allowDrop_function:" + err.name + err.message );
    }
}

function drop( ev ) {
    var image = ev.dataTransfer.getData( "text" );
    var element = ev.target;
    ev.preventDefault( );
    if ( element.id.search( "grid" ) >= 0 ) {
        element.appendChild( document.getElementById( image ) );
    } else if ( document.getElementById( image )
        .name[ 0 ] != element.name[ 0 ] ) {
        if ( !element.classList.contains( 'box' ) ) {
            element = ev.target.parentNode;
            ev.target.remove( );
        }
        element.appendChild( document.getElementById( image ) );
    }

}
