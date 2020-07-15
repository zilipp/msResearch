# python libraries
import sys
import logging
import numpy as np
import math
import copy
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from sklearn.decomposition import PCA

import open3d as o3d
import alphashape
from descartes import PolygonPatch
from shapely.geometry import Polygon
from shapely import affinity
import numpy.polynomial.polynomial as poly

# self defined functions
import utilities


def get_left_part(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    # todo: coefficient
    left_box = Polygon([(minx, miny), (minx, maxy), (minx / 1.5, maxy), (minx / 1.5, miny)])
    left_bone = alpha_shape.intersection(left_box)

    left_bone_line = left_bone.exterior
    left_bone_points = []
    for x, y in left_bone_line.coords:
        left_bone_points.append([x, y])
    left_bone_points = left_bone_points[:-1]

    max_diff_y = 0
    a_idx = 0
    for i in range(len(left_bone_points) - 1):
        diff_cur = abs(left_bone_points[i][1] - left_bone_points[i + 1][1])
        if diff_cur > max_diff_y:
            max_diff_y = diff_cur
            a_idx = i

    # a(-, +), b(-, -)
    # point_a = left_bone_points[a_idx]
    # point_b = left_bone_points[a_idx + 1]
    # start with point_b(right-lower point)
    left_bone_points_ordered = left_bone_points[a_idx + 1:] + left_bone_points[:a_idx + 1]

    return left_bone, left_bone_points_ordered


def get_center_part(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    # todo: coefficient
    center_box = Polygon([(minx / 3, miny), (minx / 3, maxy), (maxx / 3, maxy), (maxx / 3, miny)])
    center_bone = alpha_shape.intersection(center_box)

    center_bone_line = center_bone.exterior
    center_bone_points = []
    for x, y in center_bone_line.coords:
        center_bone_points.append([x, y])
    center_bone_points = center_bone_points[:-1]

    return center_bone, center_bone_points


def get_right_part(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    # todo: coefficient
    right_box = Polygon([(maxx / 1.5, miny), (maxx / 1.5, maxy), (maxx, maxy), (maxx, miny)])
    right_bone = alpha_shape.intersection(right_box)

    right_bone_line = right_bone.exterior
    right_bone_points = []
    for x, y in right_bone_line.coords:
        right_bone_points.append([x, y])
    right_bone_points = right_bone_points[:-1]

    max_diff_y = 0
    a_idx = 0
    for i in range(len(right_bone_points) - 1):
        diff_cur = abs(right_bone_points[i][1] - right_bone_points[i + 1][1])
        if diff_cur > max_diff_y:
            max_diff_y = diff_cur
            a_idx = i

    # a(+, +), b(+, +)
    # point_a = left_bone_points[a_idx]
    # point_b = left_bone_points[a_idx + 1]
    # start with point_b(left-upper point)
    right_bone_points_ordered = right_bone_points[a_idx + 1:] + right_bone_points[:a_idx + 1]

    return right_bone, right_bone_points_ordered


def get_fml(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    fml = maxx - minx
    logging.info('fml: {0}'.format(fml))


def get_feb(left_bone):
    (left_bone_minx, left_bone_miny, left_bone_maxx, left_bone_maxy) = left_bone.exterior.bounds
    feb = left_bone_maxy - left_bone_miny
    logging.info('feb: {0}'.format(feb))


def get_fbml(left_bone, left_bone_points_ordered, right_bone_points_ordered):
    (left_bone_minx, left_bone_miny, left_bone_maxx, left_bone_maxy) = left_bone.exterior.bounds

    # most left point, 1st POIs
    p_left = []
    p_left_idx = 0
    for i in range(len(left_bone_points_ordered)):
        if left_bone_points_ordered[i][0] == left_bone_minx:
            p_left = left_bone_points_ordered[i]
            p_left_idx = i
            break
    # print(p_left, 'at: ', p_left_idx)

    # if ist POI is above x-axis, change the direction of line
    if left_bone_maxy - p_left[1] < (left_bone_maxy - left_bone_miny) * 0.5:
        left_bone_points_ordered.reverse()
        p_left_idx = len(left_bone_points_ordered) - 1 - p_left_idx

    left_bone_points_ordered = left_bone_points_ordered[p_left_idx + 1:]

    x_min_point = None
    x_min_point_index = 0

    # 如果最小的点不是线段头上的前十个点，说明它是P2
    while x_min_point_index < 10:
        # delete point_b(start point of left box) to current_point, fine the most left point in remaining points
        left_bone_points_ordered = left_bone_points_ordered[x_min_point_index + 1:]
        x_min_point = min(left_bone_points_ordered, key=lambda t: t[0])
        x_min_point_index = [i for i, j in enumerate(left_bone_points_ordered) if j == x_min_point][0]

    # 2nd POI
    p_left_second = x_min_point
    # print('p_left_second: ', p_left_second)

    fbml = 0
    for i in range(len(right_bone_points_ordered)):
        fbml = max(fbml, utilities.distance_point_to_line(p_left, p_left_second, right_bone_points_ordered[i]))

    logging.info('fbml: {0}'.format(fbml))


def get_fmld(center_bone_points, show_figure):
    center_bone_points = np.asarray(center_bone_points)
    center_bone_points_upper = np.asarray([x for x in center_bone_points if x[1] >= 0])
    center_bone_points_lower = np.asarray([x for x in center_bone_points if x[1] <= 0])

    # fit two lines
    top_line_p = utilities.fit_line(center_bone_points_upper, show_figure)
    bottom_line_p = utilities.fit_line(center_bone_points_lower, show_figure)
    # print(top_line_p, bottom_line_p)

    if show_figure:
        x = np.linspace(-25, 25, num=100)
        a = top_line_p[2] * x * x + top_line_p[1] * x + top_line_p[0]
        b = bottom_line_p[2] * x * x + bottom_line_p[1] * x + bottom_line_p[0]
        plt.plot(x, a, 'r')  # plotting t, a separately
        plt.plot(x, b, 'b')  # plotting t, b separately
        plt.plot([0], [0], '*')  # plotting t, c separately
        plt.show()

    # vertical line
    fmld = poly.polyval(0, top_line_p) - poly.polyval(0, bottom_line_p)

    min_line_segment_length = fmld ** 2
    for i in np.arange(-20, 20, .01):
        if i == 0:
            continue
        x = i
        y = top_line_p[2] * x * x + top_line_p[1] * x + top_line_p[0]
        k = y / x
        [x_res1, x_res2] = np.roots([bottom_line_p[2], bottom_line_p[1] - k, bottom_line_p[0]])

        y_res1 = k * x_res1
        dis_1 = x_res1 ** 2 + y_res1 ** 2
        y_res2 = k * x_res2
        dis_2 = x_res2 ** 2 + y_res2 ** 2

        [x1, y1] = [x_res1, y_res1] if dis_1 < dis_2 else [x_res2, y_res2]

        dis_cur = utilities.distance_2_point_to_point([x, y], [x1, y1])
        min_line_segment_length = min(dis_cur, min_line_segment_length)

    fmld = math.sqrt(min_line_segment_length)
    logging.info('fmld: {0}'.format(fmld))


def get_fhd(right_bone, right_bone_points_ordered):
    # 1. right_bone_points_ordered: start from left-upper point

    # 2. point with most right s-coorinate: max(x)
    (right_bone_minx, right_bone_miny, right_bone_maxx, right_bone_maxy) = right_bone.exterior.bounds

    right_most_idx = 0
    for i in range(len(right_bone_points_ordered)):
        if right_bone_points_ordered[i][0] == right_bone_maxx:
            right_most_idx = i
            break

    # 3. counting 5 points upper, find start_point
    start_idx = right_most_idx - 5

    # 4. find line go through start_point, k = 1
    #  tmp_line: start_point_y = start_point_x + intercept
    start_x = right_bone_points_ordered[start_idx][0]
    start_y = right_bone_points_ordered[start_idx][1]
    intercept = start_y - start_x


    # 5. from start_point, find the other point in right bone that on the temp_line
    # line p1: (start_x, start_y), p2:(0, intercept), p3: tmp_point2

    p_start = [start_x, start_y]
    p_y_inter = [0, intercept]

    # right: True; left : False
    right_side = True
    end_idx = start_idx + 3
    while right_side:
        cur_x = right_bone_points_ordered[end_idx][0]
        cur_y = right_bone_points_ordered[end_idx][1]
        if cur_x + intercept <= cur_y:
            right_side = False
        end_idx += 1

    line_right_point = [right_bone_points_ordered[end_idx - 2][0], right_bone_points_ordered[end_idx - 2][1]]
    line_left_point = [right_bone_points_ordered[end_idx - 1][0], right_bone_points_ordered[end_idx - 1][1]]

    dis_right_point = utilities.distance_point_to_line(p_start, p_y_inter, line_right_point)
    dis_left_point = utilities.distance_point_to_line(p_start, p_y_inter, line_left_point)

    p_start_2 = line_left_point
    p_start_2_idx = end_idx - 1
    if dis_left_point > dis_right_point:
        p_start_2 = line_right_point
        p_start_2_idx = end_idx - 2
    # print('start: ', p_start)
    # print('start2: ', p_start_2)

    # 6. 计算出点tmp_point2到 tmp_line上的投影点tmp_point3 然后算出来 start_point到tmp_point3的距离dist
    # 把dist存入一个list
    fhd = utilities.distance_point_to_point(p_start, p_start_2)
    count_decrease = 0

    # 7. start_point开始，向上遍历点 tmp_point1， 更新tmp_line   tmp_point1_y = tmp1_point_x+b
    # 8. 每次遍历，找到在上次tmp_point2附近的一个新点，使得新点到直线tmp_line距离最短
    # tmp_point2更新为新的点，然后计算tmp_point2在直线tmp_line上的投影tmp_point3 到 tmp_point1的距离，存入dist list
    # 依次循环,dist应该先增大，后减小，我们要找到的就是增到极大值，开始减小时候的那个极大的距离

    def find_down_left(p1, from_idx, right_bone_points_ordered_array):
        cur_intercept = p1[1] - p1[0]
        right_side = True
        while right_side:
            candidate_x = right_bone_points_ordered_array[from_idx][0]
            candidate_y = right_bone_points_ordered_array[from_idx][1]
            if candidate_x + cur_intercept <= candidate_y:
                right_side = False
            from_idx += 1

        left_idx = from_idx - 1
        right_idx = left_idx - 1
        left_dis = utilities.distance_point_to_line(p1, [0, cur_intercept], right_bone_points_ordered_array[left_idx])
        right_dis = utilities.distance_point_to_line(p1, [0, cur_intercept], right_bone_points_ordered_array[right_idx])

        res_point = right_bone_points_ordered_array[left_idx]
        if left_dis > right_dis:
            res_point = right_bone_points_ordered_array[right_idx]

        return res_point

    iterate_idx = start_idx
    while iterate_idx > 0:
        p_up_right = right_bone_points_ordered[iterate_idx]

        p_down_left = find_down_left(p_up_right, p_start_2_idx, right_bone_points_ordered)
        cur_fhd = utilities.distance_point_to_point(p_up_right, p_down_left)
        fhd = max(fhd, cur_fhd)
        if cur_fhd < fhd:
            count_decrease += 1
            if count_decrease >= 5:
                break
        else:
            count_decrease = 0
        iterate_idx -= 1

    logging.info('fhd: {0}'.format(fhd))


def get_measurement(alpha_shape, show_figure):
    logging.info('Start measuring femur...')

    left_bone, left_bone_points_ordered = get_left_part(alpha_shape)
    center_bone, center_bone_points = get_center_part(alpha_shape)
    right_bone, right_bone_points_ordered = get_right_part(alpha_shape)

    get_fml(alpha_shape)
    get_feb(left_bone)
    get_fbml(left_bone, left_bone_points_ordered, right_bone_points_ordered)
    get_fmld(center_bone_points, show_figure)
    get_fhd(right_bone, right_bone_points_ordered)
