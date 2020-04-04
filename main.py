#!/usr/bin/python3

##############################################################
# Aplicacion para medir la temperatura corporal de las personas
# utilizando una camara termica
# 
# CITEDEF - DVA - COVID-19
#
###############################################################

import sys
import cv2
from PySide2 import QtCore, QtWidgets
import gui


class AppWindow(QtWidgets.QDialog, gui.Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camara = cv2.VideoCapture("video.mp4")

        # Timer para la captura de un cuadro de video cada 33ms
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.read_frame)
        self.timer.start(33)

        self.show()


    def read_frame(self):
        """Captura un cuadro de la camara y lo procesa"""

        ok, frame = self.camara.read()

        if ok:
            print("OK")
        else:
            self.img.setText("Sin video")

    def unlock_conf(self):
        self.lock.setEnabled(True)
        self.unlock.setEnabled(False)
        self.temp_min.setEnabled(True)
        self.temp_max.setEnabled(True)
        self.emisividad.setEnabled(True)
        self.umbral_fiebre.setEnabled(True)

    def lock_conf(self):
        self.lock.setEnabled(False)
        self.unlock.setEnabled(True)
        self.temp_min.setEnabled(False)
        self.temp_max.setEnabled(False)
        self.emisividad.setEnabled(False)
        self.umbral_fiebre.setEnabled(False)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    win = AppWindow()
    app.exec_()

#  vim: set ts=4 sw=4 tw=79 et :
