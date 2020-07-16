# python libraries
import logging
from shapely.geometry import Polygon

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

    diff_last = abs(left_bone_points[len(left_bone_points) - 1][1] - left_bone_points[0][1])
    if diff_last > max_diff_y:
        max_diff_y = diff_last
        a_idx = len(left_bone_points) - 1

    # a(-, +), b(-, -)
    # point_a = left_bone_points[a_idx]
    # point_b = left_bone_points[(a_idx + 1) % len(left_bone_points)]
    # start with point_b(right-lower point)
    left_bone_points_ordered = left_bone_points[a_idx + 1:] + left_bone_points[:a_idx + 1]

    return left_bone, left_bone_points_ordered


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

    diff_last = abs(right_bone_points[len(right_bone_points) - 1][1] - right_bone_points[0][1])
    if diff_last > max_diff_y:
        a_idx = len(right_bone_points) - 1

    # a(+, -), b(+, +)
    # point_a = right_bone_points[a_idx]
    # point_b = right_bone_points[(a_idx + 1) % len(right_bone_points)]
    # start with point_b(left-upper point)
    right_bone_points_ordered = right_bone_points[a_idx + 1:] + right_bone_points[:a_idx + 1]
    return right_bone, right_bone_points_ordered


def get_hml(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    hml = maxx - minx
    logging.info('hml: {0:0.3f}'.format(hml))


def get_heb(left_bone):
    (left_bone_minx, left_bone_miny, left_bone_maxx, left_bone_maxy) = left_bone.exterior.bounds
    heb = left_bone_maxy - left_bone_miny
    logging.info('heb: {0:0.3f}'.format(heb))


def get_hhd(right_bone, right_bone_points_ordered):
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
    hhd = utilities.distance_point_to_point(p_start, p_start_2)
    count_decrease = 0

    # 7. start_point开始，向上遍历点 tmp_point1， 更新tmp_line   tmp_point1_y = tmp1_point_x+b
    # 8. 每次遍历，找到在上次tmp_point2附近的一个新点，使得新点到直线tmp_line距离最短
    # tmp_point2更新为新的点，然后计算tmp_point2在直线tmp_line上的投影tmp_point3 到 tmp_point1的距离，存入dist list
    # 依次循环,dist应该先增大，后减小，我们要找到的就是增到极大值，开始减小时候的那个极大的距离

    def find_down_left(p1, from_idx, right_bone_points_ordered_array):
        cur_intercept = p1[1] - p1[0]
        right_side = True
        while right_side and from_idx < len(right_bone_points_ordered_array):
            candidate_x = right_bone_points_ordered_array[from_idx][0]
            candidate_y = right_bone_points_ordered_array[from_idx][1]
            if candidate_x + cur_intercept <= candidate_y:
                right_side = False
            from_idx += 1

        if from_idx == len(right_bone_points_ordered_array):
            return None
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
        if p_down_left is None:
            break

        cur_fhd = utilities.distance_point_to_point(p_up_right, p_down_left)
        hhd = max(hhd, cur_fhd)
        if cur_fhd < hhd:
            count_decrease += 1
            if count_decrease >= 5:
                break
        else:
            count_decrease = 0
        iterate_idx -= 1
    logging.info('hhd: {0:0.3f}'.format(hhd))


def get_measurement(alpha_shape, show_figure):
    logging.info('Start measuring humerus...')

    left_bone, left_bone_points_ordered = get_left_part(alpha_shape)
    right_bone, right_bone_points_ordered = get_right_part(alpha_shape)

    get_hml(alpha_shape)
    get_heb(left_bone)
    get_hhd(right_bone, right_bone_points_ordered)