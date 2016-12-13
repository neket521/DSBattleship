import sys
import random
from common import FIELD_EMPTY, FIELD_SHIP

class Board():

    def __init__(self):
        self.size_to_print = 10
        self.size = 11
        self.info = 'Ships to position:\nCarrier of size 4 x1, Battleship of size 3 x2, Cruiser of size 2 x3, Submarine of size 1 x4'

    def add_ships(self):
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        types = ["Carrier: 4", "Battleship: 3", "Cruiser: 2", "Submarine: 1"]
        print self.info
        while 1:
            answer = raw_input("Do you want to place ships manually(m), or allow AI(a) to place them randomly?\n")
            if answer == 'a':
                self.list = [[0 for x in range(self.size)] for x in range(self.size)]
                for e in ships:
                    x = random.randint(0, self.size)
                    y = random.randint(0, self.size)
                    d = random.randint(0, 1)
                    self.add_ship(e,x,y,d)
                map(lambda x: x.pop(), self.list).pop()
                return
            if answer == 'm':
                self.list = [[0 for x in range(self.size)] for x in range(self.size)]
                self.print_board()
                for ship in ships:
                    self.ask_coordinates_and_place_ship(ship)
                    self.print_board()
                map(lambda x: x.pop(), self.list).pop()
                return

    def ask_coordinates_and_place_ship(self, ship):
        letters = 'ABCDEFGHIJ'
        while 1:
            x = raw_input('Enter ' + str(ship) + ' sized ship coordinates: letter and number(for example A1):\n')
            d = raw_input('Enter ' + str(ship) + ' sized ship direction(0 = vertical,1 = horizontal):\n')
            if x != '' and d != '':
                if x[0].lower() in letters.lower() and 0 <= int(d) <= 1:
                    break
        y = letters.lower().index(x[0].lower())
        self.place_manually(ship, int(x[1]) - 1, y, int(d))

    def place_manually(self,ship,x,y,d):
        if self.place_available(ship, x, y, d):
            if d == 0:
                print ship
                for i in range(0,ship):
                    self.list[x][y] = int(ship)
                    x += 1
            else:
                for i in range(0,ship):
                    self.list[x][y] = int(ship)
                    y += 1
        else:
            print "Not available place"
            self.ask_coordinates_and_place_ship(ship)

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
        print "    A  B  C  D  E  F  G  H  I  J"
        for i in range(self.size_to_print):
            if i == 9:
                sys.stdout.write(" " + str(i+1))
            else:
                sys.stdout.write(" " + str(i+1) + ' ')
            for j in range(self.size_to_print):
                if self.list[i][j] != 0:
                    sys.stdout.write(FIELD_SHIP)
                else:
                    sys.stdout.write(FIELD_EMPTY)
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

    def get_positioned_ships(self):
        return self.list


