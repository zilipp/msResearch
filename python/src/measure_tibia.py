# python libraries
import logging
from shapely.geometry import Polygon

from base import Bone

tml_coeff = 0.995
tpb_coeff = 0.985


def get_tml(alpha_shape):
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

    tml = max_x - min(min_x_left_upper, min_x_left_lower)
    tml /= tml_coeff
    logging.info('tml: {0:0.3f}'.format(tml))
    return tml


def get_tpb(alpha_shape):
    (min_x, min_y, max_x, max_y) = alpha_shape.exterior.bounds
    tpb = max_y - min_y
    tpb /= tpb_coeff
    logging.info('tpb: {0:0.3f}'.format(tpb))
    return tpb


def get_measurement(tibia, show_figure=False):
    logging.info('Start measuring tibia')
    tibia.tml = get_tml(tibia.alpha_shape)
    tibia.tpb = get_tpb(tibia.alpha_shape)
