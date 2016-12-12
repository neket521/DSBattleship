import sys
import random
class Board():
    def __init__(self):
        self.size = 11
        self.list = [[0 for x in range(self.size)] for x in range(self.size)]

    def add_ships(self):
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        types = ["Carrier: 4", "Battleship: 3", "Cruiser: 2", "Submarine: 1"]
        for e in ships:
            x = random.randint(0, self.size)
            y = random.randint(0, self.size)
            d = random.randint(0, 1)
            self.add_ship(e,x,y,d)
        map(lambda x: x.pop(), self.list).pop()
        self.size = 10

    def add_ship(self,ship,x,y,d):
        if self.place_available(ship, x, y, d):
            if d == 0:
                for i in range(0,ship):
                    self.list[x][y] = ship
                    x += 1
            else:
                for i in range(0,ship):
                    self.list[x][y] = ship
                    y += 1
        else:
            x = random.randint(0, self.size)
            y = random.randint(0, self.size)
            d = random.randint(0, 1)
            self.add_ship(ship,x,y,d)

    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.list[i][j] != 0:
                    sys.stdout.write(" " + str(self.list[i][j])+ " ")
                else:
                    sys.stdout.write(" _ ")
            print

    def place_available(self,size,x,y,d):
        try:
            if d == 0:
                for i in range(0,size+2):
                    if self.list[x+i-1][y] !=0 or self.list[x+i-1][y+1] !=0 or self.list[x+i-1][y-1] !=0:
                        return False
            else:
                for i in range(0,size+2):
                    if self.list[x][y+i-1] !=0 or self.list[x+1][y+i-1] !=0 or self.list[x-1][y+i-1] !=0:
                        return False
            return True
        except:
            return False

board = Board()
board.add_ships()
board.print_board()


