# python libraries
import sys
import os
from pathlib import Path
import logging
from logging import handlers
import open3d as o3d
import numpy as np
import pywavefront


# self defined functions
from base import Bone
import measure_femur
import measure_humerus
import measure_radius
import measure_tibia
import image_process


# global variants
# logging file info
_root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
_user_logs_file = os.path.join(_root_dir, 'python\\out\\logs\\user_logs', 'logs.txt')  # User logging directory.
# process more files
multi_files = False
index_default = 4
# switch for figure
show_figure = True
# bone type: Bone.Type.FEMUR / Bone.Type.TIBIA / Bone.Type.HUMERUS / Bone.Type.RADIUS
bone_type = Bone.Type.HUMERUS



def load_file(index=index_default):
    obj_dir = os.path.join(_root_dir, 'data', 'color', 'model.obj')
    scan_obj = pywavefront.Wavefront(obj_dir, strict=True, encoding="iso-8859-1", parse=True)

    vertices = np.asarray(scan_obj.vertices) * 1000
    scan_pcd = o3d.geometry.PointCloud()
    scan_pcd.points = o3d.utility.Vector3dVector(vertices)

    if show_figure:
        o3d.visualization.draw_geometries([scan_pcd], mesh_show_wireframe=True)

    return scan_pcd


def scale_image(scan_obj):
    # Scale unit length from 1m to 1mm (coordinate 1000x)
    points_center = scan_obj.get_center()
    scan_obj.scale(1000.0, points_center)
    return scan_obj


def mesh_to_points_cloud(scan_obj):
    # number_of_points = np.asarray(scan_obj.vertices).shape[0]
    # scan_obj.compute_vertex_normals()
    # scan_pcd = scan_obj.sample_points_uniformly(number_of_points)
    # return scan_pcd
    scan_pcd = o3d.geometry.PointCloud()
    scan_pcd.points = scan_obj.vertices
    scan_pcd.colors = scan_obj.vertex_colors
    scan_pcd.normals = scan_obj.vertex_normals

    color_list = np.asarray(scan_obj.vertex_colors)
    ma = np.min(color_list, axis=0)
    print(color_list.shape)


def process_color(scan_obj):
    has_color = scan_obj.colors()
    logging.info(has_color)
    if has_color:
        colors = np.asarray(scan_obj.colors)
        logging.info(colors.shape)


def main():


    # 1. Load file
    load_file()


if __name__ == "__main__":
    main()

