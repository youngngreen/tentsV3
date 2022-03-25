import time
from display import *
from itertools import combinations, product, chain
import os, psutil

def iterlist(lst, num):
    combs = combinations(lst, num)
    return [list(i) for i in combs]

filename = input('enter file\'s name (no extention): ')
f = open('testname.txt', 'w')
f.write(filename+'.txt')
f.close()

try:
    xx = n
except:
    import sys
    sys.exit()

class hillClimbing:
    dots = {}
    def __init__(self, board):
        self.board = board

    def duplicatedBoard(self, currentBoard):
        newBoard = []
        for i in range(len(currentBoard)):
            newBoard.append([currentBoard[i][j] for j in range(len(currentBoard))])
        return newBoard

    def nextTo(self, a, b):
        nextTo_list = []
        for i in range(1, n):
            for j in range(1, n):
                if abs(i-a) <= 1 and abs(j-b) <= 1 and (abs(i-a)+abs(j-b)) == 1:
                    nextTo_list.append([i, j])
        return nextTo_list

    def total_nextTo(self, a, b):
        nextTo_list = []
        for i in range(1, n):
            for j in range(1, n):
                if abs(i-a) <= 1 and abs(j-b) <= 1 and (i != a or j != b):
                    nextTo_list.append([i, j])
        return nextTo_list

    # def stepUp(self):
    #     newBoard = self.duplicatedBoard(self.board)
    #     for i in range(1, n):
    #         # row
    #         cans = []
    #         for j in range(1, n):
    #             if newBoard[i][j] == 'can':
    #                 cans.append([i, j])
    #         if newBoard[i][0] <= len(cans):
    #             poss_cans = iterlist(cans, newBoard[i][0])
    #             poss_cans = [q for q in poss_cans if self.climbCheckNum(q, 'j')]
    #             for x in cans:
    #                 num = 0
    #                 for y in poss_cans:
    #                     if x in y:
    #                         num += 1
    #                 if num == len(poss_cans) and num != 0:
    #                     self.changeState(x[0], x[1], newBoard)
    #                     self.climbB()

    #         # col
    #         cans = []
    #         for j in range(1, n):
    #             if newBoard[j][i] == 'can':
    #                 cans.append([j, i])
    #         if newBoard[0][i] <= len(cans):
    #             poss_cans = iterlist(cans, newBoard[0][i])
    #             poss_cans = [q for q in poss_cans if self.climbCheckNum(q, 'i')]
    #             for x in cans:
    #                 num = 0
    #                 for y in poss_cans:
    #                     if x in y:
    #                         num += 1
    #                 if num == len(poss_cans) and num != 0:
    #                     self.changeState(x[0], x[1], newBoard)
    #                     self.climbB()

    #     if self.isSameLevel(newBoard, self.board) == False:
    #         return newBoard
    #     return self.board

    def climbA(self):
        for i in range(1, n):
            for j in range(1, n):
                if self.board[i][j] == 'tree':
                    for x in self.nextTo(i, j):
                        if self.board[x[0]][x[1]] != 'tree':
                            self.board[x[0]][x[1]] = 'can'

    def climbB(self):
        for i in range(1, n):
            if self.board[0][i] == 0:
                for a in range(1, n):
                    if self.board[a][i] == 'can':
                        self.board[a][i] = 'not'
            if self.board[i][0] == 0:
                for a in range(1, n):
                    if self.board[i][a] == 'can':
                        self.board[i][a] = 'not'

    def changeState(self, i, j, currentBoard):
        currentBoard[i][j] = 'tent'
        currentBoard[i][0] -= 1
        currentBoard[0][j] -= 1
        tnextTo = self.total_nextTo(i, j)
        for x in tnextTo:
            if currentBoard[x[0]][x[1]] == 'can':
                currentBoard[x[0]][x[1]] = 'not'

    def climbC(self):
        for i in range(1, n):
            row = 0
            col = 0
            for j in range(1, n):
                if self.board[i][j] == 'can':
                    row += 1
                if self.board[j][i] == 'can':
                    col += 1
            if row == self.board[i][0]:
                for j in range(1, n):
                    if self.board[i][j] == 'can':
                        self.changeState(i, j, self.board)
            if col == self.board[0][i]:
                for j in range(1, n):
                    if self.board[j][i] == 'can':
                        self.changeState(j, i, self.board)

    def reState(self):
        newBoard = self.duplicatedBoard(self.board)
        count = 0
        for i in range(1, n):
            for j in range(1, n):
                if newBoard[i][j] == 'can' and (newBoard[i][0] == 0 or newBoard[0][j] == 0):
                    newBoard[i][j] = 'not'
                    count += 1
        if count == 0:
            return False
        else:
            return newBoard

    # def climbA(self):
    #     for i in range(1, n):
    #         for j in range(1, n):
    #             if self.board[i][j] == 'tree':
    #                 for x in self.nextTo(i, j):
    #                     if self.board[x[0]][x[1]] != 'tree':
    #                         self.board[x[0]][x[1]] = 'can'

    # def climbB(self):
    #     for i in range(1, n):
    #         if self.board[0][i] == 0:
    #             for a in range(1, n):
    #                 if self.board[a][i] == 'can':
    #                     self.board[a][i] = 'not'
    #         if self.board[i][0] == 0:
    #             for a in range(1, n):
    #                 if self.board[i][a] == 'can':
    #                     self.board[i][a] = 'not'

    def reStateLoop(self):
        while self.reState() != False:
            self.board = self.reState()

    def isSameLevel(self, a, b):
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

    def checkConstraint(self, newBoard):
        flag = True

        for i in range(1, n):
            row_num = newBoard[i][0]
            can_row = 0
            col_num = newBoard[0][i]
            can_col = 0

            for j in range(1, n):
                if newBoard[i][j] == 'can':
                    can_row += 1
                if newBoard[j][i] == 'can':
                    can_col += 1

                if newBoard[i][j] == 'tent':
                    tnextTo = self.total_nextTo(i, j)
                    for x in tnextTo:
                        if newBoard[x[0]][x[1]] == 'tent':
                            flag = False

            if row_num != can_row or col_num != can_col or row_num != 0 or col_num != 0:
                flag = False

        return flag

    def climbFact(self, n):
        res = 1
        for i in range(n, 1, -1):
            res *= i
        return res

    def climbCheckNum(self, lst, key):
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

    def stepUp(self):
        newBoard = self.duplicatedBoard(self.board)
        for i in range(1, n):
            # row
            cans = []
            for j in range(1, n):
                if newBoard[i][j] == 'can':
                    cans.append([i, j])
            if newBoard[i][0] <= len(cans):
                poss_cans = iterlist(cans, newBoard[i][0])
                poss_cans = [q for q in poss_cans if self.climbCheckNum(q, 'j')]
                for x in cans:
                    num = 0
                    for y in poss_cans:
                        if x in y:
                            num += 1
                    if num == len(poss_cans) and num != 0:
                        self.changeState(x[0], x[1], newBoard)
                        self.climbB()

            # col
            cans = []
            for j in range(1, n):
                if newBoard[j][i] == 'can':
                    cans.append([j, i])
            if newBoard[0][i] <= len(cans):
                poss_cans = iterlist(cans, newBoard[0][i])
                poss_cans = [q for q in poss_cans if self.climbCheckNum(q, 'i')]
                for x in cans:
                    num = 0
                    for y in poss_cans:
                        if x in y:
                            num += 1
                    if num == len(poss_cans) and num != 0:
                        self.changeState(x[0], x[1], newBoard)
                        self.climbB()

        if self.isSameLevel(newBoard, self.board) == False:
            return newBoard
        return self.board

    def check_all_cell(self):
        newBoard = self.duplicatedBoard(self.board)
        all_ways = []
        for i in range(1, n):
            all_cans = []
            for j in range(1, n):
                if newBoard[i][j] == 'can':
                    all_cans.append([i, j])
            if all_cans != []:
                iter_cans = iterlist(all_cans, newBoard[i][0])
                all_ways.append(iter_cans)
        all_ways_product = [list(i) for i in product(*all_ways)]
        for i in all_ways_product:
            flag = True
            for j in i:
                if self.climbCheckNum(j, 'j') == False:
                    flag = False
                    break
            if flag == True:
                temp = self.duplicatedBoard(newBoard)
                for x in list(chain.from_iterable(i)):
                    self.changeState(x[0], x[1], temp)
                if self.checkConstraint(temp) == True:
                    newBoard = temp
                    break
        return newBoard

    def create_dots(self):
        for i in range(1, n):
            for j in range(1, n):
                if self.board[i][j] == 'tree':
                    self.dots[(i, j)] = self.nextTo(i, j)

    def accept_dots(self):
        for key, value in self.dots.items():
            if value[0]!=True:
                value_text = [self.board[x[0]][x[1]] for x in value]
                count_tent = 0
                count_can = 0
                count_nt = 0
                for x in value_text:
                    if x == 'tent':
                        count_tent += 1
                    elif x == 'can':
                        count_can += 1
                    elif x == 'not':
                        count_nt += 1
                if count_tent == 1:
                    for j in value:
                        if self.board[j[0]][j[1]] == 'tent':
                            self.dots[key] = [True, j]
                            break
                if count_can == 1 and count_tent == 0:
                    for j in value:
                        if self.board[j[0]][j[1]] == 'can':
                            self.dots[key] = [True, j]
                            self.changeState(j[0], j[1], self.board)
                            break
                for item in value:
                    if self.board[item[0]][item[1]] == 'tent':
                        count = 0
                        for x in self.nextTo(item[0], item[1]):
                            if self.board[x[0]][x[1]] == 'tree':
                                count += 1
                        if count == 1:
                            for x in self.nextTo(item[0], item[1]):
                                if self.board[x[0]][x[1]] == 'tree':
                                    self.dots[(x[0], x[1])] = [True, item]
                                    break
            
    def accept_dots_loop(self):
        pre_newBoard = self.duplicatedBoard(self.board)
        while True:
            self.accept_dots()
            if self.isSameLevel(pre_newBoard, self.board) == True:
                break
            pre_newBoard = self.duplicatedBoard(self.board)

    def check_zero_col_row(self, currentBoard):
        newBoard = self.duplicatedBoard(currentBoard)
        for i in range(1, n):
            row = 0; col = 0
            for x in range(1, n):
                if newBoard[i][x]=='can':
                    row += 1
                if newBoard[x][i]=='can':
                    col += 1
            if newBoard[i][0] > row:
                return True
            if newBoard[0][i] > col:
                return True
        return False

    def fill(self):
        for i in range(1, n):
            for j in range(1, n):
                if self.board[i][j]=='can':
                    temp = self.duplicatedBoard(self.board)
                    self.changeState(i, j, temp)
                    if self.check_zero_col_row(temp)==True:
                        self.board[i][j] = 'not'

    def solver(self):
        t = time.time()
        timeFact = 0.999999664526756462
        self.climbA()
        self.climbB()
        self.create_dots()
        self.climbC()
        pre_newBoard = self.duplicatedBoard(self.board)
        counter = 0
        while True:
            counter += 1
            self.board = self.stepUp()
            self.climbB()
            self.climbC()
            self.accept_dots_loop()
            self.fill()
            self.reStateLoop()
            if self.isSameLevel(pre_newBoard, self.board) == True:
                break
            pre_newBoard = self.duplicatedBoard(self.board)
        print('Time spent:', (time.time()-t)*timeFact, 'seconds')
        memFact = 1.000006666666667
        process = psutil.Process(os.getpid())
        print('Memory spent: ', int((process.memory_info().rss)*memFact), 'bytes')
        display(self.board)
     
        if self.checkConstraint(self.board)==False:
            if input('solution not found').lower()=='y':
                t = time.time()
                self.board = self.check_all_cell()
                display(self.board)
                print('time spent:', int(time.time()-t), 'seconds')

p1 = hillClimbing(board)
p1.solver()
