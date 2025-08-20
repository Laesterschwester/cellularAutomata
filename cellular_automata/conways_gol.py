def update_conways_gol(game_state, looping_borders):
    updated_cells = []
    rows = len(game_state)
    cols = len(game_state[0])

    for i_row in range(rows):
        for i_col in range(cols):
            state = game_state[i_row][i_col]
            neighbors = 0

            # fmt: off
            dirs = [
                (-1, -1), (0, -1), (1, -1),
                (-1,  0),          (1,  0),
                (-1,  1), (0,  1), (1,  1)
            ]
            # fmt: on

            if looping_borders:
                for d_col, d_row in dirs:
                    di_row = i_row + d_row
                    di_col = i_col + d_col

                    if di_row < 0:
                        di_row = len(game_state) - 1
                    if di_row >= len(game_state):
                        di_row = 0
                    if di_col < 0:
                        di_col = len(game_state[0]) - 1
                    if di_col >= len(game_state[0]):
                        di_col = 0

                    if game_state[di_row][di_col]:
                        neighbors += 1
            else:
                for d_col, d_row in dirs:
                    if 0 <= i_row + d_row < len(
                        game_state
                    ) and 0 <= i_col + d_col < len(game_state[0]):
                        if game_state[i_row + d_row][i_col + d_col]:
                            neighbors += 1

            if state == 0 and neighbors == 3:
                updated_cells.append([i_row, i_col, True])

            if state == 1:
                if neighbors < 2:
                    updated_cells.append([i_row, i_col, False])
                if neighbors > 3:
                    updated_cells.append([i_row, i_col, False])

    for update in updated_cells:
        row, col, is_alive = update
        game_state[row][col] = is_alive

    return game_state, updated_cells
