# prints the board very properly
from board import *

import os
import time

import pygame
from pygame.transform import scale

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

main_resolution = (500, 500)
green = (63, 224, 87)
black = (14, 15, 18)
white = (255, 255, 255)
red = (255, 0, 0)
gra = (153, 255, 153) # grass
grey = (100, 100, 100)

EMPTY = 0
GRASS = 1
TENT = 2
TREE = 3

##############################################

def printer(Board):
    # print()
    # for i in range(n):
    #     if i==0:
    #         print('empty  ', end='')
    #     else:
    #         if i<10:
    #             print(' '+str(i), end='    ')
    #         else:
    #             print(' '+str(i), end='   ')
    # print()
    # for i in range(1, n):
    #     if i<10:
    #         print('  '+str(i), end='    ')
    #     else:
    #         print('  '+str(i), end='   ')

    #     for j in range(1, len(Board[i])):
    #         if Board[i][j]=='tr' or Board[i][j]=='nt':
    #             print(' '+Board[i][j], end='   ')
    #         elif Board[i][j]=='cbt':
    #             print(Board[i][j], end='   ')
    #         else: # tents
    #             print(Board[i][j], end='  ')
    #     print()
    # print()

##############################################

################## try to display input

    pygame.init()
    window = pygame.display.set_mode(main_resolution)
    pygame.display.set_caption('TENTS')
    window.fill(white)

    tent_img = pygame.image.load(
        os.path.join("assets", "tent.png")
    ).convert()
    tree_img = pygame.image.load(
        os.path.join("assets", "tree.png")
    ).convert()

    num_img = pygame.image.load(
        os.path.join("assets", "num.png")
    ).convert()


    grid_size = len(Board[0])
    width, height = main_resolution
    offset = 50
    margin = 4
    cell_size = int((width - 2 * offset - (grid_size - 1) * margin) / grid_size)
    step = cell_size + 5
    font = pygame.font.SysFont("ubuntumono", cell_size // 2)

    # Draw cells colors
    coord_x = offset
    for y in range(grid_size):
        coord_y = offset
        for x in range(grid_size):
            cell = pygame.Rect(coord_x, coord_y, cell_size, cell_size)
            if Board[x][y] == 'nt':
                pygame.draw.rect(window, gra, cell)
            elif Board[x][y] == 'tr':
                window.blit(scale(tree_img, (cell_size, cell_size)), cell)
            elif Board[x][y] == 'cbt':
                window.blit(scale(num_img, (cell_size, cell_size)), cell)
            else: # tents
                window.blit(scale(tent_img, (cell_size, cell_size)), cell)
            coord_y += step
        coord_x += step

    # Draw cells borders
    for x in range(offset, height - offset, step):
        for y in range(offset, width - offset, step):
            cell = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, grey, cell, 2)

    start = offset + (cell_size // 4)
    stop = height - cell_size

    # # Display row constraints
    # for y, row_constraint in zip(
    #     range(start, stop, step), row_constraints
    # ):
    #     text = font.render(str(row_constraint), True, black)
    #     window.blit(text, [offset - 2 * text.get_width(), y])

    # start = offset + (cell_size // 3)
    # stop = width - cell_size
    # # Display col constraints
    # for x, col_constraint in zip(
    #     range(start, stop, step), col_constraints
    # ):
    #     text = font.render(str(col_constraint), True, black)
    #     self.window.blit(text, [x, offset - text.get_height()])



    pygame.display.flip()  # Refresh display

    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    launched = False
        time.sleep(0.1)
