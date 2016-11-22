import curses
from curses import wrapper
import random
import time
import os
import unicodedata


def starting_coords():
    l = random.randrange(3, 8)
    c = random.randrange(1, 10)
    return [l, c]


def createfield():
    field = []
    for l in range(30):
        field.append([])
        for c in range(30):
            field[l].append(0)
    return field


def drawfield(field):
    for line in range(len(field)):
        gamewindow.addstr("\n")
        for column in range(len(field[line])):
            if field[line][column] == 0:
                gamewindow.addstr("{0:^{1}}".format(" ", 2))
            elif field[line][column] < 10:
                # gamewindow.addstr("■")
                gamewindow.addstr("{0:^{1}}".format("■", 2))
            else:
                gamewindow.addstr("{0:^{1}}".format("■", 2))
            gamewindow.noutrefresh()


def snake_placement(field, l, c, over=False):
    snakelength = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    if over:
        field[l][c] = snakelength[0]
        return
    for i in range(len(snakelength)):
        field[l - i][c] = snakelength[i]


def movement_vert(field, l, c, orient):
    if l == 29:
        l = -1
        snake_placement(field, l, c, True)
    elif l == -1:
        l = 29
        snake_placement(field, l, c, True)

    field[l + orient][c] = field[l][c] + 1  # places the head at its proper place
    for line in range(len(field)):
        for column in range(len(field[line])):
            if field[line][column] != 0:
                field[line][column] -= 1
    return [l + orient, c]


def movement_hori(field, l, c, orient):
    if c == 29:
        c = -1
        snake_placement(field, l, c, True)
    elif c == -1:
        c = 29
        snake_placement(field, l, c, True)

    field[l][c + orient] = field[l][c] + 1  # places the head at its proper place

    for line in range(len(field)):
        for column in range(len(field[line])):
            if field[line][column] != 0:
                field[line][column] -= 1
    return [l, c + orient]


def automove(field, current_position, current_orient):
    if current_orient == "up":
        current_position = movement_vert(field, current_position[0], current_position[1], -1)
    elif current_orient == "down":
        current_position = movement_vert(field, current_position[0], current_position[1], 1)
    elif current_orient == "left":
        current_position = movement_hori(field, current_position[0], current_position[1], -1)
    elif current_orient == "right":
        current_position = movement_hori(field, current_position[0], current_position[1], 1)
    return current_position


def main(mainscreen):
    current_orient = "down"
    field = createfield()

    current_position = starting_coords()
    snake_placement(field, current_position[0], current_position[1])

    starttime = time.time()

    curses.cbreak()
    gamewindow.keypad(1)
    key = ""

    try:
        while True:
            gamewindow.nodelay(1)
            key = gamewindow.getch()
            if key == curses.KEY_UP:
                current_position = movement_vert(field, current_position[0], current_position[1], -1)
                current_orient = "up"
            elif key == curses.KEY_DOWN:
                current_position = movement_vert(field, current_position[0], current_position[1], 1)
                current_orient = "down"
            elif key == curses.KEY_LEFT:
                current_position = movement_hori(field, current_position[0], current_position[1], -1)
                current_orient = "left"
            elif key == curses.KEY_RIGHT:
                current_position = movement_hori(field, current_position[0], current_position[1], 1)
                current_orient = "right"
            else:
                current_position = automove(field, current_position, current_orient)

            gamewindow.clear()
            drawfield(field)
            time.sleep(0.1)
            gamewindow.refresh()
    except IndexError:
        curses.endwin()
    mainscreen.refresh()
    curses.endwin()

mainscreen = curses.initscr()
gamewindow = curses.newwin(70, 70, 6, 54)
wrapper(main)
