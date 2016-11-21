import curses
import random
import time
import os


def createfield():
    field = []
    for l in range(10):
        field.append([])
        for c in range(10):
            field[l].append(0)
    return field


def drawfield(field):
    for line in range(len(field)):
        print("\r")
        for column in range(len(field[line])):
            print("{0:^{1}}".format(field[line][column], 2), end="")


def snake_placement(l, c):
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

field = createfield()

snake_placement(3, 5)
current_position = [3, 5]

starttime = time.time()
while True:
    current_position = movement(field, current_position[0], current_position[1])
    drawfield(field)
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
