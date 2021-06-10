var index = 0;
var turn = 0;
var old_pos;
var new_pos;

function previous( ) {
    let a = $( "#moves" )
        .text( );

    if ( a[ index - 4 ] >= 0 ) {
        index -= 4;
        console.log( "index = ", index );
        new_pos = "grid_box_" + a[ index ] + a[ index + 1 ];
        old_pos = "grid_box_" + a[ index + 2 ] + a[ index + 3 ];
        console.log( "old_pos = ", old_pos );
        console.log( "new_pos = ", new_pos );
        move_piece( { "start_id": old_pos, "end_id": new_pos } );
    } else {
        index = 0;
        alert( "There are no more previous moves" );
    }
}

function next( ) {
    let a = $( "#moves" )
        .text( );
    if ( a[ index + 3 ] != null ) {
        console.log( "index = ", index );
        old_pos = "grid_box_" + a[ index ] + a[ index + 1 ];
        new_pos = "grid_box_" + a[ index + 2 ] + a[ index + 3 ];
        console.log( "old_pos = ", old_pos );
        console.log( "new_pos = ", new_pos );
        move_piece( { "start_id": old_pos, "end_id": new_pos } );
        index += 4;
    } else {
        alert( "There are no more next moves" );
    }
}

function drag( ev ) {
    alert( ev.target.parentNode.id );
}

function move_piece( data ) {
    let from = $( "#" + data.start_id )
        .html( );
    let to = $( "#" + data.end_id )
        .html( );
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
