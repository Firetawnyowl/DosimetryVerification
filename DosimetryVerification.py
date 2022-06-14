# -*- coding: utf-8 -*-

import sys
import os
import time

import numpy as np
import multiprocessing as mp
import json
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import matplotlib.pyplot as plt
import LoadFile
import Phantom
import MeasuringPlate
import gui_main


class DoseCalculating(QObject):
    finished = pyqtSignal(np.ndarray)
    progress = pyqtSignal(list)

    def __init__(self, measuring_plate: MeasuringPlate.MeasuringPlate, phantom_part: Phantom.PhantomPart, filename):
        super().__init__()
        self.measuring_plate = measuring_plate
        self.phantom_part = phantom_part
        self.filename = filename
        self.number_of_processes = mp.cpu_count()

    def run(self):
        dose_distribution = MeasuringPlate.DoseDistribution(self.measuring_plate, self.phantom_part)
        rows_number = dose_distribution.rows_number
        voxels_in_row_number = dose_distribution.voxels_number
        doses = dose_distribution.doses
        # doses = np.transpose(dose_distribution.doses, (1, 0))
        for i in dose_distribution.dose_map():
            # print(i[3])
            try:
                self.progress.emit(["строка: "+str(i[0])+"  воксель: "+str(i[1])+"  доза: "+str(i[2])+" Гр", i[3], i[4]])
            except Exception as ex:
                print(type(ex).__name__, ex.args)
        with open(self.filename + ".txt", "w") as file:
            for line in doses:
                for value in line:
                    file.write(str(round(value, 4)) + " ")
                file.write("\n")
        np.save(self.filename, doses)
        self.finished.emit(doses)


class App(QtWidgets.QMainWindow, gui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file = None
        if os.path.exists("path.json"):
            with open("path.json", "r") as file:
                self.dir_name = json.load(file)
        else:
            self.dir_name = os.path.abspath(os.curdir)
        self.vox_set = None
        self.action_LoadTomo.triggered.connect(self.show_dialog_load)
        self.action_ChoosePath.triggered.connect(self.show_dialog_choose_path)
        self.action.triggered.connect(lambda: self.show_dialog_visualise_numpy())
        self.tomo_shape = (0, 0, 0)
        self.spinBoxShapeX.valueChanged.connect(lambda: self.shape_value_changed())
        self.spinBoxShapeY.valueChanged.connect(lambda: self.shape_value_changed())
        self.spinBoxShapeZ.valueChanged.connect(lambda: self.shape_value_changed())
        self.pushButton_Show3D.clicked.connect(lambda: self.show_3d())
        self.pushButton_Run.clicked.connect(lambda: self.calculate_dose_distribution())
        self.pushButton_ShowResult2D.clicked.connect(lambda: self.show_dose_distribution())

        self.voxel_size = (self.doubleSpinBoxXSize.value(),
                           self.doubleSpinBoxYSize.value(),
                           self.doubleSpinBoxZSize.value())
        self.doubleSpinBoxXSize.valueChanged.connect(lambda: self.change_voxel_size())
        self.doubleSpinBoxYSize.valueChanged.connect(lambda: self.change_voxel_size())
        self.doubleSpinBoxZSize.valueChanged.connect(lambda: self.change_voxel_size())

        self.phantom = None
        self.measuring_plate = None
        self.phantom_part = None
        self.doses = None

    def get_phantom_configuration(self):
        self.phantom = Phantom.Phantom(self.vox_set, self.tomo_shape, voxel_size=self.voxel_size)

        self.measuring_plate = MeasuringPlate.MeasuringPlate(self.doubleSpinBox_PlaceY.value(),
                                                             self.doubleSpinBox_RotX.value(),
                                                             self.doubleSpinBox_RotZ.value(),
                                                             self.voxel_size,
                                                             (1, self.tomo_shape[2], self.tomo_shape[0]))

        self.phantom_part = Phantom.PhantomPart(self.phantom, self.measuring_plate)

    def show_dialog_load(self):
        home_dir = os.path.join(os.path.abspath(os.curdir), "data")
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        if self.file[0]:
            self.vox_set = LoadFile.LoadFile(self.file[0])
            self.textBrowser.setText("Загружен файл " + str(self.file[0]) + "\nКоличество вокселей:  "
                                     + str(self.vox_set.size) + "\nЗадайте размеры вокселя и форму томограммы.")
            self.shape_value_changed()

    def show_dialog_choose_path(self):
        self.dir_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose Path', self.dir_name)
        print(self.dir_name)
        with open('path.json', "w") as file:
            json.dump(self.dir_name, file)

    def show_dialog_visualise_numpy(self):
        try:
            dose_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open numpy file', self.dir_name)
            doses = np.load(dose_file[0])
            plt.figure(num=(str(dose_file[0])[len(self.dir_name) + 1:]))
            ax1 = plt.axes()
            ax1.imshow(doses)
            plt.show()
            self.textBrowser.clear()
        except ValueError:
            # except Exception as ex:
            # print(type(ex).__name__, ex.args)
            self.textBrowser.setText("Выбран неподходящий формат файла! Выберите файл *.npy из папки "
                                     "с результатами расчётов")

    def shape_value_changed(self):
        shape_x = self.spinBoxShapeX.value()
        shape_y = self.spinBoxShapeY.value()
        shape_z = self.spinBoxShapeZ.value()
        if self.vox_set is not None:
            if shape_x * shape_y * shape_z != self.vox_set.size:
                self.textBrowser.append("Количество вокселей " + str(self.vox_set.size) +
                                        " не соответствует форме " + str(shape_x) + "x" + str(shape_y)
                                        + "x" + str(shape_z))
                self.pushButton_Show3D.setEnabled(False)
                self.pushButton_Run.setEnabled(False)
            else:
                self.textBrowser.clear()
                self.pushButton_Show3D.setEnabled(True)
                self.pushButton_Run.setEnabled(True)
        else:
            self.textBrowser.setText("Файл не выбран! Пожалуйста, выберите файл\n (Файл --> Загрузить файл *.dose)")
        self.tomo_shape = (shape_x, shape_y, shape_z)

    def change_voxel_size(self):
        self.voxel_size = (self.doubleSpinBoxXSize.value(),
                           self.doubleSpinBoxYSize.value(),
                           self.doubleSpinBoxZSize.value())

    def show_3d(self):
        self.get_phantom_configuration()
        ax = plt.axes(projection='3d')
        self.phantom.plot_edges(ax)
        self.measuring_plate.plot_edges(ax)
        self.phantom_part.plot_edges(ax)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    def report_progress(self, progress):
        # print(progress[0], progress[1])
        self.textBrowser.append(progress[0])
        progress_value = progress[1]
        self.progressBar.setValue(int(progress_value))
        if progress[2] is not None:
            rest_time_minutes = progress[2]//60
            rest_time_seconds = progress[2] % 60
            self.labelTtimeProgress.setText("осталось примерно "+str(int(rest_time_minutes)) +
                                            " минут "+str(int(rest_time_seconds))+" секунд")
        if int(progress_value) == 100:
            self.labelTtimeProgress.setText("расчёт окончен")

    def get_doses(self, doses):
        self.doses = doses

    def calculate_dose_distribution(self):
        self.textBrowser.clear()
        self.labelTtimeProgress.clear()
        self.shape_value_changed()
        self.get_phantom_configuration()
        filename = self.save_result()
        # dose_distribution = MeasuringPlate.DoseDistribution(self.measuring_plate, self.phantom_part)
        # self.doses = np.transpose(dose_distribution.doses, (1, 0))
        # print("shape doses: ", self.doses.shape)
        # for i in dose_distribution.dose_map():
        #     self.textBrowser.append(str(i))
        # with open(filename + ".txt", "w") as file:
        #     for line in self.doses:
        #         for value in line:
        #             file.write(str(value) + " ")
        #         file.write("\n")
        #
        # np.save(filename, self.doses)
        # self.textBrowser.append(str(time.time() - start_time) + " секунд")
        # self.textBrowser.append("Данные автоматически сохранены в " + str(filename) + ".txt")

        try:
            self.thread = QThread()
            self.worker = DoseCalculating(self.measuring_plate, self.phantom_part, filename)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.report_progress)
            self.worker.finished.connect(self.get_doses)

            self.thread.start()
            self.pushButton_Run.setEnabled(False)
            self.pushButton_ShowResult2D.setEnabled(False)
            self.thread.finished.connect(lambda: self.pushButton_Run.setEnabled(True))
            self.thread.finished.connect(lambda: self.pushButton_ShowResult2D.setEnabled(True))
        except Exception as ex:
            print(type(ex).__name__, ex.args)

        # self.pushButton_ShowResult2D.setEnabled(True)

    def show_dose_distribution(self):
        ax = plt.axes()
        ax.imshow(self.doses)
        filename = self.save_result()
        plt.savefig(filename + ".png")
        self.textBrowser.append("Картинка автоматически сохранена в " + str(filename) + ".png")
        plt.show()

    def save_result(self):
        with open("path.json", "r") as file:
            dir_name = json.load(file)
        reversed_filename = ""
        for letter in self.file[0][::-1]:
            if letter != "/":
                reversed_filename += letter
            else:
                break
        filename = dir_name + "/" + reversed_filename[:4:-1] + "_" + str(self.doubleSpinBox_PlaceY.value()) + "mm_" \
                            + str(self.doubleSpinBox_RotX.value()) + "_" + str(self.doubleSpinBox_RotZ.value())
        return filename


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()