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
import numpy as np
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

        # Carga el XML para reconocimiento facial
        self.face_detect = cv2.CascadeClassifier(
                                "lbpcascade_frontalface.xml")

        self.show()


    def read_frame(self):
        """Captura un cuadro de la camara y lo procesa"""

        ok, frame = self.camara.read()

        if not ok:
            #Cuando se terminan los videos, comienza desde el principio
            self.camara.release()
            self.i = (self.i + 1) % 3
            self.camara = cv2.VideoCapture("video_"+str(self.i)+".mp4")
            # self.img.setText("Sin video")
            return

        # Conversion a gris para deteccion de rostros
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#        frame_gray_eh = cv2.equalizeHist(frame_gray)

        frame[:,:,0] = frame_gray
        frame[:,:,1] = frame_gray
        frame[:,:,2] = frame_gray

        # Deteccion de los rostros 
        a = self.scaleFactor.value()
        b = self.minNeighbors.value()
        faces = self.face_detect.detectMultiScale(frame_gray, a, b)

        # Procesamiento de cada rostro
        for (x, y, w, h) in faces:
            # Calculo de la temperatura corporal, el maximo de la ventana del
            # rostro 
            val = frame_gray[y:y+h, x:x+w].max()

            #Obtiene todas las coordenadas relativas a la ventana del rostro
            # donde detecta el maximo
            val_x, val_y = np.where(frame_gray[y:y+h, x:x+w] == val)

            dy = self.temp_max.value() - self.temp_min.value()
            dx = 255
            temp_cuerpo_negro = val * (dy/dx) + self.temp_min.value()
            temp = temp_cuerpo_negro / self.emisividad.value()

            # Muestra la informacion sobreimpresa en la imagen
            text = "{0:0.1f} C".format(temp)
            text_s = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(frame, (x,y-4), (x+text_s[0][0], y-4-text_s[0][1]), (0,0,0), cv2.FILLED)
            cv2.putText(frame, text, (x,y-4),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255))
            cv2.circle(frame, (x+val_x[0], y+val_y[0]), 1, (255,0,0), 5)

            if temp >= self.umbral_fiebre.value():
                color = (0,0,255)
            else:
                color = (0,255,0)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        #Conversion de la imagen de opencv a qt
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
