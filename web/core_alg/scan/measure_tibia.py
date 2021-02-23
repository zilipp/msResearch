# python libraries
import logging
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from core_alg.base import Filefolder
from core_alg.utilities import bone_region_util
from core_alg.utilities import rotate_utils


def tune_params(device):
    # parameter to tune error
    global tml_coeff, tpb_coeff
    # if device == Filefolder.Type.SENSOR_I:
    #     tml_coeff = 0.995
    #     tpb_coeff = 0.985
    # else:
    #     tml_coeff = 0.9988
    #     tpb_coeff = 0.9584
    tml_coeff = 1
    tpb_coeff = 1


def get_tml(alpha_shape, show_figure, left_bone_points_ordered, right_bone_points_ordered):
    (min_x, min_y, max_x, max_y) = alpha_shape.exterior.bounds
    x_length = max_x - min_x
    y_length = max_y - min_y

    # left-upper box
    left_upper_box = Polygon([(min_x, min_y + y_length * 0.75), (min_x, max_y), (min_x + x_length / 10, max_y), (min_x + x_length / 10, min_y + y_length * 0.75)])
    left_upper_bone = alpha_shape.intersection(left_upper_box)
    (min_x_left_upper, _, _, _) = left_upper_bone.exterior.bounds


    # left-lower box
    left_lower_box = Polygon([(min_x, min_y), (min_x, min_y + y_length * 0.25), (min_x + x_length / 10, min_y + y_length * 0.25),
                              (min_x + x_length / 10,  min_y)])
    left_lower_bone = alpha_shape.intersection(left_lower_box)
    (min_x_left_lower, _, _, _) = left_lower_bone.exterior.bounds

    poi_x = min(min_x_left_upper, min_x_left_lower)
    tml = max_x - poi_x

    if not show_figure:
        # most left point, 1st POIs
        # possibly POI is the intersection with box and bone,
        # x != poi_x, the point is on the box
        p_left = []
        box_min_y = min_y + y_length * 0.25
        box_max_y = min_y + y_length * 0.75
        for i in range(len(left_bone_points_ordered)):
            if box_max_y > left_bone_points_ordered[i][1] > box_min_y:
                continue
            if left_bone_points_ordered[i][0] - poi_x < 1:
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

        p_rec_left_bottom = [min_x - 20, min_y + y_length * 0.25]
        rect = patches.Rectangle((p_rec_left_bottom[0], p_rec_left_bottom[1]), 40, y_length * 0.5, linestyle='dashed',
                                 linewidth=0.5, edgecolor='b', facecolor='none')
        ax.add_patch(rect)
        ax.set_aspect('equal')
        plt.show()

    tml /= tml_coeff
    return tml


def get_tpb(alpha_shape, show_figure, left_bone, left_bone_points_ordered):
    (left_bone_min_x, left_bone_min_y, left_bone_max_x,
     left_bone_max_y) = left_bone.exterior.bounds
    tpb = left_bone_max_y - left_bone_min_y
    rotated_list = []
    max_tpb_index = 0
    tpb_index = 0
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
        cur_tpb = max_y - min_y
        if cur_tpb >= tpb:
            tpb = cur_tpb
            max_tpb_index = tpb_index
            point_a_y = max_y
            point_b_y = min_y

        tpb = max(tpb, cur_tpb)
        tpb_index += 1

    if not show_figure:
        max_feb_points = rotated_list[max_tpb_index]
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

    tpb /= tpb_coeff
    return tpb


def get_measurement(tibia, show_figure, device=None):
    logging.info('Start measuring tibia')
    tune_params(device)

    left_region, left_region_points_ordered = bone_region_util.get_left_region(
        tibia.alpha_shape)
    _, right_region_points_ordered = bone_region_util.get_right_region(
        tibia.alpha_shape)
    tibia.tml = get_tml(tibia.alpha_shape, show_figure, left_region_points_ordered, right_region_points_ordered)
    tibia.tpb = get_tpb(tibia.alpha_shape, show_figure, left_region, left_region_points_ordered)
