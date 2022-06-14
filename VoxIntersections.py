# -*- coding: utf-8 -*-

import time
import numpy as np
import scipy.spatial.qhull
from scipy.spatial import ConvexHull
import Phantom
import VoxelStructure
import Geometry


def find_neighbors(phantom_part: Phantom.PhantomPart, fixed_voxel_indexes):
    # start_time = time.time()
    # print("start finding neighbors")
    x, y, z = fixed_voxel_indexes
    voxels = phantom_part.data
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
    # print("end finding neighbors:  %s seconds" % (time.time() - start_time))
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print("neighbors:", neighbors)
    return neighbors


def check_intersection(fixed_voxel_corners, movable_voxel_corners):
    check = False
    # print(fixed_voxel_corners)
    #  print(movable_voxel_corners)
    for point in movable_voxel_corners:
        if Geometry.is_point_in_voxel(point, fixed_voxel_corners):
            check = True
    return check


# def find_first_intersected_voxel(phantom_part: Phantom.PhantomPart, movable_voxel, movable_voxel_corners):
#     print("start finding first intersection")
#     for i in range(phantom_part.data.shape[0]):
#         for j in range(phantom_part.data.shape[1]):
#             for k in range(phantom_part.data.shape[2]):
#                 print(i, j, k)
#                 fixed_voxel = phantom_part.data[i, j, k]
#                 print(fixed_voxel)
#                 fixed_voxel_corners = phantom_part.voxel_corners(fixed_voxel)
#                 print(fixed_voxel_corners)
#                 if check_intersection(fixed_voxel_corners, movable_voxel_corners):
#                     print("check intersection is True for fixed voxel ", fixed_voxel, " and movable voxel ",
#                            movable_voxel)
#                     current_index = (i, j, k)
#                     print(current_index)
#                     return current_index


def find_first_intersected_voxel(phantom_part: Phantom.PhantomPart, movable_voxel, movable_voxel_corners):
    # start_time = time.time()
    # print("start finding first intersection")
    # print("mov vox", movable_voxel_corners)
    for voxel in phantom_part.nonzero_data:
        fixed_voxel_index = voxel[0]
        fixed_voxel = voxel[1]
        fixed_voxel_center = fixed_voxel[:3]
        if Geometry.distance(fixed_voxel_center, movable_voxel) < 2*max(phantom_part.voxel_size):
            fixed_voxel_corners = phantom_part.voxel_corners(fixed_voxel)
            #print("fix vox", fixed_voxel_corners)
            if check_intersection(fixed_voxel_corners, movable_voxel_corners):
                # print("check intersection is True for fixed voxel ", fixed_voxel, " and movable voxel ", movable_voxel)
                current_index = fixed_voxel_index
                # print("current_index", current_index)
                # print("end finding first intersected voxel:  %s seconds" % (time.time() - start_time))
                # print("--- %s seconds ---" % (time.time() - start_time))
                return current_index


def check_neighbors(movable_voxel_corners, movable_voxel, phantom_part):
    # start_time = time.time()
    # print("start checking neighbors")
    first_intersected_voxel_index = find_first_intersected_voxel(phantom_part, movable_voxel, movable_voxel_corners)
    # print("first intersected voxel: ", first_intersected_voxel_index)
    intersected_voxels_indexes = [first_intersected_voxel_index]
    check = True
    current_intersected_voxel_index = first_intersected_voxel_index
    # intersections = []
    not_intersected_neighbors = []
    while check:
        neighbors = find_neighbors(phantom_part, current_intersected_voxel_index)
        for neighbor in neighbors:
            neighbor_voxel = neighbor[0]
            neighbor_voxel_corners = phantom_part.voxel_corners(neighbor_voxel)
            neighbor_index = neighbor[1]
            if neighbor_index not in not_intersected_neighbors:
                if check_intersection(neighbor_voxel_corners, movable_voxel_corners):
                    if neighbor_index not in intersected_voxels_indexes:
                        intersected_voxels_indexes.append(neighbor_index)
                        current_intersected_voxel_index = neighbor_index
                        # voxel = phantom_part.data[neighbor_index[0], neighbor_index[1], neighbor_index[2]]
                        # intersections.append(voxel)
                    else:
                        check = False
                else:
                    not_intersected_neighbors.append(neighbor_index)
    # print(not_intersected_neighbors)
    intersections = []
    for voxel_index in intersected_voxels_indexes:
        voxel = phantom_part.data[voxel_index[0], voxel_index[1], voxel_index[2]]
        intersections.append(voxel)
        # print("intersections", intersections)
    # print("end checking neighbors:  %s seconds" % (time.time() - start_time))
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print("Пересекаемые воксели:", intersections)
    return intersections


def find_intersected_voxels(movable_voxel, measuring_plate: VoxelStructure.MovableVoxelStructure,
                            phantom_part: Phantom.PhantomPart):
    # start_time = time.time()
    # print("start finding intersected voxels")
    # movable_voxel_before_rotation = measuring_plate.voxel_corners(movable_voxel)
    movable_voxel_corners = measuring_plate.voxel_corners_after_rotation(movable_voxel)
    # print("corners before rotation: ", movable_voxel_before_rotation)
    # print("movable_voxel_corners: ", movable_voxel_corners)
    intersections = check_neighbors(movable_voxel_corners, movable_voxel, phantom_part)
    # print("intersected_voxels: ", intersections)
    # print("end finding intersected voxels:  %s seconds" % (time.time() - start_time))
    # print("--- %s seconds ---" % (time.time() - start_time))
    return intersections


def find_intersection_points_of_two_voxels(movable_voxel_points, fixed_voxel,
                                           phantom_part: VoxelStructure.FixedVoxelStructure,
                                           measuring_plate: VoxelStructure.MovableVoxelStructure):
    points = []
    movable_voxel_edges = VoxelStructure.Parallelepiped.edges(movable_voxel_points)
    fixed_voxel_plains = VoxelStructure.FixedVoxelStructure.plains(phantom_part, fixed_voxel)
    fixed_voxel_points = phantom_part.voxel_corners(fixed_voxel)
    for edge in movable_voxel_edges:
        for plane in fixed_voxel_plains:
            try:
                point = Geometry.find_intersection_point(plane, edge[0], edge[1])
                if (point is not None) and Geometry.is_point_on_edge_checking(point, edge[0], edge[1]) and Geometry.is_point_in_voxel(
                        point, fixed_voxel_points):
                    points.append(point)
            except ZeroDivisionError:
                continue
    fixed_voxel_edges = VoxelStructure.Parallelepiped.edges(fixed_voxel_points)
    movable_voxel_plains = measuring_plate.plains(movable_voxel_points)
    for edge in fixed_voxel_edges:
        for plane in movable_voxel_plains:
            try:
                point = Geometry.find_intersection_point(plane, edge[0], edge[1])
                if (point is not None) and Geometry.is_point_on_edge_checking(point, edge[0], edge[1]) and Geometry.is_point_in_voxel(
                        point, movable_voxel_points):
                    if point not in points:
                        points.append(point)
            except ZeroDivisionError:
                continue
    # print("Intersection points: ", points)
    return points


def corners_of_the_intersection_area(measuring_plate: VoxelStructure.MovableVoxelStructure, movable_voxel,
                                     phantom_part: VoxelStructure.FixedVoxelStructure, fixed_voxel):
    points = []
    movable_voxel_points = measuring_plate.voxel_corners_after_rotation(movable_voxel)
    fixed_voxel_points = phantom_part.voxel_corners(fixed_voxel)
    # print(list(movable_voxel_points), list(fixed_voxel_points))
    for point in movable_voxel_points:
        if Geometry.is_point_in_voxel(point, fixed_voxel_points):
            points.append(point)
    for point in fixed_voxel_points:
        if Geometry.is_point_in_voxel(point, movable_voxel_points):
            points.append(point)
    # print("Common points: ", points)
    points += find_intersection_points_of_two_voxels(movable_voxel_points, fixed_voxel, phantom_part, measuring_plate)
    return np.array(points)


def contribution_to_dose(measuring_plate: VoxelStructure.MovableVoxelStructure, movable_voxel,
                         phantom_part: VoxelStructure.FixedVoxelStructure, fixed_voxel):
    # print("start calculation dose contribution")
    if fixed_voxel[3] == 0:
        dose_contribution = 0
    else:
        intersection = corners_of_the_intersection_area(measuring_plate, movable_voxel, phantom_part, fixed_voxel)
        voxel_volume = phantom_part.voxel_size[0] * phantom_part.voxel_size[1] * phantom_part.voxel_size[2]
        # print("voxel volume: ", voxel_volume)
        if len(intersection) > 3:
            try:
                intersection_volume = ConvexHull(intersection).volume
                # print("точки пересечения: ", intersection)
            except scipy.spatial.qhull.QhullError:
                intersection_volume = 0
        else:
            intersection_volume = 0
        # print("intersection volume: ", intersection_volume)
        # print(fixed_voxel, "объём пересекаемой области: ", intersection_volume)
        dose_contribution = fixed_voxel[3] * intersection_volume / voxel_volume
        # print("dose contribution by voxel ", fixed_voxel, dose_contribution)
    return dose_contribution


def dose_in_movable_voxel(measuring_plate, movable_voxel, phantom_part):
    # print("start calculating dose in movable voxel: ", movable_voxel)
    intersected_voxels = find_intersected_voxels(movable_voxel, measuring_plate, phantom_part)
    # print("intersected_voxels ", intersected_voxels)
    dose = 0.
    for fixed_voxel in intersected_voxels:
        dose += contribution_to_dose(measuring_plate, movable_voxel, phantom_part, fixed_voxel)
    return dose
