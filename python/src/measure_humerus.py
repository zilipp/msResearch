# python libraries
import logging
from shapely.geometry import Polygon

# self defined functions
from utilities import distance_util
from utilities import bone_region_util


def get_hml(alpha_shape):
    (min_x, _min_y, max_x, _max_y) = alpha_shape.exterior.bounds
    hml = max_x - min_x
    logging.info('hml: {0:0.3f}'.format(hml))


def get_heb(left_bone):
    (_left_bone_min_x, left_bone_min_y, _left_bone_max_x, left_bone_max_y) = left_bone.exterior.bounds
    heb = left_bone_max_y - left_bone_min_y
    logging.info('heb: {0:0.3f}'.format(heb))


def get_hhd(right_bone, right_bone_points_ordered):
    # 1. right_bone_points_ordered: start from left-upper point

    # 2. point with most right s-coorinate: max(x)
    (_right_bone_min_x, _right_bone_min_y, right_bone_max_x, _right_bone_max_y) = right_bone.exterior.bounds

    right_most_idx = 0
    for i in range(len(right_bone_points_ordered)):
        if right_bone_points_ordered[i][0] == right_bone_max_x:
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
    hhd = distance_util.distance_point_to_point(p_start, p_start_2)
    count_decrease = 0

    # 7. start_point开始，向上遍历点 tmp_point1， 更新tmp_line   tmp_point1_y = tmp1_point_x+b
    # 8. 每次遍历，找到在上次tmp_point2附近的一个新点，使得新点到直线tmp_line距离最短
    # tmp_point2更新为新的点，然后计算tmp_point2在直线tmp_line上的投影tmp_point3 到 tmp_point1的距离，存入dist list
    # 依次循环,dist应该先增大，后减小，我们要找到的就是增到极大值，开始减小时候的那个极大的距离

    def find_down_left(p1, from_idx, right_bone_points_ordered_array):
        cur_intercept = p1[1] - p1[0]
        at_right_side = True
        while at_right_side and from_idx < len(right_bone_points_ordered_array):
            candidate_x = right_bone_points_ordered_array[from_idx][0]
            candidate_y = right_bone_points_ordered_array[from_idx][1]
            if candidate_x + cur_intercept <= candidate_y:
                at_right_side = False
            from_idx += 1

        if from_idx == len(right_bone_points_ordered_array):
            return None
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
        if p_down_left is None:
            break

        cur_fhd = distance_util.distance_point_to_point(p_up_right, p_down_left)
        hhd = max(hhd, cur_fhd)
        if cur_fhd < hhd:
            count_decrease += 1
            if count_decrease >= 5:
                break
        else:
            count_decrease = 0
        iterate_idx -= 1
    logging.info('hhd: {0:0.3f}'.format(hhd))


def get_hhd_new(bone_right_region, right_region_points_ordered):
    (x_min, y_min, x_max, y_max) = bone_right_region.exterior.bounds

    convex_hull = list()
    for x, y in bone_right_region.convex_hull.exterior.coords:
        convex_hull.append([x, y])

    left_most_idx = [i for i, x_y in enumerate(convex_hull) if x_y[0] == x_min]
    if left_most_idx[1] - left_most_idx[0] == 1:
        convex_hull = convex_hull[left_most_idx[1]:] + convex_hull[:left_most_idx[0] + 1]

    up_most_idx = [i for i, x_y in enumerate(convex_hull) if x_y[1] == y_max]
    right_most_idx = [i for i, x_y in enumerate(convex_hull) if x_y[0] == x_max]
    bottom_most_idx = [i for i, x_y in enumerate(convex_hull) if x_y[1] == y_min]

    # Find point a and point b to get the upper point c
    y_delta_max = 0
    upper_point_a_idx = 0
    for i in range(up_most_idx[0], right_most_idx[0]):
        y_delta = convex_hull[i][1] - convex_hull[i+1][1]
        if y_delta > y_delta_max:
            y_delta_max = y_delta
            upper_point_a_idx = i
    point_a = convex_hull[upper_point_a_idx]
    point_b = convex_hull[upper_point_a_idx+1]


    point_a_idx = [i for i, x_y in enumerate(right_region_points_ordered) if x_y[0] == point_a[0]]
    point_b_idx = [i for i, x_y in enumerate(right_region_points_ordered) if x_y[0] == point_b[0]]

    max_dist = 0
    point_c_idx = 0
    for i in range(point_a_idx[0], point_b_idx[0]):
        dist = distance_util.distance_point_to_line(point_a, point_b, right_region_points_ordered[i])
        if dist > max_dist:
            max_dist = dist
            point_c_idx = i
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

    # import numpy
    # from matplotlib import pyplot
    #
    # data = numpy.array(right_region_points_ordered)
    # x, y = data.T
    # pyplot.scatter(x, y, marker='o')
    #
    # data = numpy.array(convex_hull)
    # x, y = data.T
    # pyplot.scatter(x, y, marker='*')
    #
    # data = numpy.array([point_a, point_b, point_c, point_d])
    # x, y = data.T
    # pyplot.scatter(x, y, marker='+')
    #
    # pyplot.show()

    hhd = distance_util.distance_point_to_point(point_c, point_d)
    logging.info('hhd new: {0:0.3f}'.format(hhd))
    return hhd


def get_measurement(alpha_shape):
    logging.info('Start measuring humerus...')

    left_region, _ = bone_region_util.get_left_region(alpha_shape)
    right_region, right_region_points_ordered = bone_region_util.get_right_region(alpha_shape)

    get_hml(alpha_shape)
    get_heb(left_region)
    get_hhd(right_region, right_region_points_ordered)
    get_hhd_new(right_region, right_region_points_ordered)
