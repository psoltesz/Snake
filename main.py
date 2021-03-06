import curses
from curses import *
import random
import time
import os


def starting_coords():
    l = random.randrange(4, 27)
    c = random.randrange(1, 30)
    return [l, c]


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
                gamewindow.addstr("{0:^{1}}".format("🍍", 2), color_pair(3) + A_BOLD)
            elif field[line][column] == 902:
                gamewindow.addstr("{0:^{1}}".format("🍌", 2), color_pair(3) + A_BOLD)
            elif field[line][column] == 903:
                gamewindow.addstr("{0:^{1}}".format("🍎", 2), color_pair(3) + A_BOLD)
            elif field[line][column] == 904:
                gamewindow.addstr("{0:^{1}}".format("🍒", 2), color_pair(3) + A_BOLD)
            elif field[line][column] == 905:
                gamewindow.addstr("{0:^{1}}".format("🐹", 2), color_pair(3) + A_BOLD)
            elif type(field[line][column]) == int and field[line][column] < snake_head:
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(1))  # snake body
            elif field[line][column] == "tb" or field[line][column] == "lb" or field[line][column] == "bb" or field[line][column] == "rb":
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(4))  # borders
            else:
                gamewindow.addstr("{0:^{1}}".format("■", 2), color_pair(2))  # snake head
            gamewindow.noutrefresh()


def draw_snakehead():
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
                  "\n",
                  '''                              Press ENTER to start!''']
    return snake_list


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
    food = [901, 902, 903, 904, 905]
    for line in range(1, 31):
        for column in range(1, 31):
            if field[line][column] != 0 and field[line][column] not in food:
                field[line][column] -= 1
    return field


def food_placement(field):
    while True:
        l = random.randrange(1, 30)
        c = random.randrange(1, 30)
        if field[l][c] == 0:
            food = random.randrange(901, 906)
            field[l][c] = food  # food counter will be a random unit between 901 and 905
            return field
        else:
            continue


def hungerbar_full():
    hungerbar = [0] * 40
    return hungerbar


def hunger_decrease(hungerbar):
    del hungerbar[0]
    if len(hungerbar) == 0:
        while True:
            gamewindow.clear()
            gameover.border(0)
            gameover.addstr(19, 30, "GAME OVER", color_pair(5) + A_BOLD)
            gameover.refresh()
    return hungerbar


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


def score_increase_vert(field, l_mod, c):
    if field[l_mod][c] == 901:
        return 50
    elif field[l_mod][c] == 902:
        return 100
    elif field[l_mod][c] == 903:
        return 150
    elif field[l_mod][c] == 904:
        return 200
    elif field[l_mod][c] == 905:
        return 250


def score_increase_hori(field, l, c_mod):
    if field[l][c_mod] == 901:
        return 50
    elif field[l][c_mod] == 902:
        return 100
    elif field[l][c_mod] == 903:
        return 150
    elif field[l][c_mod] == 904:
        return 200
    elif field[l][c_mod] == 905:
        return 250


def movement_vert(field, l, c, direction, current_orientation, correct_key):
    global food_counter
    global score
    global hunger
    food = [901, 902, 903, 904, 905]
    head = field[l][c]
    l_mod = wall_check_vert(l, current_orientation, correct_key)
    if l != l_mod:  # if a wall pass happens
        if field[l_mod][c] in food:  # if there is food at the edge of the field
            # pulling the score amount from the score_increase function
            score_increase = score_increase_vert(field, l_mod, c)
            score = score + score_increase  # setting the score to the desired amount
            field[l_mod][c] = head + 1
            snakelength.insert(0, head + 1)
            field = food_placement(field)
            food_counter += 1
            hunger = hungerbar_full()
            return [l_mod, c]
        else:  # if there is no food at the edge
            field[l_mod][c] = head + 1
            field = slither(field)
            return [l_mod, c]
    elif field[l + direction][c] in food:
        # pulling the score amount from the score_increase function
        score_increase = score_increase_vert(field, l + direction, c)
        score = score + score_increase  # setting the score to the desired amount
        field[l + direction][c] = head + 1
        snakelength.insert(0, head + 1)
        field = food_placement(field)
        food_counter += 1
        hunger = hungerbar_full()
        return [l + direction, c]
    else:
        field[l + direction][c] = head + 1  # places the head at its proper place
        field = slither(field)
        return [l + direction, c]


def movement_hori(field, l, c, direction, current_orientation, correct_key):
    global food_counter
    global score
    global hunger
    food = [901, 902, 903, 904, 905]
    head = field[l][c]
    c_mod = wall_check_hori(c, current_orientation, correct_key)
    if c != c_mod:
        if field[l][c_mod] in food:
            # pulling the score amount from the score_increase function
            score_increase = score_increase_hori(field, l, c_mod)
            score = score + score_increase  # setting the score to the desired amount
            field[l][c_mod] = head + 1
            snakelength.insert(0, head + 1)
            field = food_placement(field)
            food_counter += 1
            hunger = hungerbar_full()
            return [l, c_mod]
        else:
            field[l][c_mod] = head + 1
            field = slither(field)
            return [l, c_mod]
    elif field[l][c + direction] in food:
        # pulling the score amount from the score_increase function
        score_increase = score_increase_vert(field, l, c + direction)
        score = score + score_increase  # setting the score to the desired amount
        field[l][c + direction] = head + 1
        snakelength.insert(0, head + 1)
        field = food_placement(field)
        food_counter += 1
        hunger = hungerbar_full()
        return [l, c + direction]
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


def controls(field, correct_key, current_position, current_orientation):
    if correct_key == curses.KEY_UP and current_orientation != "down":
        current_position = movement_vert(field, current_position[0], current_position[
            1], -1, current_orientation, correct_key)
        current_orientation = "up"
        return [field, correct_key, current_position, current_orientation]
    elif correct_key == curses.KEY_DOWN and current_orientation != "up":
        current_position = movement_vert(field, current_position[0], current_position[
            1], 1, current_orientation, correct_key)
        current_orientation = "down"
        return [field, correct_key, current_position, current_orientation]
    elif correct_key == curses.KEY_LEFT and current_orientation != "right":
        current_position = movement_hori(field, current_position[0], current_position[
            1], -1, current_orientation, correct_key)
        current_orientation = "left"
        return [field, correct_key, current_position, current_orientation]
    elif correct_key == curses.KEY_RIGHT and current_orientation != "left":
        current_position = movement_hori(field, current_position[0], current_position[
            1], 1, current_orientation, correct_key)
        current_orientation = "right"
        return [field, correct_key, current_position, current_orientation]
    else:
        current_position = automove(field, current_position, current_orientation, correct_key)
        return [field, correct_key, current_position, current_orientation]


def menu_window(menu):
    curses.cbreak()
    menu.keypad(1)
    entering_key = ""
    snake_list = draw_snakehead()
    drawmenu(snake_list, menu)
    entering_key = menu.getch()
    if entering_key == curses.KEY_ENTER:
        menu = curses.endwin()


def speed_increase(food_counter, speed, done_this_round):
    if food_counter % 10 == 0 and done_this_round == 0:
        speed *= 0.95
        done_this_round = 1
    elif food_counter % 10 != 0:
        done_this_round = 0
    return [food_counter, speed, done_this_round]


def draw_score_window(hunger):
    scorewindow.border()
    #scorewindow.addstr("Speed: %s\n" % round(speed, 3))
    scorewindow.addstr(1, 1, "Score: %s\n" % score, color_pair(5) + A_BOLD)
    scorewindow.addstr(2, 1, "Length: %s\n" % food_counter, color_pair(5) + A_BOLD)
    scorewindow.addstr(3, 1, "Hunger: ", color_pair(5) + A_BOLD)
    for item in range(len(hunger)):
        scorewindow.addstr("{0:{1}}".format("■", 1), color_pair(5) + A_BOLD)


def main(mainscreen):
    global food_counter
    global speed
    global hunger
    # Define colors
    start_color()
    use_default_colors()
    init_pair(1, COLOR_CYAN, -1)
    init_pair(2, COLOR_GREEN, -1)
    init_pair(3, COLOR_YELLOW, -1)
    init_pair(4, COLOR_BLACK, COLOR_WHITE)
    init_pair(5, COLOR_WHITE, -1)

    current_orientation = "down"
    field = createfield()
    field = food_placement(field)
    done_this_round = 0

    current_position = starting_coords()
    snake_placement(field, current_position[0], current_position[1])

    starttime = time.time()

    try:
        curses.curs_set(0)
        menu_window(menu)
        menu.clear()
        menu.refresh()

        while True:
            curses.cbreak()
            gamewindow.keypad(1)
            gamewindow.nodelay(1)
            key = -1
            correct_key = ""
            time.sleep(speed)
            key = gamewindow.getch()
            correct_key = key
            # Get the latest key from the user
            while True:
                key = gamewindow.getch()
                if key == -1:
                    break
                correct_key = key
            # Controlling
            controls_return = controls(field, correct_key, current_position, current_orientation)
            field = controls_return[0]
            correct_key = controls_return[1]
            current_position = controls_return[2]
            current_orientation = controls_return[3]
            gamewindow.clear()
            drawfield(field, snakelength[0])
            draw_score_window(hunger)
            gamewindow.refresh()
            scorewindow.refresh()
            scorewindow.clear()

            result = speed_increase(food_counter, speed, done_this_round)
            food_counter = result[0]
            speed = result[1]
            done_this_round = result[2]
            hunger = hunger_decrease(hunger)
    except IndexError:
        curses.endwin()
        print(current_orientation, current_position)
        raise
    mainscreen.refresh()
    curses.endwin()


snakelength = [3, 2, 1]
food_counter = 3
score = 0
speed = 0.16
hunger = hungerbar_full()
mainscreen = curses.initscr()
menu = curses.newwin(50, 70, 6, 30)  # Create Menu window
scorewindow = curses.newwin(5, 64, 1, 41)  # Score window
gamewindow = curses.newwin(40, 80, 5, 41)  # Create Game window
gameover = curses.newwin(40, 70, 1, 40)
wrapper(main)
