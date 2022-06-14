# -*- coding: utf-8 -*-

import math
import numpy as np
from scipy.spatial import ConvexHull


def rad_angle(angle):
    r_angle = (angle * math.pi) / 180
    return r_angle


def point_rotation(coordinates, rot_matrix):
    rotated_point_coordinates = np.dot(rot_matrix, np.array(coordinates))
    # x = rotated_point_coordinates[0]
    # y = rotated_point_coordinates[1]
    # z = rotated_point_coordinates[2]
    # rotated_point = np.array([x, y, z])
    return rotated_point_coordinates


def rotation_matrix(x_rotate, z_rotate):
    x_rotate = rad_angle(x_rotate)
    z_rotate = rad_angle(z_rotate)
    rot_matrix_x = np.array([[1., 0., 0, ],
                             [0., math.cos(x_rotate), -math.sin(x_rotate)],
                             [0., math.sin(x_rotate), math.cos(x_rotate)]])

    rot_matrix_z = np.array([[math.cos(z_rotate), -math.sin(z_rotate), 0.],
                             [math.sin(z_rotate), math.cos(z_rotate), 0.],
                             [0., 0., 1.]])

    rot_matrix = np.dot(rot_matrix_x, rot_matrix_z)
    return rot_matrix


def is_point_in_voxel(p, vox_points):
    hull = ConvexHull(vox_points)
    new_points = np.append(vox_points, [p], axis=0)
    new_hull = ConvexHull(new_points)
    if list(hull.vertices) == list(new_hull.vertices):
        # print(p, "is in voxel")
        return True
    else:
        return False


#  Функция для нахождения параметра в параметрическом уравнении прямой, проходящей через точки point1 и point2,
#  пересекающей плоскость ABCD
def find_parameter(plane, point1, point2):
    a, b, c, d = plane
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    l_param = -(a*x1 + b*y1 + c*z1 + d)/(a*(x2 - x1) + b*(y2 - y1) + c*(z2 - z1))
    return l_param


def distance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    dist = ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5
    return dist


def is_point_on_edge_checking(intersection_point, point1, point2):
    check = False
    if (distance(intersection_point, point1) <= distance(point1, point2)) and \
            (distance(intersection_point, point2) <= distance(point1, point2)):
        check = True
    return check


def find_intersection_point(plane, point1, point2):
    l_parameter = find_parameter(plane, point1, point2)
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    x = l_parameter*(x2 - x1) + x1
    y = l_parameter*(y2 - y1) + y1
    z = l_parameter*(z2 - z1) + z1
    intersection_point = (x, y, z)
    return intersection_point



