from figures import piece, pawn, rook, knight, bishop, king, queen

images = {1:"br", 2:"bn", 3:"bb", 4:"bq", 5:"bk", 6:"bp", 7:"wr", 8:"wn", 9:"wb", 10:"wq", 11:"wk", 12:"wp"}

ROWS = '12345678'
COLS = 'ABCDEFGHabcdefgh'
A, B, C, D, E, F, G, H = 1, 2, 3, 4, 5, 6, 7, 8

ltn = {'A':0, 'a':0, 'B':1, 'b':1, 'C':2, 'c':2, 'D':3, 'd':3, 'E':4, 'e':4, 'F':5, 'f':5, 'G':6, 'g':6, 'H':7, 'h':7}
ntl = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}
filter_y = {8:0, 7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7, 0:8}

class table:
    def __init__(self):
        self.turn = 1
        self.white_king = [7,4]
        self.black_king = [0,4]
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
        
        abs_x = abs(coords[3]-coords[1])
        abs_y = abs(coords[2]-coords[0])
        
        if abs_x == abs_y:
            
            if coords[1] > coords[3]:
                dif_x = -1
            else:
                dif_x = 1
       
            if coords[0] > coords[2]:
                dif_y = -1
            else:
                dif_y = 1
            
            for i in range(abs_x - 1):
                if self.board[coords[0] + dif_y][coords[1] + dif_x].name != "--":
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
    
    def check_taking(self, p1_y, p1_x, p2_y, p2_x):
        if self.board[p1_y][p1_x].name[1] == 'p' and self.board[p1_y][p2_x].name[1] == 'p' and p1_x - p2_x != 0:
            if self.board[p1_y][p2_x].passant:
                return True
            
        if (self.board[p1_y][p1_x].name != "--"
        and self.board[p2_y][p2_x].name != "--" 
        and self.board[p1_y][p1_x].name[0] != self.board[p2_y][p2_x].name[0]):
            print("taking true")
            return True
        print("taking false")
        return False
    
    def check_turn(self, color):
        print("color input = ", color)
        if self.turn % 2 == 0 and color == 2:
            print("black")
            self.turn += 1
            return True
        if self.turn % 2 == 1 and color == 1:
            print("wite")
            self.turn += 1
            return True
        print("wrong color")
        return False
    
    def check_legal(self, oldcol, oldrow, newcol, newrow):
        taking = self.check_taking(oldcol, oldrow, newcol, newrow)
        
        if (self.board[oldcol][oldrow].legal(newrow+1, filter_y[newcol], taking)
        and not self.check_for_pieces_between(oldcol, oldrow, newcol, newrow)
        and self.board[oldcol][oldrow].name[0] != self.board[newcol][newrow].name[0]
        and self.check_turn(self.board[oldcol][oldrow].col)):
            
            self.board[oldcol][oldrow].move(newrow+1, filter_y[newcol])
            
            print("king in check = ", self.king_in_check())
            
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
    
    def king_in_check(self):
        if self.turn % 2 == 1:
            print("white was this")
            print("self.white_king = ", self.white_king)
            print("self.black_king = ", self.black_king)
            return self.is_check(self.white_king[0], self.white_king[1], "w")
        if self.turn % 2 == 0:
            print("black was this")
            return self.is_check(self.black_king[0], self.black_king[1], "b")
    
    def is_check(self, col, row, color):
        if color == "w":
            check_for_color = ["b", "w"]
        if color == "b":
            check_for_color = ["w", "b"]
            
        print("color[0] = ", check_for_color[0])
        print("color[1] = ", check_for_color[1])
        
        for up in range(col + 1 , 8):
            print("up = ", up)
            print("row = ", row)
            if row >= 7 or up >= 7:
                break
            if self.board[up][row].name[0] == check_for_color[0]:
                return True
            if self.board[up][row].name[0] == check_for_color[1]:
                break
        for down in range(col - 1 , 0, -1):
            if down >= 7 or row >= 7:
                break
            if self.board[down][row].name[0] == check_for_color[0]:
                return True
            if self.board[down][row].name[0] == check_for_color[1]:
                break
        for left in range(row - 1, 0, -1):
            if left >= 7 or col >= 7:
                break
            if self.board[col][left].name[0] == check_for_color[0]:
                return True
            if self.board[col][left].name[0] == check_for_color[1]:
                break
        for right in range(row + 1, 8):
            if col >= 7 or right >= 7:
                break
            if self.board[col][right].name[0] == check_for_color[0]:
                return True
            if self.board[col][right].name[0] == check_for_color[1]:
                break
        
        for left_up in range(1, 8):
            if col + left_up >= 7 or row + left_up >= 7:
                break
            if self.board[col + left_up][row + left_up].name[0] == check_for_color[0]:
                return True
            if self.board[col + left_up][row + left_up].name[0] == check_for_color[1]:
                break
        for left_down in range(1, 8):
            if col - left_down >= 7 or row + left_down >= 7:
                break
            if self.board[col - left_down][row + left_down].name[0] == check_for_color[0]:
                return True
            if self.board[col - left_down][row + left_down].name[0] == check_for_color[1]:
                break
        for right_up in range(1, 8):
            if col + right_up >= 7 or row - right_up >= 7:
                break
            if self.board[col + right_up][row - right_up].name[0] == check_for_color[0]:
                return True
            if self.board[col + right_up][row - right_up].name[0] == check_for_color[1]:
                break
        for right_down in range(1, 8):
            if col - right_down >= 7 or row - right_down >= 7:
                break
            if self.board[col - left_down][row - left_down].name[0] == check_for_color[0]:
                return True
            if self.board[col - left_down][row - left_down].name[0] == check_for_color[1]:
                break
            
            if col+2 < 7 and row + 1 < 7:
                if self.board[col+2][row+1].name[0] == check_for_color[0]:
                    return True
            if col+2 < 7 and row - 1 < 7:
                if self.board[col+2][row-1].name[0] == check_for_color[0]:
                    return True
            if col-2 < 7 and row + 1 < 7:
                if self.board[col-2][row+1].name[0] == check_for_color[0]:
                    return True
            if col-2 < 7 and row - 1 < 7:
                if self.board[col-2][row-1].name[0] == check_for_color[0]:
                    return True    
        return False
        
    def checkmate(self):
        pass

    def check_move(self, oldcol, oldrow, newcol, newrow):
        if self.check_legal(oldcol, oldrow, newcol, newrow):
            if self.board[oldcol][oldrow].name == "wk":
                self.white_king = [newrow, newcol]
            if self.board[oldcol][oldrow].name == "bk":
                self.black_king = [newrow, newcol]
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
            color = "w"
            if move == "0-0":
                coords = self.convert_input_string_to_coordinates("e1", "h1")
            if move == "0-0-0":
                coords = self.convert_input_string_to_coordinates("a1", "e1")
        if turn == 0:
            color = "b"
            if move == "0-0":
                coords = self.convert_input_string_to_coordinates("e8", "h8")
            if move == "0-0-0":
                coords = self.convert_input_string_to_coordinates("a8", "e8")
        
        if (not self.check_for_pieces_between(coords[0], coords[1], coords[2], coords[3])
            and not self.board[coords[0]][coords[1]].moved
            and not self.board[coords[2]][coords[3]].moved
            and self.board[coords[0]][coords[1]].name in kings_rooks
            and self.board[coords[2]][coords[3]].name in kings_rooks):
            
                for i in range(coords[1], coords[3]):
                    if self.is_check(coords[0], i, color) == True:
                        print("You Are In Check!")
                        print("Not Legal")
                        return False
            
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
            
            print("coords = ", coords)
            
            return self.check_move(coords[0], coords[1], coords[2], coords[3])
        
        elif start == "0-0" or start == "0-0-0":
            return self.castle(start)
        else:
            print("Wrong input handed, Please enter strings, e.g. (\"A1\",\"A2\") ")
            return False
        
    def print_turn(self):
        if self.turn % 2 == 0:
            return "Black turn is"
        else:
            return "White turn is"