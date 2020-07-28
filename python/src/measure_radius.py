# python libraries
import logging
import numpy as np
import math
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

# self defined functions
from utilities import distance_util
from utilities import bone_region_util


def get_rml(alpha_shape):
    (min_x, min_y, max_x, max_y) = alpha_shape.exterior.bounds
    rml = max_x - min_x
    logging.info('rml: {0:0.3f}'.format(rml))


def get_rmld(center_bone_points, show_figure):
    center_bone_points = np.asarray(center_bone_points)
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
    rmld = poly.polyval(0, top_line_p) - poly.polyval(0, bottom_line_p)

    min_line_segment_length = rmld ** 2
    for i in np.arange(-30, 30, .05):
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

    rmld = math.sqrt(min_line_segment_length)
    logging.info('rmld: {0:0.3f}'.format(rmld))
    return rmld


def get_measurement(alpha_shape, show_figure):
    logging.info('Start measuring radius...')

    center_region, center_region_points = bone_region_util.get_center_region(alpha_shape)

    get_rml(alpha_shape)
    get_rmld(center_region_points, show_figure)
