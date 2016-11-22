import curses
from curses import *
import random
import time
import os


def starting_coords():
    l = random.randrange(3, 28)
    c = random.randrange(1, 30)
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
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(3))
            else:
                gamewindow.addstr("{0:^{1}}".format("■", 2))
            gamewindow.noutrefresh()


def drawmenu(snake_list, menu):
    for line in range(len(snake_list)):
        menu.addstr("\n")
        for i in range(len(snake_list[line])):
            menu.addstr(str(snake_list[line][i]), color_pair(2) + A_BOLD)


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


def menu_things(snake_list, menu):
    curses.cbreak()
    menu.keypad(1)
    entering_key = ""

    drawmenu(snake_list, menu)
    entering_key = menu.getch()
    if entering_key == curses.KEY_ENTER:
        menu = curses.endwin()


def main(mainscreen):
    start_color()
    use_default_colors()

    init_pair(1, COLOR_RED, -1)
    init_pair(2, COLOR_GREEN, -1)

    snake_list = ['''                                                  .o@*hu''',
                  '''                          ..      .........   .u*"    ^Rc''',
                  '''                        oP""*Lo*#"""""""""""7d  .d*N.   $''',
                  '''                      S  u@""           .u*"  o*"  #   ?b''',
                  '''                      N   "                .d"  .C@      ?b.''',
                  '''                     A                    @*@me@#         '"Nu''',
                  '''                    K                                        .#b''',
                  '''                  .E                                           $r''',
                  '''                .X"                                  $L        $''',
                  '''              .S"                                   8"R      dP''',
                  '''           .N#"                                  .dP d"   .d#''',
                  '''          xA              .e                 .ud#"  dE.o@"(''',
                  '''          K             s*"              .u@*""     '""\dP"''',
                  '''          ?E  ..                    ..o@""        .$  uP''',
                  '''           #c:$"*u.             .u@*""$          uR .@"''',
                  '''            ?L$. '"""***Nc    x@""   @"         d" JP''',
                  '''             ^#$         #L  .$     8"         d" d"''',
                  '''               '          "b.'$    @"         $" 8"''',
                  '''                            "*@   $"         $  @''',
                  '''                           @    $"         d" 8''',
                  '''                           $$u.u$"         dF dF''',
                  '''                           $ """   ^      dP xR''',
                  '''                           $      dFNu...@"  $''',
                  '''                           "N..   ?B ^"""   :R''',
                  '''                             """"* RL       d>''',
                  '''                                    "$u.   .$''',
                  '''                                      ^"*bo@"''',
                  ''' \n ''',
                  '''                              Press ENTER to start!''']

    current_orient = "down"
    field = createfield()

    current_position = starting_coords()
    snake_placement(field, current_position[0], current_position[1])

    starttime = time.time()

    try:
        menu_things(snake_list, menu)
        menu.clear()
        menu.refresh()
        while True:
            gamewindow.border()
            curses.cbreak()
            gamewindow.keypad(1)
            key = ""
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
menu = curses.newwin(50, 70, 6, 30)
gamewindow = curses.newwin(31, 61, 6, 40)
wrapper(main)
