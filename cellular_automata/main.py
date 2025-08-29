from curses import wrapper
import curses
import conways_gol
import time
import signal
import sys

ON = "⚪"  # "⬜"
OFF = "⚫"  # "⬛"


def update_screen_partial(screen_dimensions, updated_cells, stdscr):
    rows, cols = screen_dimensions
    last_cell_yx = [rows - 1, cols]
    for cell in updated_cells:
        row, col, is_alive = cell
        state = ON if is_alive else OFF
        if row == last_cell_yx[0] and (col + 1) * 2 == last_cell_yx[1]:
            stdscr.insnstr(row, col * 2, state, 2)
        else:
            stdscr.addstr(row, col * 2, state)


def update_screen(screen_dimensions, game_state, mouse_position, stdscr):
    mouse_position[0] = mouse_position[0] // 2
    rows, cols = screen_dimensions
    for row in range(len(game_state)):
        for col in range(len(game_state[0])):
            # cant addstr bottom right cell
            if row + 1 == rows and (col + 1) * 2 >= cols:
                if game_state[row][col]:
                    stdscr.insnstr(row, col * 2, ON, 2)
                else:
                    stdscr.insnstr(row, col * 2, OFF, 2)
            else:
                if game_state[row][col]:
                    stdscr.addstr(row, col * 2, ON)
                else:
                    stdscr.addstr(row, col * 2, OFF)


def toggle_block(game_board, mouse_position):
    row, col = mouse_pos_to_arr_pos(mouse_position)
    game_board[row][col] = not game_board[row][col]
    return [row, col, game_board[row][col]]


def mouse_pos_to_arr_pos(mouse_position):
    return [mouse_position[1], mouse_position[0] // 2]


def init_game_state(screen_dimensions, prev_game_state=None):
    rows, cols = screen_dimensions
    game_state = [[False for x in range(cols // 2)] for y in range(rows)]
    if not prev_game_state:
        return game_state

    rows = min(len(prev_game_state), len(game_state))
    cols = min(len(prev_game_state[0]), len(game_state[0]))
    for row in range(rows):
        for col in range(cols):
            game_state[row][col] = prev_game_state[row][col]
    return game_state


def signal_handler(sig, frame):
    sys.exit()


def main(stdscr):
    curses.mouseinterval(0)
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    print("\033[?1003h\n")
    stdscr.nodelay(True)
    screen_dimensions = stdscr.getmaxyx()

    mouse_position = [0, 0]
    game_state = init_game_state(screen_dimensions)
    paused = True
    looping_borders = True
    time_between_frames = 0.2

    last_time = time.perf_counter()
    dtime = 0

    update_screen(screen_dimensions, game_state, mouse_position, stdscr)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        updated_cells = []

        key = stdscr.getch()

        if key == curses.KEY_RESIZE:
            screen_dimensions = stdscr.getmaxyx()
            game_state = init_game_state(screen_dimensions, game_state)
            update_screen(screen_dimensions, game_state, mouse_position, stdscr)

        # escape
        if key == 27:
            sys.exit()

        if key == ord("c"):
            game_state = init_game_state(screen_dimensions)
            update_screen(screen_dimensions, game_state, mouse_position, stdscr)

        if key == curses.KEY_MOUSE:
            try:
                event = curses.getmouse()
                mouse_position = [event[1], event[2]]

                if (
                    event[4] & curses.BUTTON1_PRESSED
                    or event[4] & curses.BUTTON1_CLICKED
                ):
                    updated_cells.append(toggle_block(game_state, mouse_position))
            except curses.error:
                pass

        if key == ord(" "):
            paused = not paused

        current_time = time.perf_counter()
        dtime = current_time - last_time
        if (not paused) and dtime > time_between_frames:
            last_time = current_time
            game_state, updated = conways_gol.update_conways_gol(
                game_state, looping_borders
            )
            updated_cells = updated_cells + updated
        if updated_cells:
            update_screen_partial(screen_dimensions, updated_cells, stdscr)
            stdscr.refresh()


wrapper(main)
