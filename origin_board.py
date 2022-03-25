f = open('testname.txt')
filename = f.read().strip()
f.close()

try:
    f = open(f'tests/{filename}')
    file = f.readlines()
    f.close()
    origin_board = [i.strip().split() for i in file]
    origin_board[0][0] = ''

except FileNotFoundError:
    print('\nERROR: No file: ', filename[0:-4])

