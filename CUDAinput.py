# -*- coding: utf-8 -*-

import MeasuringPlate
import Phantom


def cuda_input_matrix(measuring_plate: MeasuringPlate.MeasuringPlate, phantom_part: Phantom.PhantomPart):
    phantom_matrix = phantom_part.cuda_matrix()
    plate_matrix = measuring_plate.cuda_matrix()
    return phantom_matrix, plate_matrix
