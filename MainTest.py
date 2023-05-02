# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
import LoadFile
import Phantom
import MeasuringPlate
import CUDAinput
# import VoxIntersections
import VoxelStructure

if __name__ == "__main__":
    start_time = time.time()

    # vox_set = LoadFile.LoadFile("170.dose", shape=(320, 320, 200))
    # phantom = Phantom.Phantom(vox_set, voxel_size=(1, 1, 1))
    # measuring_plate = MeasuringPlate.MeasuringPlate(30, 0, 0, voxel_size=(1, 1, 1), shape=(1, 200, 320))

    vox_set = LoadFile.LoadFile("data\\TestTomo.dose")
    print(vox_set.data.shape)
    phantom = Phantom.Phantom(vox_set, shape=(20, 20, 20), voxel_size=(5, 5, 5))
    measuring_plate = MeasuringPlate.MeasuringPlate(50, -30, 0, voxel_size=(5, 5, 5), shape=(1, 20, 20))
    print(phantom.dose_data.size)
    print("phantom.shape", phantom.shape)

    phantom_part = Phantom.PhantomPart(phantom, measuring_plate)
    print("phantom_part.data.shape", phantom_part.data.shape)
    print("measuring_plate shape", measuring_plate.structure.shape)
    m1, m2 = CUDAinput.cuda_input_matrix(measuring_plate, phantom_part)
    print(m1.shape)
    print(m1)
    print()
    print(m2.shape)
    print(m2)



    ax = plt.axes(projection='3d')
    phantom.plot_edges(ax)
    measuring_plate.plot_edges(ax)
    phantom_part.plot_edges(ax)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()



