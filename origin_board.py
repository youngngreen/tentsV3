# getting the origin_board's name
f = open('testname.txt')
filename = f.read().strip()
f.close()

# checking if the given name is wrong
try:
    # getting the origin_board
    f = open(f'tests/{filename}')
    file = f.readlines()
    f.close()
    origin_board = [i.strip().split() for i in file]
    origin_board[0][0] = ''

except FileNotFoundError:
    print('\nERROR: there is no file called', filename[0:-4])
    input('\npress enter...')

