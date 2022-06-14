# -*- coding: utf-8 -*-

import numpy as np
import VoxelStructure


class Phantom:
    def __init__(self, load_data, shape, voxel_size=(1, 1, 1)):
        self.dose_data = load_data.reshaped_data(shape)
        self.original_data = load_data.data

        # воксели считаются по горизонтальным слоям
        self.original_data_layers = self.original_data.reshape(shape[2], shape[1], shape[0])
        self.shape = shape
        self.voxel_size = voxel_size
        self.size = (self.shape[0]*self.voxel_size[0], self.shape[1]*self.voxel_size[1],
                     self.shape[2]*self.voxel_size[2])

    def layer_y_borders(self, layer_index):
        min_y = layer_index * self.voxel_size[1]
        max_y = min_y + self.voxel_size[1]
        return min_y, max_y

    def find_layers(self, measuring_plate_boundaries):
        min_layer = max_layer = 0
        for layer_index in range(self.shape[1]):
            layer_borders = self.layer_y_borders(layer_index)
            if layer_borders[0] <= measuring_plate_boundaries[0] <= layer_borders[1]:
                min_layer = layer_index
            elif layer_borders[0] <= measuring_plate_boundaries[1] <= layer_borders[1]:
                max_layer = layer_index + 1
            elif measuring_plate_boundaries[0] < 0:
                min_layer = 0
            elif measuring_plate_boundaries[1] > self.size[1]:
                max_layer = self.shape[0] - 1
        return min_layer, max_layer

    # def desired_layers_structure(self, measuring_plate_boundaries):
    #     min_layer, max_layer = self.find_layers(measuring_plate_boundaries)
    #     structure = []
    #     for layer_num in range(min_layer, max_layer):
    #         layer = []
    #         for row_num in range(self.shape[1]):
    #             row = []
    #             for voxel_num in range(self.shape[2]):
    #                 x_coordinate_of_center = self.voxel_size[0] * (voxel_num + 0.5) - (self.shape[2] *
    #                                                                                    self.voxel_size[0] / 2)
    #                 y_coordinate_of_center = self.voxel_size[1] * (layer_num + 0.5)
    #                 z_coordinate_of_center = self.voxel_size[2] * (row_num + 0.5) - (self.shape[1] *
    #                                                                                  self.voxel_size[1] / 2)
    #                 row.append([x_coordinate_of_center, y_coordinate_of_center, z_coordinate_of_center,
    #                             self.dose_data[layer_num, row_num, voxel_num]])
    #             layer.append(row)
    #         structure.append(layer)
    #     return np.array(structure)

    def desired_layers_structure(self, measuring_plate_boundaries):
        min_layer, max_layer = self.find_layers(measuring_plate_boundaries)
        structure = np.zeros((len(range(min_layer, max_layer)), self.shape[2], self.shape[0]), dtype=list)
        for layer_index, layer_num in enumerate((range(min_layer, max_layer))):
            for row_num in range(self.shape[2]):
                for voxel_num in range(self.shape[0]):
                    x_coordinate_of_center = self.voxel_size[0] * (voxel_num + 0.5) - (self.shape[0] *
                                                                                       self.voxel_size[0] / 2)
                    y_coordinate_of_center = self.voxel_size[1] * (layer_num + 0.5)
                    z_coordinate_of_center = self.voxel_size[2] * (row_num + 0.5) - (self.shape[2] *
                                                                                     self.voxel_size[2] / 2)
                    structure[layer_index, row_num, voxel_num] = [x_coordinate_of_center, y_coordinate_of_center,
                                                                  z_coordinate_of_center,
                                                                  self.dose_data[layer_num, row_num, voxel_num]]
        return np.array(structure)

    def corners(self):
        relative_corners = VoxelStructure.Parallelepiped.corners_relative_to_center(self.size)
        return VoxelStructure.Parallelepiped.corners(relative_corners, (0, self.size[0]/2, 0))

    def plot_edges(self, ax, color='blue'):
        VoxelStructure.Parallelepiped.plot_edges(ax, self.corners(), color=color)


class PhantomPart(VoxelStructure.FixedVoxelStructure):
    def __init__(self, phantom, measuring_plate):
        min_layer_index, max_layer_index = phantom.find_layers(measuring_plate.boundaries)
        self.data = phantom.desired_layers_structure(measuring_plate.boundaries)
        # self.y_coordinate = measuring_plate.y_coordinate
        self.nonzero_boundaries, self.nonzero_data = self.nonzero_part()
        super().__init__(self.data, phantom.voxel_size)
        self.y_coordinate = self.voxel_size[1] * (min_layer_index + (max_layer_index - min_layer_index) / 2)

    def plot_edges(self, ax):
        size = [self.data.shape[2]*self.voxel_size[0], self.data.shape[0]*self.voxel_size[1],
                self.data.shape[1]*self.voxel_size[2]]

        relative_corners = VoxelStructure.Parallelepiped.corners_relative_to_center(size)

        corners = VoxelStructure.Parallelepiped.corners(relative_corners, (0, self.y_coordinate, 0))
        VoxelStructure.Parallelepiped.plot_edges(ax, corners, color="green")

    @staticmethod
    def nonzero_part_boundaries(one_dim_data_nonzero):
        max_x = max(one_dim_data_nonzero, key=lambda c: c[0])[0]
        min_x = min(one_dim_data_nonzero, key=lambda c: c[0])[0]
        max_z = max(one_dim_data_nonzero, key=lambda c: c[2])[2]
        min_z = min(one_dim_data_nonzero, key=lambda c: c[2])[2]
        return max_x, min_x, max_z, min_z

    def nonzero_part(self):
        nonzero_part = []
        one_dim_data_nonzero = []
        # counter = 0
        for layer_number, layer in enumerate(self.data):
            for row_number, row in enumerate(layer):
                for voxel_number, voxel in enumerate(row):
                    if voxel[3] != 0:
                        nonzero_part.append([(layer_number, row_number, voxel_number), voxel])
                        one_dim_data_nonzero.append(voxel)
                        # counter += 1
        if one_dim_data_nonzero:
            nonzero_boundaries = self.nonzero_part_boundaries(one_dim_data_nonzero)
        else:
            nonzero_boundaries = (0, 0, 0, 0)
        return nonzero_boundaries, nonzero_part
