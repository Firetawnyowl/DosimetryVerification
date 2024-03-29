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
        if not os.path.exists("results"):
            os.mkdir("results")
        if os.path.exists("path.json"):
            with open("path.json", "r") as file:
                dir_name = json.load(file)
                if dir_name != "":
                    self.dir_name = dir_name
                else:
                    result_dir = os.path.join(os.path.abspath(os.curdir), "results")
                    self.dir_name = result_dir
                    with open('path.json', "w") as file:
                        json.dump(self.dir_name, file)
        else:
            with open('path.json', "w") as file:
                dir_name = os.path.abspath(os.curdir)
                result_dir = os.path.join(dir_name, "results")
                self.dir_name = result_dir
                json.dump(self.dir_name, file)
            #  self.dir_name = os.path.abspath(os.curdir)
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


    # def create_results_folder(self):


    def get_phantom_configuration(self):
        self.phantom = Phantom.Phantom(self.vox_set, self.tomo_shape, voxel_size=self.voxel_size)

        self.measuring_plate = MeasuringPlate.MeasuringPlate(self.doubleSpinBox_PlaceY.value(),
                                                             self.doubleSpinBox_RotX.value(),
                                                             self.doubleSpinBox_RotZ.value(),
                                                             self.voxel_size,
                                                             (self.tomo_shape[0], 1, self.tomo_shape[2]))

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
        dir_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose Path', self.dir_name)
        print(dir_name)
        if dir_name != "":
            self.dir_name = dir_name
            with open('path.json', "w") as file:
                json.dump(self.dir_name, file)

    def show_dialog_visualise_numpy(self):
        try:
            dose_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open numpy file', self.dir_name)
            #doses = np.load(dose_file[0])
            with open(dose_file[0], "r") as file:
                doses = json.load(file)
            layer_dosemap = np.array(doses[0])
            extent = doses[1]
            plt.figure(num=(str(dose_file[0])[len(self.dir_name) + 1:]))
            ax1 = plt.axes()
            ax1.imshow(layer_dosemap, origin="lower", extent=extent)
            plt.show()
            self.textBrowser.clear()
        except ValueError:
            self.textBrowser.setText("Выбран неподходящий формат файла! Выберите файл *.jnpy из папки "
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
            extent = [0, self.tomo_shape[1] * self.voxel_size[1], 0, self.tomo_shape[2] * self.voxel_size[2]]
            pixelsperline = self.tomo_shape[1]
            linesperimage = self.tomo_shape[2]
            xresolution = self.voxel_size[1]
            yresolution = self.voxel_size[2]
        elif self.axis == "Z":
            layer = self.phantom.original_data_layers[layer_index, :, :]
            extent = [0, self.tomo_shape[0] * self.voxel_size[0], 0, self.tomo_shape[1] * self.voxel_size[1]]
            pixelsperline = self.tomo_shape[0]
            linesperimage = self.tomo_shape[1]
            xresolution = self.voxel_size[0]
            yresolution = self.voxel_size[1]
        else:
            layer = self.phantom.original_data_layers[:, layer_index, :]
            extent = [0, self.tomo_shape[0] * self.voxel_size[0], 0, self.tomo_shape[2] * self.voxel_size[2]]
            pixelsperline = self.tomo_shape[0]
            linesperimage = self.tomo_shape[2]
            xresolution = self.voxel_size[0]
            yresolution = self.voxel_size[2]
        if mode == "show":
            ax2 = plt.axes()
            # ax2.imshow(layer, origin="lower")
            ax2.imshow(layer, origin="lower", extent=extent)
            plt.show()
        if mode == "save":
            # with open("path.json", "r") as file:
            #     dir_name = json.load(file)
            dir_name = self.dir_name
            filename = "layer_"+str(layer_index)+"_axis_"+self.axis
            full_name = os.path.join(dir_name, self.short_filename() + "_" + filename)
            with open(full_name + ".dat", "w") as file:
                file.write("PTW-Image File Format\n"+
                           "VERSION		1.0\n"+
                           "PIXELSPERLINE "+str(pixelsperline)+"\n"+
                           "LINESPERIMAGE "+str(linesperimage)+"\n"+
                           "XRESOLUTION "+ str(xresolution).replace(".", ",")+"\n"+
                           "YRESOLUTION "+ str(yresolution).replace(".", ",")+"\n"+
                           "OFFSET		0,00\n"+
                           "UNIT		Gy\n\n")
                for line in np.flip(layer, 0):
                    for value in line:
                        file.write(str("%.4f" % round(value, 4)) + " ")
                    file.write("\n")
            # np.save(full_name, layer)
            layer_ext = [layer.tolist(), extent]
            with open(full_name+".jnpy", "w") as file:
                json.dump(layer_ext, file)
            self.textBrowser.append("Файл сохранён в " + str(full_name) + ".dat и "+str(full_name) + ".jnpy")

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
        pixelsperline = self.tomo_shape[0]
        linesperimage = self.tomo_shape[2]
        xresolution = self.voxel_size[0]
        yresolution = self.voxel_size[2]
        with open(filename + ".dat", "w") as file:
            file.write("PTW-Image File Format\n" +
                       "VERSION		1.0\n" +
                       "PIXELSPERLINE " + str(pixelsperline) + "\n" +
                       "LINESPERIMAGE " + str(linesperimage) + "\n" +
                       "XRESOLUTION " + str(xresolution).replace(".", ",") + "\n" +
                       "YRESOLUTION " + str(yresolution).replace(".", ",") + "\n" +
                       "OFFSET		0,00\n" +
                       "UNIT		Gy\n\n")
            for line in np.flip(self.doses, 0):
                for value in line:
                    file.write(str("%.4f" % round(value, 4)) + " ")
                file.write("\n")

        # np.save(filename, self.doses)
        layer_ext = [self.doses.tolist(), [0, self.tomo_shape[0] * self.voxel_size[0], 0, self.tomo_shape[2] *
                                           self.voxel_size[2]]]
        with open(filename + ".jnpy", "w") as file:
            json.dump(layer_ext, file)
        self.textBrowser.append(str(time.time() - start_time) + " секунд")
        self.textBrowser.append("Данные автоматически сохранены в " + str(filename) + ".dat и в " +
                                str(filename)+".jnpy")

    def show_dose_distribution(self):
        ax = plt.axes()
        ax.imshow(self.doses, origin="lower", extent=[0, self.tomo_shape[0] * self.voxel_size[0], 0, self.tomo_shape[2] *
                                                      self.voxel_size[2]])
        plt.show()

    def short_filename(self):
        rfilename = ""
        for letter in self.file[0][::-1]:
            if letter != "/" and letter != "\\":
                rfilename += letter
            else:
                break
        filename = rfilename[:4:-1]
        return filename

    def save_result(self):
        # with open("path.json", "r") as file:
        #     dir_name = json.load(file)
        # print(dir_name)

        print(self.short_filename())
        filename = os.path.join(self.dir_name, self.short_filename() + "_" + str(self.doubleSpinBox_PlaceY.value()) + "mm_" + str(
            self.doubleSpinBox_RotX.value()) + "_" + str(self.doubleSpinBox_RotZ.value()))
        return filename


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    mp.freeze_support()
    main()
