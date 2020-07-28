# python libraries
import logging


def get_tml_and_tpb(alpha_shape):
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    tml = maxx - minx
    logging.info('tml: {0:0.3f}'.format(tml))

    tpb = maxy - miny
    logging.info('tpb: {0:0.3f}'.format(tpb))


def get_measurement(alpha_shape):
    logging.info('Start measuring tibia...')
    get_tml_and_tpb(alpha_shape)
