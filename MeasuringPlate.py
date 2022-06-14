# -*- coding: utf-8 -*-

# import math

import time
import numpy as np
import Geometry
# import matplotlib.pyplot as plt
import Phantom
import VoxelStructure
import VoxIntersections


class MeasuringPlatePlacement:
    def __init__(self, y_coordinate, x_rotate, z_rotate, size=(1, 200, 320)):
        self.size = size
        self.y_coordinate = y_coordinate
        self.center = [0, self.y_coordinate, 0]
        self.rotation_matrix = Geometry.rotation_matrix(x_rotate, z_rotate)
        self.corners = self.corners_after_rotation_and_placing()
        self.boundaries = self.find_boundaries()

    def corners_relative_to_center_before_rotation(self):
        x_relative_to_center = self.size[2] / 2
        y_relative_to_center = self.size[0] / 2
        z_relative_to_center = self.size[1] / 2
        points = []
        for i in [x_relative_to_center, -x_relative_to_center]:
            for j in [y_relative_to_center, -y_relative_to_center]:
                for k in [z_relative_to_center, -z_relative_to_center]:
                    points.append([i, j, k])
        return np.array(points)

    def many_points_rotation(self, points):
        rotated_points = []
        for point in points:
            new_point = Geometry.point_rotation(point, self.rotation_matrix)
            rotated_points.append(new_point)
        return np.array(rotated_points)

    def corners_relative_to_center_after_rotation(self):
        points = self.corners_relative_to_center_before_rotation()
        rotated_points = self.many_points_rotation(points)
        return rotated_points

    def corners_after_rotation_and_placing(self):
        points = self.corners_relative_to_center_after_rotation()
        for point in points:
            point[0] += self.center[0]
            point[1] += self.center[1]
            point[2] += self.center[2]

        return np.array(points)

    def find_boundaries(self):
        min_y = min(self.corners, key=lambda coordinates: coordinates[1])[1]
        max_y = max(self.corners, key=lambda coordinates: coordinates[1])[1]
        return [min_y, max_y]

    def plot_edges(self, ax, color="red"):
        VoxelStructure.Parallelepiped.plot_edges(ax, self.corners, color)


class MeasuringPlate(MeasuringPlatePlacement, VoxelStructure.MovableVoxelStructure):
    def __init__(self, y_coordinate, x_rotate, z_rotate, voxel_size=(1, 1, 1), shape=(1, 200, 320)):
        self.voxel_size = voxel_size
        self.size = (shape[0]*voxel_size[1], shape[1]*voxel_size[2], shape[2]*voxel_size[0])
        self.number_of_voxels_by_x = shape[2]  # int(self.size[2]/voxel_size[0])
        self.number_of_voxels_by_z = shape[1]  # int(self.size[1]/voxel_size[1])
        self.y_coordinate = y_coordinate
        self.structure = self.voxel_structure()
        super(MeasuringPlate, self).__init__(y_coordinate, x_rotate, z_rotate, self.size)
        super(MeasuringPlatePlacement, self).__init__(self.structure, voxel_size, x_rotate, z_rotate)

    def voxel_structure(self):
        structure = np.zeros((self.number_of_voxels_by_x, self.number_of_voxels_by_z), dtype=list)
        for line_number in range(self.number_of_voxels_by_z):
            for voxel_number in range(self.number_of_voxels_by_x):
                vox_x = self.voxel_size[0] * (voxel_number + 0.5) - (self.number_of_voxels_by_x *
                                                                     self.voxel_size[0] / 2)
                vox_y = self.y_coordinate
                vox_z = self.voxel_size[2] * (line_number + 0.5) - (self.number_of_voxels_by_z *
                                                                    self.voxel_size[2] / 2)
                structure[voxel_number, line_number] = [vox_x, vox_y, vox_z]
        return structure

    def plot_voxel(self, ax, index):
        voxel = self.structure[index[0], index[1]]
        voxel_corners = self.voxel_corners_after_rotation(voxel)
        VoxelStructure.Parallelepiped.plot_edges(ax, voxel_corners)


class DoseDistribution:
    def __init__(self, measuring_plate: MeasuringPlate, phantom_part: Phantom.PhantomPart):
        self.measuring_plate = measuring_plate
        self.plate_structure = measuring_plate.structure
        self.phantom_part = phantom_part
        # self.data = self.dose_map()
        self.rows_number = self.plate_structure.shape[1]
        self.voxels_number = self.plate_structure.shape[0]
        self.doses = np.zeros((self.rows_number, self.voxels_number), dtype=float)

    def nonzero_structure(self):
        rows_number = self.plate_structure.shape[1]
        voxels_number = self.plate_structure.shape[0]
        max_x, min_x, max_z, min_z = self.phantom_part.nonzero_boundaries
        vox_x = self.measuring_plate.voxel_size[0]
        vox_z = self.measuring_plate.voxel_size[2]
        voxels = []
        for i in range(voxels_number):
            for j in range(rows_number):
                voxel = self.plate_structure[i, j]
                if max_x+vox_x/2 > voxel[0] > min_x-vox_x/2 and max_z+vox_z/2 > voxel[2] > min_z-vox_z/2:
                    voxels.append([j, i])
        return np.array(voxels)

    def dose_map(self):
        # rows_number = self.plate_structure.shape[1]
        # voxels_number = self.plate_structure.shape[0]
        max_x, min_x, max_z, min_z = self.phantom_part.nonzero_boundaries
        # doses = np.zeros((voxels_number, rows_number), dtype=float)
        vox_x = self.measuring_plate.voxel_size[0]
        vox_z = self.measuring_plate.voxel_size[2]
        num_of_nonzero_voxels = int((max_x - min_x + vox_x)/vox_x)*int((max_z - min_z + vox_z)/vox_z)
        nonzero_operations_counter = 0
        end_time = 0
        for i in range(self.rows_number):
            for j in range(self.voxels_number):
                progress_value = (self.voxels_number*i + j + 1)*100/(self.voxels_number*self.rows_number)
                voxel = self.plate_structure[j, i]
                # if max_x >= voxel[0] >= min_x and max_z >= voxel[2] >= min_z:
                if max_x+vox_x/2 > voxel[0] > min_x-vox_x/2 and max_z+vox_z/2 > voxel[2] > min_z-vox_z/2:
                    nonzero_operations_counter += 1
                    try:
                        start_time = time.time()
                        self.doses[i, j] = VoxIntersections.dose_in_movable_voxel(self.measuring_plate,
                                                                                  self.plate_structure[j, i],
                                                                                  self.phantom_part)
                        if self.doses[i, j] != 0:
                            end_time += (time.time() - start_time)
                            average_time = end_time/nonzero_operations_counter
                            rest_time = (num_of_nonzero_voxels -
                                         nonzero_operations_counter)*average_time
                            # print("average time ", average_time)
                            # print("current voxels ", nonzero_operations_counter)
                            # print("rest voxels ", num_of_nonzero_voxels - nonzero_operations_counter)
                        else:
                            rest_time = None
                        # print(i, j, self.doses[i, j])
                        yield i, j, self.doses[i, j], progress_value, rest_time
                    except TypeError:
                        # print(i, j, 0)
                        yield i, j, 0.0, progress_value, None
                        continue
                else:
                    # print(i, j, 0)
                    yield i, j, 0.0, progress_value, None
        # return doses
