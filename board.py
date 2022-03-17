# nt : not-tent, the places that is impossible to be tent
# cbt : can-be-tent, the places that can be tent

# getting the board's name
f = open('testname.txt')
filename = f.read().strip()
f.close()

# checking if the given name is wrong
try:
    # getting the board
    f = open(f'tests/{filename}')
    file = f.readlines()
    f.close()
    board = [i.strip().split() for i in file]
    n = len(board)
    board[0][0] = ''
    for i in range(1, n):
        board[0][i] = int(board[0][i])
        board[i][0] = int(board[i][0])
        for j in range(1, n):
            if board[i][j]=='a':
                board[i][j] = 'tr'
            if board[i][j]=='b':
                board[i][j] = 'nt'

except FileNotFoundError:
    print('\nERROR: there is no file called', filename[0:-4])
    input('\npress enter...')

