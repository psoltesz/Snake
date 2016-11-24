import curses
from curses import *
import random
import time
import os


def starting_coords():
    l = random.randrange(4, 27)
    c = random.randrange(2, 30)
    return [l, c]


def createfield():
    field = []
    first_line = []
    for i in range(30):
        first_line.append("tb")

    field.insert(0, first_line)

    for l in range(30):
        field.append([])
        for c in range(30):
            field[l].append(0)

    for l in range(1, 30):
        field[l].insert(0, "lb")
        field[l].insert(-1, "rb")

    last_line = []
    for i in range(30):
        last_line.append("bb")
    field.append(last_line)

    return field


def drawfield(field):
    for line in range(1, 30):
        gamewindow.addstr("\n")
        for column in range(1, 30):
            if field[line][column] == 0:
                gamewindow.addstr("{0:^{1}}".format(field[line][column], 2))
            elif field[line][column] < 10:
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(3))
                # gamewindow.addstr("{0:^{1}}".format(field[line][column], 2))
            elif field[line][column] == "tb" or field[line][column] == "lb" or field[line][column] == "bb" or field[line][column] == "rb":
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(1))
            else:
                gamewindow.addstr("{0:^{1}}".format("■", 2))
                # gamewindow.addstr("{0:^{1}}".format(field[line][column], 2))
            gamewindow.noutrefresh()


def drawmenu(snake_list, menu):
    for line in range(len(snake_list)):
        menu.addstr("\n")
        for i in range(len(snake_list[line])):
            menu.addstr(str(snake_list[line][i]), color_pair(2) + A_BOLD)


def snake_placement(field, l, c):
    snakelength = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    for i in range(len(snakelength)):
        field[l - i][c] = snakelength[i]


def slither(field):
    for line in range(1, 30):
        for column in range(1, 30):
            if field[line][column] != 0:
                field[line][column] -= 1
    return field


def wall_check_vert(l, current_orientation, correct_key):
    if current_orientation == "right" or current_orientation == "left":
        if l == 0 and correct_key == curses.KEY_UP:
            l = 29
            return l
        elif (l == 29 and correct_key == curses.KEY_DOWN):
            l = 0
            return l
    elif current_orientation == "down" and l == 29:
        l = 0
        return l
    elif current_orientation == "up" and l == 0:
        l = 29
        return l
    return l


def wall_check_hori(c, current_orientation, correct_key):
    if current_orientation == "up" or current_orientation == "down":
        if c == 0 and correct_key == curses.KEY_LEFT:
            c = 29
            return c
        elif c == 29 and correct_key == curses.KEY_RIGHT:
            c = 0
            return c
    elif current_orientation == "right" and c == 29:
        c = 0
        return c
    elif current_orientation == "left" and c == 0:
        c = 29
        return c
    return c


def movement_vert(field, l, c, direction, current_orientation, correct_key):
    head = field[l][c]
    l = wall_check_vert(l, current_orientation, correct_key)
    field[l][c] = head
    field[l + direction][c] = field[l][c] + 1  # places the head at its proper place
    field = slither(field)
    return [l + direction, c]


def movement_hori(field, l, c, direction, current_orientation, correct_key):
    head = field[l][c]
    c = wall_check_hori(c, current_orientation, correct_key)
    field[l][c] = head
    field[l][c + direction] = field[l][c] + 1  # places the head at its proper place
    field = slither(field)
    return [l, c + direction]


def automove(field, current_position, current_orientation, correct_key):
    if current_orientation == "up":
        current_position = movement_vert(field, current_position[0], current_position[
                                         1], -1, current_orientation, correct_key)
    elif current_orientation == "down":
        current_position = movement_vert(field, current_position[0], current_position[
                                         1], 1, current_orientation, correct_key)
    elif current_orientation == "left":
        current_position = movement_hori(field, current_position[0], current_position[
                                         1], -1, current_orientation, correct_key)
    elif current_orientation == "right":
        current_position = movement_hori(field, current_position[0], current_position[
                                         1], 1, current_orientation, correct_key)
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

    current_orientation = "down"
    field = createfield()

    current_position = starting_coords()
    snake_placement(field, current_position[0], current_position[1])

    starttime = time.time()

    try:
        curses.curs_set(0)
        menu_things(snake_list, menu)
        menu.clear()
        menu.refresh()

        while True:
            curses.cbreak()
            gamewindow.keypad(1)
            gamewindow.nodelay(1)
            key = -1
            correct_key = ""

            time.sleep(0.1)
            print(field)
            key = gamewindow.getch()
            correct_key = key
            while True:
                key = gamewindow.getch()
                if key == -1:
                    break
                correct_key = key

            if correct_key == curses.KEY_UP:
                current_position = movement_vert(field, current_position[0], current_position[
                    1], -1, current_orientation, correct_key)
                current_orientation = "up"
            elif correct_key == curses.KEY_DOWN:
                current_position = movement_vert(field, current_position[0], current_position[
                    1], 1, current_orientation, correct_key)
                current_orientation = "down"
            elif correct_key == curses.KEY_LEFT:
                current_position = movement_hori(field, current_position[0], current_position[
                    1], -1, current_orientation, correct_key)
                current_orientation = "left"
            elif correct_key == curses.KEY_RIGHT:
                current_position = movement_hori(field, current_position[0], current_position[
                    1], 1, current_orientation, correct_key)
                current_orientation = "right"
            else:
                current_position = automove(field, current_position, current_orientation, correct_key)
            gamewindow.clear()
            drawfield(field)
            gamewindow.refresh()
    except IndexError:
        curses.endwin()
        print(current_orientation, current_position)
        raise
    mainscreen.refresh()
    curses.endwin()

mainscreen = curses.initscr()
menu = curses.newwin(50, 70, 6, 30)
gamewindow = curses.newwin(32, 61, 6, 40)
wrapper(main)
