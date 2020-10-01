# python libraries
import logging
import numpy as np
import math
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

# self defined functions
from base import Bone
from utilities import distance_util
from utilities import bone_region_util

fml_coeff = 0.997
feb_coeff = 0.995
fbml_coeff = 0.997
fmld_coeff = 0.958
fhd_coeff = 0.971


def get_fml(alpha_shape):
    (min_x, min_y, max_x, max_y) = alpha_shape.exterior.bounds
    fml = max_x - min_x
    # fml /= fml_coeff
    logging.info('fml: {0:0.3f}'.format(fml))
    return fml


def get_feb(left_bone):
    (left_bone_min_x, left_bone_min_y, left_bone_max_x, left_bone_max_y) = left_bone.exterior.bounds
    feb = left_bone_max_y - left_bone_min_y
    # feb /= feb_coeff
    logging.info('feb: {0:0.3f}'.format(feb))
    return feb


def get_fbml(left_bone, left_bone_points_ordered, right_bone_points_ordered):
    (left_bone_min_x, left_bone_min_y, left_bone_max_x, left_bone_max_y) = left_bone.exterior.bounds

    # most left point, 1st POIs
    p_left = []
    p_left_idx = 0
    for i in range(len(left_bone_points_ordered)):
        if left_bone_points_ordered[i][0] == left_bone_min_x:
            p_left = left_bone_points_ordered[i]
            p_left_idx = i
            break
    # print(p_left, 'at: ', p_left_idx)

    # if ist POI is above x-axis, change the direction of line
    if left_bone_max_y - p_left[1] < (left_bone_max_y - left_bone_min_y) * 0.5:
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
        fbml = max(fbml, distance_util.distance_point_to_line(p_left, p_left_second, right_bone_points_ordered[i]))

    # fbml /= fbml_coeff
    logging.info('fbml: {0:0.3f}'.format(fbml))
    return fbml


def get_fmld(center_bone_points, show_figure):
    center_bone_points = np.asarray(center_bone_points)
    # sort upper and lower points in order by x-value
    center_bone_points_upper = np.asarray([x for x in center_bone_points if x[1] >= 0])
    center_bone_points_upper = center_bone_points_upper[np.argsort(center_bone_points_upper[:, 0])]

    center_bone_points_lower = np.asarray([x for x in center_bone_points if x[1] <= 0])
    center_bone_points_lower = center_bone_points_lower[np.argsort(center_bone_points_lower[:, 0])]

    # fit two lines
    top_line_p = distance_util.fit_line(center_bone_points_upper, show_figure)
    bottom_line_p = distance_util.fit_line(center_bone_points_lower, show_figure)
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

        dis_cur = distance_util.distance_2_point_to_point([x, y], [x1, y1])
        min_line_segment_length = min(dis_cur, min_line_segment_length)

    fmld = math.sqrt(min_line_segment_length)
    # fmld /= fmld_coeff
    logging.info('fmld: {0:0.3f}'.format(fmld))
    return fmld


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

    dis_right_point = distance_util.distance_point_to_line(p_start, p_y_inter, line_right_point)
    dis_left_point = distance_util.distance_point_to_line(p_start, p_y_inter, line_left_point)

    p_start_2 = line_left_point
    p_start_2_idx = end_idx - 1
    if dis_left_point > dis_right_point:
        p_start_2 = line_right_point
        p_start_2_idx = end_idx - 2
    # print('start: ', p_start)
    # print('start2: ', p_start_2)

    # 6. 计算出点tmp_point2到 tmp_line上的投影点tmp_point3 然后算出来 start_point到tmp_point3的距离dist
    # 把dist存入一个list
    fhd = distance_util.distance_point_to_point(p_start, p_start_2)
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
        left_dis = distance_util.distance_point_to_line(p1, [0, cur_intercept], right_bone_points_ordered_array[left_idx])
        right_dis = distance_util.distance_point_to_line(p1, [0, cur_intercept], right_bone_points_ordered_array[right_idx])

        res_point = right_bone_points_ordered_array[left_idx]
        if left_dis > right_dis:
            res_point = right_bone_points_ordered_array[right_idx]

        return res_point

    iterate_idx = start_idx
    while iterate_idx > 0:
        p_up_right = right_bone_points_ordered[iterate_idx]

        p_down_left = find_down_left(p_up_right, p_start_2_idx, right_bone_points_ordered)
        cur_fhd = distance_util.distance_point_to_point(p_up_right, p_down_left)
        fhd = max(fhd, cur_fhd)
        if cur_fhd < fhd:
            count_decrease += 1
            if count_decrease >= 5:
                break
        else:
            count_decrease = 0
        iterate_idx -= 1

    # fhd /= fhd_coeff
    logging.info('fhd: {0:0.3f}'.format(fhd))
    return fhd


def get_measurement(femur, show_figure):
    logging.info('Start measuring femur')

    left_region, left_region_points_ordered = bone_region_util.get_left_region(femur.alpha_shape)
    center_region, center_region_points = bone_region_util.get_center_region(femur.alpha_shape)
    right_region, right_region_points_ordered = bone_region_util.get_right_region(femur.alpha_shape)

    femur.fml = get_fml(femur.alpha_shape)
    femur.feb = get_feb(left_region)
    femur.fbml = get_fbml(left_region, left_region_points_ordered, right_region_points_ordered)
    femur.fmld = get_fmld(center_region_points, show_figure)
    femur.fhd = get_fhd(right_region, right_region_points_ordered)