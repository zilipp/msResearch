# python libraries
import logging
from shapely.geometry import Polygon

# self defined functions
import utilities


def get_tml(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    tml = maxx - minx
    logging.info('tml: {0:0.3f}'.format(tml))


def get_tpb(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    tpb = maxy - miny
    logging.info('tpb: {0:0.3f}'.format(tpb))


def get_measurement(alpha_shape):
    logging.info('Start measuring tibia...')
    get_tml(alpha_shape)
    get_tpb(alpha_shape)