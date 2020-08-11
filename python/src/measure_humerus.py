# python libraries
import logging
from shapely.geometry import Polygon
import numpy
from matplotlib import pyplot

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


def get_hhd(bone_right_region, right_region_points_ordered, show_figure):
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

    num_of_points_between_a_b = point_b_idx[0] - point_a_idx[0]
    if num_of_points_between_a_b >= 3:
        for i in range(point_a_idx[0], point_b_idx[0] - 2):
            dist = 0
            for j in range(0, 3):
                dist = dist + distance_util.distance_point_to_line(point_a, point_b, right_region_points_ordered[i+j])
            if dist > max_dist:
                max_dist = dist
                point_c_idx = i + 1

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
        data = numpy.array(right_region_points_ordered)
        x, y = data.T
        pyplot.scatter(x, y, marker='o')

        data = numpy.array(convex_hull)
        x, y = data.T
        pyplot.scatter(x, y, marker='*')

        data = numpy.array([point_a, point_b, point_c, point_d])
        x, y = data.T
        pyplot.scatter(x, y, marker='+')

        pyplot.axis('equal')
        pyplot.show()

    hhd = distance_util.distance_point_to_point(point_c, point_d)
    logging.info('hhd: {0:0.3f}'.format(hhd))
    return hhd


def get_measurement(alpha_shape, show_figure):
    logging.info('Start measuring humerus...')

    left_region, _ = bone_region_util.get_left_region(alpha_shape)
    right_region, right_region_points_ordered = bone_region_util.get_right_region(alpha_shape)

    get_hml(alpha_shape)
    get_heb(left_region)
    get_hhd(right_region, right_region_points_ordered, show_figure)
