# python libraries
import sys
import os
from pathlib import Path
import logging
from logging import handlers
import open3d as o3d

# self defined functions
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
multi_files = True
index_default = 2
# switch for figure
show_figure = False
# bone type: 'femur' / 'tibia' / 'humerus' / 'radius'
bone_type = 'femur'


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
    obj_dir = os.path.join(_root_dir, 'data', bone_type, '{}_{}.obj'.format(bone_type, str(index)))
    scan_obj = o3d.io.read_triangle_mesh(obj_dir)

    logging.info('Loading {0} file from {1}'.format(bone_type, obj_dir))
    logging.info(scan_obj)

    if show_figure:
        o3d.visualization.draw_geometries([scan_obj], mesh_show_wireframe=True)
    return scan_obj


def main():
    # 0. Prepare logging file
    init_logger(_user_logs_file)

    # 1. Load file
    scan_obj = load_file()

    # 2. 3D model pre-processing
    alpha_shape = image_process.preprocess_bone(scan_obj, bone_type, show_figure)

    # 3 Measurements
    if bone_type == 'femur':
        measure_femur.get_measurement(alpha_shape, show_figure)
    elif bone_type == 'tibia':
        measure_tibia.get_measurement(alpha_shape)
    elif bone_type == 'humerus':
        measure_humerus.get_measurement(alpha_shape)
    elif bone_type == 'radius':
        measure_radius.get_measurement(alpha_shape, show_figure)


def multi_main():
    # 0. Prepare logging file
    init_logger(_user_logs_file)

    for i in range(9):
        # 1. Load file
        scan_obj = load_file(i)

        # 2. 3D model pre-processing
        alpha_shape = image_process.preprocess_bone(scan_obj, bone_type, show_figure)

        # 3 Measurements
        if bone_type == 'femur':
            measure_femur.get_measurement(alpha_shape, show_figure)
        elif bone_type == 'tibia':
            measure_tibia.get_measurement(alpha_shape)
        elif bone_type == 'humerus':
            measure_humerus.get_measurement(alpha_shape)
        elif bone_type == 'radius':
            measure_radius.get_measurement(alpha_shape, show_figure)


if __name__ == "__main__":
    if multi_files:
        multi_main()
    else:
        main()

