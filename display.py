from board import *
from origin_board import *

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
gra = (153, 255, 153)
grey = (100, 100, 100)

EMPTY = 0
GRASS = 1
TENT = 2
TREE = 3


def display(Board):

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

    board_size = len(Board[0])

    width, height = main_resolution
    offset = 50
    margin = 4
    cell_size = int((width - 2 * offset - (board_size - 1) * margin) / board_size)
    step = cell_size + 5
    font = pygame.font.SysFont("ubuntumono", cell_size)

    coord_x = offset

    for y in range(board_size):
        coord_y = offset
        for x in range(board_size):
            cell = pygame.Rect(coord_x, coord_y, cell_size, cell_size)

            if Board[x][y] == 'not':
                pygame.draw.rect(window, gra, cell)
            elif Board[x][y] == 'tree':
                window.blit(scale(tree_img, (cell_size, cell_size)), cell)
            elif Board[x][y] == 'tent':
                window.blit(scale(tent_img, (cell_size, cell_size)), cell)
            else:
                text = font.render(str(origin_board[x][y]), True, black)
                window.blit(text, cell)
            coord_y += step
        coord_x += step

    for x in range(offset + step, height - offset, step):
        for y in range(offset + step, width - offset, step):
            cell = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, grey, cell, 2)

    start = offset + (cell_size // 4)
    stop = height - cell_size

    pygame.display.flip() 

    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    launched = False
        time.sleep(0.1)