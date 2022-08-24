# -*- coding: utf-8 -*-

import sys
import os
import time
import multiprocessing as mp
import numpy as np
import json
from PyQt5 import QtWidgets
import matplotlib
import matplotlib.pyplot as plt
import LoadFile
import Phantom
import MeasuringPlate
import gui_main


# from PyQt5 import QtCore


# class EmittingStream(QtCore.QObject):
#
#     textWritten = QtCore.pyqtSignal(str)
#
#     def write(self, text):
#         self.textWritten.emit(str(text))


class App(QtWidgets.QMainWindow, gui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # sys.stdout = EmittingStream()
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
        self.pushButton_showLayer3D.clicked.connect(lambda: self.show_3d_original_layer())

        self.voxel_size = (self.doubleSpinBoxXSize.value(),
                           self.doubleSpinBoxYSize.value(),
                           self.doubleSpinBoxZSize.value())
        self.doubleSpinBoxXSize.valueChanged.connect(lambda: self.change_voxel_size())
        self.doubleSpinBoxYSize.valueChanged.connect(lambda: self.change_voxel_size())
        self.doubleSpinBoxZSize.valueChanged.connect(lambda: self.change_voxel_size())
        self.radioButton_X.clicked.connect(lambda: self.choose_axis())
        self.radioButton_Y.clicked.connect(lambda: self.choose_axis())
        self.radioButton_Z.clicked.connect(lambda: self.choose_axis())
        self.pushButton_layerDoseMap.clicked.connect(lambda: self.dose_map_in_layer())
        self.pushButton_saveLayer.clicked.connect(lambda: self.dose_map_in_layer(mode="save"))

        self.phantom = None
        self.measuring_plate = None
        self.phantom_part = None
        self.doses = None
        self.axis = "Y"

    # def __del__(self):
    #     # Restore sys.stdout
    #     sys.stdout = sys.__stdout__
    #
    # def normalOutputWritten(self, text):
    #     """Append text to the QTextEdit."""
    #     self.textBrowser.append(text)

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
            # self.get_phantom_configuration()

    def show_dialog_choose_path(self):
        # if os.path.exists("path.json"):
        #     print("exists")
        #     with open("path.json", "r") as file:
        #         home_dir = json.load(file)
        #         print(home_dir)
        #         print("test")
        # else:
        #     home_dir = os.path.abspath(os.curdir)
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
            self.textBrowser.setText("Выбран неподходящий формат файла! Выберите файл *.npy из папки "
                                     "с результатами расчётов")
        except FileNotFoundError:
            self.textBrowser.setText("Файл не был выбран.")

    def choose_axis(self):
        self.spinBox_layerNumber.setValue(0)
        if self.radioButton_X.isChecked():
            self.axis = "X"
            self.spinBox_layerNumber.setMaximum(self.spinBoxShapeX.value()-1)
        elif self.radioButton_Y.isChecked():
            self.axis = "Y"
            self.spinBox_layerNumber.setMaximum(self.spinBoxShapeY.value()-1)
        elif self.radioButton_Z.isChecked():
            self.axis = "Z"
            self.spinBox_layerNumber.setMaximum(self.spinBoxShapeZ.value()-1)

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
                self.pushButton_showLayer3D.setEnabled(False)
                self.pushButton_layerDoseMap.setEnabled(False)
                self.pushButton_saveLayer.setEnabled(False)
            else:
                self.textBrowser.clear()
                self.pushButton_Show3D.setEnabled(True)
                self.pushButton_Run.setEnabled(True)
                self.pushButton_showLayer3D.setEnabled(True)
                self.pushButton_layerDoseMap.setEnabled(True)
                self.pushButton_saveLayer.setEnabled(True)
                self.phantom = Phantom.Phantom(self.vox_set, (shape_x, shape_y, shape_z), voxel_size=self.voxel_size)
                self.choose_axis()

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

    def show_3d_original_layer(self):
        layer_index = self.spinBox_layerNumber.value()
        ax = plt.axes(projection='3d')
        self.phantom.plot_edges(ax)
        self.phantom.plot_layer(ax, self.axis, layer_index, "red")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    def dose_map_in_layer(self, mode="show"):
        layer_index = self.spinBox_layerNumber.value()
        if self.axis == "X":
            layer = self.phantom.original_data_layers[:, :, layer_index]
        elif self.axis == "Z":
            layer = self.phantom.original_data_layers[layer_index, :, :]
        else:
            layer = self.phantom.original_data_layers[:, layer_index, :]
        if mode == "show":
            ax2 = plt.axes()
            ax2.imshow(layer)
            plt.show()
        if mode == "save":
            with open("path.json", "r") as file:
                dir_name = json.load(file)
                filename = "layer_"+str(layer_index)+"_axis_"+self.axis
            full_name = dir_name+"/"+self.short_filename() + "_" + filename
            with open(full_name + ".txt", "w") as file:
                for line in layer:
                    for value in line:
                        file.write(str("%.4f" % round(value, 4)) + " ")
                    file.write("\n")
            np.save(full_name, layer)
            self.textBrowser.append("Файл сохранён в " + str(full_name) + ".txt и "+str(full_name) + ".npy")

    def calculate_dose_distribution(self):
        self.textBrowser.clear()
        self.shape_value_changed()
        self.get_phantom_configuration()
        start_time = time.time()
        dose_distribution = MeasuringPlate.DoseDistribution(self.measuring_plate, self.phantom_part)
        filename = self.save_result()

        self.pushButton_ShowResult2D.setEnabled(True)
        try:
            dose_distribution.dose_map()
        except Exception as ex:
            print(type(ex).__name__, ex.args)
        self.doses = np.transpose(dose_distribution.doses, (1, 0))
        print("Расчёт завершён. Ожидайте вывод данных на экран приложения.")
        # for i in dose_distribution.dose_map():
        #     self.textBrowser.append(str(i))
        try:
            for i in range(self.doses.shape[0]):
                for j in range(self.doses.shape[1]):
                    self.textBrowser.append(str(i)+" "+str(j)+" "+str(self.doses[i, j]))
        except Exception as ex:
            print(type(ex).__name__, ex.args)
        with open(filename + ".txt", "w") as file:
            for line in self.doses:
                for value in line:
                    file.write(str("%.4f" % round(value, 4)) + " ")
                file.write("\n")

        np.save(filename, self.doses)
        self.textBrowser.append(str(time.time() - start_time) + " секунд")
        self.textBrowser.append("Данные автоматически сохранены в " + str(filename) + ".txt")

    def show_dose_distribution(self):
        ax = plt.axes()
        ax.imshow(self.doses)
        filename = self.save_result()
        plt.savefig(filename + ".png")
        self.textBrowser.append("Картинка автоматически сохранена в " + str(filename) + ".png")
        plt.show()

    def short_filename(self):
        rfilename = ""
        for letter in self.file[0][::-1]:
            if letter != "/":
                rfilename += letter
            else:
                break
        filename = rfilename[:4:-1]
        return filename

    def save_result(self):
        with open("path.json", "r") as file:
            dir_name = json.load(file)
        filename = dir_name + "/" + self.short_filename() + "_" + str(self.doubleSpinBox_PlaceY.value()) + "mm_" + str(
            self.doubleSpinBox_RotX.value()) + "_" + str(self.doubleSpinBox_RotZ.value())
        return filename


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    mp.freeze_support()
    main()
