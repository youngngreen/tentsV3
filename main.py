# nt : not-tent, the places that is impossible to be tent
# cbt : can-be-tent, the places that can be tent

# imports
import time
from board import *
from display import *
from iterlist import *
import pygame

# get the name of the board to be solved
filename = input('enter file\'s name (without extention): ')
f = open('testname.txt', 'w')
f.write(filename+'.txt')
f.close()

# if the name is not right, then exiting the program
try:
    xx = n
except:
    import sys
    sys.exit()

# The solver class
class TaT:
    # this dictionary is used to remove the un-tent-able checks
    # it's according to the other tents that are connected to a tree
    # { TREE_COORDINATE : A_LIST_OF_COORDINATES_OF_THE_SIDES_OF_THE_TREE }
    dots = {}

    # initializing
    def __init__(self, board):
        self.board = board

    # returns only four sides of the given check
    def sides(self, a, b):
        sides_list = []
        for i in range(1, n):
            for j in range(1, n):
                if abs(i-a) <= 1 and abs(j-b) <= 1 and (abs(i-a)+abs(j-b)) == 1:
                    sides_list.append([i, j])
        return sides_list

    # returns total sides of the given check
    def total_sides(self, a, b):
        sides_list = []
        for i in range(1, n):
            for j in range(1, n):
                if abs(i-a) <= 1 and abs(j-b) <= 1 and (i != a or j != b):
                    sides_list.append([i, j])
        return sides_list

    # copies the board and returns it
    def copy(self, BD):
        bd = []
        for i in range(len(BD)):
            bd.append([BD[i][j] for j in range(len(BD))])
        return bd

    # makes sides of trees, cbt
    def func1(self):
        for i in range(1, n):
            for j in range(1, n):
                if self.board[i][j] == 'tr':
                    for x in self.sides(i, j):
                        if self.board[x[0]][x[1]] != 'tr':
                            self.board[x[0]][x[1]] = 'cbt'

    # makes every row or col that is 0, nt
    def func2(self):
        for i in range(1, n):
            if self.board[0][i] == 0:
                for a in range(1, n):
                    if self.board[a][i] == 'cbt':
                        self.board[a][i] = 'nt'
            if self.board[i][0] == 0:
                for a in range(1, n):
                    if self.board[i][a] == 'cbt':
                        self.board[i][a] = 'nt'

    # makes the check, 'tent', and lowers its row and col number by 1 + fills surroundings
    def convert(self, i, j, BD):
        BD[i][j] = 'tent'
        BD[i][0] -= 1
        BD[0][j] -= 1
        tsides = self.total_sides(i, j)
        for x in tsides:
            if BD[x[0]][x[1]] == 'cbt':
                BD[x[0]][x[1]] = 'nt'

    # if the row's or col's cbts are equal to it's number, then give each cbt to convert function
    def func3(self):
        for i in range(1, n):
            row = 0
            col = 0
            for j in range(1, n):
                if self.board[i][j] == 'cbt':
                    row += 1
                if self.board[j][i] == 'cbt':
                    col += 1
            if row == self.board[i][0]:
                for j in range(1, n):
                    if self.board[i][j] == 'cbt':
                        self.convert(i, j, self.board)
            if col == self.board[0][i]:
                for j in range(1, n):
                    if self.board[j][i] == 'cbt':
                        self.convert(j, i, self.board)

    # cleans every row or col with the number of 0 but some cbts
    def cleaner(self):
        bd = self.copy(self.board)
        count = 0
        for i in range(1, n):
            for j in range(1, n):
                if bd[i][j] == 'cbt' and (bd[i][0] == 0 or bd[0][j] == 0):
                    bd[i][j] = 'nt'
                    count += 1
        if count == 0:
            return False
        else:
            return bd

    # loops in the cleaner until there is no need to
    def cleanerLoop(self):
        while self.cleaner() != False:
            self.board = self.cleaner()

    # checks if a and b (two arrays) are equal
    def is_equal(self, a, b):
        count = 0
        total = 0
        for i in range(len(a)):
            for j in range(len(a)):
                total += 1
                if a[i][j] == b[i][j]:
                    count += 1
        if count == total:
            return True
        else:
            return False

    # checks if board is complete or not
    def checker(self, bd):
        flag = True

        for i in range(1, n):
            row_num = bd[i][0]
            cbt_row = 0
            col_num = bd[0][i]
            cbt_col = 0

            for j in range(1, n):
                # check the number of cbts
                # row
                if bd[i][j] == 'cbt':
                    cbt_row += 1
                  #col
                if bd[j][i] == 'cbt':
                    cbt_col += 1

                # checking the tsides of tents
                if bd[i][j] == 'tent':
                    tsides = self.total_sides(i, j)
                    for x in tsides:
                        if bd[x[0]][x[1]] == 'tent':
                            flag = False

            if row_num != cbt_row or col_num != cbt_col or row_num != 0 or col_num != 0:
                flag = False

        return flag

    # returns factorial
    def fact(self, n):
        res = 1
        for i in range(n, 1, -1):
            res *= i
        return res

    # checks if the combination (list) of tents, is possible or not, according to i(row) or j(col)
    def check_odd(self, lst, key):
        i_s = [x[0] for x in lst]
        i_s.sort()
        j_s = [x[1] for x in lst]
        j_s.sort()

        if key == 'i':
            for i in range(len(i_s)-1):
                if abs(i_s[i]-i_s[i+1]) <= 1:
                    return False
        elif key == 'j':
            for j in range(len(j_s)-1):
                if abs(j_s[j]-j_s[j+1]) <= 1:
                    return False
        return True

    # finding the intersections of each row or col and then filling it
    def fill_intersection(self):
        bd = self.copy(self.board)
        for i in range(1, n):
            # row
            cbts = []
            for j in range(1, n):
                if bd[i][j] == 'cbt':
                    cbts.append([i, j])
            if bd[i][0] <= len(cbts):
                poss_cbts = iterlist(cbts, bd[i][0])
                poss_cbts = [q for q in poss_cbts if self.check_odd(q, 'j')]
                for x in cbts:
                    num = 0
                    for y in poss_cbts:
                        if x in y:
                            num += 1
                    if num == len(poss_cbts) and num != 0:
                        self.convert(x[0], x[1], bd)
                        self.func2()

            # col
            cbts = []
            for j in range(1, n):
                if bd[j][i] == 'cbt':
                    cbts.append([j, i])
            if bd[0][i] <= len(cbts):
                poss_cbts = iterlist(cbts, bd[0][i])
                poss_cbts = [q for q in poss_cbts if self.check_odd(q, 'i')]
                for x in cbts:
                    num = 0
                    for y in poss_cbts:
                        if x in y:
                            num += 1
                    if num == len(poss_cbts) and num != 0:
                        self.convert(x[0], x[1], bd)
                        self.func2()

        if self.is_equal(bd, self.board) == False:
            return bd
        return self.board

    # all the possible ways to finish the board (it uses rows to find solution)
    def find_all(self):
        bd = self.copy(self.board)
        all_ways = []
        for i in range(1, n):
            all_cbts = []
            for j in range(1, n):
                if bd[i][j] == 'cbt':
                    all_cbts.append([i, j])
            if all_cbts != []:
                iter_cbts = iterlist(all_cbts, bd[i][0])
                all_ways.append(iter_cbts)
        all_ways_product = [list(i) for i in product(*all_ways)]
        for i in all_ways_product:
            flag = True
            for j in i:
                if self.check_odd(j, 'j') == False:
                    flag = False
                    break
            if flag == True:
                temp = self.copy(bd)
                for x in list(chain.from_iterable(i)):
                    self.convert(x[0], x[1], temp)
                if self.checker(temp) == True:
                    bd = temp
                    break
        return bd

    # dots initializer (uses rows)
    def init_dots(self):
        for i in range(1, n):
            for j in range(1, n):
                if self.board[i][j] == 'tr':
                    self.dots[(i, j)] = self.sides(i, j)

    # changes the board according to the dots
    def apply_dots(self):
        for key, value in self.dots.items():
            if value[0]!=True:
                value_text = [self.board[x[0]][x[1]] for x in value]
                count_tent = 0
                count_cbt = 0
                count_nt = 0
                for x in value_text:
                    if x == 'tent':
                        count_tent += 1
                    elif x == 'cbt':
                        count_cbt += 1
                    elif x == 'nt':
                        count_nt += 1
                if count_tent == 1:
                    for j in value:
                        if self.board[j[0]][j[1]] == 'tent':
                            self.dots[key] = [True, j]
                            break
                if count_cbt == 1 and count_tent == 0:
                    for j in value:
                        if self.board[j[0]][j[1]] == 'cbt':
                            self.dots[key] = [True, j]
                            self.convert(j[0], j[1], self.board)
                            break
                for item in value:
                    if self.board[item[0]][item[1]] == 'tent':
                        count = 0
                        for x in self.sides(item[0], item[1]):
                            if self.board[x[0]][x[1]] == 'tr':
                                count += 1
                        if count == 1:
                            for x in self.sides(item[0], item[1]):
                                if self.board[x[0]][x[1]] == 'tr':
                                    self.dots[(x[0], x[1])] = [True, item]
                                    break
            
    # loops the apply_dots method
    def apply_dots_loop(self):
        pre_bd = self.copy(self.board)
        while True:
            self.apply_dots()
            if self.is_equal(pre_bd, self.board) == True:
                break
            pre_bd = self.copy(self.board)

    # checks if the number of the row or col is bigger than the number of their cbts or not
    def check_0th(self, BD):
        bd = self.copy(BD)
        for i in range(1, n):
            row = 0; col = 0
            for x in range(1, n):
                if bd[i][x]=='cbt':
                    row += 1
                if bd[x][i]=='cbt':
                    col += 1
            if bd[i][0] > row:
                return True
            if bd[0][i] > col:
                return True
        return False

    # fullfils the untentable checks
    # it's according to the fact that if one of the cbts get changed it may reduce 
    #   other row or cols' cbts so their number will be more than their number of cbts
    def fullfil(self):
        for i in range(1, n):
            for j in range(1, n):
                if self.board[i][j]=='cbt':
                    temp = self.copy(self.board)
                    self.convert(i, j, temp)
                    if self.check_0th(temp)==True:
                        self.board[i][j] = 'nt'

    # starts the program
    def start(self):
        self.func1()
        self.func2()
        self.init_dots()
        self.func3()
        pre_bd = self.copy(self.board)
        counter = 0
        while True:
            counter += 1
            self.board = self.fill_intersection()
            self.func2()
            self.func3()
            self.apply_dots_loop()
            self.fullfil()
            self.cleanerLoop()
            if self.is_equal(pre_bd, self.board) == True:
                break
            pre_bd = self.copy(self.board)

        display(self.board)

        if self.checker(self.board)==False:
            if input('solution not found\nchecking all the ways?(y/n) ').lower()=='y':
                t = time.time()
                self.board = self.find_all()
                display(self.board)
                print('time spent:', int(time.time()-t), 'seconds')


# starting
p1 = TaT(board)
p1.start()

# input('\npress enter...')



