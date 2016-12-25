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
                    self.add_ship(e, x, y, d)
                map(lambda x: x.pop(), self.list).pop()
                break
            if answer == 'm':
                self.list = [[0 for x in range(self.size)] for x in range(self.size)]
                self.print_board()
                self.old_list = [row[:] for row in self.list]
                for ship in ships:
                    self.manual_helper(ship)
                map(lambda x: x.pop(), self.list).pop()
                break

    def manual_helper(self, ship):
        self.ask_coordinates_and_place_ship(ship)
        self.print_board()
        while 1:
            x = raw_input("Confirm (c) or reposition the last ship (r):\n")
            if x == 'c':
                self.old_list = [row[:] for row in self.list]
                break
            if x == 'r':
                self.list = [row[:] for row in self.old_list]
                self.print_board()
                self.manual_helper(ship)
                break

    def ask_coordinates_and_place_ship(self, ship):
        letters = 'ABCDEFGHIJ'
        while 1:
            x = raw_input('Enter ' + str(
                ship) + ' sized ship coordinates in a form of A1 followed by direction(0 = vertical,1 = horizontal)(for example A50):\n')
            if x != '' and len(x) == 3 or len(x) == 4:
                if len(x) == 3:
                    if x[0].lower() in letters.lower() and 1 <= int(x[1]) <= 10 and 0 <= int(x[2]) <= 1:
                        y = letters.lower().index(x[0].lower())
                        self.place_manually(ship, int(x[1]) - 1, y, int(x[2]))
                        break
                if len(x) == 4:
                    if x[0].lower() in letters.lower() and 1 <= int(x[1] + x[2]) <= 10 and 0 <= int(x[3]) <= 1:
                        y = letters.lower().index(x[0].lower())
                        self.place_manually(ship, int(x[1] + x[2]) - 1, y, int(x[3]))
                        break

    def place_manually(self, ship, x, y, d):
        if self.place_available(ship, x, y, d):
            if d == 0:
                print ship
                for i in range(0, ship):
                    self.list[x][y] = int(ship)
                    x += 1
            else:
                for i in range(0, ship):
                    self.list[x][y] = int(ship)
                    y += 1
        else:
            print "Not available place"
            self.ask_coordinates_and_place_ship(ship)

    def add_ship(self, ship, x, y, d):
        if self.place_available(ship, x, y, d):
            if d == 0:
                for i in range(0, ship):
                    self.list[x][y] = ship
                    x += 1
            else:
                for i in range(0, ship):
                    self.list[x][y] = ship
                    y += 1
        else:
            x = random.randint(0, self.size)
            y = random.randint(0, self.size)
            d = random.randint(0, 1)
            self.add_ship(ship, x, y, d)

    def print_board(self):
        print "    A  B  C  D  E  F  G  H  I  J"
        for i in range(self.size_to_print):
            if i == 9:
                sys.stdout.write(" " + str(i + 1))
            else:
                sys.stdout.write(" " + str(i + 1) + ' ')
            for j in range(self.size_to_print):
                if self.list[i][j] != 0:
                    sys.stdout.write(FIELD_SHIP)
                else:
                    sys.stdout.write(FIELD_EMPTY)
            print

    def print_2_boards(self, list2):
        print "    A  B  C  D  E  F  G  H  I  J            A  B  C  D  E  F  G  H  I  J  "
        for i in range(self.size_to_print):
            if i == 9:
                sys.stdout.write(" " + str(i + 1))
            else:
                sys.stdout.write(" " + str(i + 1) + ' ')
            for j in range(self.size_to_print):
                if self.list[i][j] != 0:
                    sys.stdout.write(FIELD_SHIP)
                else:
                    sys.stdout.write(FIELD_EMPTY)

            if i == 9:
                sys.stdout.write("        " + str(i + 1))
            else:
                sys.stdout.write("        " + str(i + 1) + " ")
            for j in range(self.size_to_print):
                if list2[i][j] != 0:
                    sys.stdout.write(FIELD_SHIP)
                else:
                    sys.stdout.write(FIELD_EMPTY)
            print

    def print_n_boards(self, boards):
        sys.stdout.write("            your board" + " "*30)
        for i in range(len(boards)):
            sys.stdout.write(boards.keys()[i] +"'s board" +  " "*27)
        print
        for i in range(len(boards)+1):
            sys.stdout.write("    A  B  C  D  E  F  G  H  I  J        ")
        print
        for i in range(self.size_to_print):
            if i == 9:
                sys.stdout.write(" " + str(i + 1))
            else:
                sys.stdout.write(" " + str(i + 1) + ' ')
            for j in range(self.size_to_print):
                if self.list[i][j] != 0:
                    sys.stdout.write(FIELD_SHIP)
                else:
                    sys.stdout.write(FIELD_EMPTY)

            for k in range(len(boards)):
                if i == 9:
                    sys.stdout.write("        " + str(i + 1))
                else:
                    sys.stdout.write("        " + str(i + 1) + " ")
                for j in range(self.size_to_print):
                    if boards.values()[k][i][j] != 0:
                        sys.stdout.write(FIELD_SHIP)
                    else:
                        sys.stdout.write(FIELD_EMPTY)
            print

    def place_available(self, size, x, y, d):
        try:
            if d == 0:
                for i in range(0, size + 2):
                    if self.list[x + i - 1][y] != 0 or self.list[x + i - 1][y + 1] != 0 or self.list[x + i - 1][
                                y - 1] != 0:
                        return False
            else:
                for i in range(0, size + 2):
                    if self.list[x][y + i - 1] != 0 or self.list[x + 1][y + i - 1] != 0 or self.list[x - 1][
                                        y + i - 1] != 0:
                        return False
            return True
        except:
            return False

    def get_positioned_ships(self):
        return self.list

#b = Board()
#b.add_ships()
#boards = {}
#boards["user1"] = b.list
#boards["user2"] = b.list
#boards["user3"] = b.list
#boards["user4"] = b.list
#list2 = b.list
#b.print_n_boards(boards)