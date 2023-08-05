#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 04:18:54 2018

@author: abdul
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton, 
QAction, QLabel, QMessageBox)
from PyQt5.QtWidgets import QGraphicsView,QGraphicsScene,QGraphicsEllipseItem
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush,QPen

class Structure(QMainWindow):
    
    def __init__(self,parent=None,nDims=0):
        super(Structure,self).__init__(parent)
        self.nDims=nDims
        
        self.gView=QGraphicsView(self)
        self.scene = QGraphicsScene(self.gView)
        self.scene.setBackgroundBrush(QtCore.Qt.black)
        self.item = QGraphicsEllipseItem(-20, -10, 40, 20)

        self.item.setPen(QPen(QtCore.Qt.white))
        self.scene.addItem(self.item)
        self.gView.setScene(self.scene)