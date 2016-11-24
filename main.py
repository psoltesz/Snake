import curses
from curses import *
import random
import time
import os


def starting_coords():
    l = random.randrange(4, 27)
    c = random.randrange(2, 30)
    return [l, c]


def food_coords_generator():
    food_l = random.randrange(1, 30)
    food_c = random.randrange(1, 30)
    return [food_l, food_c]


def food_placement(field, l, c):
    while True:
        if field[l][c] == 0:
            field[l][c] = 901  # food counter will be 901
            return field
        else:
            food_coords = food_coords_generator()


def createfield():
    field = []
    first_line = []
    for i in range(32):
        first_line.append("tb")

    field.append(first_line)

    for l in range(1, 31):
        field.append([])
        for c in range(30):
            field[l].append(0)

    for l in range(1, 31):
        field[l].insert(0, "lb")
        field[l].append("rb")

    last_line = []
    for i in range(32):
        last_line.append("bb")
    field.append(last_line)

    return field


def drawfield(field, snake_head):
    for line in range(len(field)):
        gamewindow.addstr("\n")
        for column in range(len(field[line])):
            if field[line][column] == 0:
                gamewindow.addstr("{0:^{1}}".format(" ", 2))
            elif field[line][column] == 901:
                gamewindow.addstr("{0:^{1}}".format("X", 2))
            elif type(field[line][column]) == int and field[line][column] < snake_head:
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(1))
                # gamewindow.addstr("{0:^{1}}".format(field[line][column], 2))
            elif field[line][column] == "tb" or field[line][column] == "lb" or field[line][column] == "bb" or field[line][column] == "rb":
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(4))
            else:
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(2))
                # gamewindow.addstr("{0:^{1}}".format(field[line][column], 2))
            gamewindow.noutrefresh()

    return snake_head


def drawmenu(snake_list, menu):
    for line in range(len(snake_list)):
        menu.addstr("\n")
        for i in range(len(snake_list[line])):
            menu.addstr(str(snake_list[line][i]), color_pair(2) + A_BOLD)


def snake_placement(field, l, c):
    snakelength = [3, 2, 1]
    for i in range(len(snakelength)):
        field[l - i][c] = snakelength[i]

    return snakelength[0]


def slither(field):
    for line in range(1, 31):
        for column in range(1, 31):
            if field[line][column] != 0 and field[line][column] != 901:
                field[line][column] -= 1
    return field


def wall_check_vert(l, current_orientation, correct_key):
    if current_orientation == "right" or current_orientation == "left":
        if l == 1 and correct_key == curses.KEY_UP:
            l = 30
            return l
        elif l == 30 and correct_key == curses.KEY_DOWN:
            l = 1
            return l
    elif current_orientation == "down" and l == 30:
        l = 1
        return l
    elif current_orientation == "up" and l == 1:
        l = 30
        return l
    return l


def wall_check_hori(c, current_orientation, correct_key):
    if current_orientation == "up" or current_orientation == "down":
        if c == 1 and correct_key == curses.KEY_LEFT:
            c = 30
            return c
        elif c == 30 and correct_key == curses.KEY_RIGHT:
            c = 1
            return c
    elif current_orientation == "right" and c == 30:
        c = 1
        return c
    elif current_orientation == "left" and c == 1:
        c = 30
        return c
    return c


def movement_vert(field, l, c, direction, current_orientation, correct_key):
    head = field[l][c]
    l_mod = wall_check_vert(l, current_orientation, correct_key)
    if l != l_mod:
        field[l_mod][c] = head + 1
        field = slither(field)
        return [l_mod, c]
    else:
        field[l + direction][c] = head + 1  # places the head at its proper place
        field = slither(field)
        return [l + direction, c]


def movement_hori(field, l, c, direction, current_orientation, correct_key):
    head = field[l][c]
    c_mod = wall_check_hori(c, current_orientation, correct_key)
    if c != c_mod:
        field[l][c_mod] = head + 1
        field = slither(field)
        return [l, c_mod]
    else:
        field[l][c + direction] = head + 1  # places the head at its proper place
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

    init_pair(1, COLOR_CYAN, -1)
    init_pair(2, COLOR_GREEN, -1)
    init_pair(3, COLOR_GREEN, -1)
    init_pair(4, COLOR_BLACK, COLOR_WHITE)

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
    food_coords = food_coords_generator()
    field = food_placement(field, food_coords[0], food_coords[1])

    current_position = starting_coords()
    snake_head = snake_placement(field, current_position[0], current_position[1])

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
            snake_head = drawfield(field, snake_head)
            gamewindow.refresh()
    except IndexError:
        curses.endwin()
        print(current_orientation, current_position)
        raise
    mainscreen.refresh()
    curses.endwin()

mainscreen = curses.initscr()
menu = curses.newwin(50, 70, 6, 30)
gamewindow = curses.newwin(40, 80, 5, 41)
wrapper(main)
