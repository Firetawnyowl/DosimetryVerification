# -*- coding: utf-8 -*-

# import math
import os
import numpy as np
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import Geometry
# import matplotlib.pyplot as plt
import Phantom
import VoxelStructure
import VoxIntersections


class MeasuringPlatePlacement:
    def __init__(self, y_coordinate, x_rotate, z_rotate, size=(1, 200, 320)):
        self.size = size
        self.y_coordinate = y_coordinate
        self.center = [self.size[2]/2, self.y_coordinate, self.size[1]/2]
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
                    points.append(np.array([i, j, k]))
        return np.array(points)

    def many_points_rotation(self, points):
        rotated_points = []
        try:
            for point in points:
                new_point = Geometry.point_rotation(point, self.rotation_matrix)
                rotated_points.append(new_point)
            return np.array(rotated_points)
        except Exception as ex:
            print(type(ex).__name__, ex.args)

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
        # print("measuring_plate_boundaries: ", min_y, max_y)
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
                structure[voxel_number, line_number] = np.array([vox_x, vox_y, vox_z])
        return structure

    def plot_voxel(self, ax, index):
        voxel = self.structure[index[0], index[1]]
        voxel_corners = self.voxel_corners_after_rotation(voxel)
        VoxelStructure.Parallelepiped.plot_edges(ax, voxel_corners)


class DoseDistribution:
    def __init__(self, measuring_plate: MeasuringPlate, phantom_part: Phantom.PhantomPart):
        self.measuring_plate = measuring_plate
        self.max_vox_size = max(self.measuring_plate.voxel_size)
        self.plate_structure = measuring_plate.structure
        self.phantom_part = phantom_part
        # self.data = self.dose_map()
        self.rows_number = self.plate_structure.shape[1]
        self.voxels_number = self.plate_structure.shape[0]
        self.doses = np.zeros((self.voxels_number, self.rows_number), dtype=float)

    def nonzero_structure(self):
        rows_number = self.plate_structure.shape[1]
        voxels_number = self.plate_structure.shape[0]
        max_x, min_x, max_z, min_z = self.phantom_part.nonzero_boundaries
        voxels = []
        for i in range(voxels_number):
            for j in range(rows_number):
                voxel = VoxelStructure.MovableVoxelStructure.voxel_center_after_rotation(self.measuring_plate,
                                                                                         self.plate_structure[i, j])
                if max_x+self.max_vox_size*2 > voxel[0] > min_x-self.max_vox_size*2 and max_z+self.max_vox_size*2 > voxel[2] > min_z-self.max_vox_size*2:
                    voxels.append([i, j])
        return np.array(voxels)

    def dose_map(self):
        manager = mp.Manager()
        voxels = manager.Queue()
        doses = manager.Queue()
        ncpu = mp.cpu_count()
        for voxel in self.nonzero_structure():
            voxels.put(voxel)
        # print(voxels.qsize())

        with ProcessPoolExecutor(max_workers=ncpu) as process:
            for i in range(ncpu):
                try:
                    process.submit(self.dose_in_nonzero_voxel, voxels, doses)

                except Exception as ex:
                    print(type(ex).__name__, ex.args)
        # with ThreadPoolExecutor(max_workers=6) as thread:
        #     for i in range(6):
        #         try:
        #             thread.submit(self.dose_in_nonzero_voxel, voxels, doses)
        #
        #         except Exception as ex:
        #             print(type(ex).__name__, ex.args)

        # processes = []
        # for i in range(mp.cpu_count()):
        #     p = mp.Process(target=self.dose_in_nonzero_voxel, args=(voxels, doses))
        #     # processes.append(p)
        #     p.start()
        # for p in processes:
        #     p.join()
        while not doses.empty():
            dose = doses.get()
            self.doses[dose[0], dose[1]] = dose[2]

    # def threading_in_process(self, voxels, doses):
    #     with ThreadPoolExecutor(max_workers=3) as thread:
    #         for i in range(3):
    #             try:
    #                 thread.submit(self.dose_in_nonzero_voxel, voxels, doses)
    #
    #             except Exception as ex:
    #                 print(type(ex).__name__, ex.args)

    def dose_in_nonzero_voxel(self, voxels, doses):
        # nonzero_voxels = self.nonzero_structure()
        # for voxel in nonzero_voxels:
        is_cubic = False
        if self.measuring_plate.voxel_size[0] == self.measuring_plate.voxel_size[1] == self.measuring_plate.voxel_size[2]:
            is_cubic = True
        number_of_nonzero_voxels = len(self.nonzero_structure())
        while not voxels.empty():
            voxel = voxels.get()
            i = voxel[0]
            j = voxel[1]
            try:
                # self.doses[i, j] = VoxIntersections.dose_in_movable_voxel(self.measuring_plate,
                #                                                           self.plate_structure[i, j],
                #                                                           self.phantom_part)
                dose = VoxIntersections.dose_in_movable_voxel(self.measuring_plate,
                                                              self.plate_structure[i, j],
                                                              self.phantom_part,
                                                              is_cubic)
                dose_in_voxel = [i, j, dose]
                doses.put(dose_in_voxel)
                # print(dose_in_voxel)
                # yield i, j, self.doses[i, j]
            except TypeError:
                pass
            # except Exception as ex:
                # print("номер вокселя", i, j)
                # print(type(ex).__name__, ex.args)
                # print(i, j, 0.0)
                # yield i, j, 0.0

            os.system("cls")
            print("complete: ", int((number_of_nonzero_voxels - voxels.qsize()) / number_of_nonzero_voxels * 100), "%")

    # def dose_map(self):
    #     # rows_number = self.plate_structure.shape[1]
    #     # voxels_number = self.plate_structure.shape[0]
    #     max_x, min_x, max_z, min_z = self.phantom_part.nonzero_boundaries
    #     # doses = np.zeros((voxels_number, rows_number), dtype=float)
    #     vox_x = self.measuring_plate.voxel_size[0]
    #     vox_z = self.measuring_plate.voxel_size[2]
    #     for i in range(self.voxels_number):
    #         for j in range(self.rows_number):
    #             voxel = self.plate_structure[i, j]
    #             if max_x+vox_x/2 > voxel[0] > min_x-vox_x/2 and max_z+vox_z/2 > voxel[2] > min_z-vox_z/2:
    #             # if max_x >= voxel[0] >= min_x and max_z >= voxel[2] >= min_z:
    #                 try:
    #                     self.doses[i, j] = VoxIntersections.dose_in_movable_voxel(self.measuring_plate,
    #                                                                          self.plate_structure[i, j],
    #                                                                          self.phantom_part)
    #                     print(i, j, self.doses[i, j])
    #                     yield i, j, self.doses[i, j]
    #                 except TypeError:
    #                     print(i, j, 0)
    #                     yield i, j, 0
    #                     continue
    #             # else:
    #             #     print(i, j, 0)
    #             #     yield i, j, 0
    #     # return doses
