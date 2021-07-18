import numpy as np
from statistics import mean


def get_border_dimensions(img_path):
    outside_contours = np.load(f"temp/{img_path.split('/')[1]}_outside_contours.npy")
    inside_contours = np.load(f"temp/{img_path.split('/')[1]}_inside_contours.npy")

    leftmost = tuple(inside_contours[inside_contours[:, :, 0].argmin()][0])
    rightmost = tuple(inside_contours[inside_contours[:, :, 0].argmax()][0])
    topmost = tuple(inside_contours[inside_contours[:, :, 1].argmin()][0])
    bottommost = tuple(inside_contours[inside_contours[:, :, 1].argmax()][0])

    inside_left_max = leftmost[0]
    inside_right_max = rightmost[0]
    inside_top_max = topmost[1]
    inside_bottom_max = bottommost[1]

    top_inside_border = []
    right_inside_border = []
    bottom_inside_border = []
    left_inside_border = []

    for point in inside_contours:
        coordinates = tuple(point[0])
        if inside_left_max + 20 < coordinates[0] < inside_right_max - 20 and inside_top_max + 20 > coordinates[1] > inside_top_max - 20:
            top_inside_border.append(coordinates)
        if inside_right_max - 20 < coordinates[0] < inside_right_max + 20:
            right_inside_border.append(coordinates)
        if inside_left_max + 20 < coordinates[0] < inside_right_max - 20 and inside_bottom_max + 20 > coordinates[1] > inside_bottom_max - 20:
            bottom_inside_border.append(coordinates)
        if inside_left_max - 20 < coordinates[0] < inside_left_max + 20:
            left_inside_border.append(coordinates)

    top_measure_point = mean([coordinate[1] for coordinate in top_inside_border])
    right_measure_point = mean([coordinate[0] for coordinate in right_inside_border])
    bottom_measure_point = mean([coordinate[1] for coordinate in bottom_inside_border])
    left_measure_point = mean([coordinate[0] for coordinate in left_inside_border])

    ########################################################################################

    outside_leftmost = tuple(outside_contours[outside_contours[:, :, 0].argmin()][0])
    outside_rightmost = tuple(outside_contours[outside_contours[:, :, 0].argmax()][0])
    outside_topmost = tuple(outside_contours[outside_contours[:, :, 1].argmin()][0])
    outside_bottommost = tuple(outside_contours[outside_contours[:, :, 1].argmax()][0])

    outside_left_max = outside_leftmost[0]
    outside_right_max = outside_rightmost[0]
    outside_top_max = outside_topmost[1]
    outside_bottom_max = outside_bottommost[1]

    top_outside_border = []
    right_outside_border = []
    bottom_outside_border = []
    left_outside_border = []

    for point in outside_contours:
        coordinates = tuple(point[0])
        if inside_left_max + 20 < coordinates[0] < inside_right_max - 20 and outside_top_max + 20 > coordinates[1] > outside_top_max - 20:
            top_outside_border.append(coordinates)
        if outside_right_max - 20 < coordinates[0] < outside_right_max + 20:
            right_outside_border.append(coordinates)
        if inside_left_max + 20 < coordinates[0] < inside_right_max - 20 and outside_bottom_max + 5 > coordinates[1] > outside_bottom_max - 5:
            bottom_outside_border.append(coordinates)
        if outside_left_max - 20 < coordinates[0] < outside_left_max + 20:
            left_outside_border.append(coordinates)

    top_outside_measure_point = mean([coordinate[1] for coordinate in top_outside_border])
    right_outside_measure_point = mean([coordinate[0] for coordinate in right_outside_border])
    bottom_outside_measure_point = mean([coordinate[1] for coordinate in bottom_outside_border])
    left_outside_measure_point = mean([coordinate[0] for coordinate in left_outside_border])

    ########################################################################################

    top_border = abs(top_outside_measure_point - top_measure_point)
    right_border = abs(right_outside_measure_point - right_measure_point)
    bottom_border = abs(bottom_outside_measure_point - bottom_measure_point)
    left_border = abs(left_outside_measure_point - left_measure_point)

    return top_border, right_border, bottom_border, left_border
