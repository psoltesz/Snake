import curses
from curses import wrapper
import random
import time
import os


def starting_coords():
    l = random.randrange(3, 8)
    c = random.randrange(1, 10)
    return [l, c]


def createfield():
    field = []
    for l in range(10):
        field.append([])
        for c in range(10):
            field[l].append(0)
    return field


def drawfield(field):
    for line in range(len(field)):
        mainscreen.addstr("\n")
        for column in range(len(field[line])):
            mainscreen.addstr(str(field[line][column]))
    mainscreen.refresh()


def snake_placement(field, l, c):
    snakelength = [3, 2, 1]
    for i in range(len(snakelength)):
        field[l - i][c] = snakelength[i]


def movement(field, l, c):
    field[l + 1][c] = field[l][c] + 1  # places the head at its proper place

    for line in range(len(field)):
        for column in range(len(field[line])):
            if field[line][column] != 0:
                field[line][column] -= 1
    return [l + 1, c]


def main(mainscreen):

    field = createfield()

    current_position = starting_coords()
    snake_placement(field, current_position[0], current_position[1])

    starttime = time.time()
    while True:
        mainscreen.clear()
        current_position = movement(field, current_position[0], current_position[1])
        drawfield(field)
        time.sleep(0.5)
        mainscreen.refresh()

    mainscreen.refresh()
    curses.endwin()

mainscreen = curses.initscr()
wrapper(main)
