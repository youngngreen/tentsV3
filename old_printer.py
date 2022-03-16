# prints the board very properly
from board import *

##############################################

def printer(Board):
    print()
    for i in range(n):
        if i==0:
            print('empty  ', end='')
        else:
            if i<10:
                print(' '+str(i), end='    ')
            else:
                print(' '+str(i), end='   ')
    print()
    for i in range(1, n):
        if i<10:
            print('  '+str(i), end='    ')
        else:
            print('  '+str(i), end='   ')

        for j in range(1, len(Board[i])):
            if Board[i][j]=='tr' or Board[i][j]=='nt':
                print(' '+Board[i][j], end='   ')
            elif Board[i][j]=='cbt':
                print(Board[i][j], end='   ')
            else: # tents
                print(Board[i][j], end='  ')
        print()
    print()

