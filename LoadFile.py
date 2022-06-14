# -*- coding: utf-8 -*-

import os
import numpy as np


class LoadFile:
    def __init__(self, filename):
        self.filename = filename
        # self.shape = shape
        self.data, self.size = self.read_file()


        # делим на слои не по z, а по y (вдоль хода пучка) [слой по y, строка, воксель в строке]:
        # self.reshaped_data = np.transpose(self.original_data, (1, 0, 2))

    def read_file(self):
        # dir_ = os.path.join(os.path.abspath(os.curdir), 'data\\')
        with open(self.filename, 'rb') as f:
            data = np.fromfile(f, dtype=np.float32)
        number_of_voxels = len(data)
        return data[::-1], number_of_voxels

    def reshaped_data(self, shape):
        original_data = self.data.reshape(shape[2], shape[1], shape[0])
        reshaped_data = np.transpose(original_data, (1, 0, 2))
        return reshaped_data
