# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
import LoadFile
import Phantom
import MeasuringPlate
# import VoxIntersections
# import VoxelStructure

if __name__ == "__main__":
    start_time = time.time()

    # vox_set = LoadFile.LoadFile("170.dose", shape=(320, 320, 200))
    # phantom = Phantom.Phantom(vox_set, voxel_size=(1, 1, 1))
    # measuring_plate = MeasuringPlate.MeasuringPlate(30, 0, 0, voxel_size=(1, 1, 1), shape=(1, 200, 320))

    vox_set = LoadFile.LoadFile("data\\170.dose")
    print(vox_set.data.shape)
    phantom = Phantom.Phantom(vox_set, shape=(320, 320, 200), voxel_size=(1, 1, 1))
    measuring_plate = MeasuringPlate.MeasuringPlate(6, 0, 0, voxel_size=(1, 1, 1), shape=(1, 200, 320))
    print(phantom.dose_data.size)
    print("phantom.shape", phantom.shape)
    # print(measuring_plate.boundaries)
    # print(phantom.find_layers(measuring_plate.boundaries))

    # measured_part = phantom.desired_layers_structure(measuring_plate.boundaries)
    # print(measured_part.size)

    phantom_part = Phantom.PhantomPart(phantom, measuring_plate)
    print("phantom_part.data.shape", phantom_part.data.shape)
    # print(phantom_part.data)
    print("measuring_plate shape", measuring_plate.structure.shape)
    # movable_voxel = measuring_plate.structure[11, 3]
    # voxel_corners = measuring_plate.voxel_corners_after_rotation(movable_voxel)
    # print("movable voxel corners: ", voxel_corners)
    # fixed_voxel = phantom_part.data[1, 11, 3]
    #
    # first_intersected_voxel = phantom_part.data[0, 18, 18]
    # first_intersected_voxel_corners = phantom_part.voxel_corners(first_intersected_voxel)
    # # fixed_voxel_corners = phantom_part.voxel_corners(fixed_voxel)
    # print("fixed voxel: ", fixed_voxel)

    dose_distribution = MeasuringPlate.DoseDistribution(measuring_plate, phantom_part)

    ax = plt.axes(projection='3d')
    phantom.plot_edges(ax)
    measuring_plate.plot_edges(ax)
    # phantom_part.plot_edges(ax)

    # for voxel_index in dose_distribution.nonzero_structure():
    #     measuring_plate.plot_voxel(ax, voxel_index)

    # for voxel in phantom_part.nonzero_data:
    #     print(voxel)
    #     fixed_voxel_corners = phantom_part.voxel_corners(voxel[1])
    #     VoxelStructure.Parallelepiped.plot_edges(ax, fixed_voxel_corners, "magenta")

    # VoxelStructure.Parallelepiped.plot_edges(ax, first_intersected_voxel_corners, "orange")
    # VoxelStructure.Parallelepiped.plot_edges(ax, fixed_voxel_corners, "magenta")
    # ax.scatter(voxel[0], voxel[1], voxel[2], color="red")
    # measuring_plate.plot_voxel(ax, [11, 3])
    # measuring_plate.plot_voxel(ax, [1, 0])
    # measuring_plate.plot_voxel(ax, [2, 0])
    # measuring_plate.plot_voxel(ax, [0, 1])
    # measuring_plate.plot_voxel(ax, [199, 0])
    # measuring_plate.plot_voxel(ax, [0, 319])
    # measuring_plate.plot_voxel(ax, [199, 319])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

    test_layer = phantom.original_data_layers[:, 30, :]
    print(phantom.original_data_layers.shape)

    #test_layer = phantom.dose_data[17, :, :]
    ax2 = plt.axes()
    ax2.imshow(test_layer)
    plt.show()

    with open("layer30.txt", "w") as file:
        line_number = 0
        for line_number, line in enumerate(test_layer):
            # file.write(str(line)+"\n")
            for voxel_number, voxel in enumerate(line):
                if voxel > 0:
                    file.write(str((line_number, voxel_number, voxel))+"\n")


    # dose_distribution = MeasuringPlate.DoseDistribution(measuring_plate, phantom_part)

    # doses = dose_distribution.doses
    # ax = plt.axes()
    # ax.imshow(doses)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # plt.show()

    # doses = MeasuringPlate.DoseDistribution(measuring_plate, phantom_part)
    # print(doses)

    # voxel = phantom_part.data[1, 5, 5]
    # print(VoxIntersections.find_neighbors(phantom_part, (1, 5, 5)),
    #       len(VoxIntersections.find_neighbors(phantom_part, (1, 5, 5))))
