import sys
import random
class Board():
    def __init__(self):
        self.size = 10

    def add_ships(self):
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        types = ["Carrier: 4", "Battleship: 3", "Cruiser: 2", "Submarine: 1"]
        while 1:
            print"Do you want to place ships manually(m), or allow AI(a) to place them randomly?"
            answer = raw_input()
            if answer == 'a':
                self.size = 11
                self.list = [[0 for x in range(self.size)] for x in range(self.size)]
                for e in ships:
                    x = random.randint(0, self.size)
                    y = random.randint(0, self.size)
                    d = random.randint(0, 1)
                    self.add_ship(e,x,y,d)
                map(lambda x: x.pop(), self.list).pop()
                self.size = 10
                break
            if answer == 'm':
                self.size = 11
                self.list = [[0 for x in range(self.size)] for x in range(self.size)]
                for e in ships:
                    letters = 'ABCDEFGHIJ'
                    while 1:
                        x = raw_input('Enter ' + str(e) + ' sized ship coordinates: letter and number(for example A1) ')
                        d = raw_input('Enter ' + str(e) + ' sized ship direction(0 = vertical,1 = horisontal) ')
                        if x != '' and d != '':
                            if x[0].lower() in letters.lower() and 0 <= int(d) <= 1:
                                break
                    self.size = 11
                    y = letters.lower().index(x[0].lower())
                    self.place_manually(e,int(x[1])-1,y,int(d))
                    #print self.list
                    self.size = 10
                    self.print_board()

                map(lambda x: x.pop(), self.list).pop()
                print
                break

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
            while 1:
                x = raw_input('Enter ' + str(ship) + ' sized ship x coordinate ')
                y = raw_input('Enter ' + str(ship) + ' sized ship y coordinate ')
                d = raw_input('Enter ' + str(ship) + ' sized ship direction(0 = vertical,1 = horizontal) ')
                if x != '' and y != '' and d != '':
                            if 0 <= int(x) <= 9 and  0 <= int(y) <= 9 and 0 <= int(d) <= 1:
                                break
            self.place_manually(ship,int(y),int(x),int(d))

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
        for i in range(self.size):
            if i == 9:
                sys.stdout.write(" " + str(i+1))
            else:
                sys.stdout.write(" " + str(i+1) + ' ')
            for j in range(self.size):
                if self.list[i][j] != 0:
                    sys.stdout.write(" " + str(self.list[i][j])+ " ")
                else:
                    sys.stdout.write(" 0 ")
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


