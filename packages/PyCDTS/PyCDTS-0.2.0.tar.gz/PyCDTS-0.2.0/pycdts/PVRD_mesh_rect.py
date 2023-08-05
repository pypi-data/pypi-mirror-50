#!/usr/bin/env python3
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.
#
# The authors acknowledge that this material is based upon work supported 
# by the U.S. Department of Energy’s Office of Energy Efficiency and Renewable
# Energy (EERE) under Solar Energy Technologies Office (SETO) Agreement 
# Number DE-EE0007536.
#
# This work is the combined efforts of ASU, First Solar, SJSU and Purdue 
# University. People involved in this project are
# Abdul Rawoof Shaik (ASU)
# Christian Ringhofer (ASU)
# Dragica Vasileska (ASU)
# Daniel Brinkman (SJSU)
# Igor Sankin (FSLR)
# Dmitry Krasikov (FSLR)
# Hao Kang (Purdue)
# Benes Bedrich (Purdue)
#
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:51:13 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from PyQt5.QtGui import (
        QPen,QBrush,QKeyEvent,QPainter
        )

from PyQt5.QtWidgets import (
        QMessageBox,QGraphicsItem,QGraphicsRectItem,QGraphicsLineItem
        )

from PyQt5.QtCore import (
        Qt,QLineF
        )

from PyQt5 import QtCore

from PVRD_geometryMainWindow import fac
from PVRD_sim_rectDlg import PVRD_sim_rectDlg

class PVRD_mesh_rect(QGraphicsRectItem):
    def __init__(self,bx=0,by=0,width=0,height=0,Name="",matName="",pen=None,brush=None,projWindow=None,parent=None,pCindx=None):
        super(PVRD_mesh_rect,self).__init__(bx*fac,by*fac,width*fac,height*fac,parent)
        self.projWindow=projWindow
        self.bx=bx*fac
        self.by=by*fac
        self.w=width*fac
        self.h=height*fac
        if pen is None:
            pen=QPen(QtCore.Qt.black)
            pen.setCosmetic(True)
            pen.setWidth(1)
            pen.setStyle(Qt.SolidLine)
        if brush is None:
            brush=QBrush(QtCore.Qt.white)
        self.pen=pen
        self.brush=brush
        self.setPen(pen)
#        self.setBrush(brush)
        self.setAcceptHoverEvents(True)
        self.selectionOffset=2
        self.pCindx=pCindx
        
        self.setFlags(
                QGraphicsItem.ItemIsSelectable
                |QGraphicsItem.ItemIsFocusable
                )
        self.dlgBox=PVRD_sim_rectDlg(bx,by,width,height,Name,matName,parent=self)
        self.dlgBox.Mechanism_CB.addItem('')
        for mech in self.projWindow.pC.allRectList[self.pCindx].mechList:
            self.dlgBox.Mechanism_CB.addItem(mech)
            
        self.dlgBox.Reactions_CB.addItem('')
        for mech in self.projWindow.pC.allRectList[self.pCindx].reactionList:
            self.dlgBox.Reactions_CB.addItem(mech)
            
        self.dlgBox.PointDefects_CB.addItem('')
        for mech in self.projWindow.pC.allRectList[self.pCindx].speciesList:
            self.dlgBox.PointDefects_CB.addItem(mech)
        
#        nPoints=10
#        for ii in range(0,nPoints):
#            line=QGraphicsLineItem(self.bx,self.by,self.bx+ii*self.w/nPoints,self.by,parent)
#            line.setPen(QPen(QtCore.Qt.white))
        
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Q and self.isSelected:
                self.dlgBox.exec_()
            
            if event.key() == Qt.Key_F:
                self.projWindow.fit()
                
    def paint(self,painter,options,index):
        painter.setPen(self.pen)
        nPoints=10
        for ii in range(0,nPoints):
            painter.drawLine(QLineF(self.bx,self.by,self.bx+ii*self.w/nPoints,self.by))