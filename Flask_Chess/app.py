from flask import Flask
from flask import render_template, request, redirect, make_response, url_for, flash, jsonify

app = Flask(__name__)

images = {1:"br", 2:"bn", 3:"bb", 4:"bq", 5:"bk", 6:"bp", 7:"wr", 8:"wn", 9:"wb", 10:"wq", 11:"wk", 12:"wp"}
board = [[0 for x in range(8)] for y in range(8)]


class piece:
    """ The super class for all piece types.
        x = x position on board, each space is assigned an x,y position e.g. A1 is 1,1
        y = y position on board
        col = color, 1 for white, 2 for black
        active = True if piece is on board, False if it has been removed or taken
        moved = True if pieces has been moved, False if not (used for pawn first move and castling)
    """
    def __init__(self, x, y, name, col=1):
        self.x = x
        self.y = y
        self.col = col
        self.active = True
        self.moved = False
        self.name = name

    def move(self, new_x, new_y):
        self.moved = True
        self.x = new_x
        self.y = new_y

    def taken(self):
        self.x = 0
        self.y = 0
        self.active = False

    def legal(self, new_x, new_y, taking=False):
        return True

class pawn(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'P'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        # pawn can only move forward, fact equation maps color to direction (1 for white and -1 for black moving up and down the board respectively)
        fact = -2*self.col+3
        print("fact = {}    in legal in pawn".format(fact))
        # pawns move is directional, therefore no abs val
        print("new_y = ", new_y)
        print("new_x = ", new_x)
        print("self.y = ", self.y)
        print("self.x = ", self.x)
        xdif = new_x - self.x
        ydif = new_y - self.y
        print("xdif = {0}\n ydif = {1}   in legal in pawn".format(xdif, ydif))
        # on the pawn's first move, it can move forward two spaces if not taking a piece
        if (not taking) and (not self.moved) and xdif == 0 and ydif == 2*fact:
            return True
        elif taking:
            # if the pawn is taking it can move diagonally either way 1 space
            if abs(xdif) == 1 and ydif == fact:
                return True
            else:
                return False
        # if not taking and not moving directly forward one space, move is illegal
        elif not (xdif == 0 and ydif == fact):
            return False
        return True


class rook(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'R'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        # rook can move in any direction so abs val of move is taken
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        # rook can only move straight
        if not (xdif == 0 or ydif == 0):
            return False
        return True

class knight(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'N'  # type is "N" so as not to be confused with king
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        # knight can move in any direction so abs val of move is taken
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        print("xdif = {0}\n ydif = {1}   in legal in knight".format(xdif, ydif))
        # knight is legal if making l-shape, after abs val there are 2 scenarios
        if not ((xdif == 2 and ydif == 1) or (xdif == 1 and ydif == 2)):
            return False
        return True

class bishop(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'B'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        # bishop can move in any direction so abs val of move is taken
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        # bishop can only move diagonally
        if not xdif == ydif:
            return False
        return True

class king(piece):
    """ each class has a string assigned to type in order to determine its type in other functions
        each class inherits from piece and uses the super() call to initialize all attributes except type
        legal methods do not include castling (handle in Game class functions) because multiple pieces move
    """
    def __init__(self, x, y, name, col=1):
        self.type = 'K'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        # king can move in any direction so abs val of move is taken
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        # return false only if either direction is moving more than 1 space
        if not (xdif <= 1 and ydif <= 1):
            return False
        return True

class queen(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'Q'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        # queen can move in any direction so abs val of move is taken
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        # queen is legal if move is diagonal or straight, hence the 3 cases
        if not (xdif == ydif or xdif == 0 or ydif == 0):
            return False
        return True
    
############################

ROWS = '12345678'
COLS = 'ABCDEFGHabcdefgh'
A, B, C, D, E, F, G, H = 0, 1, 2, 3, 4, 5, 6, 7

ltn = {'A':0, 'a':0, 'B':1, 'b':1, 'C':2, 'c':2, 'D':3, 'd':3, 'E':4, 'e':4, 'F':5, 'f':5, 'G':6, 'g':6, 'H':7, 'h':7}
filter_y = {7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7, 0:8}
filter_y_rev = {1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1, 8:0}

class table:
    def __init__(self):
        wk = king(E, 1, "wk")
        wq = queen(D, 1, "wq")
        wb1 = bishop(C, 1, "wb")
        wb2 = bishop(F, 1, "wb")
        wn1 = knight(B, 1, "wn")
        wn2 = knight(G, 1, "wn")
        wr1 = rook(A, 1, "wr")
        wr2 = rook(H, 1, "wr")
        wp1 = pawn(A, 2, "wp")
        wp2 = pawn(B, 2, "wp")
        wp3 = pawn(C, 2, "wp")
        wp4 = pawn(D, 2, "wp")
        wp5 = pawn(E, 2, "wp")
        wp6 = pawn(F, 2, "wp")
        wp7 = pawn(G, 2, "wp")
        wp8 = pawn(H, 2, "wp")
        bk = king(E, 8, "bk", 2)
        bq = queen(D, 8, "bq", 2)
        bb1 = bishop(C, 8, "bb", 2)
        bb2 = bishop(F, 8, "bb", 2)
        bn1 = knight(B, 8, "bn", 2)
        bn2 = knight(G, 8, "bn", 2)
        br1 = rook(A, 8, "br", 2)
        br2 = rook(H, 8, "br", 2)
        bp1 = pawn(A, 7, "bp", 2)
        bp2 = pawn(B, 7, "bp", 2)
        bp3 = pawn(C, 7, "bp", 2)
        bp4 = pawn(D, 7, "bp", 2)
        bp5 = pawn(E, 7, "bp", 2)
        bp6 = pawn(F, 7, "bp", 2)
        bp7 = pawn(G, 7, "bp", 2)
        bp8 = pawn(H, 7, "bp", 2)
        p_ran = piece(None, None, "--", None)
        self.w_pcs = [wk, wq, wb1, wb2, wn1, wn2, wr1, wr2, wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8]
        self.b_pcs = [bk, bq, bb1, bb2, bn1, bn2, br1, br2, bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8]
        self.board = [
                    [br1, bn1, bb1, bq, bk, bb2, bn2, br2],
                    [bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8],
                    [p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran],
                    [p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran],
                    [p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran],
                    [p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran, p_ran],
                    [wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8],
                    [wr1, wn1, wb1, wq, wk, wb2, wn2, wr2]
                ]

    def print_board(self):
        for col in range(8):
            for row in range(8):
                print(self.board[col][row].name, end=" ")
            print()
        print()
    
    def is_black(self, col, row):
        return self.board[col][row].name[0] == "w"
    
    def is_white(self, col, row):
        return self.board[col][row].name[0] == "b"
    
    def check_for_pieces_between(self, first_col, first_row, second_col, second_row):
        coords = [first_col, first_row, second_col, second_row]
        
        for i in range(4):
            print("coords[{}] = {}".format(i, coords[i]))
        
        if(abs(coords[0]-coords[2]) == abs(coords[1]-coords[3])):
            return True
        
        if(coords[0] == coords[2]):
            start = min(coords[1], coords[3])
            for i in range(start + 1, start + abs(coords[1] - coords[3])):
                if self.board[coords[0]][i].name != "--":
                    print("check betwen fn when equal y")
                    return True
                
        if(coords[1] == coords[3]):
            start = min(coords[0], coords[2])
            for i in range(start + 1, start + abs(coords[0] - coords[2])):
                if self.board[i][coords[1]].name != "--":
                    print("check betwen fn when equal x")
                    return True
        return False
    
    def check_legal(self, oldcol, oldrow, newcol, newrow):
        print("self.board[oldcol][oldrow].name = ", self.board[oldcol][oldrow].name)
        print("self.board[newcol][newrow].name = ", self.board[newcol][newrow].name)
        
        if self.board[oldcol][oldrow].name == "--":
            return False
        if self.board[oldcol][oldrow].legal(newrow, filter_y[newcol]) == False:
            return False
        if self.check_for_pieces_between(oldcol, oldrow, newcol, newrow):
            return False
        if self.board[newcol][newrow].name == "--" and self.board[newcol][newrow].name[0] != self.board[oldcol][oldrow].name[0]:
            return True
        return False

    def checkmate(self):
        pass

    def check_move(self, oldcol, oldrow, newcol, newrow):
        
        if self.check_legal(oldcol, oldrow, newcol, newrow):
            self.board[newcol][newrow] = self.board[oldcol][oldrow]
            self.board[oldcol][oldrow] = piece(None, None, "--", None)
            print("Legal")
            return True
        print("NOT legal")
        return False
    
    def convert_input_string_to_coordinates(self, first, second):
        fir_x = ltn[first[0]]
        fir_y = filter_y_rev[int(first[1])]
        sec_x = ltn[second[0]]
        sec_y = filter_y_rev[int(second[1])]
        return [fir_y, fir_x, sec_y, sec_x]
    
    def get_move_input(self, start, end=""):
        print("\nNewMove: {} -> {}\n".format(start, end))
        if(type(start) == type(end) == str and end != ""):
            
            if start[0] not in COLS or end[0] not in COLS or start[1] not in ROWS or end[1] not in ROWS:
                print("Wrong input handed, Please enter strings, e.g. (\"A1\",\"A2\") ")
                return False
            
            coords = self.convert_input_string_to_coordinates(start, end)
            return self.check_move(coords[0], coords[1], coords[2], coords[3])
        
        elif start == "0-0" or start == "0-0-0":
            print("CASTLE FUNCTION NOT READY")
            return True
        else:
            print("Wrong input handed, Please enter strings, e.g. (\"A1\",\"A2\") ")
            return False


@app.route('/')
def first_page():
    for i in range(1,6):
        board[0][i-1] = i
        board[7][i-1] = 6+i
    for i in range(3,0,-1):
        board[0][5+3-i] = i
        board[7][5+3-i] = 6+i
    for i in range(0,8):
        board[1][i] = 6
        board[6][i] = 12

    return render_template("display_board.html", board=board, images=images)

@app.route('/2')
def second_page():
    for i in range(1,6):
        board[0][i-1] = i
        board[7][i-1] = 6+i
    for i in range(3,0,-1):
        board[0][5+3-i] = i
        board[7][5+3-i] = 6+i
    for i in range(0,8):
        board[1][i] = 6
        board[6][i] = 12

    return render_template("index.html", board=board, images=images)


@app.route('/3', methods=['GET', 'POST'])
def third_page():
    if request.method == "POST":
        return "OK"
    game = table()
    print(game.board[0][0].name)

    return render_template('third.html', board=game.board)


@app.route('/ajax', methods = ['POST'])
def ajax_request():
    position = request.form['position']
    position = position[9:]
    print(position)
    return jsonify(position=position)

if __name__ == '__main__':
    app.run(debug=True)

