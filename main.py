import curses
import random
import time


def createfield():
    field = []
    for l in range(50):
        field.append([])
        for c in range(50):
            field[l].append(0)


def drawfield(field):
    for line in range(len(field)):
        for column in range(len(field[line])):
            print(field[line][column], end='')

mainscreen = curses.initscr()

mainscreen.border(0)
mainscreen.addstr(5, 45, "Snake v1.0")
mainscreen.refresh()
mainscreen.getch()

starttime = time.time()
while True:
    print("tick")
    time.sleep(0.3)
    mainscreen.refresh()


mainscreen.getch()

curses.endwin()
