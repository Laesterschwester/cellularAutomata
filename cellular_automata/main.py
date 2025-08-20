from curses import wrapper
import curses
import conways_gol
import time

ON = "⚪"  # "⬜"
OFF = "⚫"  # "⬛"


def draw_screen(game_state, mouse_position, stdscr):
    mouse_position[0] = mouse_position[0] // 2
    max_yx = stdscr.getmaxyx()
    for y in range(len(game_state)):
        for x in range(len(game_state[0])):
            # cant addstr bottom right cell
            if y + 1 == max_yx[0] and (x + 1) * 2 >= max_yx[1]:
                if game_state[y][x]:
                    stdscr.insnstr(y, x * 2, ON, 2)
                else:
                    stdscr.insnstr(y, x * 2, OFF, 2)
            else:
                if game_state[y][x]:
                    stdscr.addstr(y, x * 2, ON)
                else:
                    stdscr.addstr(y, x * 2, OFF)


def toggle_block(game_board, mouse_position):
    pos = mouse_pos_to_arr_pos(mouse_position)
    game_board[pos[0]][pos[1]] = not game_board[pos[0]][pos[1]]


def mouse_pos_to_arr_pos(mouse_position):
    return [mouse_position[1], mouse_position[0] // 2]


def init_game_state(cols, rows, prev_game_state=None):
    game_state = [[False for x in range(cols // 2)] for y in range(rows)]
    if not prev_game_state:
        return game_state

    rows = min(len(prev_game_state), len(game_state))
    cols = min(len(prev_game_state[0]), len(game_state[0]))
    for row in range(rows):
        for col in range(cols):
            game_state[row][col] = prev_game_state[row][col]
    return game_state


def main(stdscr):
    curses.mouseinterval(0)
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    print("\033[?1003h\n")
    stdscr.nodelay(True)
    rows, cols = stdscr.getmaxyx()

    mouse_position = [0, 0]
    game_state = init_game_state(cols, rows)
    paused = True
    looping_borders = True
    time_between_frames = 0.2

    last_time = time.perf_counter()
    dtime = 0

    while True:
        key = stdscr.getch()

        if key == curses.KEY_RESIZE:
            rows, cols = stdscr.getmaxyx()
            game_state = init_game_state(cols, rows, game_state)
            pass

        # escape
        if key == 27:
            quit()

        if key == ord("c"):
            rows, cols = stdscr.getmaxyx()
            game_state = init_game_state(cols, rows)

        if key == curses.KEY_MOUSE:
            try:
                event = curses.getmouse()
                mouse_position = [event[1], event[2]]

                if (
                    event[4] & curses.BUTTON1_PRESSED
                    or event[4] & curses.BUTTON1_CLICKED
                ):
                    toggle_block(game_state, mouse_position)
            except curses.error:
                pass

        if key == ord(" "):
            paused = not paused

        current_time = time.perf_counter()
        dtime = current_time - last_time
        if (not paused) and dtime > time_between_frames:
            last_time = current_time
            game_state = conways_gol.update_conways_gol(game_state, looping_borders)

        draw_screen(game_state, mouse_position, stdscr)

        stdscr.refresh()


wrapper(main)
