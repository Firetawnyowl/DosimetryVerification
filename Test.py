import numpy as np
import matplotlib.pyplot as plt

# data = []
# with open("result_by_TestTomo1.txt") as file:
#     for line in file:
#         data.append(float(line))
# doses = np.data, dtype=np.float32)
# reshaped_doses = doses.reshape(20, 20)
# print(reshaped_doses)
#
# ax = plt.axes()
# ax.imshow(reshaped_doses)
# plt.show()


# data = np.range(1, 28, 1))
# print(data)
# reshaped_data = data.reshape(3, 3, 3)
# print(reshaped_data)
# print(reshaped_data[2, 1, 0])
# transposed_data = np.transpose(reshaped_data, (2, 1, 0))
# print(transposed_data)
# print(transposed_data[0, 1, 2])

# measuring_plate_30mm = np.load("170_30.5mm_0.0_0.0.npy")
#
# ax = plt.axes()
# ax.imshow(measuring_plate_30mm)
# plt.show()
# print(type(measuring_plate_30mm), measuring_plate_30mm.shape)
# with open("mp30.txt", "w") as file:
#     line_number = 0
#     for line_number, line in enumerate(measuring_plate_30mm):
#         for voxel_number, voxel in enumerate(line):
#             if voxel > 0:
#                 file.write(str((line_number, voxel_number, voxel)) + "\n")

# movable_voxel = np.array([[-14.,  31.,   0.], [-14.,  31.,  -1.], [-14.,  30.,   0.], [-14.,  30.,  -1.], [-15.,  31., 0.], [-15.,  31.,  -1.], [-15.,  30.,   0.], [-15.,  30.,  -1.]])
# fixed_voxel = np.array([[-13.,  31.,   0.], [-13.,  31.,  -1.], [-13.,  30.,   0.], [-13.,  30.,  -1.], [-14.,  31., 0.], [-14.,  31.,  -1.], [-14.,  30.,   0.], [-14.,  30.,  -1.]])
# intersection = np.array([[-14., 31.,  0.], [-14., 31., -1.], [-14., 30.,  0.], [-14., 30., -1.], [-14., 31.,  0.], [-14., 31., -1.], [-14., 30.,  0.], [-14., 30., -1.], [-14., 31.,  0.], [-14., 30.,  0.], [-15., 31.,  0.], [-15., 30.,  0.]])
#
# ax = plt.axes(projection='3d')
# ax.scatter(movable_voxel[:, 0], movable_voxel[:, 1], movable_voxel[:, 2], color="blue")
# ax.scatter(fixed_voxel[:, 0], fixed_voxel[:, 1], fixed_voxel[:, 2], color = "red")
# ax.scatter(intersection[:, 0], intersection[:, 1], intersection[:, 2], color="yellow")
# plt.show()

import multiprocessing as mp

print(mp.cpu_count())
