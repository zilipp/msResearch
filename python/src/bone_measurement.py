# python libraries
import sys
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

# self defined functions
import measure_femur
import measure_humerus
import measure_radius
import measure_tibia
import image_process


# global variants
# switch for figure
show_figure = True

# 'femur' / 'tibia' / 'humerus' / 'radius'
bone_type = 'femur'


def load_file():
    print('loading file...')
    scan_obj = o3d.io.read_triangle_mesh("../../data/femur_half_4.obj")
    print(scan_obj)
    if show_figure:
        o3d.visualization.draw_geometries([scan_obj], mesh_show_wireframe=True)
    return scan_obj


def main():
    # 1. Load file
    scan_obj = load_file()

    # 2. 3D model pre-processing
    alpha_shape = image_process.preprocess_bone(scan_obj, bone_type, show_figure)

    # 3 Measurements
    if bone_type == 'femur':
        measure_femur.get_measurement(alpha_shape, show_figure)
    elif bone_type == 'tibia':
        measure_tibia.get_measurement()
    elif bone_type == 'humerus':
        measure_humerus.get_measurement()
    elif bone_type == 'radius':
        measure_radius.get_measurement()


if __name__ == "__main__":
    main()
