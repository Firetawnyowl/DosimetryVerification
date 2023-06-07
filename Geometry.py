# -*- coding: utf-8 -*-

import math
import numpy as np
from scipy.spatial import ConvexHull
from numba import njit


@njit(cache=True)
def rad_angle(angle):
    r_angle = (angle * math.pi) / 180
    return r_angle


@njit(cache=True)
def point_rotation(coordinates, rot_matrix):
    coordinates = np.array([[coordinates[0], 0., 0.],
                            [coordinates[1], 0., 0.],
                            [coordinates[2], 0., 0.]])
    rotated_point_coordinates = np.dot(rot_matrix, coordinates)
    x = rotated_point_coordinates[0][0]
    y = rotated_point_coordinates[1][0]
    z = rotated_point_coordinates[2][0]
    rotated_point = np.array([x, y, z])
    return rotated_point


@njit(cache=True)
def rotation_matrix(x_rotate, z_rotate):
    x_rotate = rad_angle(x_rotate)
    z_rotate = rad_angle(z_rotate)
    rot_matrix_x = np.array([[1., 0., 0., ],
                             [0., math.cos(x_rotate), -math.sin(x_rotate)],
                             [0., math.sin(x_rotate), math.cos(x_rotate)]])

    rot_matrix_z = np.array([[math.cos(z_rotate), -math.sin(z_rotate), 0.],
                             [math.sin(z_rotate), math.cos(z_rotate), 0.],
                             [0., 0., 1.]])

    rot_matrix = np.dot(rot_matrix_x, rot_matrix_z)
    return rot_matrix


@njit(cache=True)
def voxel_boundaries(voxel_size, voxel):
    boundaries = np.zeros(shape=(3, 2))
    boundaries[0, 0] = voxel[0] - voxel_size[0] / 2
    boundaries[0, 1] = voxel[0] + voxel_size[0] / 2
    boundaries[1, 0] = voxel[1] - voxel_size[1] / 2
    boundaries[1, 1] = voxel[1] + voxel_size[1] / 2
    boundaries[2, 0] = voxel[2] - voxel_size[2] / 2
    boundaries[2, 1] = voxel[2] + voxel_size[2] / 2
    return boundaries


@njit(cache=True)
def is_point_in_fixed_voxel(p, voxel, voxel_size):
    vox_boundaries = voxel_boundaries(voxel_size, voxel)
    # print("fix_vox_bound: ", vox_boundaries)
    # print("point", p, type(p))
    # print("round", round(p[0], 3), round(p[1], 3), round(p[2], 3))
    # print("voxel: ", voxel)
    if (((vox_boundaries[0][0]-0.00001) <= round(p[0], 3) <= (vox_boundaries[0][1]+0.00001)) and ((vox_boundaries[1][0]-0.00001) <= round(p[1], 3) <= (vox_boundaries[1][1]+0.00001))
            and ((vox_boundaries[2][0]-0.00001) <= round(p[2], 3) <= (vox_boundaries[2][1])+0.00001)):
        # print("point IS in voxel")
        return True
    else:
        return False


@njit(cache=True)
def projection_to_plain(point, plane):
    a, b, c, d = plane
    t = -((a * point[0] + b * point[1] + c * point[2] + d) / (a * a + b * b + c * c))
    x_new = a * t + point[0]
    y_new = b * t + point[1]
    z_new = c * t + point[2]
    projected_point = (x_new, y_new, z_new)
    return projected_point

# def is_point_in_movable_voxel(p, vox_plains, vox_size):
#     # print("point: ", p, "distance: ", distance(p, projection_to_plain(p, vox_plains[0])) + distance(p, projection_to_plain(p, vox_plains[1])), "vox_x: ", vox_size[0])
#     # print("point: ", p, "distance: ", distance(p, projection_to_plain(p, vox_plains[2])) + distance(p, projection_to_plain(p, vox_plains[3])), "vox_y: ", vox_size[1])
#     # print("point: ", p, "distance: ", distance(p, projection_to_plain(p, vox_plains[4])) + distance(p, projection_to_plain(p, vox_plains[5])), "vox_z: ", vox_size[2])
#     if (math.isclose(distance(p, projection_to_plain(p, vox_plains[0])) + distance(p, projection_to_plain(p, vox_plains[1])), vox_size[0], abs_tol=1e-03) and
#             math.isclose(distance(p, projection_to_plain(p, vox_plains[2])) + distance(p, projection_to_plain(p, vox_plains[3])), vox_size[1], abs_tol=1e-03) and
#             math.isclose(distance(p, projection_to_plain(p, vox_plains[4])) + distance(p, projection_to_plain(p, vox_plains[5])), vox_size[2], abs_tol=1e-03)):
#         return True
#     else:
#         return False

@njit(cache=True)
def is_point_in_movable_voxel(p, vox_plains, vox_size):
    if (round(distance(p, projection_to_plain(p, vox_plains[0])) + distance(p, projection_to_plain(p, vox_plains[1])), 3) == round(vox_size[0], 3) and
            round(distance(p, projection_to_plain(p, vox_plains[2])) + distance(p, projection_to_plain(p, vox_plains[3])), 3) == round(vox_size[1], 3) and
            round(distance(p, projection_to_plain(p, vox_plains[4])) + distance(p, projection_to_plain(p, vox_plains[5])), 3) == round(vox_size[2], 3)):
        return True
    else:
        return False

# def is_point_in_voxel(p, vox_points):
#     hull = ConvexHull(vox_points)
#     new_points = np.append(vox_points, [p], axis=0)
#     new_hull = ConvexHull(new_points)
#     if list(hull.vertices) == list(new_hull.vertices):
#         # print(p, "is in voxel")
#         return True
#     else:
#         return False


#  Функция для нахождения параметра в параметрическом уравнении прямой, проходящей через точки point1 и point2,
#  пересекающей плоскость ABCD
@njit(cache=True)
def find_parameter(plane, point1, point2):
    a, b, c, d = plane
    x1, y1, z1 = point1
    x2, y2, z2 = point2

    m = (a * (x2 - x1) + b * (y2 - y1) + c * (z2 - z1))
    if m != 0:
        l_param = -(a * x1 + b * y1 + c * z1 + d) / m
    else:
        l_param = None
    return l_param


@njit(cache=True)
def distance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
    return dist


@njit(cache=True)
def is_point_on_edge_checking(intersection_point, point1, point2):
    check = False
    if (round(distance(intersection_point, point1), 3) <= round(distance(point1, point2), 3)) and \
            (round(distance(intersection_point, point2), 3) <= round(distance(point1, point2), 3)):
        check = True
    return check


@njit(cache=True)
def find_intersection_point(plane, point1, point2):
    l_parameter = find_parameter(plane, point1, point2)
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    if l_parameter is not None:
        x = l_parameter * (x2 - x1) + x1
        y = l_parameter * (y2 - y1) + y1
        z = l_parameter * (z2 - z1) + z1
        intersection_point = (x, y, z)
    else:
        intersection_point = None
    return intersection_point
