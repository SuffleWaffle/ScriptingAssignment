# >>>> </> STANDARD IMPORTS </>
# >>>> ************************************************************************************************
import os
import logging
# >>>> ************************************************************************************************

# >>>> </> EXTERNAL IMPORTS </>
# >>>> ************************************************************************************************
# --- Data Processing ---
import numpy as np
from matplotlib import pyplot as plt

# --- Image Processing ---
import cv2
from PIL import Image

# --- IceCream Debugger ---
from icecream import ic
# >>>> ************************************************************************************************

# >>>> </> SCRIPT METHODS </>
# >>>> ************************************************************************************************


# ___________________________________________________________________________________________
# --- VALIDATE INPUT FILE DIMENSIONS ---
def validate_input_dims(input_fname: str):
    with open(input_fname, "r") as f:
        input_arr_dims = tuple([int(string) for string in f.readline().split()])
        input_arr_data = f.read().splitlines()[0:]

    input_arr_data = np.array([line.split() for line in input_arr_data])


    if input_arr_dims != input_arr_data.shape:
        raise ValueError("STATED input array dimensions do not match the ACTUAL input array dimensions.")

    return input_arr_dims


# ___________________________________________________________________________________________
# --- CREATE BLANK IMAGE FOR PLOTS ---
def create_blank_image(width: int, height: int):
    rgb_color = (255, 255, 255)
    blank_image_fname = f"blank_image_{width}x{height}.jpg"

    if not os.path.exists(blank_image_fname):
        img = Image.new(mode="RGB",
                        size=(width, height),
                        color=rgb_color)
        img.save(fp=blank_image_fname,
                 format="JPEG")

    else:
        logging.info(f"File {blank_image_fname} already exists, skipping creation...")

    return blank_image_fname


# ___________________________________________________________________________________________
# --- APPLY PLOT STYLE ---
def apply_plot_style(grid_color: str, x_len: int, y_len: int):
    plt_obj = plt.gca()
    plt_obj.grid(color=grid_color, linestyle="-", linewidth=1.5, which="major"),
    plt_obj.minorticks_on()
    plt_obj.set_xticks(np.arange(-.5, x_len, 1))
    plt_obj.set_yticks(np.arange(-.5, y_len, 1))
    plt_obj.set_xticklabels(np.arange(0, x_len+1, 1))
    plt_obj.set_yticklabels(np.arange(0, y_len+1, 1))


# ___________________________________________________________________________________________
# --- MAIN SCRIPT ---
def contour_detect(input_fname: str):
    # ___________________________________________________________________________________________
    # --- VALIDATE INPUT FILE DIMENSIONS ---
    input_arr_dims = validate_input_dims(input_fname=input_fname)

    # ___________________________________________________________________________________________
    # --- CREATE AND READ THE BLANK IMAGE FOR PLOTS ---
    blank_image_fname = create_blank_image(width=input_arr_dims[1],
                                           height=input_arr_dims[0])

    blank_image = cv2.imread(blank_image_fname)

    # ___________________________________________________________________________________________
    # --- 1.0 - READ THE INPUT FROM txt FILE
    bin_input_arr: np.ndarray = np.loadtxt(fname=input_fname,
                                           dtype=np.uint8,
                                           skiprows=1)
    # >>>> PLOT - 1
    plt.subplot(221), plt.imshow(bin_input_arr, cmap="gray_r"), plt.title("1 - BINARY INPUT")
    apply_plot_style("red", input_arr_dims[1], input_arr_dims[0])

    # ___________________________________________________________________________________________
    # --- 1.1 - FIND CONTOURS IN bin_input_arr (Suzuki Tracing from OpenCV)
    contours, hierarchy = cv2.findContours(bin_input_arr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ic(contours)

    # ___________________________________________________________________________________________
    # --- 2.0 - CONTOURS IMAGE
    contours_img = cv2.drawContours(image=blank_image, contours=contours, contourIdx=0,
                                    color=(255, 0, 0), thickness=0)
    # >>>> PLOT - 2
    plt.subplot(222), plt.imshow(contours_img), plt.title("2 - CONTOURS")
    apply_plot_style("black", input_arr_dims[1], input_arr_dims[0])

    # ___________________________________________________________________________________________
    # --- 3.0 - FILL CONTOURS ---
    contours_arr: np.ndarray = np.zeros_like(bin_input_arr, dtype=np.int32)
    for contour in contours[0]:
        # row, col = contour[0]
        contours_arr[contour[:-1]] = 1
    ic(contours_arr)

    filled_contours_rgb_arr = cv2.fillPoly(img=blank_image, pts=contours, color=(1, 0, 0))
    filled_contours_rgb_arr[filled_contours_rgb_arr == 255] = 0

    bin_output_arr = filled_contours_rgb_arr[:, :, 0]
    ic(bin_output_arr)

    # >>>> PLOT - 3
    plt.subplot(223), plt.imshow(bin_output_arr, cmap="gray_r"), plt.title("3 - BINARY OUTPUT")
    apply_plot_style("red", input_arr_dims[1], input_arr_dims[0])

    # ___________________________________________________________________________________________
    # --- PLOT THE IMAGES ---
    plt.tight_layout()
    plt.show()

    # ___________________________________________________________________________________________
    # --- COUNT NUMBER OF FILLED CELLS ---
    filled_cells_num = np.sum(bin_input_arr != bin_output_arr)
    ic(filled_cells_num)

    # ___________________________________________________________________________________________
    # --- SAVE THE OUTPUT TO txt FILE ---
    output_fname = input_fname.replace("input", "output")
    np.savetxt(fname=output_fname, X=bin_output_arr,
               fmt="%d", delimiter=" ", newline="\n",
               header=" ".join([str(integer) for integer in input_arr_dims]),
               footer=f"{filled_cells_num}",
               comments="",
               encoding=None)


# >>>> ************************************************************************************************


if __name__ == "__main__":
    # ___________________________________________________________________________________________
    # --- RUN CONTOUR DETECTION SCRIPT ---
    bin_input_fname = "input_v1.txt"

    if os.path.exists(bin_input_fname):
        contour_detect(input_fname=bin_input_fname)
    else:
        raise FileNotFoundError(f"File {bin_input_fname} not found!")
