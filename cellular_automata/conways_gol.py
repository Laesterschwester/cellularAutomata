import copy


def update_conways_gol(conways_arr, looping_borders):
    new_conway = copy.deepcopy(conways_arr)
    rows = len(conways_arr)
    cols = len(conways_arr[0])

    for i_row in range(rows):
        for i_col in range(cols):
            state = conways_arr[i_row][i_col]
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
                        di_row = len(conways_arr) - 1
                    if di_row >= len(conways_arr):
                        di_row = 0
                    if di_col < 0:
                        di_col = len(conways_arr[0]) - 1
                    if di_col >= len(conways_arr[0]):
                        di_col = 0

                    if conways_arr[di_row][di_col]:
                        neighbors += 1
            else:
                for d_col, d_row in dirs:
                    if 0 <= i_row + d_row < len(
                        conways_arr
                    ) and 0 <= i_col + d_col < len(conways_arr[0]):
                        if conways_arr[i_row + d_row][i_col + d_col]:
                            neighbors += 1

            if state == 0 and neighbors == 3:
                new_conway[i_row][i_col] = 1
            if state == 1:
                if neighbors < 2:
                    new_conway[i_row][i_col] = 0
                if neighbors > 3:
                    new_conway[i_row][i_col] = 0

    return new_conway
