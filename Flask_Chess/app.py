from flask import Flask
from flask import render_template, request, redirect, make_response, url_for, flash, jsonify

app = Flask(__name__)

images = {1:"br", 2:"bn", 3:"bb", 4:"bq", 5:"bk", 6:"bp", 7:"wr", 8:"wn", 9:"wb", 10:"wq", 11:"wk", 12:"wp"}

class piece:
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
        self.passant = False
        super().__init__(x, y, name, col)

    def move(self, new_x, new_y):
        if self.moved == False:
            self.passant = True
        else:
            self.passant = False
        super().move(new_x, new_y)

    def legal(self, new_x, new_y, taking=False):
        fact = -2*self.col+3
        xdif = new_x - self.x
        ydif = new_y - self.y
        if (not taking) and (not self.moved) and xdif == 0 and ydif == 2*fact:
            self.passant = True
            return True
        elif taking:
            if abs(xdif) == 1 and ydif == fact:
                return True
            else:
                return False
        elif not (xdif == 0 and ydif == fact):
            return False
        return True

class rook(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'R'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        if not (xdif == 0 or ydif == 0):
            return False
        return True

class knight(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'N'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        if not ((xdif == 2 and ydif == 1) or (xdif == 1 and ydif == 2)):
            return False
        return True

class bishop(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'B'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        if not xdif == ydif:
            return False
        return True

class king(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'K'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        if not (xdif <= 1 and ydif <= 1):
            return False
        return True

class queen(piece):
    def __init__(self, x, y, name, col=1):
        self.type = 'Q'
        super().__init__(x, y, name, col)

    def legal(self, new_x, new_y, taking=False):
        xdif = abs(new_x-self.x)
        ydif = abs(new_y-self.y)
        if not (xdif == ydif or xdif == 0 or ydif == 0):
            return False
        return True

ROWS = '12345678'
COLS = 'ABCDEFGHabcdefgh'
A, B, C, D, E, F, G, H = 1, 2, 3, 4, 5, 6, 7, 8

ltn = {'A':0, 'a':0, 'B':1, 'b':1, 'C':2, 'c':2, 'D':3, 'd':3, 'E':4, 'e':4, 'F':5, 'f':5, 'G':6, 'g':6, 'H':7, 'h':7}
ntl = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}
filter_y = {8:0, 7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7, 0:8}

class table:
    def __init__(self):
        self.turn = 1
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
        print()
        for col in range(8):
            for row in range(8):
                print(self.board[col][row].name, end=" ")
            print()
        print()
    
    def check_for_pieces_between(self, first_col, first_row, second_col, second_row):
        coords = [first_col, first_row, second_col, second_row]
        
        abs_x = abs(coords[1]-coords[3])
        abs_y = abs(coords[0]-coords[2])
        
        if(abs_x == abs_y):
            start_x = min(coords[1], coords[3])
            start_y = max(coords[0], coords[2])
            for i in range(start_x + 1, start_x + abs_x):
                if self.board[start_y - (i - start_x)][i].name != "--":
                    return True
        
        if(coords[0] == coords[2]):
            start = min(coords[1], coords[3])
            for i in range(start + 1, start + abs(coords[1] - coords[3])):
                if self.board[coords[0]][i].name != "--":
                    return True
                
        if(coords[1] == coords[3]):
            start = min(coords[0], coords[2])
            for i in range(start + 1, start + abs(coords[0] - coords[2])):
                if self.board[i][coords[1]].name != "--":
                    return True
        return False
    
    def check_taking(self, p1_y, p1_x, p2_y, p2_x):
        if self.board[p1_y][p1_x].name[1] == 'p' and self.board[p1_y][p2_x].name[1] == 'p' and p1_x - p2_x != 0:
            if self.board[p1_y][p2_x].passant:
                return True
            
        if (self.board[p1_y][p1_x].name != "--"
        and self.board[p2_y][p2_x].name != "--" 
        and self.board[p1_y][p1_x].name[0] != self.board[p2_y][p2_x].name[0]):
            return True
        return False
    
    def check_turn(self, color):
        if self.turn % 2 == 0 and color == 2:
            self.turn += 1
            return True
        if self.turn % 2 == 1 and color == 1:
            self.turn += 1
            return True
        return False
    
    def check_legal(self, oldcol, oldrow, newcol, newrow):
        taking = self.check_taking(oldcol, oldrow, newcol, newrow)
        
        if (self.board[oldcol][oldrow].legal(newrow+1, filter_y[newcol], taking)
        and not self.check_for_pieces_between(oldcol, oldrow, newcol, newrow)
        and self.board[oldcol][oldrow].name[0] != self.board[newcol][newrow].name[0]
        and self.check_turn(self.board[oldcol][oldrow].col)):
            self.board[oldcol][oldrow].move(newrow+1, filter_y[newcol])
            if taking:
                if self.board[oldcol][newrow].name[1] == "p":
                    if self.board[oldcol][newrow].passant:
                        self.board[oldcol][newrow].taken()
                        self.board[oldcol][newrow] = piece(None, None, "--", None)
                else:
                    self.board[newcol][newrow].taken()
            return True
        else:
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
        fir_y = filter_y[int(first[1])]
        fir_x = ltn[first[0]]
        sec_y = filter_y[int(second[1])]
        sec_x = ltn[second[0]]

        return [fir_y, fir_x, sec_y, sec_x]
    
    def convert_coordinates_to_string(self, first_x, first_y, second_x, second_y):
        first = ntl[first_x] + str(filter_y[first_y])
        second = ntl[second_x] + str(filter_y[second_y])
        return [first, second]
    
    def castle(self, move):
        turn = self.turn % 2
        kings_rooks = ["wk", "wr", "bk", "br"]
        if move == "0-0":
            x1 = 1
            x2 = -1
        else:
            x1 = 2
            x2 = -1
            
        if turn == 1:
            if move == "0-0":
                coords = self.convert_input_string_to_coordinates("e1", "h1")
            if move == "0-0-0":
                coords = self.convert_input_string_to_coordinates("a1", "e1")
        if turn == 0:
            if move == "0-0":
                coords = self.convert_input_string_to_coordinates("e8", "h8")
            if move == "0-0-0":
                coords = self.convert_input_string_to_coordinates("a8", "e8")
        
        if (not self.check_for_pieces_between(coords[0], coords[1], coords[2], coords[3])
            and not self.board[coords[0]][coords[1]].moved
            and not self.board[coords[2]][coords[3]].moved
            and self.board[coords[0]][coords[1]].name in kings_rooks
            and self.board[coords[2]][coords[3]].name in kings_rooks):
                self.board[coords[0]][coords[1]].move(coords[3]+x2, filter_y[coords[2]])
                self.board[coords[2]][coords[3]].move(coords[1]+x1, filter_y[coords[0]])
                self.board[coords[0]][coords[1]+x1], self.board[coords[2]][coords[3]+x2] = self.board[coords[2]][coords[3]], self.board[coords[0]][coords[1]]
                self.board[coords[0]][coords[1]] = piece(None, None, "--", None)
                self.board[coords[2]][coords[3]] = piece(None, None, "--", None)
                self.turn += 1
                print("Legal")
                return True
        print("Not Legal")
        return False    
        
        
    def get_move_input(self, start, end=""):
        print("\nNewMove: {} -> {}\n".format(start, end))
        if(type(start) == type(end) == str and end != ""):
            
            if start[0] not in COLS or end[0] not in COLS or start[1] not in ROWS or end[1] not in ROWS:
                print("Wrong input handed, Please enter strings, e.g. (\"A1\",\"A2\") ")
                return False
            coords = self.convert_input_string_to_coordinates(start, end)
            return self.check_move(coords[0], coords[1], coords[2], coords[3])
        
        elif start == "0-0" or start == "0-0-0":
            return self.castle(start)
        else:
            print("Wrong input handed, Please enter strings, e.g. (\"A1\",\"A2\") ")
            return False
    
game = table()

@app.route('/', methods=['GET', 'POST'])
def index():
    print(game.board[0][0].name)
    return render_template('index.html', board=game.board)

@app.route('/ajax', methods = ['POST'])
def ajax_request():
    old_pos_x = ""
    old_pos_y = ""
    new_pos_x = ""
    new_pos_y = ""

    old_pos = request.form['old_pos']
    if old_pos != "":
        old_pos_x = int(old_pos[9])
        old_pos_y = int(old_pos[10])

    new_pos = request.form['new_pos']
    if new_pos != "":
        new_pos_x = int(new_pos[9])
        new_pos_y = int(new_pos[10])

    restart = request.form['restart']
    if restart == "True":
        global game
        game = table()

    if old_pos != "" and new_pos != "":
        coordinates = game.convert_coordinates_to_string(old_pos_x, old_pos_y, new_pos_x, new_pos_y)
        if ((coordinates[0][0] == "E" or coordinates[1][0] == "E")
        and (coordinates[1][0] == "A" or coordinates[0][0] == "A")):
            allowed = game.get_move_input("0-0-0")
            restart = "refresh"
        elif ((coordinates[0][0] == "E" or coordinates[1][0] == "E")
        and (coordinates[1][0] == "H" or coordinates[0][0] == "H")):
            allowed = game.get_move_input("0-0")
            restart = "refresh"
        else:
            allowed = game.get_move_input(coordinates[0], coordinates[1])
    else:
        coordinates = ["","","",""]
        allowed = False

    return jsonify(old_position=coordinates[0], new_position=coordinates[1], allowed=allowed, restart=restart)

if __name__ == '__main__':
    app.run(debug=True)
