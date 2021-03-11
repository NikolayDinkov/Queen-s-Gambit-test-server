//"use strict";

var old_pos;
var new_pos;

function drag( ev ) {
    old_pos = ev.target.parentNode.id
    ev.dataTransfer.setData( "text", ev.target.id );
    let bcolor = window.getComputedStyle( document.getElementById( ev.target.parentNode.id ) )
        .backgroundColor.toString( );
    if ( bcolor == "rgb(181, 221, 95)" ) {
        ev.target.parentNode.style.backgroundColor = "rgb(181, 145, 95)";
    } else if ( bcolor == "rgb(68, 121, 3)" ) {
        ev.target.parentNode.style.backgroundColor = "rgb(68, 26, 3)";
    }
}

function allowDrop( ev ) {
    ev.preventDefault( );
}

function drop( ev ) {
    new_pos = ev.target.id
    if ( new_pos.includes( "image" ) ) {
        new_pos = ev.target.parentNode.id
    }
    SendPos( old_pos, new_pos )

    let image = ev.dataTransfer.getData( "text" );
    let element = ev.target;
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

function dragEnter( ev ) {
    if ( ev.target.className == "box" ) {
        let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
            .backgroundColor.toString( );
        if ( bcolor == "rgb(181, 145, 95)" ) {
            ev.target.style.backgroundColor = "rgb(181, 221, 95)";
        } else {
            ev.target.style.backgroundColor = "rgb(68, 121, 3)";
        }
    }
}

function dragLeave( ev ) {
    if ( ev.target.className == "box" ) {
        let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
            .backgroundColor
            .toString( );
        if ( bcolor == "rgb(181, 221, 95)" ) {
            ev.target.style.backgroundColor = "rgb(181, 145, 95)";
        } else {
            ev.target.style.backgroundColor = "rgb(68, 26, 3)";
        }
    }
}

/*++++++++++++++++++++++++++++++++++++*/

function GetMyData( data ) {
    alert( "data = ", data )
    return data;
}

function Restart( old_pos, new_pos ) {
    var req = new XMLHttpRequest( )
    req.onreadystatechange = function ( ) {
        if ( req.readyState == 4 && req.status == 200 ) {
            var response = JSON.parse( req.responseText )
            console.log( response.restart )
        }
    }
    req.open( 'POST', '/ajax' )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var variables = 'old_pos=' + "&new_pos=" + "&restart=True"
    req.send( variables )

    return false;
}


function SendPos( old_pos, new_pos ) {
    var req = new XMLHttpRequest( )
    req.onreadystatechange = function ( ) {
        if ( req.readyState == 4 && req.status == 200 ) {
            var response = JSON.parse( req.responseText )
            document.getElementById( 'myDiv' )
                .innerHTML = response.old_position + " -> " + response.new_position

        }
    }
    req.open( 'POST', '/ajax' )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var coords = 'old_pos=' + old_pos + "&new_pos=" + new_pos + "&restart=False"
    req.send( coords )

    return false;
}

/*
function SendPos( old_pos, new_pos ) {
    var req = new XMLHttpRequest( )
    req.onreadystatechange = function ( ) {
        if ( req.readyState == 4 && req.status == 200 ) {
            var response = JSON.parse( req.responseText )
            document.getElementById( 'myDiv' )
                .innerHTML = response.old_position + " -> " + response.new_position
        }
    }
    req.open( 'POST', '/ajax' )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var coords = 'old_pos=' + old_pos + "&new_pos=" + new_pos
    req.send( coords )

    return false;
}
*/
