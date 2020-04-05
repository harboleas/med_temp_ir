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
from PySide2 import QtCore, QtGui, QtWidgets
import gui


class AppWindow(QtWidgets.QDialog, gui.Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.camara = cv2.VideoCapture("video_0.mp4")
        self.i = 0

        # Timer para la captura de un cuadro de video cada 33ms
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.read_frame)
        self.timer.start(33)

        # Cargo el XML para reconocimiento facial
        self.face_detect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        self.show()


    def read_frame(self):
        """Captura un cuadro de la camara y lo procesa"""

        ok, frame = self.camara.read()

        if not ok:
            #Cuando se termina el video, comienzo desde el principio
            self.camara.release()
            self.i = (self.i + 1) % 2
            self.camara = cv2.VideoCapture("video_"+str(self.i)+".mp4")
            # self.img.setText("Sin video")
            return

        # Convierto a gray para deteccion de rostros
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame[:,:,0] = frame_gray
        frame[:,:,1] = frame_gray
        frame[:,:,2] = frame_gray
        # Detecto rostros y los recuadro
        a = self.scaleFactor.value()
        b = self.minNeighbors.value()
        faces = self.face_detect.detectMultiScale(frame_gray, a, b)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0))

        #Convierto imagen de opencv a qt
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0],
                frame.shape[1]*frame.shape[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())

        self.img.setPixmap(pixmap)


    def unlock_conf(self):
        self.lock.setEnabled(True)
        self.unlock.setEnabled(False)
        self.temp_min.setEnabled(True)
        self.temp_max.setEnabled(True)
        self.emisividad.setEnabled(True)
        self.umbral_fiebre.setEnabled(True)
        self.scaleFactor.setEnabled(True)
        self.minNeighbors.setEnabled(True)

    def lock_conf(self):
        self.lock.setEnabled(False)
        self.unlock.setEnabled(True)
        self.temp_min.setEnabled(False)
        self.temp_max.setEnabled(False)
        self.emisividad.setEnabled(False)
        self.umbral_fiebre.setEnabled(False)
        self.scaleFactor.setEnabled(False)
        self.minNeighbors.setEnabled(False)



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    win = AppWindow()
    app.exec_()

#  vim: set ts=4 sw=4 tw=79 et :
