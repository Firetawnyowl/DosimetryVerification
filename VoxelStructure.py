# -*- coding: utf-8 -*-

import numpy as np
from numba import njit
import Geometry


class Parallelepiped:

    @staticmethod
    @njit(cache=True)
    def corners_relative_to_center(size):
        x_relative_to_center = size[0] / 2
        y_relative_to_center = size[1] / 2
        z_relative_to_center = size[2] / 2
        points = []
        for i in [x_relative_to_center, -x_relative_to_center]:
            for j in [y_relative_to_center, -y_relative_to_center]:
                for k in [z_relative_to_center, -z_relative_to_center]:
                    points.append([i, j, k])
        return np.array(points)

    @staticmethod
    @njit(cache=True)
    def corners(relative_corners, center):
        corners = relative_corners
        for point in corners:
            point[0] += center[0]
            point[1] += center[1]
            point[2] += center[2]
        return corners

    @staticmethod
    @njit(cache=True)
    def edges(corners):
        #corners = np.array(corners_l)
        # print(corners)
        edges = np.array([[[corners[0][0], corners[0][1], corners[0][2]], [corners[1][0], corners[1][1], corners[1][2]]],
                          [[corners[2][0], corners[2][1], corners[2][2]], [corners[3][0], corners[3][1], corners[3][2]]],
                          [[corners[0][0], corners[0][1], corners[0][2]], [corners[2][0], corners[2][1], corners[2][2]]],
                          [[corners[3][0], corners[3][1], corners[3][2]], [corners[1][0], corners[1][1], corners[1][2]]],
                          [[corners[4][0], corners[4][1], corners[4][2]], [corners[5][0], corners[5][1], corners[5][2]]],
                          [[corners[6][0], corners[6][1], corners[6][2]], [corners[7][0], corners[7][1], corners[7][2]]],
                          [[corners[4][0], corners[4][1], corners[4][2]], [corners[6][0], corners[6][1], corners[6][2]]],
                          [[corners[5][0], corners[5][1], corners[5][2]], [corners[7][0], corners[7][1], corners[7][2]]],
                          [[corners[0][0], corners[0][1], corners[0][2]], [corners[4][0], corners[4][1], corners[4][2]]],
                          [[corners[1][0], corners[1][1], corners[1][2]], [corners[5][0], corners[5][1], corners[5][2]]],
                          [[corners[2][0], corners[2][1], corners[2][2]], [corners[6][0], corners[6][1], corners[6][2]]],
                          [[corners[3][0], corners[3][1], corners[3][2]], [corners[7][0], corners[7][1], corners[7][2]]]])
        return edges

    @staticmethod
    def plot_edges(ax, points, color="blue"):
        try:
            for p in Parallelepiped.edges(np.array(points)):
                ax.plot(p[:, 0], p[:, 1], p[:, 2], color=color)
        except Exception as ex:
            print(type(ex).__name__, ex.args)


class VoxelStructure:
    def __init__(self, data, voxel_size):
        self.voxels = data
        self.voxel_size = voxel_size

    def voxel_corners_relative_to_center(self):
        return Parallelepiped.corners_relative_to_center(self.voxel_size)

    def voxel_corners(self, voxel):
        return Parallelepiped.corners(self.voxel_corners_relative_to_center(), (voxel[0], voxel[1], voxel[2]))


class FixedVoxelStructure(VoxelStructure):
    def __init__(self, data, voxel_size):
        super().__init__(data, voxel_size)

    # def plains(self, voxel):
    #     x_coordinates, y_coordinates, z_coordinates = self.voxel_boundaries(voxel)
    #     plains = ((0, 0, 1, z_coordinates[0]), (0, 0, 1, z_coordinates[1]), (0, 1, 0, y_coordinates[0]),
    #               (0, 1, 0, y_coordinates[1]), (1, 0, 0, x_coordinates[0]), (1, 0, 0, x_coordinates[1]))
    #     return plains


class MovableVoxelStructure(VoxelStructure):
    def __init__(self, data, voxel_size, x_rot, z_rot):
        super().__init__(data, voxel_size)
        self.rot_matrix = Geometry.rotation_matrix(x_rot, z_rot)

    def voxel_center_after_rotation(self, voxel):
        old_center = np.array([voxel[0], 0., voxel[2]])
        new_center = Geometry.point_rotation(old_center, self.rot_matrix)
        new_center[1] += voxel[1]
        return new_center

    def voxel_corners_after_rotation(self, voxel):
        rotated_points = []
        voxel_center = self.voxel_center_after_rotation(voxel)
        for point in self.voxel_corners_relative_to_center():
            new_point = Geometry.point_rotation(point, self.rot_matrix)
            new_point[0] += voxel_center[0]
            new_point[1] += voxel_center[1]
            new_point[2] += voxel_center[2]
            rotated_points.append(new_point)
        return np.array(rotated_points)

    @staticmethod
    def plains_points(corners):
        plains_points = np.array([[corners[0], corners[1], corners[3]],
                                  [corners[4], corners[5], corners[7]],
                                  [corners[1], corners[3], corners[7]],
                                  [corners[0], corners[2], corners[6]],
                                  [corners[0], corners[1], corners[5]],
                                  [corners[3], corners[2], corners[6]]])
        return plains_points

    @staticmethod
    def plains(corners):
        pl_points = MovableVoxelStructure.plains_points(corners)
        plains = []
        for plain in pl_points:
            x1, y1, z1 = plain[0][0], plain[0][1], plain[0][2]
            x2, y2, z2 = plain[1][0], plain[1][1], plain[1][2]
            x3, y3, z3 = plain[2][0], plain[2][1], plain[2][2]

            a = ((y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1))
            b = -((x2 - x1)*(z3 - z1) - (z2 - z1)*(x3 - x1))
            c = ((x2 - x1)*(y3 - y1) - (y2 - y1)*(x3 - x1))
            d = -(a*x1 + b*y1 + c*z1)
            plain_parameters = [a, b, c, d]
            plains.append(plain_parameters)
        return np.array(plains)
