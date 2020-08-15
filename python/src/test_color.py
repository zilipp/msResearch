# python libraries
import sys
import os
from pathlib import Path
import logging
from logging import handlers
import open3d as o3d
import numpy as np

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


def init_logger(log_file=_user_logs_file):
    if not os.path.exists(log_file):
        os.makedirs(os.path.dirname(log_file))

    log = logging.getLogger('')
    log.setLevel(logging.INFO)
    output_format = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    std_out_handler = logging.StreamHandler(sys.stdout)
    std_out_handler.setFormatter(output_format)
    logging.getLogger().addHandler(std_out_handler)
    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=(1048576*5), backupCount=7)
    file_handler.setFormatter(output_format)
    logging.getLogger().addHandler(file_handler)


def load_file(index=index_default):
    obj_dir = os.path.join(_root_dir, 'data', 'color', 'model.obj')
    # obj_dir = os.path.join(_root_dir, 'data', Bone.Type.FEMUR, 'femur_0.obj')
    scan_obj = o3d.io.read_triangle_mesh(obj_dir)

    logging.info('Loading {0} file from {1}'.format(bone_type, obj_dir))
    logging.info(scan_obj)

    if show_figure:
        o3d.visualization.draw_geometries([scan_obj], mesh_show_wireframe=True)
    return scan_obj


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
    # 0. Prepare logging file
    init_logger(_user_logs_file)

    # 1. Load file
    scan_obj = load_file()
    scan_obj = scale_image(scan_obj)
    scan_pcd = mesh_to_points_cloud(scan_obj)
    process_color(scan_obj)

    # # 2. 3D model pre-processing
    # alpha_shape = image_process.preprocess_bone(scan_obj, bone_type, show_figure)
    #
    # # 3 Measurements
    # if bone_type == Bone.Type.FEMUR:
    #     measure_femur.get_measurement(alpha_shape, show_figure)
    # elif bone_type == Bone.Type.TIBIA:
    #     measure_tibia.get_measurement(alpha_shape)
    # elif bone_type == Bone.Type.HUMERUS:
    #     measure_humerus.get_measurement(alpha_shape, show_figure)
    # elif bone_type == Bone.Type.RADIUS:
    #     measure_radius.get_measurement(alpha_shape, show_figure)



if __name__ == "__main__":
    main()

