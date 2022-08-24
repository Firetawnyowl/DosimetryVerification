# -*- coding: utf-8 -*-

import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial.qhull
from scipy.spatial import ConvexHull
import Phantom
import VoxelStructure
import Geometry


def find_neighbors(voxels, fixed_voxel_indexes):
    x, y, z = fixed_voxel_indexes
    neighbors = []
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            for k in [z-1, z, z+1]:
                if i >= 0 and j >= 0 and k >= 0:
                    try:
                        neighbor_voxel = voxels[i, j, k]
                        neighbors.append([neighbor_voxel, (i, j, k)])
                    except IndexError:
                        continue
    return neighbors


def check_intersection_with_fixed_voxel(fixed_voxel, fixed_voxel_size, movable_voxel_corners):
    check = False
    for point in movable_voxel_corners:
        if Geometry.is_point_in_fixed_voxel(point, fixed_voxel, fixed_voxel_size):
            check = True
    return check


def check_special_case_intersection_with_fixed_voxel(phantom_voxel_size, fixed_voxel, movable_voxel_corners):
    bound = Geometry.voxel_boundaries(phantom_voxel_size, fixed_voxel)
    low_x_check = high_x_check = False
    low_y_check = high_y_check = False
    low_z_check = high_z_check = False
    point_in_x_boundaries = point_in_y_boundaries = point_in_z_boundaries = False
    for point in movable_voxel_corners:
        if point[0] < bound[0][0]:
            low_x_check = True
        if point[0] > bound[0][1]:
            high_x_check = True
        if bound[0][0] <= point[0] <= bound[0][1]:
            point_in_x_boundaries = True
        if point[1] < bound[1][0]:
            low_y_check = True
        if point[1] > bound[1][1]:
            high_y_check = True
        if bound[1][0] <= point[1] <= bound[1][1]:
            point_in_y_boundaries = True
        if point[2] < bound[2][0]:
            low_z_check = True
        if point[2] > bound[2][1]:
            high_z_check = True
        if bound[2][0] <= point[2] <= bound[2][1]:
            point_in_z_boundaries = True
    if (((low_x_check and high_x_check) and (low_y_check and high_y_check) and (low_z_check and high_z_check)) or
            ((low_x_check and high_x_check) and (low_y_check and high_y_check) and point_in_z_boundaries) or
            ((low_x_check and high_x_check) and point_in_y_boundaries and point_in_z_boundaries) or
            ((low_x_check and high_x_check) and (low_z_check and high_z_check) and point_in_y_boundaries) or
            ((low_y_check and high_y_check) and point_in_z_boundaries and point_in_x_boundaries) or
            ((low_y_check and high_y_check) and (low_z_check and high_z_check) and point_in_x_boundaries) or
            ((low_z_check and high_z_check) and point_in_x_boundaries and point_in_y_boundaries)):
        print("special intersection case")
        return True
    else:
        return False


def find_first_intersected_voxel(nonzero_data, voxel_size, movable_voxel, movable_voxel_corners, is_cubic):
    for voxel in nonzero_data:
        fixed_voxel_index = voxel[0]
        fixed_voxel = voxel[1]
        fixed_voxel_center = np.array(fixed_voxel[:3])
        if Geometry.distance(fixed_voxel_center, movable_voxel) < min(voxel_size):
            current_index = fixed_voxel_index
            return current_index
        # if Geometry.distance(fixed_voxel_center, movable_voxel) < 2*max(voxel_size):
        #     if check_intersection_with_fixed_voxel(fixed_voxel, voxel_size, movable_voxel_corners):
        #         current_index = fixed_voxel_index
        #         return current_index

        # if Geometry.distance(fixed_voxel_center, movable_voxel) < 2*max(voxel_size):
        #     if is_cubic:
        #         if check_intersection_with_fixed_voxel(fixed_voxel, voxel_size, movable_voxel_corners):
        #             current_index = fixed_voxel_index
        #             return current_index
        #     else:
        #         if check_intersection_with_fixed_voxel(fixed_voxel, voxel_size, movable_voxel_corners) \
        #             or check_special_case_intersection_with_fixed_voxel(voxel_size, fixed_voxel,
        #                                                                 movable_voxel_corners):
        #             current_index = fixed_voxel_index
        #             return current_index



def check_neighbors(movable_voxel_corners, movable_voxel, nonzero_data, voxel_size, voxdata, is_cubic):
    first_intersected_voxel_index = find_first_intersected_voxel(nonzero_data, voxel_size, movable_voxel, movable_voxel_corners, is_cubic)
    intersected_voxels_indexes = [first_intersected_voxel_index]
    check = True
    current_intersected_voxel_index = first_intersected_voxel_index
    not_intersected_neighbors = []
    while check:
        neighbors = find_neighbors(voxdata, current_intersected_voxel_index)
        for neighbor in neighbors:
            neighbor_voxel = neighbor[0]
            neighbor_index = neighbor[1]
            if neighbor_index not in not_intersected_neighbors:
                if is_cubic:
                    checking = check_intersection_with_fixed_voxel(neighbor_voxel, voxel_size, movable_voxel_corners)
                else:
                    try:
                        checking = check_intersection_with_fixed_voxel(neighbor_voxel, voxel_size, movable_voxel_corners) \
                               or check_special_case_intersection_with_fixed_voxel(voxel_size, neighbor_voxel,
                                                                                   movable_voxel_corners)
                    except Exception as ex:
                        print(type(ex).__name__, ex.args)
                        checking = False
                if checking:
                    neighbors_of_intersected_voxel = find_neighbors(voxdata, neighbor_index)
                    for current_neighbor in neighbors_of_intersected_voxel:
                        if current_neighbor[1] not in intersected_voxels_indexes:
                            intersected_voxels_indexes.append(current_neighbor[1])
                    if neighbor_index not in intersected_voxels_indexes:
                        intersected_voxels_indexes.append(neighbor_index)
                        current_intersected_voxel_index = neighbor_index
                    else:
                        check = False
                else:
                    not_intersected_neighbors.append(neighbor_index)
    intersections = []
    for voxel_index in intersected_voxels_indexes:
        voxel = voxdata[voxel_index[0], voxel_index[1], voxel_index[2]]
        intersections.append(voxel)
    return intersections


def find_intersected_voxels(movable_voxel, movable_voxel_corners, nonzero_data, voxel_size, voxdata, is_cubic):
    # movable_voxel_corners = measuring_plate.voxel_corners_after_rotation(movable_voxel)
    # is_cubic = False
    # if voxel_size[0] == voxel_size[1] == voxel_size[2]:
    #     is_cubic = True
    intersections = check_neighbors(movable_voxel_corners, movable_voxel, nonzero_data, voxel_size, voxdata, is_cubic)
    return intersections


def find_intersection_points_of_two_voxels(movable_voxel_points, fixed_voxel,
                                           plate_voxel_size, fixed_voxel_points, phantom_voxel_size):
    points = []
    movable_voxel_edges = VoxelStructure.Parallelepiped.edges(movable_voxel_points)
    # fixed_voxel_points = phantom_part.voxel_corners(fixed_voxel)
    fixed_voxel_plains = VoxelStructure.MovableVoxelStructure.plains(fixed_voxel_points)
    for edge in movable_voxel_edges:
        for plane in fixed_voxel_plains:
            try:
                point = Geometry.find_intersection_point(plane, edge[0], edge[1])
                if (point is not None) and Geometry.is_point_on_edge_checking(point, edge[0], edge[1]) and \
                        Geometry.is_point_in_fixed_voxel(point, fixed_voxel, phantom_voxel_size):
                    points.append(point)
            except ZeroDivisionError:
                continue
    fixed_voxel_edges = VoxelStructure.Parallelepiped.edges(fixed_voxel_points)
    movable_voxel_plains = VoxelStructure.MovableVoxelStructure.plains(movable_voxel_points)
    for edge in fixed_voxel_edges:
        for plane in movable_voxel_plains:
            try:
                point = Geometry.find_intersection_point(plane, edge[0], edge[1])
                if (point is not None) and Geometry.is_point_on_edge_checking(point, edge[0], edge[1]) and \
                        Geometry.is_point_in_movable_voxel(point, movable_voxel_plains, plate_voxel_size):
                    #  Geometry.is_point_in_voxel(point, movable_voxel_points):
                    if point not in points:
                        points.append(point)
            except ZeroDivisionError:
                continue
    return points


def corners_of_the_intersection_area(plate_voxel_size, movable_voxel_points, fixed_voxel, fixed_voxel_points, phantom_voxel_size):
    points = []
    movable_voxel_plains = VoxelStructure.MovableVoxelStructure.plains(movable_voxel_points)
    for point in movable_voxel_points:
        try:
            if Geometry.is_point_in_fixed_voxel(point, fixed_voxel, phantom_voxel_size):
                points.append(point)
        except Exception as ex:
            print(type(ex.__name__), ex.args)
    for point in fixed_voxel_points:
        if Geometry.is_point_in_movable_voxel(point, movable_voxel_plains, plate_voxel_size):
            points.append(point)
    points += find_intersection_points_of_two_voxels(movable_voxel_points, fixed_voxel, plate_voxel_size, fixed_voxel_points, phantom_voxel_size)
    return np.array(points)


def contribution_to_dose(plate_voxel_size, movable_voxel_points, phantom_voxel_size,
                        fixed_voxel, fixed_voxel_points):
    if fixed_voxel[3] == 0:
        dose_contribution = 0
    else:
        intersection = corners_of_the_intersection_area(plate_voxel_size, movable_voxel_points, fixed_voxel, fixed_voxel_points, phantom_voxel_size)
        voxel_volume = phantom_voxel_size[0] * phantom_voxel_size[1] * phantom_voxel_size[2]
        # print("voxel volume: ", voxel_volume)
        if len(intersection) > 3:
            try:
                intersection_volume = ConvexHull(intersection).volume
                # print("точки пересечения: ", intersection)
            except scipy.spatial.qhull.QhullError:
                intersection_volume = 0
        else:
            intersection_volume = 0
        # print(fixed_voxel, "объём пересекаемой области: ", intersection_volume)
        dose_contribution = fixed_voxel[3] * intersection_volume / voxel_volume

        # ax = plt.axes(projection='3d')
        # VoxelStructure.Parallelepiped.plot_edges(ax, measuring_plate.voxel_corners_after_rotation(movable_voxel), "orange")
        # VoxelStructure.Parallelepiped.plot_edges(ax, phantom_part.voxel_corners(fixed_voxel[1]), "red")
        # plt.show()

        # print("dose contribution by voxel ", fixed_voxel, dose_contribution)
    return dose_contribution


def dose_in_movable_voxel(measuring_plate, movable_voxel, phantom_part, is_cubic):
    movable_voxel_center = VoxelStructure.MovableVoxelStructure.voxel_center_after_rotation(measuring_plate, movable_voxel)
    movable_voxel_corners = measuring_plate.voxel_corners_after_rotation(movable_voxel)
    voxdata = phantom_part.data
    nonzero_data = phantom_part.nonzero_data
    phantom_voxel_size = phantom_part.voxel_size
    plate_voxel_size = measuring_plate.voxel_size
    intersected_voxels = find_intersected_voxels(movable_voxel_center, movable_voxel_corners, nonzero_data, phantom_voxel_size, voxdata, is_cubic)
    dose = 0.
    for fixed_voxel in intersected_voxels:
        fixed_voxel_points = phantom_part.voxel_corners(fixed_voxel)
        dose += contribution_to_dose(plate_voxel_size, movable_voxel_corners, phantom_voxel_size, fixed_voxel, fixed_voxel_points)
    return dose
