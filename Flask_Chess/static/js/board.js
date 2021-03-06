//"use strict";

var socket = io( );
var room;
var old_pos;
var new_pos;
var turn = 0;

var player_white = $( "#white" )
    .text( );
var player_black = $( "#black" )
    .text( );

function drag( ev ) {
    //alert( player_black );
    //alert( player_white );
    let turn_color = $( "#" + ev.target.id )
        .attr( "name" )[ 0 ];
    old_pos = ev.target.parentNode.id
    ev.dataTransfer.setData( "img", ev.target.id );
    let bcolor = window.getComputedStyle( document.getElementById( ev.target.parentNode.id ) )
        .backgroundColor.toString( );
    /*
    if ( bcolor == "rgb(181, 221, 95)" ) {
        ev.target.parentNode.style.backgroundColor = "rgb(181, 145, 95)";
    } else if ( bcolor == "rgb(68, 121, 3)" ) {
        ev.target.parentNode.style.backgroundColor = "rgb(68, 26, 3)";
    }
    */
}

function allowDrop( ev ) {
    ev.preventDefault( );
}

function drop( ev ) {
    ev.preventDefault( );
    //if ( turn ) {
    let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
        .backgroundColor
        .toString( );
    let image = ev.dataTransfer.getData( "img" );
    let element = ev.target;
    var al = false;
    new_pos = ev.target.id
    if ( new_pos.includes( "image" ) ) {
        new_pos = ev.target.parentNode.id
    }
    $.ajax( {
            url: "/ajax",
            method: "POST",
            data: {
                "old_pos": old_pos,
                "new_pos": new_pos,
                "room_id": room_id,
                "restart": "False"
            },
            async: true
        } )
        .done( function ( data ) {
            al = data.allowed
            let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
                .backgroundColor
                .toString( );
            /*
            if ( bcolor == "rgb(181, 221, 95)" ) {
                ev.target.style.backgroundColor = "rgb(181, 145, 95)";
            } else {
                ev.target.style.backgroundColor = "rgb(68, 26, 3)";
            }
            */
            if ( !al ) {
                $( "#myDiv" )
                    .html( data.turn )
                return true;
            }
            $( "#myDiv" )
                .html( data.old_position + " -> " + data.new_position );
            if ( data.redirect != "" ) {
                socket.emit( "game_end", {
                    "room": room_id,
                    "url": data.redirect
                } );
            }
            socket.emit( "move", { "start_id": old_pos, "end_id": new_pos, "room": room_id, "turn": turn } );
            //move_piece( { "start_id": old_pos, "end_id": new_pos } );
            /*
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
            */
        } );
    //}
}

function move_piece( data ) {
    let from = $( "#" + data.start_id )
        .html( );
    console.log( "from" + from );
    let to = $( "#" + data.end_id )
        .html( );
    console.log( "to: " + to );
    if ( to ) {
        $( "#" + data.end_id )
            .html( from );
        $( "#" + data.start_id )
            .html( "" );
    } else {
        $( "#" + data.end_id )
            .html( from );

        $( "#" + data.start_id )
            .html( to );
    }
    if ( turn % 2 ) {
        turn = 1;
    } else {
        turn = 0;
    }
}

function dragEnter( ev ) {
    if ( ev.target.className == "box" ) {
        let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
            .backgroundColor.toString( );
        /*
        if ( bcolor == "rgb(181, 145, 95)" ) {
            ev.target.style.backgroundColor = "rgb(181, 221, 95)";
        } else {
            ev.target.style.backgroundColor = "rgb(68, 121, 3)";
        }
        */
    }
}

function dragLeave( ev ) {
    if ( ev.target.className == "box" ) {
        let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
            .backgroundColor
            .toString( );
        /*
        if ( bcolor == "rgb(181, 221, 95)" ) {
            ev.target.style.backgroundColor = "rgb(181, 145, 95)";
        } else {
            ev.target.style.backgroundColor = "rgb(68, 26, 3)";
        }
        */
    }
}

/*++++++++++++++++++++++++++++++++++++*/

function Restart( old_pos, new_pos ) {
    var req = new XMLHttpRequest( )
    req.onreadystatechange = function ( ) {
        if ( req.readyState == 4 && req.status == 200 ) {
            var response = JSON.parse( req.responseText )
            console.log( response.restart )
        }
    }
    req.open( 'POST', '/ajax', false )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var variables = 'old_pos=' + "&new_pos=" + "&restart=True"
    req.send( variables )

    return false;
}


/*
function Restart( old_pos, new_pos ) {
    var req = new XMLHttpRequest( )
    req.onreadystatechange = function ( ) {
        if ( req.readyState == 4 && req.status == 200 ) {
            var response = JSON.parse( req.responseText )
            console.log( response.restart )
        }
    }
    req.open( 'POST', '/ajax', false )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var variables = 'old_pos=' + "&new_pos=" + "&restart=True"
    req.send( variables )
    return false;
}
*/


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
    req.open( 'POST', '/ajax', true )
    req.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" )
    var coords = 'old_pos=' + old_pos + "&new_pos=" + new_pos + "&restart=False"
    req.send( coords )
    return false;
}
*/

/*
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
*/


/*
function drop( ev ) {
    let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
        .backgroundColor
        .toString( );
    let image = ev.dataTransfer.getData( "text" );
    let element = ev.target;
    var al = false;
    ev.preventDefault( );
    new_pos = ev.target.id
    if ( new_pos.includes( "image" ) ) {
        new_pos = ev.target.parentNode.id
    }
    $.ajax( {
            url: "/ajax",
            method: "POST",
            data: {
                "old_pos": old_pos,
                "new_pos": new_pos,
                "restart": "False"
            },
            async: false
        } )
        .done( function ( data ) {
            al = data.allowed
            $( "#myDiv" )
                .html( data.old_position + " -> " + data.new_position )
            let bcolor = window.getComputedStyle( document.getElementById( ev.target.id ) )
                .backgroundColor
                .toString( );
            if ( bcolor == "rgb(181, 221, 95)" ) {
                ev.target.style.backgroundColor = "rgb(181, 145, 95)";
            } else {
                ev.target.style.backgroundColor = "rgb(68, 26, 3)";
            }
            if ( !al ) {
                $( "#myDiv" )
                    .html( "WRONG MOVE!!!" )
                return true
            }
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
        } );
}
*/

socket.on( "connect", ( ) => {
    console.log( "just connected the index page" );
    turn = parseInt( $( "#turn_id" )
        .html( ) );
    room_id = $( "#room_id" )
        .text( );
    socket.emit( "join", {
        "room": room_id
    } );
} );

socket.on( "message", function ( msg ) {
    console.log( msg );
} );

socket.on( "move", function ( data ) {
    move_piece( data );
} );

socket.on( "guests_names", function ( data ) {
    $( "#white" )
        .html( data.white );
    $( "#black" )
        .html( data.black );
} );

socket.on( "game_end", function ( data ) {
    alert( "Game ended" );
    window.location.replace( data.url );
} );
/*
window.onbeforeunload = function ( ) {
        socket.emit( 'refreshing', { "rooom_id": room_id } );
    } 
*/
