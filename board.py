f = open('testname.txt')
filename = f.read().strip()
f.close()

try:
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
                board[i][j] = 'tree'
            if board[i][j]=='b':
                board[i][j] = 'not'

except FileNotFoundError:
    print('\nERROR: No file: ', filename[0:-4])

