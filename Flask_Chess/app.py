from flask import Flask
from flask import render_template, request, redirect, make_response, url_for, flash

app = Flask(__name__)

images = {1:"br", 2:"bn", 3:"bb", 4:"bq", 5:"bk", 6:"bp", 7:"wr", 8:"wn", 9:"wb", 10:"wq", 11:"wk", 12:"wp"}
board = [[0 for x in range(8)] for y in range(8)]


A, B, C, D, E, F, G, H = 1, 2, 3, 4, 5, 6, 7, 8
class piece(object):
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
        # pawns move is directional, therefore no abs val
        xdif = new_x-self.x
        ydif = new_y-self.y
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
class game(object):
    def __init__(self):
        wk = king(E, 1, "wk")
        wq = queen(D, 1, "wq")
        wb1 = bishop(C, 1, "wb")
        wb2 = bishop(F, 1, "wb")
        wh1 = knight(B, 1, "wh")
        wh2 = knight(G, 1, "wh")
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
        bh1 = knight(B, 8, "bh", 2)
        bh2 = knight(G, 8, "bh", 2)
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
        self.w_pcs = [wk, wq, wb1, wb2, wh1, wh2, wr1, wr2, wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8]
        self.b_pcs = [bk, bq, bb1, bb2, bh1, bh2, br1, br2, bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8]
        self.board1 = [
                    [br1, bh1, bb1, bq, bk, bb2, bh2, br2],
                    [bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8],
                    [wr1, wh1, wb1, wq, wk, wb2, wh2, wr2]
                ]  

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

@app.route('/3')
def third_page():
    game1 = game()
    print(game1.board1[0][0].name)
    return render_template('third.html', board=game1.board1)

if __name__ == '__main__':
    app.run(debug=True)

