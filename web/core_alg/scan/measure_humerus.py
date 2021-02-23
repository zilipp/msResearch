# python libraries
import logging
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt

# self defined functions
from core_alg.base import Filefolder
from core_alg.utilities import distance_util
from core_alg.utilities import bone_region_util
from core_alg.utilities import rotate_utils


def tune_params(device):
    # parameter to tune error
    global hml_coeff, heb_coeff, hhd_coeff

    # if device == Filefolder.Type.SENSOR_I:
    #     hml_coeff = 0.996
    #     heb_coeff = 0.994
    #     hhd_coeff = 0.965
    # else:
    #     hml_coeff = 0.9986
    #     heb_coeff = 0.9516
    #     hhd_coeff = 0.9388
    hml_coeff = 1
    heb_coeff = 1
    hhd_coeff = 1


def get_hml(alpha_shape, show_figure, left_bone_points_ordered, right_bone_points_ordered):
    (min_x, _min_y, max_x, _max_y) = alpha_shape.exterior.bounds
    hml = max_x - min_x

    if not show_figure:
        # most left point, 1st POIs
        p_left = []
        for i in range(len(left_bone_points_ordered)):
            if left_bone_points_ordered[i][0] == min_x:
                p_left = left_bone_points_ordered[i]
                break

        # most right point, 2nd POIs
        p_right = []
        right_most_idx = 0
        for i in range(len(right_bone_points_ordered)):
            if right_bone_points_ordered[i][0] == max_x:
                p_right = right_bone_points_ordered[i]
                break

        fig, ax = plt.subplots()
        x, y = alpha_shape.exterior.xy
        ax.plot(x, y)
        ax.plot(p_left[0], p_left[1], 'r+')
        ax.plot(p_right[0], p_right[1], 'r+')
        ax.set_aspect('equal')
        plt.show()

    hml /= hml_coeff
    return hml


def get_heb(left_bone, show_figure, left_bone_points_ordered, alpha_shape):
    (left_bone_min_x, left_bone_min_y, left_bone_max_x,
     left_bone_max_y) = left_bone.exterior.bounds
    heb = left_bone_max_y - left_bone_min_y
    rotated_list = []
    max_heb_index = 0
    heb_index = 0
    point_a_y = []
    point_b_y = []
    for rad in range(-10, 20, 1):
        rotated_points = []
        for point in left_bone_points_ordered:
            new_point = rotate_utils.rotate(point, rad)
            rotated_points.append(new_point)
        rotated_list.append(rotated_points)

        rotated_points = np.asarray(rotated_points)
        max_y = rotated_points.max(axis=0)[1]
        min_y = rotated_points.min(axis=0)[1]
        cur_heb = max_y - min_y
        if cur_heb >= heb:
            heb = cur_heb
            max_heb_index = heb_index
            point_a_y = max_y
            point_b_y = min_y

        heb = max(heb, cur_heb)
        heb_index += 1

    if not show_figure:
        max_feb_points = rotated_list[max_heb_index]
        # top point, 1st POIs
        p_top = []
        for i in range(len(max_feb_points)):
            if max_feb_points[i][1] == point_a_y:
                p_top = max_feb_points[i]
                break

        # bottom point, 1st POIs
        p_bottom = []
        for i in range(len(max_feb_points)):
            if max_feb_points[i][1] == point_b_y:
                p_bottom = max_feb_points[i]
                break

        fig, ax = plt.subplots()
        max_feb_points = np.array(max_feb_points)
        x = max_feb_points[:, 0].tolist()
        y = max_feb_points[:, 1].tolist()
        ax.scatter(x, y, marker='o')

        ax.plot(p_top[0], p_top[1], 'r+')
        ax.plot(p_bottom[0], p_bottom[1], 'r+')
        ax.set_aspect('equal')
        plt.show()

    heb /= heb_coeff
    return heb


def get_hhd(bone_right_region, right_region_points_ordered, show_figure, alpha_shape):
    (x_min, y_min, x_max, y_max) = bone_right_region.exterior.bounds

    convex_hull = list()
    for x, y in bone_right_region.convex_hull.exterior.coords:
        convex_hull.append([x, y])

    left_most_idx = [i for i, x_y in enumerate(convex_hull) if x_y[0] == x_min]
    if left_most_idx[1] - left_most_idx[0] == 1:
        convex_hull = convex_hull[left_most_idx[1]
            :] + convex_hull[:left_most_idx[0] + 1]

    up_most_idx = [i for i, x_y in enumerate(convex_hull) if x_y[1] == y_max]
    right_most_idx = [i for i, x_y in enumerate(
        convex_hull) if x_y[0] == x_max]
    bottom_most_idx = [i for i, x_y in enumerate(
        convex_hull) if x_y[1] == y_min]

    # Find point a and point b to get the upper point c
    y_delta_max = 0
    upper_point_a_idx = 0
    for i in range(up_most_idx[0], right_most_idx[0]):
        y_delta = convex_hull[i][1] - convex_hull[i+1][1]
        if y_delta > y_delta_max:
            y_delta_max = y_delta
            upper_point_a_idx = i

    dis_delta_max = 0
    for i in range(upper_point_a_idx - 2, upper_point_a_idx + 2):
        x_delta = convex_hull[i][0] - convex_hull[i + 1][0]
        y_delta = convex_hull[i][1] - convex_hull[i + 1][1]
        dis_delta = x_delta ** 2 + y_delta ** 2
        if dis_delta > dis_delta_max:
            dis_delta_max = dis_delta
            upper_point_a_idx = i

    point_a = convex_hull[upper_point_a_idx]
    point_b = convex_hull[upper_point_a_idx + 1]

    point_a_idx = [i for i, x_y in enumerate(
        right_region_points_ordered) if x_y[0] == point_a[0]]
    point_b_idx = [i for i, x_y in enumerate(
        right_region_points_ordered) if x_y[0] == point_b[0]]

    max_dist = 0
    point_c_idx = 0

    num_of_points_between_a_b = point_b_idx[0] - point_a_idx[0]
    if num_of_points_between_a_b >= 3:
        for i in range(point_a_idx[0], point_b_idx[0] - 2):
            dist = 0
            for j in range(0, 3):
                dist = dist + distance_util.distance_point_to_line(
                    point_a, point_b, right_region_points_ordered[i+j])
            if dist > max_dist:
                max_dist = dist
                point_c_idx = i + 1

    # no points between point_a and point_b
    if point_c_idx == 0:
        point_c_idx = point_a_idx[0]

    point_c = right_region_points_ordered[point_c_idx]

    # Find bottom point d
    x_delta_max = 0
    point_d_idx = 0
    for i in range(bottom_most_idx[0], len(convex_hull)):
        x_delta = convex_hull[i-1][0] - convex_hull[i][0]
        if x_delta > x_delta_max:
            x_delta_max = x_delta
            point_d_idx = i-1
    point_d = convex_hull[point_d_idx]

    if not show_figure:
        fig, ax = plt.subplots()

        data = np.asarray(right_region_points_ordered)
        x = data[:, 0].tolist()
        y = data[:, 1].tolist()
        ax.scatter(x, y, marker='o')

        data = np.asarray(convex_hull)
        x = data[:, 0].tolist()
        y = data[:, 1].tolist()
        ax.scatter(x, y, marker='*', facecolor='g')

        data = np.asarray([point_a, point_b])
        x = data[:, 0].tolist()
        y = data[:, 1].tolist()
        ax.scatter(x, y, marker='+', facecolor='orange')

        data = np.asarray([point_c, point_d])
        x = data[:, 0].tolist()
        y = data[:, 1].tolist()
        ax.scatter(x, y, marker='+', facecolor='r')

        ax.set_aspect('equal')
        plt.show()

    if show_figure:
        fig, ax = plt.subplots()
        x, y = alpha_shape.exterior.xy
        ax.plot(x, y)
        ax.plot(point_c[0], point_c[1], 'r+')
        ax.plot(point_d[0], point_d[1], 'r+')
        ax.set_aspect('equal')
        plt.show()

    hhd = distance_util.distance_point_to_point(point_c, point_d)
    hhd /= hhd_coeff
    return hhd


def get_measurement(humerus, show_figure, device=None):
    logging.info('Start measuring humerus...')

    tune_params(device)

    left_region, left_region_points_ordered = bone_region_util.get_left_region(humerus.alpha_shape)
    right_region, right_region_points_ordered = bone_region_util.get_right_region(
        humerus.alpha_shape)

    humerus.hml = get_hml(humerus.alpha_shape, show_figure, left_region_points_ordered, right_region_points_ordered)
    humerus.heb = get_heb(left_region, show_figure, left_region_points_ordered, humerus.alpha_shape)
    humerus.hhd = get_hhd(
        right_region, right_region_points_ordered, show_figure, humerus.alpha_shape)
