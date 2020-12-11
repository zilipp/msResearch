import logging
import math
import numpy as np
import os
import open3d as o3d
import pywavefront
from pathlib import Path

# self defined functions
from core_alg.utilities import logging_utils
from core_alg.utilities import visualization_util

"""
This file is a separate file that compare iphone and sensor taking the same picture
"""

# global variables
# root directory
_root_dir = Path(os.path.dirname(os.path.abspath(__file__)))  # compare_box

# user log directory
_user_logs_file = os.path.join(
    _root_dir.parent, 'out', 'core_alg', 'logs', 'logs.txt')

# switch for figure
show_figure = True
# switch for structure sensor or iphone10
structure_sensor = True


# params for remove background
distance_threshold = 1
ransac_n = 3
num_iterations = 10000

nb_neighbors = 50
std_ratio = 2


def load_file(index=0):
    if structure_sensor:
        device = 'struct'
    else:
        device = 'iphone'
    obj_dir = os.path.join(_root_dir, 'data', device,
                           '{}_{}.obj'.format(device, str(index)))

    logging.info('Loading {0} dataset from {1}'.format(device, obj_dir))
    scan_obj = pywavefront.Wavefront(
        obj_dir, strict=True, encoding="iso-8859-1", parse=True)

    # Scale unit length to 1 mm(coordinate 1000x)
    vertices = np.asarray(scan_obj.vertices) * 1000

    if not structure_sensor:
        # iphone_ten image has color info on "v" line
        vertices = vertices[:, :3]

    scan_pcd = o3d.geometry.PointCloud()
    scan_pcd.points = o3d.utility.Vector3dVector(vertices)

    if show_figure:
        o3d.visualization.draw_geometries([scan_pcd], mesh_show_wireframe=True)
    return scan_pcd, vertices.shape[0]


def remove_background(scan_pcd, show_figure):
    """
    return object outside the plane and function of plane
    """
    # find plane using RANSAC: plane function: ax + by + cz + d = 0
    # todo: check for randomness
    plane_model, inliers = scan_pcd.segment_plane(distance_threshold=distance_threshold,
                                                  ransac_n=ransac_n,
                                                  num_iterations=num_iterations)

    plane = plane_model
    # print(f"Plane equation: {plane[0]:.5f}x + {plane[1]:.5f}y + {plane[2]:.5f}z + {plane[3]:.5f} = 0")

    # floor
    inlier_cloud = scan_pcd.select_by_index(inliers)

    inlier_cloud.paint_uniform_color([1.0, 0, 0])

    # bone
    obj_cloud = scan_pcd.select_by_index(inliers, invert=True)
    # show image without background
    if show_figure:
        o3d.visualization.draw_geometries([obj_cloud], mesh_show_wireframe=True)
    return obj_cloud, plane, np.asarray(obj_cloud.points).shape[0]


def remove_noise_points(bone_cloud, show_figure):
    cl, ind = bone_cloud.remove_statistical_outlier(nb_neighbors=nb_neighbors,
                                                    std_ratio=std_ratio)

    # display outliers
    if show_figure:
        visualization_util.display_inlier_outlier(bone_cloud, ind)

    bone_cloud = bone_cloud.select_by_index(ind)
    return bone_cloud


def angle_of_two_plane(plane_1, plane_2):
    """
    plane: [A B C D]
    Ax + By +Cz + D = 0
    """
    [a1, b1, c1, d1] = plane_1
    [a2, b2, c2, d2] = plane_2
    d = (a1 * a2 + b1 * b2 + c1 * c2)
    e1 = math.sqrt(a1 * a1 + b1 * b1 + c1 * c1)
    e2 = math.sqrt(a2 * a2 + b2 * b2 + c2 * c2)
    d = d / (e1 * e2)
    A = math.degrees(math.acos(d))
    return A


def get_plane_plane_intersection(plane_1, plane_2):
    """
    Returns line direction, and a point on the line
      - plane_1:  A1 * x + B1 * y + C1 * z + D1 = 0
      - plane_2:  A2 * x + B2 * y + C2 * z + D2 = 0
      - direction [A3 B3 C3] = cross([A1 B1 C1], [A2, B2, C2])
      - point on line [x1, y1, z1]
        A1*x1 + B1*y1 + C1*z1 + D1 = 0
        A2*x1 + B2*y1 + C2*z1 + D2 = 0
        A3*x1 + B3*y1 + C3*z1 = 0
      - line function:
        x = x1 + A3 * t
        y = y1 + B3 * t
        z = z1 + C3 * t
    """
    # direction of the line:
    a_vec, b_vec = np.array(plane_1[:3]), np.array(plane_2[:3])
    direction_vec = np.cross(a_vec, b_vec)

    # a point on the plane
    A = np.array([a_vec, b_vec, direction_vec])
    d = np.array([-plane_1[3], -plane_2[3], 0.]).reshape(3, 1)
    # If A and B are parallel, a numpy.linalg.LinAlgError exception is raised
    p_inter = np.linalg.solve(A, d).T

    return direction_vec, p_inter


def normalized(X):
    return X/np.sqrt(np.sum(X ** 2))


def dis_point_to_line(point, point_on_line, line_direction):
    """
    https://onlinemschool.com/math/library/analytic_geometry/p_line/
    	 |M0M1×s|
     d = ---------
            |s|
    point: M0
    point_on_line: M1
    line_direction: [s0 s1 s2]
    """
    M0 = np.asarray(point)
    M1 = np.asarray(point_on_line)

    s = np.asarray(line_direction)
    M0_M1 = M1 - M0
    M0_M1Xs = np.cross(M0_M1, s)
    M0_M1Xs_magnitude = np.linalg.norm(M0_M1Xs)
    s_magnitude = np.linalg.norm(s)

    d = M0_M1Xs_magnitude / s_magnitude
    return d


def get_box_length(scan_pcd, obj_cloud, plane_1, plane_2):
    """
    scan_pcd: original all points
    obj_cloud: residuals
    """

    # all points
    all_points = np.asarray(scan_pcd.points)

    # intersection of two plane
    direction_vec, p_inter = get_plane_plane_intersection(plane_1, plane_2)

    # points near intersection plane
    point_in_intersection_line = []
    for point in all_points:
        if dis_point_to_line(point, p_inter, direction_vec) <= 5:
            point_in_intersection_line.append(point)

    print(len(point_in_intersection_line))
    point_in_intersection = np.asarray(point_in_intersection_line)
    point_in_intersection_pcd = o3d.geometry.PointCloud()
    point_in_intersection_pcd.points = o3d.utility.Vector3dVector(point_in_intersection)
    point_in_intersection_pcd.paint_uniform_color([0, 0, 0])
    if show_figure:
        o3d.visualization.draw_geometries([scan_pcd, point_in_intersection_pcd], mesh_show_wireframe=True)



    print(len(point_in_intersection_line))







if __name__ == "__main__":
    logging_utils.init_logger(_user_logs_file)
    logging.info("setup")

    # load file, return pcd and numeber of points
    scan_pcd, number_points_all = load_file()
    print(number_points_all)

    # remove ground
    obj_cloud, plane_g, number_residual_g = remove_background(scan_pcd, show_figure)
    print("after removing ground", plane_g, number_residual_g)

    # remove face1
    obj_cloud, plane_1, number_residual_1 = remove_background(obj_cloud, show_figure)
    print("after removing one face", plane_1, number_residual_1)

    # remove face2
    obj_cloud, plane_2, number_residual_2 = remove_background(obj_cloud, show_figure)
    print("after removing two faces", plane_2, number_residual_2)

    # 1. angle of two vector
    angle_two_face = angle_of_two_plane(plane_1, plane_2)
    print("Angle of two plane is:", angle_two_face, "degree")

    # 3. number_residuals / number_input_points
    print("ratio of residuals / all input points: ", number_residual_2/number_points_all)

    # 2. distance
    get_box_length(scan_pcd, obj_cloud, plane_1, plane_2)









