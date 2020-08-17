# python libraries
import logging
import os
import open3d as o3d
import sys

from datetime import datetime
from logging import handlers
from pathlib import Path

# self defined functions
from base import Bone
import image_process


# global variables
# logging file info
_root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
# user log directory
_user_logs_file = os.path.join(_root_dir, 'python\\out\\logs\\user_logs', 'logs.txt')
_user_result_dir = os.path.join(_root_dir, 'python\\out\\results')
# process more files
multi_files = True
index_default = 4
# switch for figure
show_figure = False
bone_type = Bone.Type.RADIUS


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
    bone_type_str = bone_type.name.lower()
    obj_dir = os.path.join(_root_dir, 'data', bone_type_str, '{}_{}.obj'.format(bone_type_str, str(index)))
    scan_obj = o3d.io.read_triangle_mesh(obj_dir)

    logging.info('Loading {0} dataset from {1}'.format(bone_type_str, obj_dir))
    logging.info(scan_obj)

    if show_figure:
        o3d.visualization.draw_geometries([scan_obj], mesh_show_wireframe=True)
    return scan_obj


def process(scan_obj):
    # 1. Init Bone
    bone = None
    if bone_type == Bone.Type.FEMUR:
        bone = Bone.Femur()
    elif bone_type == Bone.Type.HUMERUS:
        bone = Bone.Humerus()
    elif bone_type == Bone.Type.RADIUS:
        bone = Bone.Radius()
    elif bone_type == Bone.Type.TIBIA:
        bone = Bone.Tibia()

    # 2. 3D model pre-processing
    alpha_shape = image_process.preprocess_bone(scan_obj, bone_type, show_figure)
    bone.set_alpha_shape(alpha_shape)

    # 3 Measurements
    bone.measure(show_figure)
    results = bone.get_measurement_results()
    logging.info(results)
    bone.reset_alpha_shape()

    return bone


def csv_out(bones):
    bone_type_str = bone_type.name.lower()
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    filename = '{}-{}.csv'.format(dt_string, bone_type_str)
    output_file = os.path.join(_user_result_dir, filename)
    if not os.path.exists(_user_result_dir):
        os.makedirs(_user_result_dir)
    logging.info('Writing results to {}'.format(output_file))
    f = open(output_file, 'w')

    result = bones[0].get_measurement_results()
    keys = sorted(result)
    title = ','.join(keys)
    f.write(title+'\n')
    for bone in bones:
        row = list()
        measurement_results = bone.get_measurement_results()
        for key in keys:
            row.append(str(measurement_results[key]))
        line = ','.join(row)
        f.write(line+'\n')
    f.close()


if __name__ == "__main__":
    init_logger(_user_logs_file)

    bones = list()
    if multi_files:
        for i in range(9):
            # 1. Load file
            scan_obj = load_file(i)
            bones.append(process(scan_obj))
    else:
        scan_obj = load_file()
        bones.append(process(scan_obj))

    csv_out(bones)

