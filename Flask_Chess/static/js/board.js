//"use strict";

function drag( ev ) {
    loadXMLDoc( ev.target.parentNode.id )

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
    let image = ev.dataTransfer.getData( "text" );
    let element = ev.target;
    let bcolor = document.getElementById( ev.target.id )
        .style.backgroundColor

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


function loadXMLDoc( pos ) {
    var req = new XMLHttpRequest( )
    req.onreadystatechange = function ( ) {
        if ( req.readyState == 4 ) {
            if ( req.status != 200 ) {
                //error handling code here
            } else {
                var response = JSON.parse( req.responseText )
                document.getElementById( 'myDiv' )
                    .innerHTML = response.position
            }
        }
    }

    req.open( 'POST', '/ajax' )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var postVars = 'position=' + pos
    req.send( postVars )

    return false
}


/*
function loadXMLDoc( pos ) {
    var req = new XMLHttpRequest( )
    req.onreadystatechange = function ( ) {
        if ( req.readyState == 4 ) {
            if ( req.status != 200 ) {
                //error handling code here
            } else {
                var response = JSON.parse( req.responseText )
                document.getElementById( 'myDiv' )
                    .innerHTML = response.username
            }
        }
    }

    req.open( 'POST', '/ajax' )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var postVars = 'uname=' + pos
    req.send( postVars )

    return false
}
*/
