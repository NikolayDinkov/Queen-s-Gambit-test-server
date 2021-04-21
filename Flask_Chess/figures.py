
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
        print("xdif = {0}\n ydif = {1}   in legal in knight".format(xdif, ydif))
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