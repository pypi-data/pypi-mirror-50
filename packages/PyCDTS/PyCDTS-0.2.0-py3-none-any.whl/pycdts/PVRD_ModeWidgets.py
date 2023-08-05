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
Created on Sun Nov  4 21:59:59 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from PyQt5.QtWidgets import (
        QWidget, QPushButton, QVBoxLayout, QGraphicsView, QGraphicsScene,
        QHBoxLayout, QMessageBox, QToolBar, QStackedWidget, QAction,
        QGraphicsRectItem, QGraphicsItem, QLabel, QGroupBox, QComboBox, 
        QAbstractItemView, QScrollArea, QGridLayout, QLineEdit, QGraphicsLineItem,
        QGraphicsTextItem, QCheckBox, QSizePolicy, QTextEdit, QProgressBar
        )
from PyQt5.QtCore import (
        Qt, QDataStream, QIODevice
        )
from .generalFunctions import (
        createTBAction, fac, colorList, bStyleList
        )
from PyQt5.QtGui import (
        QKeyEvent, QBrush, QPen, QFont, QDoubleValidator
        )

from .PVRD_DialogBox import (
        PVRD_RectangleDlg_Mode1_Boundary,
        PVRD_RectangleDlg_Mode1_Material,
        PVRD_MaterialDlg_Mode1_GrainBoundary,
        PVRD_LineDlg_Mode1_GrainBoundary,
        PVRD_Mode4_TemperatureDlg_Point,
        PVRD_Mode4_TemperatureDlg_NCooling,
        PVRD_Mode4_LightDlg_Point,
        PVRD_Mode4_BiasDlg_Point
        )
from .PVRD_GraphicsItems import (
        PVRD_Rectangle_Mode1_Boundary,
        PVRD_Rectangle_Mode1_Material,
        PVRD_Rectangle_Mode1_GrainBoundary,
        PVRD_Line_Mode1_GrainBoundary,
        PVRD_Line_Mode1_GrainBoundary_NoSelect,
        PVRD_Rectangle_Mode2,
        PVRD_Line_Mode2,
        PVRD_Point_Mode2,
        PVRD_pgLine_Mode4,
        PVRD_Rectangle_Mode5
        )
from .PVRD_projectContainer import (
        PVRD_rectData,
        PVRD_lineData,
        PVRD_ParTimeData,
        initEndTime,
        PVRD_IC_Data,
        PVRD_BC_Data
        )
from numpy import isclose

from .generalFunctions import (
        prec, PVRD_formEnergyWindow, OutLog, getReactionRHS, getReactionLHS
        )

from .solutionBrowser import (
        PVRD_FormEnergyVisualizer
        )

from .latexQLabel import latexQLabel

import pyqtgraph as pg
import numpy as np

import pyqtgraph.console

import scipy.constants as PhysConst

from .solutionBrowser import (
        PVRD_ConcVisualizer,PVRD_FiVisualizer,PVRD_FieldVisualizer,
        PVRD_FluxVisualizer,PVRD_BandsVisualizer
        )

import h5py

import sys


###############################################################################

class PVRD_Mode0_Widget(QWidget):
    """
    Mode 0 Widget is for displaying all widgets for selecting the material database.
    """
    def __init__(self,projWindow=None,parent=None):
        super(PVRD_Mode0_Widget,self).__init__(parent)
        self.projWindow=projWindow
#        self.pb=QPushButton("Display DB information")
#        vLayout=QVBoxLayout()
#        vLayout.addWidget(self.pb)
#        vLayout.addStretch()
#        self.setLayout(vLayout)
#        self.pb.setEnabled(False)
        
    def updateDisplay(self):
#        self.scrollArea = QScrollArea(self)
#        self.scrollArea.setWidgetResizable(True)
        self.matGBox=QGroupBox("Materials")
        self.speciesGBox=QGroupBox("Species")
        self.reactionsGBox=QGroupBox("Reactions")
        
        matSBox=QScrollArea()
        matSBox.setWidget(self.matGBox)
        matSBox.setWidgetResizable(True)
        speciesSBox=QScrollArea()
        speciesSBox.setWidget(self.speciesGBox)
        speciesSBox.setWidgetResizable(True)
        reactionsSBox=QScrollArea()
        reactionsSBox.setWidget(self.reactionsGBox)
        reactionsSBox.setWidgetResizable(True)
        
        
        
        hLayout=QHBoxLayout()
        hLayout.addWidget(matSBox)
        hLayout.addWidget(speciesSBox)
        hLayout.addWidget(reactionsSBox)
        hLayout.addStretch()
        
        vLayout=QVBoxLayout()
        self.pbList=list()
        for mat in self.projWindow.pC.db.materials:
            pb=QPushButton(mat)
            pb.clicked.connect(self.openFormEnergyWindow)
            self.pbList.append(pb)
            vLayout.addWidget(pb)
        vLayout.addStretch()
        self.matGBox.setLayout(vLayout)
        
        vLayout=QVBoxLayout()
        for species in self.projWindow.pC.db.species:
            vLayout.addWidget(QLabel(species))
        vLayout.addStretch()
        self.speciesGBox.setLayout(vLayout)
        
        vLayout=QVBoxLayout()
        for reaction in self.projWindow.pC.db.reactions:
            vLayout.addWidget(QLabel(reaction))
        vLayout.addStretch()
        self.reactionsGBox.setLayout(vLayout)
        
#        self.qLabel.setText()
#        self.qLabel.setFont(QFont("Times",weight=QFont.Bold))
        vLayout=QVBoxLayout()
#        vLayout.addWidget(self.scrollArea)
#        vLayout.addWidget(self.qLabel)
        vLayout.addLayout(hLayout)
        vLayout.addStretch()
        self.setLayout(vLayout)
        
    def openFormEnergyWindow(self):
        pb=self.sender()
        matName=pb.text()

        window=PVRD_formEnergyWindow(matName,self.projWindow.pC.db,self)
        window.show()
        window1=PVRD_FormEnergyVisualizer(matName,self.projWindow.pC.db,None,1,self)
        window1.show()

############################################################################### 
       
class PVRD_Mode1_Widget(QWidget):
    """
    Mode 1 Widget is for displaying all widgets for creating the geometric structure.
    """
    def __init__(self,projWindow=None,parent=None):
        super(PVRD_Mode1_Widget,self).__init__(parent)
        
        self.projWindow=projWindow
        self.stackWidget=QStackedWidget()
        
        self.mode0_widget=PVRD_Mode1_GeoMode0_Widget(projWindow=projWindow,modeWidget=self)
        self.mode1_widget=PVRD_Mode1_GeoMode1_Widget(projWindow=projWindow,modeWidget=self)
        self.mode2_widget=PVRD_Mode1_GeoMode2_Widget(projWindow=projWindow,modeWidget=self)
        
        self.stackWidget.addWidget(self.mode0_widget)
        self.stackWidget.addWidget(self.mode1_widget)
        self.stackWidget.addWidget(self.mode2_widget)
        
        self.stackWidget.setCurrentIndex(0)
        
        vLayout=QVBoxLayout()
        
        self.createTopBar()
        vLayout.addWidget(self.topBar)
        vLayout.addWidget(self.stackWidget)
        
        self.setLayout(vLayout)
        
    def createTopBar(self):
        self.topBar=QToolBar('TestTB')
        self.topBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.topBar.boundaryAction=createTBAction("",
                                     "Boundary",
                                     "To Specify the Boundaries",
                                     "2D Boundary",
                                     self.projWindow.pC.geoMode==0,
                                     self.updateLayout,self)
        self.topBar.addAction(self.topBar.boundaryAction)
        
        self.topBar.materialAction=createTBAction("",
                                     "Materials",
                                     "To Specify the Materials",
                                     "2D Materials",
                                     self.projWindow.pC.geoMode==1,
                                     self.updateLayout,self)
        self.topBar.addAction(self.topBar.materialAction)
        
        self.topBar.gBoundaryAction=createTBAction("",
                                     "Grain Boundaries",
                                     "To Specify the Grain Boundaries",
                                     "2D Grain Boundaries",
                                     self.projWindow.pC.geoMode==2,
                                     self.updateLayout,self)
        self.topBar.addAction(self.topBar.gBoundaryAction)
        
        self.topBar.setOrientation(Qt.Horizontal)
        
    def updateLayout(self):
        geoMode=0
        action = self.sender()
        
        if isinstance(action, QAction):
            if self.topBar.boundaryAction==action:
                geoMode=0
            if self.topBar.materialAction==action:
                geoMode=1
            if self.topBar.gBoundaryAction==action:
                geoMode=2
        else:
            geoMode=self.projWindow.pC.geoMode
        self.stackWidget.setCurrentIndex(geoMode)

###############################################################################

class PVRD_Mode1_GeoMode0_Widget(QWidget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode1_GeoMode0_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.modeWidget=modeWidget
        
        self.isBoundaryDone=False
        self.projWindow.pC.geoMode=0
        
    def updateLayout(self):
        hLayout=QHBoxLayout()
        
        self.gView=QGraphicsView()
        self.scene = QGraphicsScene(self.gView)
        self.scene.setBackgroundBrush(Qt.black)

        self.gView.setScene(self.scene)
        self.gView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        hLayout.addWidget(self.gView)
        
        self.createSideBar()
        hLayout.addWidget(self.sideBar)
        self.setLayout(hLayout)
        if self.isBoundaryDone:
            self.modeWidget.mode1_widget.updateLayout()
        
    def createSideBar(self):
        self.sideBar=QToolBar('GeoMode0_ToolBar')
        self.sideBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.sideBar.boundaryAction_0D=createTBAction("",
                                     "Dot (0D)",
                                     "To Specify the 0D Boundaries",
                                     "0D Boundary",
                                     self.projWindow.pC.nDims==0,
                                     self.BoundModeCB,self)
        self.sideBar.addAction(self.sideBar.boundaryAction_0D)
        
        self.sideBar.boundaryAction_1D=createTBAction("",
                                     "Line (1D)",
                                     "To Specify the 1D Boundaries",
                                     "1D Boundary",
                                     self.projWindow.pC.nDims==1,
                                     self.BoundModeCB,self)
        self.sideBar.addAction(self.sideBar.boundaryAction_1D)
        
        self.sideBar.boundaryAction_2D=createTBAction("",
                                     "Rect (2D)",
                                     "To Specify the 2D Boundaries",
                                     "2D Boundary",
                                     self.projWindow.pC.nDims==2,
                                     self.BoundModeCB,self)
        self.sideBar.addAction(self.sideBar.boundaryAction_2D)
        
        self.sideBar.boundaryAction_save=createTBAction("",
                                     "Save",
                                     "To Save the created boundaries",
                                     "Save Boundary",
                                     self.isBoundaryDone,
                                     self.boundaryDoneSave,self)
        self.sideBar.addAction(self.sideBar.boundaryAction_save)
        
        self.sideBar.setOrientation(Qt.Vertical)
        
    def BoundModeCB(self):
        nDims=self.projWindow.pC.nDims
        if not self.isBoundaryDone:
            rectDlg=PVRD_RectangleDlg_Mode1_Boundary(nDims=nDims)
            rectDlg.setWindowTitle("Create {0}D Boundary".format(nDims))
            if rectDlg.exec_():
                width,height,bottomX,bottomY=rectDlg.result()
                self.boundaryItem=PVRD_Rectangle_Mode1_Boundary(bottomX*fac,
                                            bottomY*fac,width*fac,height*fac)
                self.boundaryItem.dlgBox=rectDlg
                self.boundaryItem.updateRect()
                self.scene.addItem(self.boundaryItem)
                self.isBoundaryDone=True
                self.projWindow.pC.geoMode=1
                self.projWindow.pC.boundaryX0=bottomX
                self.projWindow.pC.boundaryY0=bottomY
                self.projWindow.pC.boundaryWidth=width
                self.projWindow.pC.boundaryHeight=height
                
                message="Created Boundary"
                self.projWindow.setModified(True)
                self.projWindow.updateStatus(message)
                self.sideBar.boundaryAction_save.setEnabled(True)
                self.modeWidget.mode1_widget.updateLayout()
#                self.modeWidget.mode1_widget.updateBoundaryRect()
        else:
            QMessageBox.about(self,"Warning","Boundary is already added and displayed.\
                              \nTo Change Properties select boundary and press Q")
    def reDrawBoundary(self):
        pC=self.projWindow.pC
        self.boundaryItem=PVRD_Rectangle_Mode1_Boundary(pC.boundaryX0*fac,
                                                        pC.boundaryY0*fac,
                                                        pC.boundaryWidth*fac,
                                                        pC.boundaryHeight*fac)
        rectDlg=PVRD_RectangleDlg_Mode1_Boundary(pC.boundaryX0,pC.boundaryY0,
                                                 pC.boundaryWidth,pC.boundaryHeight,
                                                 pC.nDims)
        self.boundaryItem.dlgBox=rectDlg
        self.boundaryItem.updateRect()
        self.scene.addItem(self.boundaryItem)
        
    def boundaryDoneSave(self):
#        QMessageBox.about(self,"Warning","Still Developing")
        self.sideBar.boundaryAction_save.setEnabled(False)
        self.modeWidget.topBar.materialAction.setEnabled(True)
        self.projWindow.save()
        
    def wheelEvent(self,Event):
        if Event.angleDelta().y()>0:
            factor=1.25
        else:
            factor=0.8
        if self.gView is not None:
            self.gView.scale(factor, factor)
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_F and self.gView is not None:
                self.gView.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
            if event.key() == Qt.Key_Q:
                if self.isBoundaryDone and self.boundaryItem.isSelected():
                    self.boundaryItem.dlgBox.setWindowTitle("Edit Boundary Properties")
                    if self.boundaryItem.dlgBox.exec_():
                        rW,rH,botX,botY=self.boundaryItem.dlgBox.result()
                        self.boundaryItem.setRect(botX*fac,botY*fac,rW*fac,rH*fac)
                        self.scene.setSceneRect(botX*fac-5,botY*fac-5,rW*fac+10,rH*fac+10)
                        hasChanged=False
                        if rW !=self.projWindow.pC.boundaryWidth:
                            self.projWindow.pC.boundaryWidth=rW
                            hasChanged=True
                        if rH !=self.projWindow.pC.boundaryHeight:
                            self.projWindow.pC.boundaryHeight=rH
                            hasChanged=True
                        if botX !=self.projWindow.pC.boundaryX0:
                            self.projWindow.pC.boundaryX0=botX
                            hasChanged=True
                        if botY !=self.projWindow.pC.boundaryY0:
                            self.projWindow.pC.boundaryY0=botY
                            hasChanged=True
                        if hasChanged:
                            message="Changed Boundary"
                            self.projWindow.setModified(True)
                            self.projWindow.updateStatus(message)
                            self.sideBar.boundaryAction_save.setEnabled(True)

################################################################################
                            
class PVRD_Mode1_GeoMode1_Widget(QWidget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode1_GeoMode1_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.modeWidget=modeWidget
        self.isMaterialDone=False
        self.tempSave=False
        self.materialItem=None
        self.materialItemList=list()
        
    def updateLayout(self):
#        QMessageBox.about(self,"Warning","insdie UpdateLayout of geoMode1 {0} mat".format(self.projWindow.pC.db.materials))
        hLayout=QHBoxLayout()
        self.gView=QGraphicsView()
        self.scene = QGraphicsScene(self.gView)
        self.scene.setBackgroundBrush(Qt.black)

        self.gView.setScene(self.scene)
        self.gView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        self.updateBoundaryRect()
        

        self.createSideBar()
        
        hLayout.addWidget(self.gView)
        hLayout.addWidget(self.sideBar)
        self.setLayout(hLayout)
        self.projWindow.pC.geoMode=2
        
    def createSideBar(self):
        self.sideBar=QToolBar('GeoMode1_ToolBar')
        self.sideBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        matList=self.projWindow.pC.db.materials
        self.matActionList=list()
        brushList=list()
        ii=0
        jj=0
        num_i=0
        num_j=0
        matBrushDict={}
        matColorDict={}
        for mat in matList:
            ii=num_i%len(colorList)
            if ii==0:
                jj=num_j%len(bStyleList)
                num_j=num_j+1
            
            num_i=num_i+1
            brush=QBrush(colorList[ii],bStyleList[jj])
            brushList.append(brush)
            action=createTBAction("",
                                     mat,
                                     "To Add {0} Material".format(mat),
                                     "Add Material",
                                     True,
                                     self.materialModeCB,self)
            action.matName=mat
            action.brushVal=brush
            matBrushDict[mat]=brush
            self.matActionList.append(action)
            matColorDict[mat]=colorList[ii]
            self.sideBar.addAction(action)
        
        self.projWindow.pC.matBrushDict=matBrushDict
        self.projWindow.pC.matColorDict=matColorDict
        
        self.sideBar.materialAction_save=createTBAction("",
                                     "Save",
                                     "To Save the created materials",
                                     "Save Materials",
                                     self.tempSave,
                                     self.materialDoneSave,self)
        self.sideBar.addAction(self.sideBar.materialAction_save)
        
        self.sideBar.materialAction_done=createTBAction("",
                                     "Done",
                                     "To complete and move to next Mode",
                                     "Complete Materials",
                                     True,
                                     self.materialDone,self)
        self.sideBar.materialAction_done.setCheckable(True)
        self.sideBar.addAction(self.sideBar.materialAction_done)
        
        self.sideBar.setOrientation(Qt.Vertical)
        
    def updateBoundaryRect(self):
        if self.materialItem is None:
            self.materialItem=QGraphicsRectItem(
                    self.projWindow.pC.boundaryX0*fac,
                    self.projWindow.pC.boundaryY0*fac,
                    self.projWindow.pC.boundaryWidth*fac,
                    self.projWindow.pC.boundaryHeight*fac
                    )
            self.scene.addItem(self.materialItem)
        else:
            self.materialItem.setRect(
                    self.projWindow.pC.boundaryX0*fac,
                    self.projWindow.pC.boundaryY0*fac,
                    self.projWindow.pC.boundaryWidth*fac,
                    self.projWindow.pC.boundaryHeight*fac
                    )
        if self.projWindow.pC.nDims==0:
            self.materialItem.setRect(0,0,2,2)
            self.materialItem.setBrush(QBrush(Qt.white,Qt.SolidPattern))
            
        self.materialItem.setFlag(QGraphicsItem.ItemClipsChildrenToShape)
        pen=QPen(Qt.white)
        pen.setCosmetic(True)
        pen.setWidth(2)
        self.materialItem.setPen(pen)
        
    def materialDone(self):
        qa=self.sender()
        if type(qa) is QAction:
            if qa.isChecked():
                self.isMaterialDone=True
            else:
                self.isMaterialDone=False
            if self.isMaterialDone:
#                self.geoMW.mode_2_widget.updateBoundaryMatRect(0)
                if self.tempSave:
#                    self.geoMW.setWindowTitle("Structure Editor")
#                    self.projWindow.mW.fileSave()
                    self.sideBar.materialAction_save.setEnabled(False)
                
            self.modeWidget.topBar.gBoundaryAction.setEnabled(self.isMaterialDone)
            self.modeWidget.mode2_widget.updateLayout()
            
    def materialDoneSave(self):
        if self.isMaterialDone:
            self.modeWidget.topBar.gBoundaryAction.setEnabled(True)
                
#        self.geoMW.setWindowTitle("Material Editor")
#        self.geoMW.projWindow.mW.fileSave()
        self.sideBar.materialAction_save.setEnabled(False)
        self.tempSave=False
#        self.modeWidget.mode2_widget.updateLayout()
        self.projWindow.save()
        
    def materialModeCB(self):
        qa=self.sender()
        nDims=self.projWindow.pC.nDims
        if type(qa) is QAction:
            if self.isMaterialDone==0:
                rectDlg=PVRD_RectangleDlg_Mode1_Material(nDims=nDims)
                rectDlg.setWindowTitle("Add Material {0}".format(qa.matName))
                if rectDlg.exec_():
                    self.tempSave=True
                    wdth,hght,bX,bY=rectDlg.result()
                    rectItem=PVRD_Rectangle_Mode1_Material(bX*fac,bY*fac,wdth*fac,hght*fac,qa.brushVal,nDims,self.materialItem)
                    rectItem.updateRect()
                    rectData=PVRD_rectData(bX,bY,wdth,hght,qa.matName)
                    self.projWindow.pC.matRectList.append(rectData)
                    rectItem.dlgBox=rectDlg
                    if nDims==0:
                        self.materialItemList=list()
                    self.materialItemList.append(rectItem)
                    
#                    self.scene.addItem(rectItem)
#                    self.materialItem.addItem(rectItem)
                    message="Added {0} material to the structure".format(qa.matName)
#                    self.projWindow.mW.dirty=True
                    self.projWindow.updateStatus(message)
#                    self.geoMW.statusBar().showMessage(message, 5000)
#                    self.geoMW.setWindowTitle("Structure Editor*")
                    self.sideBar.materialAction_save.setEnabled(True)
                    
    def wheelEvent(self,Event):
        if Event.angleDelta().y()>0:
            factor=1.25
        else:
            factor=0.8
        if self.gView is not None:
            self.gView.scale(factor, factor)
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_F and self.gView is not None:
                self.gView.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
            if event.key() == Qt.Key_Q and not self.isMaterialDone:
                self.updateLogic()
            if event.key() == Qt.Key_S:
                if self.tempSave or self.isMaterialDone:
                    self.materialDoneSave()
            if event.key() == Qt.Key_Delete:
                if not self.isMaterialDone:
                    self.deleteMaterialItem()
    def deleteMaterialItem(self):
        itemIndx=-1
        for i in range(len(self.materialItemList)):
            if self.materialItemList[i].isSelected():
                itemIndx=i
        # only one item can be deleted at a time
        if itemIndx >=0:
            reply = QMessageBox.question(self.projWindow,
                    "PVRD Project - Delete Warning",
                    "Are you sure to delete the selected Material?\n\
                    (Undo is not supported)",
                    QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.Yes:
                del self.projWindow.pC.matRectList[itemIndx]
                self.scene.removeItem(self.materialItemList[itemIndx])
                del self.materialItemList[itemIndx]
            
    def updateLogic(self):
        itemIndx=-1
        for i in range(len(self.materialItemList)):
            if self.materialItemList[i].isSelected():
                itemIndx=i
        if itemIndx >=0:
            self.materialItemList[itemIndx].dlgBox.setWindowTitle("Edit Material {0} Properties".format(
                    self.projWindow.pC.matRectList[itemIndx].matName))
            if self.materialItemList[itemIndx].dlgBox.exec_():
                rW,rH,bX,bY=self.materialItemList[itemIndx].dlgBox.result()
                self.materialItemList[itemIndx].setRect(bX*fac,bY*fac,rW*fac,rH*fac)
                hasChanged=False
                if rW !=self.projWindow.pC.matRectList[itemIndx].W:
                    self.projWindow.pC.matRectList[itemIndx].W=rW
                    hasChanged=True
                if rH !=self.projWindow.pC.matRectList[itemIndx].H:
                    self.projWindow.pC.matRectList[itemIndx].H=rH
                    hasChanged=True
                if bX !=self.projWindow.pC.matRectList[itemIndx].X0:
                    self.projWindow.pC.matRectList[itemIndx].X0=bX
                    hasChanged=True
                if bY !=self.projWindow.pC.matRectList[itemIndx].Y0:
                    self.projWindow.pC.matRectList[itemIndx].Y0=bY
                    hasChanged=True
                        
                if hasChanged:
                    self.tempSave=True
                    message="Changed properties of {0}".format(self.projWindow.pC.matRectList[itemIndx].matName)
                    self.projWindow.setModified(True)
                    self.projWindow.updateStatus(message)
#                    self.geoMW.statusBar().showMessage(message, 5000)
#                    self.geoMW.setWindowTitle("Material Editor*")
                    self.sideBar.materialAction_save.setEnabled(True)
    
    def reDrawMaterials(self):
        self.updateBoundaryRect()
        nDims=self.projWindow.pC.nDims
        for rectData in self.projWindow.pC.matRectList:
            bX=rectData.X0
            bY=rectData.Y0
            wdth=rectData.W
            hght=rectData.H
            matName=rectData.matName
            brushVal=self.projWindow.pC.matBrushDict[matName]
            rectDlg=PVRD_RectangleDlg_Mode1_Material(bX,bY,wdth,hght,nDims)
            rectItem=PVRD_Rectangle_Mode1_Material(bX*fac,bY*fac,wdth*fac,hght*fac,brushVal,nDims,self.materialItem)
            rectItem.updateRect()
            rectItem.dlgBox=rectDlg
            self.materialItemList.append(rectItem)

###############################################################################
        
class PVRD_Mode1_GeoMode2_Widget(QWidget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode1_GeoMode2_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.modeWidget=modeWidget
        self.isGBoundaryDone=False
        self.tempSave=False
        self.gBoundaryItem=None
        self.gBoundaryList=list()
        self.gBoundaryList1=list()
        self.gBoundaryMatList=list()
        self.gBoundaryInterfaceList=list()
        
    def reDrawGB(self):
        self.commonUpdateLayout()
        nDims=self.projWindow.pC.nDims
#        QMessageBox.about(self,"Warning","ReDraw len={0} ".format(len(self.projWindow.pC.GBLineList)))        
        self.updateBoundaryMatRect(1)
#        QMessageBox.about(self,"Warning","ReDraw after len={0} ".format(len(self.projWindow.pC.GBLineList)))
        #AutoGB
        for line in self.projWindow.pC.autoGBLineList:
            lineItem=PVRD_Line_Mode1_GrainBoundary(line.x1*fac,line.y1*fac,line.x2*fac,line.y2*fac,nDims)
            self.scene.addItem(lineItem)
            self.gBoundaryList.append(lineItem)
        #interface
        for line in self.projWindow.pC.interfaceLineList:
            lineItem=PVRD_Line_Mode1_GrainBoundary_NoSelect(line.x1*fac,line.y1*fac,line.x2*fac,line.y2*fac,nDims)
            self.scene.addItem(lineItem)
            self.gBoundaryInterfaceList.append(lineItem)
        #GB
        for line in self.projWindow.pC.GBLineList:
            lineItem=PVRD_Line_Mode1_GrainBoundary(line.x1*fac,line.y1*fac,line.x2*fac,line.y2*fac,nDims)
            self.scene.addItem(lineItem)
            self.gBoundaryList1.append(lineItem)
        
    def commonUpdateLayout(self):
        hLayout=QHBoxLayout()
        self.gView=QGraphicsView()
        self.scene = QGraphicsScene(self.gView)
        self.scene.setBackgroundBrush(Qt.black)

        self.gView.setScene(self.scene)
        self.gView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        self.createSideBar()
        
        hLayout.addWidget(self.gView)
        hLayout.addWidget(self.sideBar)
        self.setLayout(hLayout)
        
    def updateLayout(self):
        self.commonUpdateLayout()
        self.updateBoundaryMatRect(0)
        
    def wheelEvent(self,Event):
        if Event.angleDelta().y()>0:
            factor=1.25
        else:
            factor=0.8
        if self.gView.underMouse():
            self.gView.scale(factor, factor)
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_F:
                self.gView.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
            if event.key() == Qt.Key_Q and not self.isGBoundaryDone:
                self.updateLogic()
                
            if event.key() == Qt.Key_S:
#                QMessageBox.about(self,"Warning","Goe Mode before Save={0} ".format())
                if self.tempSave or self.isGBoundaryDone:
                    self.GBoundaryDoneSave()
                    
    def createAutoInterfaces(self):
        self.updateBoundaryMatRect(0)
                    
    def updateBoundaryMatRect(self,isInit):
#        QMessageBox.about(self,"Warning","in updateBoundaryMatRect(GB)")
        self.tempSave=True
        nDims=self.projWindow.pC.nDims
        self.projWindow.pC.geoMode=2
        if self.gBoundaryItem is None:
            self.gBoundaryItem=QGraphicsRectItem(
                    self.projWindow.pC.boundaryX0*fac,
                    self.projWindow.pC.boundaryY0*fac,
                    self.projWindow.pC.boundaryWidth*fac,
                    self.projWindow.pC.boundaryHeight*fac
                    )
            if nDims==0:
                self.gBoundaryItem=QGraphicsRectItem(
                    self.projWindow.pC.boundaryX0*fac,
                    self.projWindow.pC.boundaryY0*fac,
                    self.projWindow.pC.boundaryWidth*fac+2,
                    self.projWindow.pC.boundaryHeight*fac+2
                    )
            self.scene.addItem(self.gBoundaryItem)
        else:
            self.gBoundaryItem.setRect(
                    self.projWindow.pC.boundaryX0*fac,
                    self.projWindow.pC.boundaryY0*fac,
                    self.projWindow.pC.boundaryWidth*fac,
                    self.projWindow.pC.boundaryHeight*fac
                    )
            if nDims==0:
                self.gBoundaryItem.setRect(
                    self.projWindow.pC.boundaryX0*fac,
                    self.projWindow.pC.boundaryY0*fac,
                    self.projWindow.pC.boundaryWidth*fac+2,
                    self.projWindow.pC.boundaryHeight*fac+2
                    )
                
        pen=QPen(Qt.white)
        pen.setCosmetic(True)
        pen.setWidth(1)
        if nDims>=1:
            self.gBoundaryItem.setPen(pen)

        
        self.gBoundaryItem.pWidget=self
        
        if nDims==0:
            pen.setStyle(Qt.SolidLine)
            brush=QBrush(Qt.white,Qt.SolidPattern)
            self.gBoundaryItem.setPen(pen)
            self.gBoundaryItem.setBrush(brush)
        
        if len(self.gBoundaryMatList)!=0 :
            for item in self.gBoundaryMatList:
                self.scene.removeItem(item)
        self.gBoundaryMatList=list()
        for rect in self.projWindow.pC.matRectList:
            pen=QPen(self.projWindow.pC.matColorDict[rect.matName])
            pen.setCosmetic(True)
            rectItem=PVRD_Rectangle_Mode1_GrainBoundary(rect.X0*fac,rect.Y0*fac,rect.W*fac,
                                          rect.H*fac,
                                          self.projWindow.pC.matBrushDict[rect.matName],
                                          pen,
                                          nDims,
                                          self.gBoundaryItem)
            self.gBoundaryMatList.append(rectItem)
            
        self.updateInterfaces(isInit)
        
        
            
    def updateInterfaces(self,isInit):
        lenVal=len(self.projWindow.pC.matRectList)*(1-isInit)
        nDims=self.projWindow.pC.nDims
        
        if lenVal!=0:
            if len(self.gBoundaryInterfaceList)!=0:
                for item in self.gBoundaryInterfaceList:
                    self.scene.removeItem(item)
            self.gBoundaryInterfaceList=list()
            if len(self.gBoundaryList)!=0:
                for item in self.gBoundaryList:
                    self.scene.removeItem(item)
            self.gBoundaryList=list()
            self.projWindow.pC.autoGBLineList=list()
            self.projWindow.pC.interfaceLineList=list()
        
        doForAll=False
        selection=False
        for ii in range(lenVal):
            jj=ii+1
            while jj<lenVal:
                rect1=self.projWindow.pC.matRectList[ii]
                rect2=self.projWindow.pC.matRectList[jj]
                jj=jj+1
                l1,w1=rect1.W,rect1.H
                l2,w2=rect2.W,rect2.H
                x1,y1=rect1.getCenter()
                x2,y2=rect2.getCenter()
                
                r1_left=round(x1-l1/2,prec)
                r1_right=round(x1+l1/2,prec)
                r1_bottom=round(y1-w1/2,prec)
                r1_top=round(y1+w1/2,prec)
                
                r2_left=round(x2-l2/2,prec)
                r2_right=round(x2+l2/2,prec)
                r2_bottom=round(y2-w2/2,prec)
                r2_top=round(y2+w2/2,prec)
                
                if nDims==2:
                    if (r1_left <= r2_left <= r1_right or r1_left <= r2_right <= r1_right) \
                    and (r1_bottom <= r2_bottom <= r1_top or r1_bottom <= r2_top <= r1_top):
                        intersectWidth=0
                        line_x1,line_x2,line_y1,line_y2=0,0,0,0
                        if (r1_left <= r2_left <= r1_right and r1_left <= r2_right <= r1_right):
                            intersectWidth=round(l2,prec)
                            line_x1=r2_left
                            line_x2=r2_right
                        elif r1_left <= r2_left <= r1_right:
                            intersectWidth = (r1_right)-(r2_left)
                            line_x1=(r2_left)
                            line_x2=(r1_right)
                        else:
                            intersectWidth = round((r2_right)-(r1_left),prec)
                            line_x1=r1_left
                            line_x2=r2_right
                        
                        intersectHeight=0
                        if (r1_bottom <= r2_bottom <= r1_top and r1_bottom <= r2_top <= r1_top):
                            intersectHeight=round(w2,prec)
                            line_y1=r2_bottom
                            line_y2=r2_top
                        elif r1_bottom <= r2_bottom <= r1_top:
                            intersectHeight = round((r1_top)-(r2_bottom),prec)
                            line_y1=r2_bottom
                            line_y2=r1_top
                        else:
                            intersectHeight = round((r2_top)-(r1_bottom),prec)
                            line_y1=r1_bottom
                            line_y2=r2_top
                        
                        iBoolW=not(isclose(intersectWidth,0))
                        iBoolH=not(isclose(intersectHeight,0))
                        if iBoolW and iBoolH:
                            QMessageBox.about(self,"Warning","Rectangular Intersection found between {0} and {1}.\nNot Supported Now".format(
                                 rect1.matName,rect2.matName))
                         
                        if iBoolW ^ iBoolH:
#                            QMessageBox.about(self,"Warning","Before Adding no Select")
                            lineItem=PVRD_Line_Mode1_GrainBoundary_NoSelect(line_x1*fac,line_y1*fac,line_x2*fac,line_y2*fac,nDims)
                            lineData=PVRD_lineData(line_x1,line_y1,line_x2,line_y2,rect1.matName)
                            if rect1.matName!=rect2.matName:
                                lineData.matName=lineData.matName+"/"+rect2.matName
                                self.scene.addItem(lineItem)
                                self.gBoundaryInterfaceList.append(lineItem)
                                self.projWindow.pC.interfaceLineList.append(lineData)
                            elif doForAll==False:
                                sameMaterialDlg=PVRD_MaterialDlg_Mode1_GrainBoundary(rect1.matName)
                                selection=sameMaterialDlg.exec_()
                                doForAll=sameMaterialDlg.checkBox.isChecked()
                                if selection:
#                                    QMessageBox.about(self,"Warning","Before Adding Line")
                                    lineItem=PVRD_Line_Mode1_GrainBoundary(line_x1*fac,line_y1*fac,line_x2*fac,line_y2*fac,nDims)
                                    lineItem.dlgBox=PVRD_LineDlg_Mode1_GrainBoundary(line_x1,line_y1,line_x2,line_y2,nDims)
                                    self.scene.addItem(lineItem)
                                    self.gBoundaryList.append(lineItem)
                                    self.projWindow.pC.autoGBLineList.append(lineData)
                            else:
                                if selection:
#                                    QMessageBox.about(self,"Warning","Before Adding Line _1")
                                    lineItem=PVRD_Line_Mode1_GrainBoundary(line_x1*fac,line_y1*fac,line_x2*fac,line_y2*fac,nDims)
                                    lineItem.dlgBox=PVRD_LineDlg_Mode1_GrainBoundary(line_x1,line_y1,line_x2,line_y2,nDims)
                                    self.scene.addItem(lineItem)
                                    self.gBoundaryList.append(lineItem)
                                    self.projWindow.pC.autoGBLineList.append(lineData)
                
                if nDims==1:
                    if isclose(r1_top,r2_bottom):
#                        QMessageBox.about(self,"Warning","Before Adding no Select")
                        lineItem=PVRD_Line_Mode1_GrainBoundary_NoSelect(r1_left*fac,r1_top*fac,r1_left*fac,r1_top*fac,nDims)
                        lineData=PVRD_lineData(r1_left,r1_top,r1_left,r1_top,rect1.matName)
                        self.scene.addItem(lineItem)
                        self.gBoundaryInterfaceList.append(lineItem)
                        self.projWindow.pC.interfaceLineList.append(lineData)
                    if isclose(r2_top,r1_bottom):
#                        QMessageBox.about(self,"Warning","Before Adding no Select")
                        lineItem=PVRD_Line_Mode1_GrainBoundary_NoSelect(r1_left*fac,r2_top*fac,r1_left*fac,r2_top*fac,nDims)
                        lineData=PVRD_lineData(r1_left,r2_top,r1_left,r2_top,rect1.matName)
                        self.scene.addItem(lineItem)
                        self.gBoundaryInterfaceList.append(lineItem)
                        self.projWindow.pC.interfaceLineList.append(lineData)
                        
                                
    def createSideBar(self):
        self.sideBar=QToolBar('GeoMode2_ToolBar')
        self.sideBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        self.sideBar.gBoundaryAction_1D=createTBAction("",
                                     "Dot (1D)",
                                     "To Specify the 1D Grain Boundaries",
                                     "1D GBoundary",
                                     self.projWindow.pC.nDims==1,
                                     self.GBoundModeCB_2D,self)
        self.sideBar.addAction(self.sideBar.gBoundaryAction_1D)
        
        self.sideBar.gBoundaryAction_2D=createTBAction("",
                                     "Line (2D)",
                                     "To Specify the 2D Grain Boundaries",
                                     "2D GBoundary",
                                     self.projWindow.pC.nDims==2,
                                     self.GBoundModeCB_2D,self)
        self.sideBar.addAction(self.sideBar.gBoundaryAction_2D)
        
        self.sideBar.gBoundaryAction_interfaces=createTBAction("",
                                     "Auto Interface",
                                     "To automatically created interfaces and grain boundaries",
                                     "Create Auto Interfaces",
                                     True,
                                     self.createAutoInterfaces,self)
        self.sideBar.addAction(self.sideBar.gBoundaryAction_interfaces)
        
        self.sideBar.gBoundaryAction_save=createTBAction("",
                                     "Save",
                                     "To Save the created boundaries",
                                     "Save Boundary",
                                     self.isGBoundaryDone==1,
                                     self.GBoundaryDoneSave,self)
        self.sideBar.addAction(self.sideBar.gBoundaryAction_save)
        
        self.sideBar.gBoundaryAction_done=createTBAction("",
                                     "Done",
                                     "To complete and move to next Mode",
                                     "Complete Grain Boundaries",
                                     True,
                                     self.GBoundaryDone,self)
        self.sideBar.gBoundaryAction_done.setCheckable(True)
        self.sideBar.addAction(self.sideBar.gBoundaryAction_done)
        
        
        self.sideBar.setOrientation(Qt.Vertical)
    
    def GBoundModeCB_2D(self):
        if not self.isGBoundaryDone:
            nDims=self.projWindow.pC.nDims
            lineDlg=PVRD_LineDlg_Mode1_GrainBoundary(nDims=nDims)
            lineDlg.setWindowTitle("Create GBoundary")
            if lineDlg.exec_():
                x1,y1,x2,y2=lineDlg.result()
                if nDims==2:
                    sameMat=self.checkPointsOfSameMat(x1,y1,x2,y2)
                else:
                    sameMat=True
                if sameMat:
                    self.tempSave=1
                    self.projWindow.pC.geoMode=2
                    lineItem=PVRD_Line_Mode1_GrainBoundary(x1*fac,y1*fac,x2*fac,y2*fac,nDims)
                    matName=self.getMatNameOfPoint(x1,y1)
                    lineItem.dlgBox=lineDlg
                    self.scene.addItem(lineItem)
                    self.gBoundaryList1.append(lineItem)
                    
                    lineData=PVRD_lineData(x1,y1,x2,y2,matName)
                    self.projWindow.pC.GBLineList.append(lineData)
                    
                    message="Added new Grain Boundary to the structure"
                    self.projWindow.setModified(True)
                    self.projWindow.updateStatus(message)
                    self.sideBar.gBoundaryAction_save.setEnabled(True)
                    
        
    def GBoundaryDoneSave(self):
        if self.isGBoundaryDone:
            self.modeWidget.toolBar.gBoundaryAction.setEnabled(True)
                
#        self.geoMW.setWindowTitle("Grain Boundary Editor")
#        self.geoMW.projWindow.mW.fileSave()
        self.sideBar.gBoundaryAction_save.setEnabled(False)
        self.tempSave=0
        self.projWindow.save()
        
    def GBoundaryDone(self):
        qa=self.sender()
        if type(qa) is QAction:
            if qa.isChecked():
                self.isGBoundaryDone=1
            else:
                self.isGBoundaryDone=0
            if self.isGBoundaryDone==1:
#                self.geoMW.mode_2_widget.updateBoundaryMatRect()
                if self.tempSave==1:
#                    self.geoMW.setWindowTitle("Grain Boundary Editor")
#                    self.geoMW.projWindow.mW.fileSave()
                    self.sideBar.gBoundaryAction_save.setEnabled(False)
                
            self.projWindow.toolBar.dcsAction.setEnabled(self.isGBoundaryDone==1)
            if self.isGBoundaryDone==1:
                self.projWindow.pC.mode=2
                self.projWindow.mode2_widget.updateWidget()
        
    def checkPointsOfSameMat(self,x1,y1,x2,y2):
        p1_mat=list()
        p2_mat=list()
        for rect in self.projWindow.pC.matRectList:
            x,y=rect.getCenter()
            l,w=rect.W,rect.H
            if round(x-l/2,prec)<=round(x1,prec)<=round(x+l/2,prec) and \
            round(y-w/2,prec)<=round(y1,prec)<=round(y+w/2,prec):
                p1_mat.append(rect.matName)
            if round(x-l/2,prec)<=round(x2,prec)<=round(x+l/2,prec) and \
            round(y-w/2,prec)<=round(y2,prec)<=round(y+w/2,prec):
                p2_mat.append(rect.matName)
        
        if len(p1_mat) !=0 and len(p2_mat) !=0:
            returnVal=False
            for mat1 in p1_mat:
                for mat2 in p2_mat:
                    if mat1==mat2:
                        returnVal=True
            if not returnVal:
                QMessageBox.about(self,"Warning","Points are not in same Material\n"
                                  +"Start Point in :"+",".join(p1_mat)+"\n"
                                  +"End Point in :"+",".join(p2_mat))
            return returnVal
        QMessageBox.about(self,"Warning","Points are not inside Boundaries")
#        QMessageBox.about(self,"Warning","End Points are not of same Materials\n"+
#                          "Start Point in {0}\nEnd Point in {1}".format(p1_mat,p2_mat))
        return False
    def getMatNameOfPoint(self,x1,y1):
        matName=""
        for rect in self.projWindow.pC.matRectList:
            x,y=rect.getCenter()
            l,w=rect.W,rect.H
            if round(x-l/2,prec)<=round(x1,prec)<=round(x+l/2,prec) and \
            round(y-w/2,prec)<=round(y1,prec)<=round(y+w/2,prec):
                matName=rect.matName
        return matName
    
    def updateLogic(self):
        itemIndx=-1
        for i in range(len(self.gBoundaryList1)):
            if self.gBoundaryList1[i].isSelected():
                itemIndx=i
        if itemIndx >=0:
            self.gBoundaryList1[itemIndx].dlgBox.setWindowTitle("Edit Grain Boundary Properties")
            if self.gBoundaryList1[itemIndx].dlgBox.exec_():
                x1,y1,x2,y2=self.gBoundaryList1[itemIndx].dlgBox.result()
                sameMat=self.checkPointsOfSameMat(x1,y1,x2,y2)
                if sameMat:
                    self.gBoundaryList1[itemIndx].setLine(x1*fac,y1*fac,x2*fac,y2*fac)
                    hasChanged=False
                    if x1 !=self.projWindow.pC.GBLineList[itemIndx].x1:
                        self.projWindow.pC.GBLineList[itemIndx].x1=x1
                        hasChanged=True
                    if x2 !=self.projWindow.pC.GBLineList[itemIndx].x2:
                        self.projWindow.pC.GBLineList[itemIndx].x2=x2
                        hasChanged=True
                    if y1 !=self.projWindow.pC.GBLineList[itemIndx].y1:
                        self.projWindow.pC.GBLineList[itemIndx].y1=y1
                        hasChanged=True
                    if y2 !=self.projWindow.pC.GBLineList[itemIndx].y2:
                        self.projWindow.pC.GBLineList[itemIndx].y2=y2
                        hasChanged=True
                        
                    if hasChanged:
                        self.tempSave=1
                        message="Changed properties of Grain Boundary"
#                        self.geoMW.projWindow.mW.dirty=True
                        self.projWindow.updateStatus(message)
#                        self.geoMW.statusBar().showMessage(message, 5000)
#                        self.geoMW.setWindowTitle("Grain Boundary Editor*")
                        self.sideBar.gBoundaryAction_save.setEnabled(True)

###############################################################################
        
class PVRD_Mode2_Widget(QWidget):
    """
    Mode 2 Widget is for displaying all widgets for specifying the defect chemistry.
    """
    def __init__(self,projWindow=None,parent=None):
        super(PVRD_Mode2_Widget,self).__init__(parent)
        self.projWindow=projWindow
        
        self.isSideBarDone=False
        
        self.hLayout=QHBoxLayout()
        self.gView=QGraphicsView()
        self.scene = PVRD_QGraphicsScene(self.gView,widget=self)
        self.scene.setBackgroundBrush(Qt.black)

        self.gView.setScene(self.scene)
        self.gView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setDragMode(QGraphicsView.RubberBandDrag)
#        self.gView.setRubberBandSelectionMode(True)
        
        self.gView.setAcceptDrops(True)
        
        self.hLayout.addWidget(self.gView)
        
        self.setLayout(self.hLayout)
        
#        self.createSideBar()
        
    def updateWidget(self):
#        QMessageBox.about(self,'Warnnning','updateWidget Mode2')
        if not self.isSideBarDone:
            self.createSideBar()
        self.projWindow.pC.simplifyBoudaries()
        
        self.bBoundList=list()
        self.tBoundList=list()
        self.lBoundList=list()
        self.rBoundList=list()
        self.allRectItemList=list()
        self.allLineItemList=list()
        self.allPointItemList=list()
        self.allItemList=list()
        
        whitePen=QPen(Qt.white)
        whitePen.setCosmetic(True)
        whitePen.setWidth(2)
        
        redPen=QPen(Qt.red)
        redPen.setCosmetic(True)
        redPen.setWidth(4)
        
        ii=0
        for mat in self.projWindow.pC.matRectList:
            ii=ii+1
#            QMessageBox.about(self,'Warnnning','matRectList ii={0}'.format(ii))
            matItem=PVRD_Rectangle_Mode2(mat.X0,mat.Y0,mat.W,mat.H,
                                   "Layer {0}".format(ii),
                                   mat.matName,
                                   None,
                                   self.projWindow.pC.matBrushDict[mat.matName],
                                   projWindow=self.projWindow,
                                   parent=self,
                                   pCindx=ii-1,
                                   nDims=self.projWindow.pC.nDims)
            self.allRectItemList.append(matItem)
            self.scene.addItem(matItem)
        self.projWindow.pC.allRectList.extend(self.projWindow.pC.matRectList)
        
        ii=0
        jj=0
        for line in self.projWindow.pC.bottomBoundaryLineList:
            line.type=3
            line.isBoundary=True
            ii=ii+1
            bottomBoundaryItem=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                              "Bottom Boundary Line {0}".format(ii),
                                              line.matName,
                                              whitePen,
                                              projWindow=self.projWindow,
                                              parent=self,
                                              pCindx=jj,
                                              nDims=self.projWindow.pC.nDims)
            self.scene.addItem(bottomBoundaryItem)
            self.bBoundList.append(bottomBoundaryItem)
            self.allLineItemList.append(bottomBoundaryItem)
            jj=jj+1
#            yBottom=line.y1
        self.projWindow.pC.allLineList.extend(self.projWindow.pC.bottomBoundaryLineList)
            
        ii=0
        for line in self.projWindow.pC.topBoundaryLineList:
            line.type=3
            line.isBoundary=True
            line.isTop=True
            ii=ii+1
            topBoundaryItem=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                           "Top Boundary Line {0}".format(ii),
                                           line.matName,
                                           whitePen,
                                           projWindow=self.projWindow,
                                           parent=self,
                                           pCindx=jj,
                                           nDims=self.projWindow.pC.nDims)
            self.scene.addItem(topBoundaryItem)
            self.tBoundList.append(topBoundaryItem)
            self.allLineItemList.append(topBoundaryItem)
            jj=jj+1
#            yTop=line.y1
        self.projWindow.pC.allLineList.extend(self.projWindow.pC.topBoundaryLineList)
            
        ii=0
        for line in self.projWindow.pC.leftBoundaryLineList:
            line.type=3
            ii=ii+1
            leftBoundaryItem=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                            "Left Boundary Line {0}".format(ii),
                                            line.matName,
                                            whitePen,
                                            projWindow=self.projWindow,
                                            parent=self,
                                            pCindx=jj,
                                            nDims=self.projWindow.pC.nDims)
            self.scene.addItem(leftBoundaryItem)
            self.lBoundList.append(leftBoundaryItem)
            self.allLineItemList.append(leftBoundaryItem)
            jj=jj+1
#            xLeft=line.x1
        self.projWindow.pC.allLineList.extend(self.projWindow.pC.leftBoundaryLineList)
            
        ii=0
        for line in self.projWindow.pC.rightBoundaryLineList:
            line.type=3
            ii=ii+1
            rightBoundaryItem=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                             "Right Boundary Line {0}".format(ii),
                                             line.matName,
                                             whitePen,
                                             projWindow=self.projWindow,
                                             parent=self,
                                             pCindx=jj,
                                             nDims=self.projWindow.pC.nDims)
            self.scene.addItem(rightBoundaryItem)
            self.rBoundList.append(rightBoundaryItem)
            self.allLineItemList.append(rightBoundaryItem)
            jj=jj+1
#            xRight=line.x1
        self.projWindow.pC.allLineList.extend(self.projWindow.pC.rightBoundaryLineList)
        
            
        whitePenDashed=QPen(Qt.white,2,Qt.DashLine)
        whitePenDashed.setCosmetic(True)
        
        whitePenDot=QPen(Qt.white,2,Qt.DotLine)
        whitePenDot.setCosmetic(True)
        
        ii=0
        for line in self.projWindow.pC.interfaceLineList:
            line.type=1
            ii=ii+1
            item=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                "Interface Line {0}".format(ii),
                                line.matName,
                                whitePenDashed,
                                projWindow=self.projWindow,
                                parent=self,
                                pCindx=jj,
                                nDims=self.projWindow.pC.nDims)
            self.scene.addItem(item)
            self.allLineItemList.append(item)
            jj=jj+1
#            self.rBoundList.append(rightBoundaryItem)
        self.projWindow.pC.allLineList.extend(self.projWindow.pC.interfaceLineList)
        
        ii=0
        for line in self.projWindow.pC.autoGBLineList:
            line.type=2
            ii=ii+1
            item=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                "GB Line {0}".format(ii),
                                line.matName,
                                whitePenDot,
                                projWindow=self.projWindow,
                                parent=self,
                                pCindx=jj,
                                nDims=self.projWindow.pC.nDims)
            self.scene.addItem(item)
            self.allLineItemList.append(item)
            jj=jj+1
        self.projWindow.pC.allLineList.extend(self.projWindow.pC.autoGBLineList)
#        ii=0
        for line in self.projWindow.pC.GBLineList:
            line.type=2
            ii=ii+1
            item=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                "GB Line {0}".format(ii),
                                line.matName,
                                whitePenDot,
                                projWindow=self.projWindow,
                                parent=self,
                                pCindx=jj,
                                nDims=self.projWindow.pC.nDims)
            self.scene.addItem(item)
            self.allLineItemList.append(item)
            jj=jj+1
        self.projWindow.pC.allLineList.extend(self.projWindow.pC.GBLineList)

        ii=0
        jj=0
        for point in self.projWindow.pC.leftBoundaryPointList:
            point.type=3
            ii=ii+1
            leftBoundaryPointItem=PVRD_Point_Mode2(point.x1,point.y1,
                                                  "Left Boundary Point {0}".format(ii),
                                                  point.matName,
                                                  redPen,
                                                  projWindow=self.projWindow,
                                                  parent=self,
                                                  pCindx=jj,
                                                  nDims=self.projWindow.pC.nDims)
            self.scene.addItem(leftBoundaryPointItem)
            self.allPointItemList.append(leftBoundaryPointItem)
            jj=jj+1
            
        self.projWindow.pC.allPointList.extend(self.projWindow.pC.leftBoundaryPointList)
        
        ii=0
        for point in self.projWindow.pC.rightBoundaryPointList:
            point.type=3
            ii=ii+1
            rightBoundaryPointItem=PVRD_Point_Mode2(point.x1,point.y1,
                                                   "Right Boundary Point {0}".format(ii),
                                                   point.matName,
                                                   redPen,
                                                   projWindow=self.projWindow,
                                                   parent=self,
                                                   pCindx=jj,
                                                   nDims=self.projWindow.pC.nDims)
            self.scene.addItem(rightBoundaryPointItem)
            self.allPointItemList.append(rightBoundaryPointItem)
            jj=jj+1
        self.projWindow.pC.allPointList.extend(self.projWindow.pC.rightBoundaryPointList)
            
        ii=0
        for point in self.projWindow.pC.topBoundaryPointList:
            point.type=3
            point.isBoundary=True
            point.isTop=True
            ii=ii+1
            topBoundaryPointItem=PVRD_Point_Mode2(point.x1,point.y1,
                                                 "Top Boundary Point {0}".format(ii),
                                                 point.matName,
                                                 redPen,
                                                 projWindow=self.projWindow,
                                                 parent=self,
                                                 pCindx=jj,
                                                 nDims=self.projWindow.pC.nDims)
            self.scene.addItem(topBoundaryPointItem)
            self.allPointItemList.append(topBoundaryPointItem)
            jj=jj+1
        self.projWindow.pC.allPointList.extend(self.projWindow.pC.topBoundaryPointList)
        
        ii=0
        for point in self.projWindow.pC.bottomBoundaryPointList:
            point.type=3
            point.isBoundary=True
            ii=ii+1
            bottomBoundaryPointItem=PVRD_Point_Mode2(point.x1,point.y1,
                                                    "Bottom Boundary Point {0}".format(ii),
                                                    point.matName,
                                                    redPen,
                                                    projWindow=self.projWindow,
                                                    parent=self,
                                                    pCindx=jj,
                                                    nDims=self.projWindow.pC.nDims)
            self.scene.addItem(bottomBoundaryPointItem)
            self.allPointItemList.append(bottomBoundaryPointItem)
            jj=jj+1
        self.projWindow.pC.allPointList.extend(self.projWindow.pC.bottomBoundaryPointList)
#            
        self.allItemList.extend(self.allRectItemList)
        self.allItemList.extend(self.allLineItemList)
        self.allItemList.extend(self.allPointItemList)
        
    def createSideBar(self):
        self.isSideBarDone=True
        vLayout=QVBoxLayout()
        
        mech_cBox=PVRD_dragQComboBox()
        mech_cBox.addItems(self.projWindow.pC.db.mechanisms)
        
        mech_label=QLabel("Mechanisms List")
        mech_label.setBuddy(mech_cBox)            
        self.mech_groupBox=QGroupBox('Mechanisms')
        vLayout_group=QVBoxLayout()
        self.mech_groupBox.setLayout(vLayout_group)
        vLayout_group.addWidget(mech_label)
        vLayout_group.addWidget(mech_cBox)
        vLayout.addWidget(self.mech_groupBox)
            
        reactions_cBox=PVRD_dragQComboBox()
        reactions_cBox.addItems(self.projWindow.pC.db.reactions)
        
        reactions_label=QLabel("Reactions List")
        reactions_label.setBuddy(reactions_cBox)            
        self.reactions_groupBox=QGroupBox('Reactions')
        reactions_vLayout_group=QVBoxLayout()
        self.reactions_groupBox.setLayout(reactions_vLayout_group)
        reactions_vLayout_group.addWidget(reactions_label)
        reactions_vLayout_group.addWidget(reactions_cBox)
        vLayout.addWidget(self.reactions_groupBox)
            
        species_cBox=PVRD_dragQComboBox()
        species_cBox.addItems(self.projWindow.pC.db.species)
        
        species_label=QLabel("Species List")
        species_label.setBuddy(species_cBox)            
        self.species_groupBox=QGroupBox('Species')
        species_vLayout_group=QVBoxLayout()
        self.species_groupBox.setLayout(species_vLayout_group)
        species_vLayout_group.addWidget(species_label)
        species_vLayout_group.addWidget(species_cBox)
        vLayout.addWidget(self.species_groupBox)
        self.DCSDonePB=QPushButton('Done')
        self.DCSDonePB.setToolTip('Click this to complete the Defect Chemistry Setup')
        self.DCSDonePB.setCheckable(True)
        self.DCSDonePB.clicked[bool].connect(self.completeDCS)
        
        vLayout.addWidget(self.DCSDonePB)
        vLayout.addStretch(1)
        self.hLayout.addLayout(vLayout)
        
    def wheelEvent(self,Event):
        if Event.angleDelta().y()>0:
            factor=1.25
        else:
            factor=0.8
        if self.gView is not None:
            self.gView.scale(factor, factor)
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_F and self.gView is not None:
                self.gView.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
#            if event.key() == Qt.Key_Save
                
    def completeDCS(self):
        self.projWindow.toolBar.dcmsAction.setEnabled(True)
        self.projWindow.save()
    
    def updateDialog(self):
        for item in self.allItemList:
#            item.dlgBox.checkMech=True
#            item.dlgBox.checkReactions=True
#            item.dlgBox.checSpecies=True
            item.dlgBox.setCB_and_TB()
        
###############################################################################
class PVRD_dragQComboBox(QComboBox):
    def __init__(self,parent=None):
        super(PVRD_dragQComboBox,self).__init__(parent)
#        self.view().setDragEnabled(True)9
        self.view().setDragDropMode(QAbstractItemView.DragOnly)

###############################################################################
        
class PVRD_QGraphicsScene(QGraphicsScene):
    def __init__(self,parent=None,widget=None):
        super(PVRD_QGraphicsScene,self).__init__(parent)
        self.parent=parent
        self.widget=widget
        
    
    def dragEnterEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
#        QMessageBox.about(self.parent,'Warnnning','QGraphicScene DragEnter')
        if event.mimeData().hasFormat(model_mime_type):
#            QMessageBox.about(self.parent,'Warnnning','QGraphicScene DragEnter Accept')
            event.accept()
        else:
#            QMessageBox.about(self.parent,'Warnnning','QGraphicScene DragEnter Reject')
            event.reject()
        
    def dragMoveEvent(self,event):
        super(PVRD_QGraphicsScene,self).dragMoveEvent(event)
        model_mime_type='application/x-qabstractitemmodeldatalist'
        if event.mimeData().hasFormat(model_mime_type):
#            QMessageBox.about(self.parent,'Warnnning','QGraphicScene DragMove Accept')
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
            
#    def keyPressEvent(self, event):
#        aa=1
#        if type(event) == QKeyEvent:
#            QMessageBox.about(self.parent,'Warnnning','start')
#            if (event.modifiers() & Qt.ControlModifier):
#                if (event.key()==Qt.Key_S):
#                    QMessageBox.about(self.parent,'Warnnning','Ctrl={0}'.format(event.key()))
#            if event.key() == Qt.Key_Control:
##                QMessageBox.about(self.parent,'Warnnning','Ctrl')
#                self.isCtrlPressed=True
#            if event.key() == Qt.Key_S:
#                QMessageBox.about(self.parent,'Warnnning','S')
#                if self.isCtrlPressed:
#                    QMessageBox.about(self.parent,'Warnnning','Ctrl+S')
            
#        super(PVRD_QGraphicsScene,self).keyPressEvent(event)
            
    def dropEvent(self,event):
#        event.accept()
#        QMessageBox.about(self.parent,'Warnnning','formats{0}'.format(event.mimeData().formats()))
        super(PVRD_QGraphicsScene,self).dropEvent(event)
#        test=1
#        event.accept()
        model_mime_type='application/x-qabstractitemmodeldatalist'
#        QMessageBox.about(self.parent,'Warnnning','formats{0}'.format(event.mimeData().formats()))
        if event.mimeData().hasFormat(model_mime_type):
            encoded = event.mimeData().data(model_mime_type)
            stream = QDataStream(encoded, QIODevice.ReadOnly)
            while not stream.atEnd():
                row = stream.readInt()
                column = stream.readInt()
                mapp = stream.readQVariantMap()
                itemName = mapp['']
                didDroppedOnRect=0
                for item in self.widget.allRectItemList:
                    if item.isDropped:
                        didDroppedOnRect+=1
                        
                for item in self.widget.allLineItemList:
                    if item.isDropped:
                        didDroppedOnRect+=1
                        
                for item in self.widget.allPointItemList:
                    if item.isDropped:
                        didDroppedOnRect+=1
                        
                if didDroppedOnRect==0:
                    reply = QMessageBox.question(self.parent,
                    "PVRD Project - Drop Warning",
                    "Dropping on all selected items (rectangles,lines and points)\n\
                    Do you want to continue?\n\
                    (Undo is not supported)",
                    QMessageBox.Yes|QMessageBox.No)
                    typeStr=""
                    if reply == QMessageBox.Yes:
                        for item in self.widget.allItemList:
                            if itemName in self.widget.projWindow.pC.db.mechanisms:
                                if item.isSelected():
                                    item.dlgBox.addMechanisms((itemName))
                                typeStr='Mechanism'
                            if itemName in self.widget.projWindow.pC.db.reactions:
#                                QMessageBox.about(self.parent,"Warning",'ItemName="{0}"'.format(itemName))
                                if item.isSelected():
                                    item.dlgBox.addReactions((itemName))
                                typeStr='Reaction'
                            if itemName in self.widget.projWindow.pC.db.species:
                                if item.isSelected():
                                    item.dlgBox.addSpecies((itemName))
                                typeStr='Species'
                        message="Added '{0}' {1} to the structure".format(itemName,typeStr)
                        self.widget.projWindow.updateStatus(message)
                            
                        QMessageBox.about(self.parent,"Warning",'"{0}" is added to all selected items'.format(itemName))
                
        for item in self.widget.allRectItemList:
            item.isDropped=False
            
###############################################################################
        
class PVRD_Mode3_Widget(QWidget):
    """
    Mode 3 Widget is for displaying all widgets for verifying or updating
    material, defect chemistry model parameters.
    """
    def __init__(self,projWindow=None,parent=None):
        super(PVRD_Mode3_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.isSideBarDone=False
        
        self.hLayout=QHBoxLayout()
        self.gView=QGraphicsView()
        self.scene = QGraphicsScene(self.gView)
        self.scene.setBackgroundBrush(Qt.black)

        self.gView.setScene(self.scene)
        self.gView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setDragMode(QGraphicsView.RubberBandDrag)
        
        self.hLayout.addWidget(self.gView)
        self.setLayout(self.hLayout)
        
    def updateWidget(self,isInit=False):
        self.projWindow.pC.mode=3
#        QMessageBox.about(self,'Warnnning','updateWidget Mode3')
        if not self.isSideBarDone:
            self.createSideBar()
#        self.projWindow.pC.simplifyBoudaries()
        
        self.bBoundList=list()
        self.tBoundList=list()
        self.lBoundList=list()
        self.rBoundList=list()
        self.allRectItemList=list()
        self.allLineItemList=list()
        self.allPointItemList=list()
        self.allItemList=list()
        
        whitePen=QPen(Qt.white)
        whitePen.setCosmetic(True)
        whitePen.setWidth(2)
        
        redPen=QPen(Qt.red)
        redPen.setCosmetic(True)
        redPen.setWidth(4)
        
        ii=0
        for mat in self.projWindow.pC.allRectList:
            rectItem=PVRD_Rectangle_Mode2(mat.X0,mat.Y0,mat.W,mat.H,
                                   "Layer {0}".format(ii),
                                   mat.matName,
                                   None,
                                   self.projWindow.pC.matBrushDict[mat.matName],
                                   self.projWindow,
                                   parent=self,
                                   pCindx=ii,
                                   nDims=self.projWindow.pC.nDims,
                                   gType=1)
            rectItem.dlgBox.updateDialog(isInit)
            ii=ii+1
            self.scene.addItem(rectItem)
            self.allRectItemList.append(rectItem)
        
        ii=0
        for line in self.projWindow.pC.allLineList:
            lineItem=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                   "Line {0}".format(ii),
                                   line.matName,
                                   whitePen,
                                   self.projWindow,
                                   self,
                                   pCindx=ii,
                                   nDims=self.projWindow.pC.nDims,
                                   gType=1)
            lineItem.dlgBox.updateDialog(isInit)
            ii=ii+1
            self.scene.addItem(lineItem)
            self.allLineItemList.append(lineItem)
            
        ii=0
        for line in self.projWindow.pC.allPointList:
            lineItem=PVRD_Point_Mode2(line.x1,line.y1,
                                    "Point {0}".format(ii),
                                    line.matName,
                                    redPen,
                                    self.projWindow,
                                    self,
                                    pCindx=ii,
                                    nDims=self.projWindow.pC.nDims,
                                    gType=1)
            lineItem.dlgBox.updateDialog(isInit)
            ii=ii+1
            self.scene.addItem(lineItem)
            self.allPointItemList.append(lineItem)
            
    def updateDialog(self):
        for item in self.allRectItemList:
            item.dlgBox.updateDialog(True)
        for item in self.allLineItemList:
            item.dlgBox.updateDialog(True)
        for item in self.allPointItemList:
            item.dlgBox.updateDialog(True)
        
    def createSideBar(self):
        self.isSideBarDone=True
        vLayout=QVBoxLayout()
        
        self.DCSDonePB=QPushButton('Done')
        self.DCSDonePB.setToolTip('Click this to complete the Defect Chemistry Model Setup')
        self.DCSDonePB.setCheckable(True)
        self.DCSDonePB.clicked[bool].connect(self.completeDCMS)
        
        vLayout.addWidget(self.DCSDonePB)
        vLayout.addStretch(1)
        self.hLayout.addLayout(vLayout)
        
    def wheelEvent(self,Event):
        if Event.angleDelta().y()>0:
            factor=1.25
        else:
            factor=0.8
        if self.gView is not None:
            self.gView.scale(factor, factor)
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_F and self.gView is not None:
                self.gView.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
                
    def completeDCMS(self):
        self.projWindow.save()
        self.projWindow.toolBar.simAction.setEnabled(True)
        self.updatePCdata()
        self.projWindow.pC.mode=4
        
    def updatePCdata(self):
        for rect in self.projWindow.pC.allRectList:
            self.projWindow.pC.db.updateProjSpeciesModelData(rect)
            self.projWindow.pC.db.updateProjReactionModelData(rect)
            
        for line in self.projWindow.pC.allLineList:
            self.projWindow.pC.db.updateProjSpeciesModelData(line)
            self.projWindow.pC.db.updateProjReactionModelData(rect)
            
        for point in self.projWindow.pC.allPointList:
            self.projWindow.pC.db.updateProjSpeciesModelData(point)
            self.projWindow.pC.db.updateProjReactionModelData(rect)
        
###############################################################################
        
class PVRD_Mode4_Widget(QWidget):
    """
    Mode 4 Widget is for displaying all widgets for specifying simulation conditions
    which include boundary conditions, initial conditions, temperature conditions,
    light conditions, bais conditions and simulation time.
    """
    def __init__(self,projWindow=None,parent=None):
        super(PVRD_Mode4_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.isSideBarDone=False
        
        self.stackWidget=QStackedWidget()
        
        self.mode0_widget=PVRD_Mode4_Structure_Widget(projWindow=projWindow,modeWidget=self)
        self.mode1_widget=PVRD_Mode4_Temperature_Widget(projWindow=projWindow,modeWidget=self)
        self.mode2_widget=PVRD_Mode4_Light_Widget(projWindow=projWindow,modeWidget=self)
        self.mode3_widget=PVRD_Mode4_Bias_Widget(projWindow=projWindow,modeWidget=self)
        
        self.stackWidget.addWidget(self.mode0_widget)
        self.stackWidget.addWidget(self.mode1_widget)
        self.stackWidget.addWidget(self.mode2_widget)
        self.stackWidget.addWidget(self.mode3_widget)
        
        self.stackWidget.setCurrentIndex(0)
        
        vLayout=QVBoxLayout()
        
        self.createBottomBar()
        vLayout.addWidget(self.stackWidget)
        vLayout.addWidget(self.bottomBar)
        
        self.setLayout(vLayout)
        
    def createBottomBar(self):
        self.bottomBar=QToolBar('Mode5_ToolBar')
        self.bottomBar.setOrientation(Qt.Horizontal)
        
        self.pb_structure=QPushButton('Structure(IC)')
        self.pb_structure.indx=0
        self.pb_structure.setToolTip('Click this to set the Initial Conditions for the Structure')
        self.pb_structure.clicked[bool].connect(self.updateWidgetDisplay)
        
        self.pb_temperature=QPushButton('Temperature')
        self.pb_temperature.indx=1
        self.pb_temperature.setToolTip('Click this to display the settings for Temperature')
        self.pb_temperature.clicked[bool].connect(self.updateWidgetDisplay)
        
        self.pb_light=QPushButton('Light')
        self.pb_light.indx=2
        self.pb_light.setToolTip('Click this to display the settings for Light')
        self.pb_light.clicked[bool].connect(self.updateWidgetDisplay)
        
        self.pb_bias=QPushButton('Bias')
        self.pb_bias.indx=3
        self.pb_bias.setToolTip('Click this to display the settings for Bias')
        self.pb_bias.clicked[bool].connect(self.updateWidgetDisplay)
        
        self.DCSDonePB=QPushButton('Done')
        self.DCSDonePB.setToolTip('Click this to complete the Simulation Specification')
        self.DCSDonePB.setCheckable(True)
        self.DCSDonePB.clicked[bool].connect(self.completeSim)
        
        self.bottomBar.addWidget(self.pb_structure)
        self.bottomBar.addWidget(self.pb_temperature)
        self.bottomBar.addWidget(self.pb_light)
        self.bottomBar.addWidget(self.pb_bias)
        self.bottomBar.addWidget(self.DCSDonePB)
                
    def completeSim(self):
        self.projWindow.toolBar.meshAction.setEnabled(True)
        self.projWindow.pC.mode=5
    
    def updateWidgetDisplay(self):
        pb=self.sender()
        self.stackWidget.setCurrentIndex(pb.indx)
        
###############################################################################
        
class PVRD_Mode4_Small_Widget(QWidget):
    def __init__(self,pb=None,view=None,parent=None):
        super(PVRD_Mode4_Small_Widget,self).__init__(parent)
        vLayout=QVBoxLayout()
        if pb is not None:
            vLayout.addWidget(pb)
        if view is not None:
            vLayout.addWidget(view)
        
        self.setLayout(vLayout)
###############################################################################
        
class PVRD_Mode4_Base_Widget(QWidget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode4_Base_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.modeWidget=modeWidget
        self.isSideBarDone=False
        
        self.hLayout=QHBoxLayout()
        self.gView=QGraphicsView()
        self.scene = QGraphicsScene(self.gView)
        self.scene.setBackgroundBrush(Qt.black)

        self.gView.setScene(self.scene)
        self.gView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setDragMode(QGraphicsView.RubberBandDrag)
        
        self.hLayout.addWidget(self.gView)
        self.setLayout(self.hLayout)
        
    def wheelEvent(self,Event):
        if Event.angleDelta().y()>0:
            factor=1.25
        else:
            factor=0.8
        if self.gView is not None:
            self.gView.scale(factor, factor)
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_F and self.gView is not None:
                self.gView.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
                
#    def completeSim(self):
#        self.projWindow.toolBar.meshAction.setEnabled(True)
#        self.projWindow.pC.mode=5
        

class PVRD_Mode4_Structure_Widget(PVRD_Mode4_Base_Widget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode4_Structure_Widget,self).__init__(projWindow,modeWidget,parent)
        self.allRectItemList=list()
        self.allLineItemList=list()
        self.allPointItemList=list()
        
    def updateWidget(self):
    
        whitePen=QPen(Qt.white)
        whitePen.setCosmetic(True)
        whitePen.setWidth(2)
        
        redPen=QPen(Qt.red)
        redPen.setCosmetic(True)
        redPen.setWidth(4)
        
        ii=0
        for mat in self.projWindow.pC.allRectList:
            mat.IC=PVRD_IC_Data(0,mat)
            mat.BC=PVRD_BC_Data(0,mat)
            rectItem=PVRD_Rectangle_Mode2(mat.X0,mat.Y0,mat.W,mat.H,
                                   "Layer {0}".format(ii),
                                   mat.matName,
                                   None,
                                   self.projWindow.pC.matBrushDict[mat.matName],
                                   self.projWindow,
                                   parent=self,
                                   pCindx=ii,
                                   nDims=self.projWindow.pC.nDims,
                                   gType=2)
            ii=ii+1
            self.scene.addItem(rectItem)
            self.allRectItemList.append(rectItem)
        ii=0
        for line in self.projWindow.pC.allLineList:
            line.IC=PVRD_IC_Data(0,line)
            line.BC=PVRD_BC_Data(0,line)
            lineItem=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
                                   "Line {0}".format(ii),
                                   line.matName,
                                   whitePen,
                                   self.projWindow,
                                   self,
                                   pCindx=ii,
                                   nDims=self.projWindow.pC.nDims,
                                   gType=2)
            ii=ii+1
            self.scene.addItem(lineItem)
            self.allLineItemList.append(lineItem)
            
        ii=0
        for line in self.projWindow.pC.allPointList:
            line.IC=PVRD_IC_Data(0,line)
            line.BC=PVRD_BC_Data(0,line)
            lineItem=PVRD_Point_Mode2(line.x1,line.y1,
                                    "Point {0}".format(ii),
                                    line.matName,
                                    redPen,
                                    self.projWindow,
                                    self,
                                    pCindx=ii,
                                    nDims=self.projWindow.pC.nDims,
                                    gType=2)
            ii=ii+1
            self.scene.addItem(lineItem)
            self.allPointItemList.append(lineItem)
            
    def updateWidgetDialog(self):
        for item in self.allRectItemList:
            item.dlgBox.updateDialog()
        for item in self.allLineItemList:
            item.dlgBox.updateDialog()
        for item in self.allPointItemList:
            item.dlgBox.updateDialog()
                
        
class PVRD_Mode4_Temperature_Widget(PVRD_Mode4_Base_Widget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode4_Temperature_Widget,self).__init__(projWindow,modeWidget,parent)
        
        self.indx=0
        self.itemList=list()
        self.hLayout.removeWidget(self.gView)
        
        self.gView=pg.PlotWidget(title="Temperature")
        
        self.gView.setLabel('bottom',"Time",units='s')
        self.gView.setLabel('left',"Temperature",units='K')
        
        self.hLayout.addWidget(self.gView)
        
        self.curTime=0
        self.curTimeIndx=0 #0 for seconds unit
        self.curTemp=300
        self.curTempIndx=0 #0 for K unit
        
        dlg=PVRD_Mode4_TemperatureDlg_Point(self.curTime,self.curTemp)
        dlg.nextTempTB.setText("{0}".format(self.curTemp))
        dlg.nextTimeTB.setText("{0}".format(initEndTime))
#        print('0a)tempParLen={0}'.format(len(self.projWindow.pC.tempParList)))
        self.projWindow.pC.tempParList.append(PVRD_ParTimeData(typeVal=0,startPar=self.curTemp,endTime=initEndTime,endPar=self.curTemp))
#        print('0b)tempParLen={0}'.format(len(self.projWindow.pC.tempParList)))
        self.curTime=initEndTime        
        pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
        
        pdata.sigClicked.connect(self.lineClicked)
        
        self.gView.addItem(pdata)
        self.itemList.append(pdata)
        
        self.CB=QComboBox()
        self.CB.addItems(["Points","Newton Cooling"])
        
        self.PB=QPushButton("Add")
        
        self.PB.clicked[bool].connect(self.addNewItem)
        
        vLayout=QVBoxLayout()
        vLayout.addWidget(self.CB)
        vLayout.addWidget(self.PB)
        vLayout.addStretch(1)
        
        self.hLayout.addLayout(vLayout)

    def lineClicked(self):
        plotItem=self.sender()
        if plotItem.dlg.exec_():
            nextTime,nextTemp,nPoints,isDeleted,curTemp=plotItem.dlg.result()
            if not isDeleted:
                print('nTime={0},nTemp={1},nPoint={2},curTemp={3}'.format(nextTime,
                      nextTemp,nPoints,curTemp))
                initLen=self.projWindow.pC.tempParList[plotItem.indx].endTimeVal - self.projWindow.pC.tempParList[plotItem.indx].startTimeVal
                delta = nextTime-initLen
                self.projWindow.pC.tempParList[plotItem.indx].endTimeVal=self.projWindow.pC.tempParList[plotItem.indx].endTimeVal+delta
                self.projWindow.pC.tempParList[plotItem.indx].endParVal=nextTemp
                self.projWindow.pC.tempParList[plotItem.indx].nParVal=nPoints
#                print('1)tempParLen={0}'.format(len(self.projWindow.pC.tempParList)))
                if plotItem.indx+1 <= len(self.projWindow.pC.tempParList)-1:
                    self.projWindow.pC.tempParList[plotItem.indx+1].startParVal=nextTemp
                if self.projWindow.pC.tempParList[plotItem.indx].startParVal != curTemp:
                    self.projWindow.pC.tempParList[plotItem.indx].startParVal=curTemp
#                    print('1)before update and setData')
#                    self.itemList[plotItem.indx].updateAndSetData()

#                print('2)tempParLen={0}'.format(len(self.projWindow.pC.tempParList)))
                for ii in range(plotItem.indx,len(self.projWindow.pC.tempParList)):
                    if ii !=plotItem.indx:
                        self.projWindow.pC.tempParList[ii].startTimeVal=self.projWindow.pC.tempParList[ii].startTimeVal+delta
                        self.projWindow.pC.tempParList[ii].endTimeVal=self.projWindow.pC.tempParList[ii].endTimeVal+delta
                        print('2)before update and setData')
                        self.itemList[ii].updateAndSetData()
                            
                self.curTime=self.projWindow.pC.tempParList[-1].endTimeVal
                self.curTemp=self.projWindow.pC.tempParList[-1].endParVal
#                print('3)tempParLen={0}'.format(len(self.projWindow.pC.tempParList)))
                print('3)before update and setData')
                plotItem.updateAndSetData()
                
            else:
                initLen=self.projWindow.pC.tempParList[plotItem.indx].endTimeVal - self.projWindow.pC.tempParList[plotItem.indx].startTimeVal
                delta = -initLen
                for ii in range(plotItem.indx,len(self.projWindow.pC.tempParList)):
                    if ii==plotItem.indx+1:
                        self.projWindow.pC.tempParList[ii].startParVal=self.projWindow.pC.tempParList[plotItem.indx].startParVal
                    if ii !=plotItem.indx:
                        self.projWindow.pC.tempParList[ii].startTimeVal=self.projWindow.pC.tempParList[ii].startTimeVal+delta
                        self.projWindow.pC.tempParList[ii].endTimeVal=self.projWindow.pC.tempParList[ii].endTimeVal+delta
                        self.itemList[ii].updateAndSetData()
                    
                        
                
                self.curTime=self.projWindow.pC.tempParList[-1].endTimeVal
                self.gView.removeItem(self.itemList[plotItem.indx])
                del self.itemList[plotItem.indx]
                del self.projWindow.pC.tempParList[plotItem.indx]
                
                if len(self.itemList)==0:
                    self.curTime=0
                
                for ii in range(0,len(self.itemList)):
                    self.itemList[ii].indx=ii
                    
                self.indx=self.indx-1
            
        
    def addNewItem(self):
        if self.CB.currentIndex()==0:
            dlg=PVRD_Mode4_TemperatureDlg_Point(self.curTime,self.curTemp,self.curTimeIndx,self.curTempIndx)
            
        if self.CB.currentIndex()==1:
            dlg=PVRD_Mode4_TemperatureDlg_NCooling(self.curTime,self.curTemp)
            
        typeVal=self.CB.currentIndex()
        if dlg.exec_():
            nextTime, nextTemp, nPoints, isDeleted,_ = dlg.result()
            if self.CB.currentIndex()==1:
                cRate=dlg.getRate()
            else:
                cRate=0.1
            if not isDeleted:
                self.projWindow.pC.tempParList.append(PVRD_ParTimeData(typeVal=typeVal,
                    startTime=self.curTime,
                    startPar=self.curTemp,
                    endTime=self.curTime+nextTime,
                    endPar=nextTemp,
                    nParVal=nPoints,cRate=cRate))
                self.curTime=self.curTime+nextTime
                self.curTemp=nextTemp
                
                pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
                pdata.sigClicked.connect(self.lineClicked)
                self.gView.addItem(pdata)
                self.itemList.append(pdata)
                self.indx=self.indx+1
                
    def updateWidgetDialog(self):
        self.indx=0
        self.itemList=list()
        self.gView.clear()
        for tempPar in self.projWindow.pC.tempParList:
            if tempPar.typeVal==0:
                dlg=PVRD_Mode4_TemperatureDlg_Point(tempPar.startTimeVal,tempPar.startParVal,0,0)
            if tempPar.typeVal==1:
                dlg=PVRD_Mode4_TemperatureDlg_NCooling(tempPar.startTimeVal,tempPar.startParVal,0,0)
                dlg.rateTB.setText("{0}".format(tempPar.cRate))
            
            dlg.nextTimeTB.setText("{0}".format(tempPar.endTimeVal-tempPar.startTimeVal))
            dlg.nextTempTB.setText("{0}".format(tempPar.endParVal))
            dlg.nPointTB.setText("{0}".format(tempPar.nParVal))
            self.curTime=tempPar.endTimeVal
            self.curTemp=tempPar.endParVal
            pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
            pdata.sigClicked.connect(self.lineClicked)
            pdata.updateAndSetData()
            self.gView.addItem(pdata)
            self.itemList.append(pdata)
            self.indx=self.indx+1
            
        
class PVRD_Mode4_Light_Widget(PVRD_Mode4_Base_Widget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode4_Light_Widget,self).__init__(projWindow,modeWidget,parent)
        self.indx=0
        self.itemList=list()
        self.hLayout.removeWidget(self.gView)
        
        self.gView=pg.PlotWidget(title="Light")
        
        self.gView.setLabel('bottom',"Time",units='s')
        self.gView.setLabel('left',"Sun Intensity",units='Suns')
        
        self.hLayout.addWidget(self.gView)
        
        self.curTime=0
        self.curTemp=0
        
        dlg=PVRD_Mode4_LightDlg_Point(self.curTime,self.curTemp)
        dlg.nextLightTB.setText("{0}".format(self.curTemp))
        dlg.nextTimeTB.setText("{0}".format(initEndTime))
        
        self.projWindow.pC.lightParList.append(PVRD_ParTimeData(typeVal=0,startPar=self.curTemp,endTime=initEndTime,endPar=self.curTemp))
        self.curTime=initEndTime        
        pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
        
        pdata.sigClicked.connect(self.lineClicked)
        
        self.gView.addItem(pdata)
        self.itemList.append(pdata)
        
        
        self.CB=QComboBox()
        self.CB.addItems(["Points"])
        self.PB=QPushButton("Add")
        self.PB.clicked[bool].connect(self.addNewItem)
        
        vLayout=QVBoxLayout()
        vLayout.addWidget(self.CB)
        vLayout.addWidget(self.PB)
        vLayout.addStretch(1)
        
        self.hLayout.addLayout(vLayout)
        
    def lineClicked(self):
        plotItem=self.sender()
        if plotItem.dlg.exec_():
            nextTime,nextTemp,nPoints,isDeleted=plotItem.dlg.result()
            if not isDeleted:
                initLen=self.projWindow.pC.lightParList[plotItem.indx].endTimeVal - self.projWindow.pC.lightParList[plotItem.indx].startTimeVal
                delta = nextTime-initLen
                self.projWindow.pC.lightParList[plotItem.indx].endTimeVal=self.projWindow.pC.lightParList[plotItem.indx].endTimeVal+delta
                self.projWindow.pC.lightParList[plotItem.indx].endParVal=nextTemp
                self.projWindow.pC.lightParList[plotItem.indx].nParVal=nPoints
                if plotItem.indx+1 <= len(self.projWindow.pC.lightParList)-1:
                    self.projWindow.pC.lightParList[plotItem.indx+1].startParVal=nextTemp
                    
                for ii in range(plotItem.indx,len(self.projWindow.pC.lightParList)):
                    if ii !=plotItem.indx:
                        self.projWindow.pC.lightParList[ii].startTimeVal=self.projWindow.pC.lightParList[ii].startTimeVal+delta
                        self.projWindow.pC.lightParList[ii].endTimeVal=self.projWindow.pC.lightParList[ii].endTimeVal+delta
                        self.itemList[ii].updateAndSetData()
                
                
                self.curTime=self.projWindow.pC.lightParList[-1].endTimeVal
                plotItem.updateAndSetData()
            else:
                initLen=self.projWindow.pC.lightParList[plotItem.indx].endTimeVal - self.projWindow.pC.lightParList[plotItem.indx].startTimeVal
                delta = -initLen
                for ii in range(plotItem.indx,len(self.projWindow.pC.lightParList)):
                    if ii==plotItem.indx+1:
                        self.projWindow.pC.lightParList[ii].startParVal=self.projWindow.pC.lightParList[plotItem.indx].startParVal
                    if ii !=plotItem.indx:
                        self.projWindow.pC.lightParList[ii].startTimeVal=self.projWindow.pC.lightParList[ii].startTimeVal+delta
                        self.projWindow.pC.lightParList[ii].endTimeVal=self.projWindow.pC.lightParList[ii].endTimeVal+delta
                        self.itemList[ii].updateAndSetData()
                    
                        
                
                self.curTime=self.projWindow.pC.lightParList[-1].endTimeVal
                self.gView.removeItem(self.itemList[plotItem.indx])
                del self.itemList[plotItem.indx]
                del self.projWindow.pC.lightParList[plotItem.indx]
                
                if len(self.itemList)==0:
                    self.curTime=0
                
                for ii in range(0,len(self.itemList)):
                    self.itemList[ii].indx=ii
                    
                self.indx=self.indx-1
            
        
    def addNewItem(self):
        if self.CB.currentIndex()==0:
            dlg=PVRD_Mode4_LightDlg_Point(self.curTime,self.curTemp)
            
        typeVal=self.CB.currentIndex()
            
        if dlg.exec_():
            nextTime, nextTemp, nPoints, isDeleted = dlg.result()
            if not isDeleted:
                self.projWindow.pC.lightParList.append(PVRD_ParTimeData(typeVal=typeVal,
                    startTime=self.curTime,
                    startPar=self.curTemp,
                    endTime=self.curTime+nextTime,
                    endPar=nextTemp,
                    nParVal=nPoints))
                
                self.curTime=self.curTime+nextTime
                self.curTemp=nextTemp
                self.indx=self.indx+1
                
                pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
                pdata.sigClicked.connect(self.lineClicked)
                self.gView.addItem(pdata)
                self.itemList.append(pdata)
                
    def updateWidgetDialog(self):
        for lightPar in self.projWindow.pC.lightParList:
            if lightPar.typeVal==0:
                dlg=PVRD_Mode4_LightDlg_Point(lightPar.startTimeVal,lightPar.startParVal)
            
            dlg.nextTimeTB.setText("{0}".format(lightPar.endTimeVal-lightPar.startTimeVal))
            dlg.nextLightTB.setText("{0}".format(lightPar.endParVal))
            dlg.nPointTB.setText("{0}".format(lightPar.nParVal))
            self.curTime=lightPar.endTimeVal
            self.curTemp=lightPar.endParVal
            pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
            pdata.sigClicked.connect(self.lineClicked)
            pdata.updateAndSetData()
            self.gView.addItem(pdata)
            self.itemList.append(pdata)
            self.indx=self.indx+1
        
class PVRD_Mode4_Bias_Widget(PVRD_Mode4_Base_Widget):
    def __init__(self,projWindow=None,modeWidget=None,parent=None):
        super(PVRD_Mode4_Bias_Widget,self).__init__(projWindow,modeWidget,parent)
        
        self.indx=0
        self.itemList=list()
        self.hLayout.removeWidget(self.gView)
        
        self.gView=pg.PlotWidget(title="Light")
        
        self.gView.setLabel('bottom',"Time",units='s')
        self.gView.setLabel('left',"Bias",units='V')
        
        self.hLayout.addWidget(self.gView)
        
        self.curTime=0
        self.curTemp=0
        
        dlg=PVRD_Mode4_BiasDlg_Point(self.curTime,self.curTemp)
        dlg.nextBiasTB.setText("{0}".format(self.curTemp))
        dlg.nextTimeTB.setText("{0}".format(initEndTime))
        
        self.projWindow.pC.biasParList.append(PVRD_ParTimeData(typeVal=0,startPar=self.curTemp,endTime=initEndTime,endPar=self.curTemp))
        self.curTime=initEndTime        
        pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
        
        pdata.sigClicked.connect(self.lineClicked)
        
        self.gView.addItem(pdata)
        self.itemList.append(pdata)
        
        
        self.CB=QComboBox()
        self.CB.addItems(["Points"]) # Sinusoidal will be added later stage
        self.PB=QPushButton("Add")
        self.PB.clicked[bool].connect(self.addNewItem)
        
        vLayout=QVBoxLayout()
        vLayout.addWidget(self.CB)
        vLayout.addWidget(self.PB)
        vLayout.addStretch(1)
        
        self.hLayout.addLayout(vLayout)
        
    def lineClicked(self):
        plotItem=self.sender()
        if plotItem.dlg.exec_():
            nextTime,nextTemp,nPoints, isDeleted, isFloating=plotItem.dlg.result()
            if not isDeleted:
                initLen=self.projWindow.pC.biasParList[plotItem.indx].endTimeVal - self.projWindow.pC.biasParList[plotItem.indx].startTimeVal
                delta = nextTime-initLen
                self.projWindow.pC.biasParList[plotItem.indx].endTimeVal=self.projWindow.pC.biasParList[plotItem.indx].endTimeVal+delta
                self.projWindow.pC.biasParList[plotItem.indx].endParVal=nextTemp
                self.projWindow.pC.biasParList[plotItem.indx].nParVal=nPoints
                self.projWindow.pC.biasParList[plotItem.indx].isFloating=isFloating
                if plotItem.indx+1 <= len(self.projWindow.pC.biasParList)-1:
                    self.projWindow.pC.biasParList[plotItem.indx+1].startParVal=nextTemp
                    
                for ii in range(plotItem.indx,len(self.projWindow.pC.biasParList)):
                    if ii !=plotItem.indx:
                        self.projWindow.pC.biasParList[ii].startTimeVal=self.projWindow.pC.biasParList[ii].startTimeVal+delta
                        self.projWindow.pC.biasParList[ii].endTimeVal=self.projWindow.pC.biasParList[ii].endTimeVal+delta
                        self.itemList[ii].updateAndSetData()
                
                self.curTime=self.projWindow.pC.biasParList[-1].endTimeVal
                plotItem.updateAndSetData()
            else:
                initLen=self.projWindow.pC.biasParList[plotItem.indx].endTimeVal - self.projWindow.pC.biasParList[plotItem.indx].startTimeVal
                delta = -initLen
                for ii in range(plotItem.indx,len(self.projWindow.pC.biasParList)):
                    if ii==plotItem.indx+1:
                        self.projWindow.pC.biasParList[ii].startParVal=self.projWindow.pC.biasParList[plotItem.indx].startParVal
                    if ii !=plotItem.indx:
                        self.projWindow.pC.biasParList[ii].startTimeVal=self.projWindow.pC.biasParList[ii].startTimeVal+delta
                        self.projWindow.pC.biasParList[ii].endTimeVal=self.projWindow.pC.biasParList[ii].endTimeVal+delta
                        self.itemList[ii].updateAndSetData()
                    
                        
                
                self.curTime=self.projWindow.pC.biasParList[-1].endTimeVal
                self.gView.removeItem(self.itemList[plotItem.indx])
                del self.itemList[plotItem.indx]
                del self.projWindow.pC.biasParList[plotItem.indx]
                
                if len(self.itemList)==0:
                    self.curTime=0
                
                
                
                for ii in range(0,len(self.itemList)):
                    self.itemList[ii].indx=ii
                    
                self.indx=self.indx-1
                
            
        
    def addNewItem(self):
        if self.CB.currentIndex()==0:
            dlg=PVRD_Mode4_BiasDlg_Point(self.curTime,self.curTemp)
            
        typeVal=self.CB.currentIndex()
            
        if dlg.exec_():
            nextTime, nextTemp, nPoints, isDeleted, isFloating = dlg.result()
            if not isDeleted:
                self.projWindow.pC.biasParList.append(PVRD_ParTimeData(typeVal=typeVal,
                            startTime=self.curTime,
                            startPar=self.curTemp,
                            endTime=self.curTime+nextTime,
                            endPar=nextTemp,
                            nParVal=nPoints,
                            isFloating=isFloating))
                self.curTime=self.curTime+nextTime
                self.curTemp=nextTemp
                self.indx=self.indx+1
                
                pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
                pdata.sigClicked.connect(self.lineClicked)
                self.gView.addItem(pdata)
                self.itemList.append(pdata)
                
    def updateWidgetDialog(self):
        for biasPar in self.projWindow.pC.biasParList:
            if biasPar.typeVal==0:
                dlg=PVRD_Mode4_BiasDlg_Point(biasPar.startTimeVal,biasPar.startParVal)
            
            dlg.nextTimeTB.setText("{0}".format(biasPar.endTimeVal-biasPar.startTimeVal))
            dlg.nextBiasTB.setText("{0}".format(biasPar.endParVal))
            dlg.nPointTB.setText("{0}".format(biasPar.nParVal))
            dlg.floatButton.setChecked(biasPar.isFloating)
            self.curTime=biasPar.endTimeVal
            self.curTemp=biasPar.endParVal
            pdata=PVRD_pgLine_Mode4(projWindow=self.projWindow,indx=self.indx,dlg=dlg)
            pdata.sigClicked.connect(self.lineClicked)
            pdata.updateAndSetData()
            self.gView.addItem(pdata)
            self.itemList.append(pdata)
            self.indx=self.indx+1
        
        
###############################################################################
        
class PVRD_Mode5_Widget(QWidget):
    """
    Mode 5 Widget is for displaying all widgets for meshing the geometric structure.
    This also includes numerical tolerances and numerical algorithm selection.
    """
    def __init__(self,projWindow=None,parent=None):
        super(PVRD_Mode5_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.isSideBarDone=False
        
        self.hLayout=QHBoxLayout()
        self.gView=QGraphicsView()
        self.scene = QGraphicsScene(self.gView)
        self.scene.setBackgroundBrush(Qt.black)

        self.gView.setScene(self.scene)
        self.gView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.gView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
#        self.gView.setDragMode(QGraphicsView.RubberBandDrag)
        
        self.hLayout.addWidget(self.gView)
        self.setLayout(self.hLayout)
        
    def updateWidget(self):
        if not self.isSideBarDone:
            self.createSideBar()
#        self.projWindow.pC.simplifyBoudaries()
        
        self.bBoundList=list()
        self.tBoundList=list()
        self.lBoundList=list()
        self.rBoundList=list()
        self.allRectItemList=list()
        self.allLineItemList=list()
        self.allPointItemList=list()
        self.allItemList=list()
        
        whitePen=QPen(Qt.white)
        whitePen.setCosmetic(True)
        whitePen.setWidth(2)
        
        redPen=QPen(Qt.red)
        redPen.setCosmetic(True)
        redPen.setWidth(4)
        
        ii=0
        for mat in self.projWindow.pC.allRectList:
            rectItem=PVRD_Rectangle_Mode5(mat.X0,mat.Y0,mat.W,mat.H,
                                   "Layer {0}".format(ii),
                                   mat.matName,
                                   redPen,
                                   self.projWindow.pC.matBrushDict[mat.matName],
                                   self.projWindow,
                                   parent=self,
                                   pCindx=ii,
                                   nDims=self.projWindow.pC.nDims
                                   )
#            rectItem.dlgBox.updateDialog()
            self.allRectItemList.append(rectItem)
            ii=ii+1
            self.scene.addItem(rectItem)
        
#        ii=0
#        for line in self.projWindow.pC.allLineList:
#            lineItem=PVRD_Line_Mode2(line.x1,line.y1,line.x2,line.y2,
#                                   "Line {0}".format(ii),
#                                   line.matName,
#                                   whitePen,
#                                   self.projWindow,
#                                   self,
#                                   pCindx=ii,
#                                   nDims=self.projWindow.pC.nDims,
#                                   gType=3)
##            lineItem.dlgBox.updateDialog()
#            ii=ii+1
#            self.scene.addItem(lineItem)
#            
#        ii=0
#        for line in self.projWindow.pC.allPointList:
#            lineItem=PVRD_Point_Mode2(line.x1,line.y1,
#                                    "Point {0}".format(ii),
#                                    line.matName,
#                                    redPen,
#                                    self.projWindow,
#                                    self,
#                                    pCindx=ii,
#                                    nDims=self.projWindow.pC.nDims,
#                                    gType=3)
##            lineItem.dlgBox.updateDialog()
#            ii=ii+1
#            self.scene.addItem(lineItem)
        
    def createSideBar(self):
        self.isSideBarDone=True
        vLayout=QVBoxLayout()
        
        self.DCSDonePB=QPushButton('Done')
        self.DCSDonePB.setToolTip('Click this to complete the Mesh Setup')
        self.DCSDonePB.setCheckable(True)
        self.DCSDonePB.clicked[bool].connect(self.completeMesh)
        
        vLayout.addWidget(self.DCSDonePB)
        vLayout.addStretch(1)
        self.hLayout.addLayout(vLayout)
        
    def wheelEvent(self,Event):
        if Event.angleDelta().y()>0:
            factor=1.25
        else:
            factor=0.8
        if self.gView is not None:
            self.gView.scale(factor, factor)
    
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_F and self.gView is not None:
                self.gView.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
                
    def completeMesh(self):
        self.createMeshFor0Dand1D()
        self.projWindow.pC.updateTempBiasLightData()
        self.projWindow.toolBar.runAction.setEnabled(True)
        self.projWindow.pC.mode=6
    
    def updateDialogProp(self):
        for item in self.allRectItemList:
            item.dlgBox.updateDialog()
            
    def createMeshFor0Dand1D(self):
        for rectData in self.projWindow.pC.allRectList:
            if self.projWindow.pC.nDims==0:
                rectData.xMeshPointList=[0]
                rectData.yMeshPointList=[0]
            if self.projWindow.pC.nDims==1:
                rectData.xMeshPointList=[0]
                
        
class PVRD_Mode6_Widget(QWidget):
    """
    Mode 6 Widget is for displaying all widgets for runtime status of simulation.
    """
    def __init__(self,projWindow=None,parent=None):
        super(PVRD_Mode6_Widget,self).__init__(parent)
        self.projWindow=projWindow
#        pb=QPushButton("Mode6")
#        vLayout=QVBoxLayout()
#        vLayout.addWidget(pb)
#        vLayout.addStretch()
#        self.setLayout(vLayout)
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        self.concRelTolRxnName=QLabel("Conc Rel Tol (in Reactions):")
        self.concRelTolRxnTB=QLineEdit("{:.2e}".format(1e-3))
        self.concRelTolRxnName.setBuddy(self.concRelTolRxnTB)
        self.concRelTolRxnTB.setValidator(QDoubleValidator())
        
        self.concRelTolDfnName=QLabel("Conc Rel Tol (in Diffusion):")
        self.concRelTolDfnTB=QLineEdit("{:.2e}".format(1e-3))
        self.concRelTolDfnName.setBuddy(self.concRelTolDfnTB)
        self.concRelTolDfnTB.setValidator(QDoubleValidator())
        
        self.potAbsTolPsnName=QLabel("Pot Abs Tol (in Poisson):")
        self.potAbsTolPsnTB=QLineEdit("{:.2e}".format(1e-3))
        self.potAbsTolPsnName.setBuddy(self.potAbsTolPsnTB)
        self.potAbsTolPsnTB.setValidator(QDoubleValidator())
        
        self.concRelTolGummelName=QLabel("Conc Rel Tol (in Gummel):")
        self.concRelTolGummelTB=QLineEdit("{:.2e}".format(1e-3))
        self.concRelTolGummelName.setBuddy(self.concRelTolGummelTB)
        self.concRelTolGummelTB.setValidator(QDoubleValidator())
        
        self.potAbsTolGummelName=QLabel("Pot Abs Tol (in Gummel):")
        self.potAbsTolGummelTB=QLineEdit("{:.2e}".format(1e-3))
        self.potAbsTolGummelName.setBuddy(self.potAbsTolGummelTB)
        self.potAbsTolGummelTB.setValidator(QDoubleValidator())
        
        self.runPB=QPushButton("Run")
        self.qText=QTextEdit()
        
        self.outLog=OutLog(self.qText,out=sys.stdout)
        
        self.pBar=QProgressBar()
        
##        namespace={'pg': pg, 'np': np}
        namespace=locals()
        text = """
        This is an interactive python console. The numpy and pyqtgraph modules have already been imported 
        as 'np' and 'pg'. 
        
        Go, play.
        """
        
        self.runConsole=pyqtgraph.console.ConsoleWidget(namespace=namespace, text=text)
        
        
    def layout_widgets(self):
        layout = QGridLayout()
        
        row=0
        layout.addWidget(self.concRelTolRxnName,row,0,1,1)
        layout.addWidget(self.concRelTolRxnTB,row,1,1,1)
        
        layout.addWidget(self.concRelTolDfnName,row,2,1,1)
        layout.addWidget(self.concRelTolDfnTB,row,3,1,1)
        
        layout.addWidget(self.potAbsTolPsnName,row,4,1,1)
        layout.addWidget(self.potAbsTolPsnTB,row,5,1,1)
        
        row=row+1
        layout.addWidget(self.concRelTolGummelName,row,0,1,1)
        layout.addWidget(self.concRelTolGummelTB,row,1,1,1)
        
        layout.addWidget(self.potAbsTolGummelName,row,2,1,1)
        layout.addWidget(self.potAbsTolGummelTB,row,3,1,1)
        
        row=row+1
        layout.addWidget(self.runPB,row,0,1,5)
        
        row=row+1
        layout.addWidget(self.qText,row,0,1,5)
        
        row=row+1
        layout.addWidget(self.pBar,row,0,1,5)
        row=row+1
        layout.addWidget(self.runConsole,row,0,1,5)
        
        self.setLayout(layout)
        
    def create_connections(self):
        self.runPB.clicked[bool].connect(self.projWindow.callNumEngwInputs)
        
        self.qText.setReadOnly(True)
        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.qText.setFont(font)
        

class PVRD_Mode7_Widget(QWidget):
    """
    Mode 7 Widget is for displaying all widgets for browsing the simulation result.
    This also includes the documentation generation for the simulation.
    """
    def __init__(self,projWindow=None,hdf5Name=None,parent=None):
        super(PVRD_Mode7_Widget,self).__init__(parent)
        self.projWindow=projWindow
        self.isPubQuality=False
        self.concVz=None
        self.fiVz=None
        self.fluxVz=None
        self.bandsVz=None
        self.fieldVz=None
        
        self.hdf5Name=hdf5Name
        
        if projWindow is not None and hdf5Name is None:
            self.hdf5Name=self.projWindow.hdf5_fileName
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def updateData(self):
        self.hdf5_fp=h5py.File(self.hdf5Name, 'r')
        self.pInfoStr=next(iter(self.hdf5_fp))+'/latestRun/Info'
        self.pSolStr=next(iter(self.hdf5_fp))+'/latestRun/Solution'
        self.pSnapShotStr=next(iter(self.hdf5_fp))+'/latestRun/SnapShot'
        
        # Do we need to recreate this?
        self.nDims=self.hdf5_fp[self.pInfoStr].attrs['nDims']
        self.nX=self.hdf5_fp[self.pInfoStr].attrs['nX']
        self.nY=self.hdf5_fp[self.pInfoStr].attrs['nY']
        self.nMesh=self.hdf5_fp[self.pInfoStr].attrs['nMesh']
        self.M=self.hdf5_fp[self.pInfoStr].attrs['nSpecies']
        self.K=self.hdf5_fp[self.pInfoStr].attrs['nReactions']
        self.eIndx=self.hdf5_fp[self.pInfoStr].attrs['eIndx']
        self.hIndx=self.hdf5_fp[self.pInfoStr].attrs['hIndx']
        
        # Should look for memory 
        self.X=np.array(self.hdf5_fp[self.pInfoStr+'/X'])
        self.Y=np.array(self.hdf5_fp[self.pInfoStr+'/Y'])
        self.dX=np.array(self.hdf5_fp[self.pInfoStr+'/dX'])
        self.dY=np.array(self.hdf5_fp[self.pInfoStr+'/dY'])
        self.Hx=np.array(self.hdf5_fp[self.pInfoStr+'/Hx'])
        self.Hy=np.array(self.hdf5_fp[self.pInfoStr+'/Hy'])
        self.hx=np.array(self.hdf5_fp[self.pInfoStr+'/hx'])
        self.hy=np.array(self.hdf5_fp[self.pInfoStr+'/hy'])
        
        self.qVec=np.array(self.hdf5_fp[self.pInfoStr+'/charge'])
        self.species=np.array(self.hdf5_fp[self.pInfoStr+'/species'])
        self.reactions=np.array(self.hdf5_fp[self.pInfoStr+'/reactions'])
        self.iTime_snapShot=np.array(self.hdf5_fp[self.pSnapShotStr+'/initTime'])
        self.fTime_snapShot=np.array(self.hdf5_fp[self.pSnapShotStr+'/finalTime'])
        self.G_snapShot=np.array(self.hdf5_fp[self.pSnapShotStr+'/G'])
        self.Vt_snapShot=np.array(self.hdf5_fp[self.pSnapShotStr+'/Vt'])
        self.Ns_snapShot=np.array(self.hdf5_fp[self.pSnapShotStr+'/Ns'])
        self.Kf_snapShot=np.array(self.hdf5_fp[self.pSnapShotStr+'/Kf'])
        self.Kb_snapShot=np.array(self.hdf5_fp[self.pSnapShotStr+'/Kb'])
        self.conc=np.array(self.hdf5_fp[self.pSolStr+'/Conc'])
        self.fi=np.array(self.hdf5_fp[self.pSolStr+'/Fi'])
        self.tVec=np.reshape(np.array(self.hdf5_fp[self.pSolStr+'/Time']),(-1,))
        self.rho=np.array([])
        self.netNd=np.array([])
        self.netNa=np.array([])
        self.Ec=np.array([])
        self.Ev=np.array([])
        self.Efn=np.array([])
        self.Efp=np.array([])
        self.hdf5_fp.close()
        
    def create_widgets(self):
        self.pub_ChkB=QCheckBox("For Publication")
        self.conc_PB=QPushButton('Concentrations')
        self.fi_PB=QPushButton('Potential')
        self.bands_PB=QPushButton('Bands')
        self.flux_PB=QPushButton('Flux')
        self.field_PB=QPushButton('Field')
        
        text="Starting an interactive console for custom plotting"
        
        namespace=locals()
        self.runConsole=pyqtgraph.console.ConsoleWidget(namespace=namespace,text=text)

        self.vLayout_1=QVBoxLayout()
        self.vLayout_2=QVBoxLayout()
        self.vLayout_3=QVBoxLayout()
        self.hLayout=QHBoxLayout()
        
    def layout_widgets(self):
        self.vLayout_1.addWidget(self.conc_PB)
        self.vLayout_1.addWidget(self.fi_PB)
        self.vLayout_1.addWidget(self.bands_PB)
        self.vLayout_1.addWidget(self.flux_PB)
        self.vLayout_1.addWidget(self.field_PB)
        self.vLayout_1.addStretch()
        
        self.vLayout_2.addWidget(self.pub_ChkB)
        self.vLayout_2.addStretch()
        
        self.vLayout_3.addWidget(self.runConsole)
        self.vLayout_3.addStretch()
        
        self.hLayout.addLayout(self.vLayout_1)
        self.hLayout.addLayout(self.vLayout_2)
        self.hLayout.addStretch()
        self.hLayout.addLayout(self.vLayout_3)
        self.runConsole.ui.exceptionBtn.setChecked(True)
        self.runConsole.ui.historyBtn.setChecked(True)
        
        self.setLayout(self.hLayout)
        
    def create_connections(self):
        self.pub_ChkB.stateChanged.connect(self.setPubQOut)
        self.conc_PB.clicked[bool].connect(self.showConc)
        self.fi_PB.clicked[bool].connect(self.showFi)
        self.bands_PB.clicked[bool].connect(self.showBands)
        
    def setPubQOut(self,state):
        if state==Qt.Checked:
            self.isPubQuality=True
#            print('Setting the Plots for Publication Quality')
        else:
            self.isPubQuality=False
            
    def showConc(self):
        if self.concVz is None:
            self.concVz=PVRD_ConcVisualizer(self.hdf5_fp,self.nDims,self)
            self.concVz.addSpeciesList(self.species)
            self.concVz.setTimeList(self.tVec)
        if not self.concVz.isVisible():
            self.concVz.show()
#        self.concVz.setFocus()
            
    def showFi(self):
        if self.fiVz is None:
            self.fiVz=PVRD_FiVisualizer(self.hdf5_fp,self.nDims,self)
            self.fiVz.setTimeList(self.tVec)
            self.fiVz.updatePlots()
        if not self.fiVz.isVisible():
            self.fiVz.show()
            
    def showBands(self):
        if self.bandsVz is None:
            self.bandsVz=PVRD_BandsVisualizer(self.hdf5_fp,self.nDims,self)
            self.bandsVz.setTimeList(self.tVec)
            self.bandsVz.updatePlots()
        if not self.bandsVz.isVisible():
            self.bandsVz.show()
            
    def updateHDF5Name(self,hdf5_fName):
        self.hdf5Name=hdf5_fName
        
    def calculateRho(self):
#        print('Conc ={0}'.format(self.conc.shape))
#        print('qVec ={0}'.format(self.qVec.shape))
        conc=np.reshape(self.conc,(-1,self.M))
        rho=conc.dot(self.qVec)
        self.rho=PhysConst.e*np.reshape(rho,(len(self.tVec),self.nX,self.nY))
        qVec=self.qVec.copy()
        qVec[self.eIndx]=0
        qVec[self.hIndx]=0
        qVec_p=qVec*(qVec>0)
        qVec_n=-qVec*(qVec<0)
        netNd=conc.dot(qVec_p)
        netNa=conc.dot(qVec_n)
        self.netNd=np.reshape(netNd,(len(self.tVec),self.nX,self.nY))
        self.netNa=np.reshape(netNa,(len(self.tVec),self.nX,self.nY))
        
    def calculateBands(self):
        eConc=self.conc[:,:,:,self.eIndx]+np.spacing(1)
        hConc=self.conc[:,:,:,self.hIndx]+np.spacing(1)
        Ev=0*eConc
        Ec=0*eConc
        Efn=0*eConc
        Efp=0*eConc
        jj=0
        for time in self.iTime_snapShot:
            t1=time
            t2=self.fTime_snapShot[jj]
            indx=np.where((self.tVec>=t1)*(self.tVec<t2))
            Ec[indx,:,:]=self.G_snapShot[jj,:,:,self.eIndx]-self.fi[indx,:,:]
            Ev[indx,:,:]=-self.G_snapShot[jj,:,:,self.hIndx]-self.fi[indx,:,:]
            Efn[indx,:,:]=Ec[indx,:,:]+self.Vt_snapShot[jj]*np.log(eConc[indx,:,:]/self.Ns_snapShot[jj,:,:,self.eIndx])
            Efp[indx,:,:]=Ev[indx,:,:]-self.Vt_snapShot[jj]*np.log(hConc[indx,:,:]/self.Ns_snapShot[jj,:,:,self.hIndx])
            
            jj=jj+1
            
        indx=-1
        jj=-1
        Ec[indx,:,:]=self.G_snapShot[jj,:,:,self.eIndx]-self.fi[indx,:,:]
        Ev[indx,:,:]=-self.G_snapShot[jj,:,:,self.hIndx]-self.fi[indx,:,:]
        Efn[indx,:,:]=Ec[indx,:,:]+self.Vt_snapShot[jj]*np.log(eConc[indx,:,:]/self.Ns_snapShot[jj,:,:,self.eIndx])
        Efp[indx,:,:]=Ev[indx,:,:]-self.Vt_snapShot[jj]*np.log(hConc[indx,:,:]/self.Ns_snapShot[jj,:,:,self.hIndx])
        
        self.Ev=Ev
        self.Ec=Ec
        self.Efn=Efn
        self.Efp=Efp
        
    def writeReactionsToFile(self):
        Kf=np.reshape(self.Kf_snapShot,(-1,))
        Kb=np.reshape(self.Kb_snapShot,(-1,))
        Gf=np.reshape(self.G_snapShot,(-1,))
        f = open("reactions.txt", "w")
        ii=0
        for reaction in self.reactions:
            lhsList=getReactionLHS(reaction)
            rhsList=getReactionRHS(reaction)
#            print('lhsList={0},type={1}'.format(lhsList,type(lhsList)))
#            print('rhsList={0},type={1}'.format(rhsList,type(rhsList)))
            speciesList=list(self.species)
            Gf_LHS=0
            Gf_RHS=0
            LHS1=''
            RHS1=''
            LHS2=''
            RHS2=''
            jj=0
            for lhs in lhsList:
                G0=0
                if lhs not in 'NULL':
                    indx=speciesList.index(lhs)
#                    print('species={0},indx={1}'.format(lhs,indx))
                    G0=Gf[indx]
                    Gf_LHS=Gf_LHS+G0
                if jj==0:
                    LHS1='{0:>15},{1:2.2f}'.format(lhs,G0)
                else:
                    LHS2='{0:>15},{1:2.2f}'.format(lhs,G0)
                jj=jj+1
            jj=0
            for rhs in rhsList:
                if rhs not in 'NULL':
#                    indx=np.where(self.species==rhs)
                    indx=speciesList.index(rhs)
#                    print('species={0},indx={1}'.format(rhs,indx))
                    G0=Gf[indx]
                    Gf_RHS=Gf_RHS+G0
                if jj==0:
                    RHS1='{0:>15},{1:2.2f}'.format(rhs,G0)
                else:
                    RHS2='{0:>15},{1:2.2f}'.format(rhs,G0)
                jj=jj+1
#            print('Gf_LHS={0},Gf_RHS={1}'.format(Gf_LHS,Gf_RHS))
            f.write('{0:>50}\t({1:2.5e}/{2:2.5e})\t{4:>25},{5:>25}\
                    {6:>25},{7:>25}\tDelG={3:2.3f})\n'.format(reaction,Kf[ii],
                    Kb[ii],Gf_LHS-Gf_RHS,LHS1,LHS2,RHS1,RHS2))
            ii=ii+1
        f.close()