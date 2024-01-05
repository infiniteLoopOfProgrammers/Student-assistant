import cv2
import numpy as np
from sklearn.model_selection import ParameterGrid
import os


def sort_point_horizontal(list1: list, size):
    total_list, temp_list = list(), list()

    for item_i in list1:
        temp_list.append(item_i)

        for item_j in list1:
            if (item_j[1] == item_i[1]) and (item_i is not item_j):
                temp_list.append(item_j)

        total_list.append(temp_list)
        temp_list = []

        if len(total_list) == size:
            break

    total_list.sort(key=lambda x: x[0][1])

    return total_list


def check_distance(numbers, target):
    for number in numbers:
        if abs(number - target) < 10:
            return True
    return False


def process_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    binary = cv2.bitwise_not(binary)

    param_grid = {'rho': [1, 2], 'threshold': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
                  'minLineLength': [50, 100, 150], 'maxLineGap': [10, 20, 30]}

    best_score = 0

    for params in ParameterGrid(param_grid):
        lines = cv2.HoughLinesP(binary, rho=params['rho'], theta=np.pi/180, threshold=params['threshold'],
                                minLineLength=params['minLineLength'], maxLineGap=params['maxLineGap'])

        score = 0
        max_vertical_length = 0
        max_horizontal_length = 0

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)

                if angle < 10:
                    if length > max_vertical_length:
                        max_vertical_length = length
                elif angle > 80:
                    if length > max_horizontal_length:
                        max_horizontal_length = length


            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)

                if angle < 10 and length > 0.9 * max_vertical_length:
                    score += 100
                elif angle > 80 and length > 0.9 * max_horizontal_length:
                    score += 100
                else:
                    score -= 80

        if score > best_score:
            best_score = score
            best_params = params

    lines = cv2.HoughLinesP(binary, rho=best_params['rho'], theta=np.pi/180, threshold=best_params['threshold'],
                            minLineLength=best_params['minLineLength'], maxLineGap=best_params['maxLineGap'])

    table_coordinates = []
    vertical_lines = []
    horizontal_lines = []
    vertical_x = []
    horizontal_y = []
    num = 0
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            table_coordinates.append([(x1, y1), (x2, y2)])

            if (x2 - x1) == 0 and (not check_distance(vertical_x, x1)):
                vertical_lines.append(line)
                vertical_x.append(x1)
            elif (y2 - y1) == 0 and (not check_distance(horizontal_y, y1)):
                horizontal_lines.append(line)
                horizontal_y.append(y1)

    vertical_lines.sort(key=lambda x: x[0][0])
    horizontal_lines.sort(key=lambda x: x[0][0])

    print(len(horizontal_lines))
    for line in vertical_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imwrite(f"testout/out{num}.png", img)
        num = num + 1

    for line in horizontal_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.imwrite(f"testout/out{num}.png", img)
        num = num + 1

    table_coordinates = find_table_coordinates(
        vertical_lines, horizontal_lines)
    print(table_coordinates)
    print(len(table_coordinates))

    output_folder = "output_cells"
    os.makedirs(output_folder, exist_ok=True)

    sorted_points = sort_point_horizontal(
        table_coordinates, len(horizontal_lines))
    crop_and_save_cells(img, sorted_points, output_folder)


def find_table_coordinates(vertical_lines, horizontal_lines):
    intersections = []

    for v_line in vertical_lines:
        for h_line in horizontal_lines:
            x1_v, y1_v, x2_v, y2_v = v_line[0]
            x1_h, y1_h, x2_h, y2_h = h_line[0]

            intersection = find_intersection(
                x1_v, y1_v, x2_v, y2_v, x1_h, y1_h, x2_h, y2_h)

            if intersection is not None:
                intersections.append(intersection)

    return intersections


def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if det != 0:
        intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) -
                          (x1 - x2) * (x3 * y4 - y3 * x4)) / det
        intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) -
                          (y1 - y2) * (x3 * y4 - y3 * x4)) / det

        return int(intersection_x), int(intersection_y)
    else:
        return None


def crop_and_save_cells(image, sorted_points, output_folder):
    number = 0
    for i in range(len(sorted_points)-1):
        item_1 = sorted_points[i]
        item_2 = sorted_points[i+1]
        for j in range(len(item_1)-1):
            cropped_img = (
                image[item_1[j][1]:item_2[j+1][1], item_1[j][0]:item_2[j+1][0]])
            cv2.imwrite(
                f"{output_folder}/Cropped_Image_{number}.jpg", cropped_img)
            number += 1


process_image("test6.jpg")
