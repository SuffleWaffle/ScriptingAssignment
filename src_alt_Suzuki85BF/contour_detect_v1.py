# >>>> </> STANDARD IMPORTS </>
# >>>> ********************************************************************************
import os
import sys
import logging
import ast
# >>>> ********************************************************************************

import numpy as np
from icecream import ic

# ________________________________________________________________________________

# --- CONFIG - LOGGER SETUP ---
if os.environ.get("ENVIRONMENT") == "PROD":
    # --- PRODUCTION ---
    logging.basicConfig(format="| %(levelname)s | %(message)s", level=logging.INFO)

    logging.info(">>> PRODUCTION - LOGGER PROD SETUP IS ACTIVE <<<")

else:
    # --- DEVELOPMENT ---
    logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.DEBUG)

    logging.info(">>> DEVELOPMENT - LOGGER DEV SETUP IS ACTIVE <<<")

# ________________________________________________________________________________

"""
    Direction Reference:

                1
                |
                |
         2 <- - | - -> 0
                |
                |
                3
"""


def next_cell(curr_pixel, curr_direction):
    """
    Border following - next_cell() function:\n
    - This function takes the current pixel and direction and returns the next pixel's position
    - and the new direction based on the current direction. It also saves the next pixel's position
    - in a variable called "save".
    """
    i, j = curr_pixel

    row: int = 0
    col: int = 0
    new_direction: int = 0
    save = None

    match curr_direction:
        case 0:
            row = i - 1
            col = j
            new_direction = 1
            save = [i, j+1]
        case 1:
            row = i
            col = j - 1
            new_direction = 2
        case 2:
            row = i + 1
            col = j
            new_direction = 3
        case 3:
            row = i
            col = j + 1
            new_direction = 0

    # return row, col, new_direction, save
    return col, row, new_direction, save


def border_follow(image, start, prev, direction, NBD):
    curr = list(start)
    exam = list(prev)
    save1 = None
    save2 = list(exam)

    contour = [list(curr)]

    while image[exam[0]][exam[1]] == 0:
        exam[0], exam[1], direction, save_pixel = next_cell(curr, direction)
        if save_pixel is not None:
            save1 = list(save_pixel)
        if save2 == exam:
            image[curr[0], curr[1]] = -NBD
            return contour

    if save1 is not None:
        image[curr[0]][curr[1]] = -NBD
        save1 = None
    elif (save1 is None or (save1 is not None and image[save1[0]][save1[1]] != 0)) \
            and image[curr[0]][curr[1]] == 1:
        image[curr[0]][curr[1]] = NBD
    else:
        pass

    prev = list(curr)
    curr = list(exam)
    contour.append(list(curr))
    #
    if direction >= 2:
        direction = direction-2
    else:
        direction = 2+direction

    flag = 0
    start_next = list(curr)
    # --- CHECK IF THE NEXT PIXEL IS ALREADY IN THE CONTOUR ---
    while True:
        if not(curr == start_next and prev == start and flag == 1):
            flag = 1
            exam[0], exam[1], direction, save_pixel = next_cell(curr, direction)

            if save_pixel is not None:
                save1 = list(save_pixel)

            # --- CHECK IF THE NEXT PIXEL IS ALREADY IN THE CONTOUR ---
            while image[exam[0]][exam[1]] == 0:
                exam[0], exam[1], direction, save_pixel = next_cell(curr, direction)
                if save_pixel is not None:
                    save1 = list(save_pixel)

            # --- CHECK IF THE NEXT PIXEL IS ALREADY IN THE CONTOUR ---
            if save1 is not None and image[save1[0]][save1[1]] == 0:
                image[curr[0]][curr[1]] = -NBD
                save1 = None

            # --- CHECK IF THE NEXT PIXEL IS ALREADY IN THE CONTOUR ---
            elif (save1 is None or (save1 is not None and image[save1[0]][save1[1]] != 0)) \
                    and image[curr[0]][curr[1]] == 1:
                image[curr[0]][curr[1]] = NBD

            prev = list(curr)
            curr = list(exam)
            contour.append(list(curr))

            if direction >= 2:
                direction = direction-2
            else:
                direction = 2+direction
        else:
            break

    return contour


def raster_scan(image_sample):
    # rows, cols = image_sample.shape
    cols, rows = image_sample.shape

    nbd = 1
    lnbd = 1
    contours = []

    parent_arr = []
    parent_arr.append(-1)

    border_type_arr = []
    border_type_arr.append(0)

    for i in range(1, rows-1):
        lnbd = 1

        for j in range(1, cols-1):
            if image_sample[i][j] == 1 and image_sample[i][j - 1] == 0:
                nbd += 1
                direction = 2
                parent_arr.append(lnbd)
                contour = border_follow(image_sample, [i, j], [i, j - 1], direction, nbd)
                contours.append(contour)
                border_type_arr.append(1)

                if border_type_arr[nbd - 2] == 1:
                    parent_arr.append(parent_arr[nbd - 2])
                else:
                    if image_sample[i][j] != 1:
                        lnbd = abs(image_sample[i][j])

            elif image_sample[i][j] >= 1 and image_sample[i][j + 1] == 0:
                nbd += 1
                direction = 0

                if image_sample[i][j] > 1:
                    lnbd = image_sample[i][j]

                parent_arr.append(lnbd)
                contour = border_follow(image_sample, [i, j], [i, j + 1], direction, nbd)
                contours.append(contour)
                border_type_arr.append(0)

                if border_type_arr[nbd - 2] == 0:
                    parent_arr.append(parent_arr[nbd - 2])
                else:
                    if image_sample[i][j] != 1:
                        lnbd = abs(image_sample[i][j])

    return contours, parent_arr, border_type_arr


# >>>> </> APP - RUN CONFIG </>
# >>>> ********************************************************************************
if __name__ == "__main__":
    contour_file = "input_v2.txt"
    contour_symbol = "1"

    data_arr: np.ndarray = np.loadtxt(fname=contour_file,
                                      dtype=int,
                                      skiprows=1)
    ic(data_arr)

    # img = np.array(ast.literal_eval(input()))
    img = data_arr
    contours_arr, parent_arr, border_type_arr = raster_scan(img)

    ic(contours_arr)
    ic(parent_arr)
    ic(border_type_arr)
