# python libraries
import logging
import numpy as np
import open3d as o3d
from sklearn.decomposition import PCA
import alphashape
from shapely import affinity
from shapely.geometry import Polygon

# self defined functions
import utilities


def scale_image(scan_obj):
    # Scale unit length from 1m to 1mm (coordinate 1000x)
    points_center = scan_obj.get_center()
    scan_obj.scale(1000.0, points_center)
    return scan_obj


def mesh_to_points_cloud(scan_obj):
    number_of_points = np.asarray(scan_obj.vertices).shape[0]
    scan_obj.compute_vertex_normals()
    scan_pcd = scan_obj.sample_points_uniformly(number_of_points)
    center = scan_pcd.get_center()
    # print(center)
    return scan_pcd


def remove_background(scan_pcd):
    # find plane using RANSAC: plane function: ax + by + cz + d = 0
    plane_model, inliers = scan_pcd.segment_plane(distance_threshold=2,
                                                  ransac_n=3,
                                                  num_iterations=1000)
    plane = plane_model
    # print(f"Plane equation: {plane[0]:.5f}x + {plane[1]:.5f}y + {plane[2]:.5f}z + {plane[3]:.5f} = 0")

    # floor
    inlier_cloud = scan_pcd.select_by_index(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])

    # bone
    bone_cloud = scan_pcd.select_by_index(inliers, invert=True)
    return bone_cloud, plane


def remove_noise_points(bone_cloud, show_figure):
    cl, ind = bone_cloud.remove_statistical_outlier(nb_neighbors=30,
                                                    std_ratio=0.5)
    # display outliers
    if show_figure:
        utilities.display_inlier_outlier(bone_cloud, ind)

    bone_cloud = bone_cloud.select_by_index(ind)
    return bone_cloud


def project_points_to_plane(bone_cloud, plane, show_figure):
    # project 3D points to the ground plane
    # return points on the ground plane
    # https://math.stackexchange.com/questions/100761/how-do-i-find-the-projection-of-a-point-onto-a-plane
    bone_points = np.array(bone_cloud.points)
    projected_bone_points = []
    for i in range(bone_points.shape[0]):
        point = bone_points[i]
        projected_bone_points.append(utilities.point_to_plane(point, plane))

    bone_points = np.array(projected_bone_points)

    bone_pcd = o3d.geometry.PointCloud()
    bone_pcd.points = o3d.utility.Vector3dVector(bone_points)

    if show_figure:
        o3d.visualization.draw_geometries([bone_pcd, utilities.get_visualization_axis()])
    return bone_pcd


def change_axis_with_PCA(bone_pcd, show_figure):
    # move the center to original point
    bone_points = np.asarray(bone_pcd.points)
    bone_points = bone_points - bone_points.mean(axis=0, keepdims=True)
    # print('bone_points move to original point: ', bone_points)

    pca = PCA(n_components=3)
    pca.fit(bone_points)
    # print('pca.components_: ', pca.components_)

    # use right-hand rule to prevent flipping
    x_ = pca.components_[0]
    y_ = pca.components_[1]
    z_ = np.cross(x_, y_)
    tran_matrix = np.array([x_, y_, z_])
    # print('tran_matrix: ', tran_matrix)

    bone_after_pca = np.dot(tran_matrix, bone_points.T).T
    # print('bone_after_pca: ', bone_after_pca)

    final_pcd = o3d.geometry.PointCloud()
    final_pcd.points = o3d.utility.Vector3dVector(bone_after_pca)
    if show_figure:
        o3d.visualization.draw_geometries([final_pcd, utilities.get_visualization_axis()])

    return final_pcd


def three_d_to_two_d(bone_pcd):
    three_d_points = np.asarray(bone_pcd.points)
    two_d_points = []
    for i in range(three_d_points.shape[0]):
        point = three_d_points[i]
        x = point[0]
        y = point[1]
        two_d_points.append([x, y])

    res = np.array(two_d_points)
    return res


def get_femur_alpha_shape(points):
    # todo: a-value
    alpha_shape = alphashape.alphashape(points, 0.4)
    # fig, ax = plt.subplots()
    # ax.scatter(points[:, 0], points[:,1])
    # ax.add_patch(PolygonPatch(alpha_shape, alpha=1))
    # plt.show()
    (minx, miny, maxx, maxy) = alpha_shape.exterior.bounds
    x_length = maxx - minx
    y_length = maxy - miny

    # object: put head to right bottom part of the image
    # head on the left or right
    left_box = Polygon([(minx, miny), (minx, maxy), (minx + x_length / 10, maxy), (minx + x_length / 10, miny)])
    left_bone = alpha_shape.intersection(left_box)
    right_box = Polygon([(maxx - x_length / 10, miny), (maxx - x_length / 10, maxy), (maxx, maxy), (maxx, miny)])
    right_bone = alpha_shape.intersection(right_box)
    if left_bone.area < right_bone.area:
        alpha_shape = affinity.scale(alpha_shape, xfact=-1, yfact=1, origin=(0, 0))

    # head on the upper or lower part
    center_box = Polygon([(minx + x_length * 0.4, miny), (minx + x_length * 0.4, maxy), (maxx + x_length * 0.6, maxy), (maxx + x_length * 0.6, miny)])
    center_bone = alpha_shape.intersection(center_box)

    if (maxy - center_bone.centroid.y) > y_length / 2:
        alpha_shape = affinity.scale(alpha_shape, xfact=1, yfact=-1, origin=(0, 0))


    # alpha_shape.boundary
    # type(alpha_shape.boundary)
    # alpha_shape.boundary.bounds
    # line = alpha_shape.exterior
    # type(line)

    return alpha_shape


def get_tibia_alpha_shape(points):
    # todo: a-value
    alpha_shape = alphashape.alphashape(points, 0.4)
    return alpha_shape


def get_humerus_alpha_shape(points):
    # todo: a-value
    alpha_shape = alphashape.alphashape(points, 0.4)
    return alpha_shape


def get_radius_alpha_shape(points):
    # todo: a-value
    alpha_shape = alphashape.alphashape(points, 0.4)
    return alpha_shape


def preprocess_bone(scan_obj, bone_type, show_figure):
    logging.info('pre-processing bones...')

    # 1. Scale unit length to 1 mm(coordinate 1000x)
    scan_obj = scale_image(scan_obj)

    # 2. Change mesh to point cloud
    scan_pcd = mesh_to_points_cloud(scan_obj)

    # 3. Remove background
    bone_cloud, plane = remove_background(scan_pcd)

    # 4. Remove noise points
    bone_cloud = remove_noise_points(bone_cloud, show_figure)

    # 5. Project points to plane
    bone_pcd = project_points_to_plane(bone_cloud, plane, show_figure)

    # 6. PCA: find longest axis
    bone_pcd = change_axis_with_PCA(bone_pcd, show_figure)

    # 7. 3d points to 2D points:
    bone_points = three_d_to_two_d(bone_pcd)

    # 7. Get alpha shape
    alpha_shape = None
    if bone_type == 'femur':
        alpha_shape = get_femur_alpha_shape(bone_points)
    elif bone_type == 'tibia':
        alpha_shape = get_tibia_alpha_shape(bone_points)
    elif bone_type == 'humerus':
        alpha_shape = get_humerus_alpha_shape(bone_points)
    elif bone_type == 'radius':
        alpha_shape = get_radius_alpha_shape(bone_points)

    # # 8. Save file
    # if bone_type == 'femur':
    #     o3d.io.write_point_cloud("./data/femur/whole_femur_2d_bone.ply", bone_pcd)
    # elif bone_type == 'tibia':
    #     o3d.io.write_point_cloud("./data/tibia/whole_tibia_2d_bone.ply", bone_pcd)
    # elif bone_type == 'humerus':
    #     o3d.io.write_point_cloud("./data/humerus/whole_humerus_2d_bone.ply", bone_pcd)
    # elif bone_type == 'radius':
    #     o3d.io.write_point_cloud("./data/radius/whole_radius_2d_bone.ply", bone_pcd)

    return alpha_shape

