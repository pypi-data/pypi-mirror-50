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
Created on Sun Nov  4 14:32:03 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from . import resources
import os

import h5py
import time

from PyQt5.QtWidgets import (
        QWidget, QToolBar, QAction, QMessageBox, QVBoxLayout, QFileDialog, 
        QStackedWidget
        )
from PyQt5.QtGui import (
        QIcon
        )
from PyQt5.QtCore import (
        Qt, QFileInfo, QDataStream, QIODevice, QFile, QThread
        )

from .PVRD_DialogBox import(
        NewProjectDlg
        )

from .PVRD_projectContainer import (PVRD_projectContainer,
                                   PVRD_rectData,
                                   PVRD_lineData,
                                   PVRD_ParTimeData
                                   )

from .Database import (Database, PVRD_speciesPropData, PVRD_reactionPropData)

from .NumericalEngine import NumericalEngine
import numpy as np
#import scipy.io
import scipy.constants
from .solutionBrowser import SolutionBrowser
from pathlib import Path
from .generalFunctions import getIndCarriers

from .PVRD_ModeWidgets import (
        PVRD_Mode0_Widget, PVRD_Mode1_Widget, PVRD_Mode2_Widget, PVRD_Mode3_Widget,
        PVRD_Mode4_Widget, PVRD_Mode5_Widget, PVRD_Mode6_Widget, PVRD_Mode7_Widget
        )

__version__=0.1
__MAGIC_NUMBER__ = 0x415355
__FILE_VERSION__ = 100

class PVRD_ProjectWidget(QWidget):
    NextId = 1
    def __init__(self,nDims=None,mainWindow=None,fileName=None,parent=None):
        super(PVRD_ProjectWidget,self).__init__(parent)
        
        self.numEng=NumericalEngine()
#        self.SB=SolutionBrowser(self)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.fileName=fileName
        if self.fileName is None:
            self.fileName = "New Project {0}".format(PVRD_ProjectWidget.NextId)
            PVRD_ProjectWidget.NextId +=1
            self.setModified(True)
        
        self.mainWindow=mainWindow
        self.hdf5_fileName=""
        self.updateStatus("Created {0}D Project".format(nDims))        
        
        self.pC = PVRD_projectContainer()
        
        if nDims is not None:
            self.pC.nDims=nDims
        else:
            self.pC.nDims=0
            
        self.pC.mode=0
        self.createToolBar()
        self.stackWidget=QStackedWidget()
        
        
        self.mode0_widget=PVRD_Mode0_Widget(projWindow=self)
        self.mode1_widget=PVRD_Mode1_Widget(projWindow=self)
        self.mode2_widget=PVRD_Mode2_Widget(projWindow=self)
        self.mode3_widget=PVRD_Mode3_Widget(projWindow=self)
        self.mode4_widget=PVRD_Mode4_Widget(projWindow=self)
        self.mode5_widget=PVRD_Mode5_Widget(projWindow=self)
        self.mode6_widget=PVRD_Mode6_Widget(projWindow=self)
        self.mode7_widget=PVRD_Mode7_Widget(projWindow=self)
        
        
        self.stackWidget.addWidget(self.mode0_widget)
        self.stackWidget.addWidget(self.mode1_widget)
        self.stackWidget.addWidget(self.mode2_widget)
        self.stackWidget.addWidget(self.mode3_widget)
        self.stackWidget.addWidget(self.mode4_widget)
        self.stackWidget.addWidget(self.mode5_widget)
        self.stackWidget.addWidget(self.mode6_widget)
        self.stackWidget.addWidget(self.mode7_widget)
        
        vLayout=QVBoxLayout()
        vLayout.addWidget(self.toolBar)
        vLayout.addWidget(self.stackWidget)
#        vLayout.addStretch()
        self.setLayout(vLayout)
        
        self.updateWidget()
        
    def closeEvent(self,event):
        if (self.isModified() and 
            QMessageBox.question(self,
                "Project has Unsaved Changes",
                "Save unsaved changes in {0}?".format(self.fileName),
                QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.Yes):
                try:
                    self.save()
                except (IOError, OSError) as err:
                    QMessageBox.warning(self,
                        "Text Editor -- Save Error",
                        "Failed to save {0}: {1}".format(self.filename, err))
        
    def createToolBar(self):
        self.toolBar=QToolBar('ProjectWidget_ToolBar')
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolBar.dbAction=self.createTBAction(":/images/1dbImg.jpg",
                                     "DB",
                                     "Loads Material Database",
                                     "Loads Material Database",
                                     True,
                                     self.setUpDB)
        self.toolBar.addAction(self.toolBar.dbAction)
        
        self.toolBar.geoAction=self.createTBAction(":/images/2Dstruct.png",
                                     "Geo",
                                     "Create/Update Geometry",
                                     "Create/Update Geometry",
                                     False,
                                     self.setUpGeometry)
        self.toolBar.addAction(self.toolBar.geoAction)
        
        self.toolBar.dcsAction=self.createTBAction(":/images/DCS.jpg",
                                     "DCS",
                                     "Defect Chemistry Specification",
                                     "Defect Chemistry Specification",
                                     False,
                                     self.setDCS)
        self.toolBar.addAction(self.toolBar.dcsAction)
        
        self.toolBar.dcmsAction=self.createTBAction(":/images/DCS.jpg",
                                     "DCSM",
                                     "Defect Chemistry Model Specification",
                                     "Defect Chemistry Model Specification",
                                     False,
                                     self.setDCMS)
        self.toolBar.addAction(self.toolBar.dcmsAction)
        
#        self.toolBar.simICBCAction=self.createTBAction(":/images/sim.jpg",
#                                     "Sim(IC & BC)",
#                                     "Simulation Initial and Boundary Condition Specification",
#                                     "Simulation Initial and Boundary Condition Specification",
#                                     False,
#                                     self.setSimICBC)
#        self.toolBar.addAction(self.toolBar.simICBCAction)

        self.toolBar.simAction=self.createTBAction(":/images/sim.jpg",
                                     "Sim",
                                     "Simulation Specification",
                                     "Simulation Specification",
                                     False,
                                     self.setSim)
        self.toolBar.addAction(self.toolBar.simAction)
        
        self.toolBar.meshAction=self.createTBAction(":/images/mesh.png",
                                     "Mesh",
                                     "Generates Mesh",
                                     "Generates Mesh",
                                     False,
                                     self.setMesh)
        self.toolBar.addAction(self.toolBar.meshAction)
        
        self.toolBar.runAction=self.createTBAction(":/images/run.jpg",
                                     "Run",
                                     "Run Simulation",
                                     "Run Simulation",
                                     False,
                                     self.runSim)
        self.toolBar.addAction(self.toolBar.runAction)
        
        self.toolBar.resultsAction=self.createTBAction("./images/results.png",
                                     "Results",
                                     "Show Simulation Results",
                                     "Show Simulation Results",
                                     False,
                                     self.startRB)
        self.toolBar.addAction(self.toolBar.resultsAction)
        
    def createTBAction(self,iconImageName,tbName,statusTip,
                                     toolTip,isEnabled,slotName):
        qa=QAction(QIcon(iconImageName),tbName,self)
        if statusTip is not None:
            qa.setStatusTip(statusTip)
        if toolTip is not None:
            qa.setToolTip(toolTip)
        qa.setEnabled(isEnabled)
        if slotName is not None:
            qa.triggered.connect(slotName)
        return qa
    
    def setUpDB(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                        "Open Database", "",
                        "Database Files (*.db);;All Files (*)", 
                        options=options)
        if fileName and self.pC.dbFname is None:
            self.pC.dbFname=fileName
            self.pC.db=Database(fileName=fileName)
            self.mode0_widget.updateDisplay()
#            self.mode0_widget.pb.setEnabled(True)
            if self.pC.mode==0:
                self.pC.mode=1
            self.setModified(True)
            message = "Loaded {0} material database".format(os.path.basename(fileName))
            self.updateStatus(message)
            self.toolBar.geoAction.setEnabled(True)
            self.mode1_widget.topBar.boundaryAction.setEnabled(True)
            self.mode1_widget.topBar.materialAction.setEnabled(False)
            self.mode1_widget.topBar.gBoundaryAction.setEnabled(False)
#            self.mode1_widget.mode1_widget.updateLayout()
            self.mode1_widget.mode0_widget.updateLayout()
            
            self.mode2_widget.updateWidget()
            
        elif fileName and fileName != self.pC.dbFname:
#            QMessageBox.about(self,"Warning","Still Developing")
            QMessageBox.about(self,"Warning","Are you Sure to Overwriting the database?")
            QMessageBox.about(self,"Warning","The feature is not yet developed")
        else:
#            QMessageBox.about(self,"Warning","Still Developing")
            QMessageBox.about(self,"Warning","DataBase is same a previous")
#        QMessageBox.about(self,"Under Development","Under Development")
        
    def setUpGeometry(self):
        self.updateWidget()
#        QMessageBox.about(self,"Under Development","Under Development")
        
    def setDCS(self):
        self.updateWidget()
#        QMessageBox.about(self,"Under Development","Under Development")
        
    def setDCMS(self):
        self.updateWidget(3)
        self.mode3_widget.updateWidget()
        
#    def setSimICBC(self):
#        QMessageBox.about(self,"Under Development","Under Development")
#        self.updateWidget()
#        self.mode4_widget.updateWidget()
        
    def setSim(self):
#        print('pCMode={0}'.format(self.pC.mode))
        if self.pC.mode>=3:
            self.updateWidget(4)
            if self.pC.mode==4:
                self.mode4_widget.mode0_widget.updateWidget()
#            self.mode4_widget.mode0_widget.updateWidgetDialog()
#        QMessageBox.about(self,"Under Development","Under Development")
        
    def setMesh(self):
#        QMessageBox.about(self,"Under Development","Under Development")
        self.updateWidget()
        self.mode5_widget.updateWidget()
        
    
    
    def runSim(self):
        self.updateWidget()
#        QMessageBox.about(self,"Under Development","Under Development")
        
    def startRB(self):
        self.updateWidget(7)
        
    def updateStatus(self,msg):
        self.mainWindow.statusBar().showMessage(msg, 5000)
        if self.isModified():
            self.setWindowTitle(os.path.basename(self.fileName)+" * ")
        else:
            self.setWindowTitle(os.path.basename(self.fileName))
#        QMessageBox.about(self,"Under Development","Update Status not implemented")
        
        
    def setModified(self,val):
        self.modified=val
        
    def isModified(self):
        return self.modified
    
    def save(self):
        if self.fileName.startswith("New Project"):
            fileName,_ = QFileDialog.getSaveFileName(self,
                        "Project -- Save As",self.fileName,
                        "PVRD Project Data files (*.ppd)")
            if fileName is None:
                return
            if "." not in fileName:
                fileName += ".ppd"
            self.fileName=fileName
            
        if self.pC.nDims >=0:
            fh = None
            fh = QFile(self.fileName)
            openVal = fh.open(QIODevice.WriteOnly)
            print("openVal={0}".format(openVal))
            if not openVal:
                print('error in opening File for writing')
            else:
                stream = QDataStream(fh)
                stream.writeInt32(__MAGIC_NUMBER__)
                stream.writeInt32(__FILE_VERSION__)
                stream.setVersion(QDataStream.Qt_5_6)
                
                stream.writeQString(self.fileName)
                stream.writeDouble(self.pC.nDims)
                stream.writeDouble(self.pC.mode)
                
                if self.pC.mode > 0:
#                    baseName=os.path.basename(self.pC.dbFname)
                    baseName=self.pC.dbFname
#                    dirName=os.path.dirname(__file__)
                    stream.writeQString(baseName)
                if self.pC.geoMode >= 0:
                    stream.writeDouble(self.pC.geoMode)
                    stream.writeBool(self.mode1_widget.mode0_widget.isBoundaryDone)
                    if self.mode1_widget.mode0_widget.isBoundaryDone:
                        stream.writeDouble(self.pC.boundaryX0)
                        stream.writeDouble(self.pC.boundaryY0)
                        stream.writeDouble(self.pC.boundaryWidth)
                        stream.writeDouble(self.pC.boundaryHeight)
                
                if self.pC.geoMode >=1:
                    stream.writeDouble(len(self.pC.matRectList))
                    for matRect in self.pC.matRectList:
                        stream.writeDouble(matRect.X0)
                        stream.writeDouble(matRect.Y0)
                        stream.writeDouble(matRect.W)
                        stream.writeDouble(matRect.H)
                        stream.writeQString(matRect.matName)
#                    stream.writeBool(self.mode1_widget.mode1_widget.isMaterialDone)
                        
                if self.pC.geoMode >=2:
                    stream.writeDouble(len(self.pC.autoGBLineList))
                    for line in self.pC.autoGBLineList:
                        stream.writeDouble(line.x1)
                        stream.writeDouble(line.y1)
                        stream.writeDouble(line.x2)
                        stream.writeDouble(line.y2)
                        stream.writeQString(line.matName)
                    stream.writeDouble(len(self.pC.interfaceLineList))
                    for line in self.pC.interfaceLineList:
                        stream.writeDouble(line.x1)
                        stream.writeDouble(line.y1)
                        stream.writeDouble(line.x2)
                        stream.writeDouble(line.y2)
                        stream.writeQString(line.matName)
                    stream.writeDouble(len(self.pC.GBLineList))
                    for line in self.pC.GBLineList:
                        stream.writeDouble(line.x1)
                        stream.writeDouble(line.y1)
                        stream.writeDouble(line.x2)
                        stream.writeDouble(line.y2)
                        stream.writeQString(line.matName)
                        
                    stream.writeBool(self.mode1_widget.mode2_widget.isGBoundaryDone)
                    
                if self.pC.mode > 1:
                    stream.writeDouble(len(self.pC.allRectList))
                    for item in self.pC.allRectList:
                        stream.writeDouble(len(item.mechList))
                        for mech in item.mechList:
                            stream.writeQString(mech)
                        stream.writeDouble(len(item.reactionList))
                        for reaction in item.reactionList:
                            stream.writeQString(reaction)
                        stream.writeDouble(len(item.speciesList))
                        for species in item.speciesList:
                            stream.writeQString(species)
                            
                    stream.writeDouble(len(self.pC.allLineList))
                    for item in self.pC.allLineList:
                        stream.writeDouble(len(item.mechList))
                        for mech in item.mechList:
                            stream.writeQString(mech)
                        stream.writeDouble(len(item.reactionList))
                        for reaction in item.reactionList:
                            stream.writeQString(reaction)
                        stream.writeDouble(len(item.speciesList))
                        for species in item.speciesList:
                            stream.writeQString(species)
                            
                    stream.writeDouble(len(self.pC.allPointList))
                    for item in self.pC.allPointList:
                        stream.writeDouble(len(item.mechList))
                        for mech in item.mechList:
                            stream.writeQString(mech)
                        stream.writeDouble(len(item.reactionList))
                        for reaction in item.reactionList:
                            stream.writeQString(reaction)
                        stream.writeDouble(len(item.speciesList))
                        for species in item.speciesList:
                            stream.writeQString(species)
                
#                print("Writing for mode 3 (DCSM) _1")
                
                if self.pC.mode > 2:
#                    print("Writing for mode 3 (DCSM)")
                    stream.writeDouble(len(self.pC.allRectList))
                    for item in self.pC.allRectList:
                        stream.writeDouble(item.matPropData.cationChemPot)
                        stream.writeDouble(item.matPropData.cationVacancy)
                        stream.writeDouble(item.matPropData.anionVacancy)
                        stream.writeDouble(item.matPropData.eEffMass)
                        stream.writeDouble(item.matPropData.hEffMass)
                        stream.writeDouble(item.matPropData.latDen)
                        stream.writeDouble(item.matPropData.elecAff)
                        stream.writeDouble(item.matPropData.dielecConst)
                        stream.writeDouble(item.matPropData.radRateConst)
                        stream.writeQString(item.matPropData.bgModelName)
                        stream.writeQString(item.matPropData.bgPar)
                        stream.writeQString(item.matPropData.eMobName)
                        stream.writeQString(item.matPropData.eMobPar)
                        stream.writeQString(item.matPropData.hMobName)
                        stream.writeQString(item.matPropData.hMobPar)
                        
                        stream.writeDouble(len(item.speciesPropDataList))
                        for speciesProp in item.speciesPropDataList:
                            stream.writeDouble(speciesProp.cationLoss)
                            stream.writeDouble(speciesProp.anionLoss)
                            stream.writeQString(speciesProp.diffModel)
                            stream.writeQString(speciesProp.diffParList)
                            stream.writeQString(speciesProp.siteDenModel)
                            stream.writeQString(speciesProp.siteDenParList)
                            stream.writeQString(speciesProp.formEnergyModel)
                            stream.writeQString(speciesProp.formEnergyParList)
                            stream.writeDouble(speciesProp.q)
                            stream.writeBool(speciesProp.elemCountLit is not None)
                            if speciesProp.elemCountLit is not None:
                                stream.writeQString(speciesProp.elemCountLit)
                        
                        stream.writeDouble(len(item.reactionPropDataList))
                        for reactionProp in item.reactionPropDataList:
                            stream.writeQString(reactionProp.rateModel)
                            stream.writeQString(reactionProp.rateParList)
                            stream.writeDouble(reactionProp.limitingSide)
                            stream.writeDouble(len(reactionProp.LHS))
                            for lhs in reactionProp.LHS:
                                stream.writeQString(lhs)
                            stream.writeDouble(len(reactionProp.RHS))
                            for rhs in reactionProp.RHS:
                                stream.writeQString(rhs)
                    
                    stream.writeDouble(len(self.pC.allLineList))
                    for item in self.pC.allLineList:
                        stream.writeDouble(item.matPropData.cationChemPot)
                        stream.writeDouble(item.matPropData.cationVacancy)
                        stream.writeDouble(item.matPropData.anionVacancy)
                        stream.writeDouble(item.matPropData.eEffMass)
                        stream.writeDouble(item.matPropData.hEffMass)
                        stream.writeDouble(item.matPropData.latDen)
                        stream.writeDouble(item.matPropData.elecAff)
                        stream.writeDouble(item.matPropData.dielecConst)
                        stream.writeDouble(item.matPropData.radRateConst)
                        stream.writeQString(item.matPropData.bgModelName)
                        stream.writeQString(item.matPropData.bgPar)
                        stream.writeQString(item.matPropData.eMobName)
                        stream.writeQString(item.matPropData.eMobPar)
                        stream.writeQString(item.matPropData.hMobName)
                        stream.writeQString(item.matPropData.hMobPar)
                        
                        stream.writeDouble(len(item.speciesPropDataList))
                        for speciesProp in item.speciesPropDataList:
                            stream.writeDouble(speciesProp.cationLoss)
                            stream.writeDouble(speciesProp.anionLoss)
                            stream.writeQString(speciesProp.diffModel)
                            stream.writeQString(speciesProp.diffParList)
                            stream.writeQString(speciesProp.siteDenModel)
                            stream.writeQString(speciesProp.siteDenParList)
                            stream.writeQString(speciesProp.formEnergyModel)
                            stream.writeQString(speciesProp.formEnergyParList)
                            stream.writeDouble(speciesProp.q)
                            stream.writeBool(speciesProp.elemCountLit is not None)
                            if speciesProp.elemCountLit is not None:
                                stream.writeQString(speciesProp.elemCountLit)
                        
                        stream.writeDouble(len(item.reactionPropDataList))
                        for reactionProp in item.reactionPropDataList:
                            stream.writeQString(reactionProp.rateModel)
                            stream.writeQString(reactionProp.rateParList)
                            stream.writeDouble(reactionProp.limitingSide)
                            stream.writeDouble(len(reactionProp.LHS))
                            for lhs in reactionProp.LHS:
                                stream.writeQString(lhs)
                            stream.writeDouble(len(reactionProp.RHS))
                            for rhs in reactionProp.RHS:
                                stream.writeQString(rhs)
                  
                    stream.writeDouble(len(self.pC.allPointList))
                    for item in self.pC.allPointList:
                        stream.writeDouble(item.matPropData.cationChemPot)
                        stream.writeDouble(item.matPropData.cationVacancy)
                        stream.writeDouble(item.matPropData.anionVacancy)
                        stream.writeDouble(item.matPropData.eEffMass)
                        stream.writeDouble(item.matPropData.hEffMass)
                        stream.writeDouble(item.matPropData.latDen)
                        stream.writeDouble(item.matPropData.elecAff)
                        stream.writeDouble(item.matPropData.dielecConst)
                        stream.writeDouble(item.matPropData.radRateConst)
                        stream.writeQString(item.matPropData.bgModelName)
                        stream.writeQString(item.matPropData.bgPar)
                        stream.writeQString(item.matPropData.eMobName)
                        stream.writeQString(item.matPropData.eMobPar)
                        stream.writeQString(item.matPropData.hMobName)
                        stream.writeQString(item.matPropData.hMobPar)
                        
                        stream.writeDouble(len(item.speciesPropDataList))
                        for speciesProp in item.speciesPropDataList:
                            stream.writeDouble(speciesProp.cationLoss)
                            stream.writeDouble(speciesProp.anionLoss)
                            stream.writeQString(speciesProp.diffModel)
                            stream.writeQString(speciesProp.diffParList)
                            stream.writeQString(speciesProp.siteDenModel)
                            stream.writeQString(speciesProp.siteDenParList)
                            stream.writeQString(speciesProp.formEnergyModel)
                            stream.writeQString(speciesProp.formEnergyParList)
                            stream.writeDouble(speciesProp.q)
                            stream.writeBool(speciesProp.elemCountLit is not None)
                            if speciesProp.elemCountLit is not None:
                                stream.writeQString(speciesProp.elemCountLit)
                        
                        stream.writeDouble(len(item.reactionPropDataList))
                        for reactionProp in item.reactionPropDataList:
                            stream.writeQString(reactionProp.rateModel)
                            stream.writeQString(reactionProp.rateParList)
                            stream.writeDouble(reactionProp.limitingSide)
                            stream.writeDouble(len(reactionProp.LHS))
                            for lhs in reactionProp.LHS:
                                stream.writeQString(lhs)
                            stream.writeDouble(len(reactionProp.RHS))
                            for rhs in reactionProp.RHS:
                                stream.writeQString(rhs)
                    
                if self.pC.mode > 3:
                    stream.writeDouble(len(self.pC.allRectList))
                    for item in self.pC.allRectList:
                        stream.writeDouble(item.IC.typeVal)
                        stream.writeDouble(len(item.speciesList))
                        ii=0
                        for species in item.speciesList:
                            stream.writeDouble(len(item.IC.icDataList[ii][0]))
                            jj=0
                            for data in item.IC.icDataList[ii][0]:
                                stream.writeDouble(item.IC.icDataList[ii][0][jj])
                                stream.writeDouble(item.IC.icDataList[ii][1][jj])
                                stream.writeDouble(item.IC.icDataList[ii][2][jj])
                                jj=jj+1
                            ii=ii+1
                        stream.writeDouble(len(item.IC.isFirst))
                        for val in item.IC.isFirst:
                            stream.writeBool(val)
                        stream.writeDouble(len(item.IC.potentialData[0]))
                        ii=0
                        for data in item.IC.potentialData[0]:
                            stream.writeDouble(item.IC.potentialData[0][ii])
                            stream.writeDouble(item.IC.potentialData[1][ii])
                            stream.writeDouble(item.IC.potentialData[2][ii])
                            ii=ii+1
                        stream.writeBool(item.IC.isFirstPotential)
                        
                        stream.writeBool(item.isBoundary)
                        if item.isBoundary:
                            stream.writeDouble(item.BC.typeVal)
                            stream.writeDouble(len(item.speciesList))
                            ii=0
                            for species in item.speciesList:
                                stream.writeDouble(len(item.BC.bcDataList[ii][0]))
                                jj=0
                                for data in item.BC.bcDataList[ii][0]:
                                    stream.writeDouble(item.BC.bcDataList[ii][0][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][1][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][2][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][3][jj])
                                    jj=jj+1
                                ii=ii+1
                            stream.writeDouble(len(item.BC.isFirst))
                            for val in item.BC.isFirst:
                                stream.writeBool(val)
                            stream.writeDouble(len(item.BC.potentialData[0]))
                            ii=0
                            for data in item.BC.potentialData[0]:
                                stream.writeDouble(item.BC.potentialData[0][ii])
                                stream.writeDouble(item.BC.potentialData[1][ii])
                                stream.writeDouble(item.BC.potentialData[2][ii])
                                stream.writeDouble(item.BC.potentialData[3][ii])
                                ii=ii+1
                            stream.writeBool(item.BC.isFirstPotential)
                    
                    stream.writeDouble(len(self.pC.allLineList))
                    for item in self.pC.allLineList:
                        stream.writeDouble(item.IC.typeVal)
                        stream.writeDouble(len(item.speciesList))
                        ii=0
                        for species in item.speciesList:
                            stream.writeDouble(len(item.IC.icDataList[ii][0]))
                            jj=0
                            for data in item.IC.icDataList[ii][0]:
                                stream.writeDouble(item.IC.icDataList[ii][0][jj])
                                stream.writeDouble(item.IC.icDataList[ii][1][jj])
                                stream.writeDouble(item.IC.icDataList[ii][2][jj])
                                jj=jj+1
                            ii=ii+1
                        stream.writeDouble(len(item.IC.isFirst))
                        for val in item.IC.isFirst:
                            stream.writeBool(val)
                        stream.writeDouble(len(item.IC.potentialData[0]))
                        ii=0
                        for data in item.IC.potentialData[0]:
                            stream.writeDouble(item.IC.potentialData[0][ii])
                            stream.writeDouble(item.IC.potentialData[1][ii])
                            stream.writeDouble(item.IC.potentialData[2][ii])
                            ii=ii+1
                        stream.writeBool(item.IC.isFirstPotential)
                        
                        stream.writeBool(item.isBoundary)
                        if item.isBoundary:
                            stream.writeDouble(item.BC.typeVal)
                            stream.writeDouble(len(item.speciesList))
                            ii=0
                            for species in item.speciesList:
                                stream.writeDouble(len(item.BC.bcDataList[ii][0]))
                                jj=0
                                for data in item.BC.bcDataList[ii][0]:
                                    stream.writeDouble(item.BC.bcDataList[ii][0][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][1][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][2][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][3][jj])
                                    jj=jj+1
                                ii=ii+1
                            stream.writeDouble(len(item.BC.isFirst))
                            for val in item.BC.isFirst:
                                stream.writeBool(val)
                            stream.writeDouble(len(item.BC.potentialData[0]))
                            ii=0
                            for data in item.BC.potentialData[0]:
                                stream.writeDouble(item.BC.potentialData[0][ii])
                                stream.writeDouble(item.BC.potentialData[1][ii])
                                stream.writeDouble(item.BC.potentialData[2][ii])
                                stream.writeDouble(item.BC.potentialData[3][ii])
                                ii=ii+1
                            stream.writeBool(item.BC.isFirstPotential)
                    
                    stream.writeDouble(len(self.pC.allPointList))
                    for item in self.pC.allPointList:
                        stream.writeDouble(item.IC.typeVal)
                        stream.writeDouble(len(item.speciesList))
                        ii=0
                        for species in item.speciesList:
                            stream.writeDouble(len(item.IC.icDataList[ii][0]))
                            jj=0
                            for data in item.IC.icDataList[ii][0]:
                                stream.writeDouble(item.IC.icDataList[ii][0][jj])
                                stream.writeDouble(item.IC.icDataList[ii][1][jj])
                                stream.writeDouble(item.IC.icDataList[ii][2][jj])
                                jj=jj+1
                            ii=ii+1
                        stream.writeDouble(len(item.IC.isFirst))
                        for val in item.IC.isFirst:
                            stream.writeBool(val)
                        stream.writeDouble(len(item.IC.potentialData[0]))
                        ii=0
                        for data in item.IC.potentialData[0]:
                            stream.writeDouble(item.IC.potentialData[0][ii])
                            stream.writeDouble(item.IC.potentialData[1][ii])
                            stream.writeDouble(item.IC.potentialData[2][ii])
                            ii=ii+1
                        stream.writeBool(item.IC.isFirstPotential)
                        
                        stream.writeBool(item.isBoundary)
                        if item.isBoundary:
                            stream.writeDouble(item.BC.typeVal)
                            stream.writeDouble(len(item.speciesList))
                            ii=0
                            for species in item.speciesList:
                                stream.writeDouble(len(item.BC.bcDataList[ii][0]))
                                jj=0
                                for data in item.BC.bcDataList[ii][0]:
                                    stream.writeDouble(item.BC.bcDataList[ii][0][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][1][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][2][jj])
                                    stream.writeDouble(item.BC.bcDataList[ii][3][jj])
                                    jj=jj+1
                                ii=ii+1
                            stream.writeDouble(len(item.BC.isFirst))
                            for val in item.BC.isFirst:
                                stream.writeBool(val)
                            stream.writeDouble(len(item.BC.potentialData[0]))
                            ii=0
                            for data in item.BC.potentialData[0]:
                                stream.writeDouble(item.BC.potentialData[0][ii])
                                stream.writeDouble(item.BC.potentialData[1][ii])
                                stream.writeDouble(item.BC.potentialData[2][ii])
                                stream.writeDouble(item.BC.potentialData[3][ii])
                                ii=ii+1
                            stream.writeBool(item.BC.isFirstPotential)
                    
                    stream.writeDouble(len(self.pC.tempParList))
                    for tempPar in self.pC.tempParList:
                        stream.writeDouble(tempPar.typeVal)
                        stream.writeDouble(tempPar.startTimeVal)
                        stream.writeDouble(tempPar.endTimeVal)
                        stream.writeDouble(tempPar.startParVal)
                        stream.writeDouble(tempPar.endParVal)
                        stream.writeDouble(tempPar.nParVal)
                        if tempPar.typeVal==1:
                            stream.writeDouble(tempPar.cRate)
                        
                    stream.writeDouble(len(self.pC.lightParList))
                    for lightPar in self.pC.lightParList:
                        stream.writeDouble(lightPar.typeVal)
                        stream.writeDouble(lightPar.startTimeVal)
                        stream.writeDouble(lightPar.endTimeVal)
                        stream.writeDouble(lightPar.startParVal)
                        stream.writeDouble(lightPar.endParVal)
                        stream.writeDouble(lightPar.nParVal)
                        
                    stream.writeDouble(len(self.pC.biasParList))
                    for biasPar in self.pC.biasParList:
                        stream.writeDouble(biasPar.typeVal)
                        stream.writeDouble(biasPar.startTimeVal)
                        stream.writeDouble(biasPar.endTimeVal)
                        stream.writeDouble(biasPar.startParVal)
                        stream.writeDouble(biasPar.endParVal)
                        stream.writeDouble(biasPar.nParVal)
                        stream.writeBool(biasPar.isFloating)
                        
                if self.pC.mode > 4:
                    stream.writeDouble(len(self.pC.allRectList))
                    for item in self.pC.allRectList:
                        stream.writeDouble(item.nY)
                        stream.writeDouble(item.nYType)
                        stream.writeDouble(len(item.yMeshPointList))
                        for yMeshPoint in item.yMeshPointList:
                            stream.writeDouble(yMeshPoint)
                        stream.writeDouble(item.nX)
                        stream.writeDouble(item.nXType)
                        stream.writeDouble(len(item.xMeshPointList))
                        for xMeshPoint in item.xMeshPointList:
                            stream.writeDouble(xMeshPoint)
                    
        self.setModified(False)
        self.updateStatus("Saved the project '{0}'".format(os.path.basename(self.fileName)))
        fh.close()
        
    def load(self,fname=None):
        if fname is not None:
            self.fileName=fname
#            QMessageBox.about(self,"Warning","fName={0}".format(fname))
            fh=QFile(self.fileName)
            fh.open(QIODevice.ReadOnly)
            stream=QDataStream(fh)
            
            magic=stream.readInt32()
            if magic != __MAGIC_NUMBER__:
                QMessageBox.about(self,"Warning","Unrecognized file type")
#            QMessageBox.about(self,"Warning","magic={0}".format(magic))
            
            version=stream.readInt32()
            if version < __FILE_VERSION__:
                QMessageBox.about(self,"Warning","Old and unreadable file format")
            if version > __FILE_VERSION__:
                QMessageBox.about(self,"Warning","New and unreadable file format")
            
#            QMessageBox.about(self,"Warning","version={0}".format(version))
                
            stream.setVersion(QDataStream.Qt_5_6)
            
            if not stream.atEnd():
#                self.fileName=stream.readQString()
                fileName=stream.readQString()
                
#            QMessageBox.about(self,"Warning","selfFileName={0}".format(self.fileName))
                
            if not stream.atEnd():
                self.pC.nDims=stream.readDouble()
                self.pC.mode=stream.readDouble()
                pC_mode=self.pC.mode
                print("Read pc Mode is {0}".format(self.pC.mode))
                
            if not stream.atEnd() and self.pC.mode >0:
                basename=stream.readQString()
#                dirName=os.path.dirname(os.path.abspath(__file__))
#                self.pC.dbFname=dirName+os.path.sep+"Database"+os.path.sep+basename
#                print("dbFileName={0}".format(self.pC.dbFname))
                my_file = Path(basename)
                if my_file.is_file():
                    self.pC.dbFname=basename
                else:
                    QMessageBox.about(self,"Warning","file {0} not Found. Please select the correct db file manually".format(basename))
                    options = QFileDialog.Options()
                    options |= QFileDialog.DontUseNativeDialog
                    fileName, _ = QFileDialog.getOpenFileName(self,
                        "Open Database", "",
                        "Database Files (*.db);;All Files (*)", 
                        options=options)
                    self.pC.dbFname=fileName
                    
                self.pC.db=Database(fileName=self.pC.dbFname)
                
            if not stream.atEnd():
                self.pC.geoMode=stream.readDouble()
                self.mode1_widget.mode0_widget.isBoundaryDone=stream.readBool()
                self.toolBar.geoAction.setEnabled(True)
                self.mode1_widget.topBar.boundaryAction.setEnabled(True)
                self.mode1_widget.topBar.materialAction.setEnabled(False)
                self.mode1_widget.topBar.gBoundaryAction.setEnabled(False)
                self.updateWidget(1)
                if self.mode1_widget.mode0_widget.isBoundaryDone:
                    self.pC.boundaryX0=stream.readDouble()
                    self.pC.boundaryY0=stream.readDouble()
                    self.pC.boundaryWidth=stream.readDouble()
                    self.pC.boundaryHeight=stream.readDouble()
                    self.mode1_widget.topBar.materialAction.setEnabled(True)
                    self.mode1_widget.mode0_widget.updateLayout()
                    self.mode1_widget.mode0_widget.reDrawBoundary()
                
                if self.pC.geoMode >=1:
                    matLen=int(stream.readDouble())
                    for ii in range(matLen):
                        x0=stream.readDouble()
                        y0=stream.readDouble()
                        w=stream.readDouble()
                        h=stream.readDouble()
                        name=stream.readQString()
                        self.pC.matRectList.append(PVRD_rectData(x0,y0,w,h,name))
                    
                    self.mode1_widget.mode1_widget.reDrawMaterials()
                    self.mode1_widget.stackWidget.setCurrentIndex(1)
                    
                if self.pC.geoMode >=2:
                    self.mode1_widget.topBar.gBoundaryAction.setEnabled(True)
                    len_val=int(stream.readDouble())
                    for ii in range(len_val):
                        x1=stream.readDouble()
                        y1=stream.readDouble()
                        x2=stream.readDouble()
                        y2=stream.readDouble()
                        matName=stream.readQString()
                        line=PVRD_lineData(x1,y1,x2,y2,matName)
                        self.pC.autoGBLineList.append(line)
                    len_val=int(stream.readDouble())
                    for ii in range(len_val):
                        x1=stream.readDouble()
                        y1=stream.readDouble()
                        x2=stream.readDouble()
                        y2=stream.readDouble()
                        matName=stream.readQString()
                        line=PVRD_lineData(x1,y1,x2,y2,matName)
                        self.pC.interfaceLineList.append(line) 
                    len_val=int(stream.readDouble())
                    for ii in range(len_val):
                        x1=stream.readDouble()
                        y1=stream.readDouble()
                        x2=stream.readDouble()
                        y2=stream.readDouble()
                        matName=stream.readQString()
                        line=PVRD_lineData(x1,y1,x2,y2,matName)
                        self.pC.GBLineList.append(line)
                        
                    self.mode1_widget.mode2_widget.reDrawGB()
                    self.mode1_widget.stackWidget.setCurrentIndex(2)
                    
                    isGBDone=stream.readBool()
                    self.mode1_widget.mode2_widget.isGBoundaryDone=isGBDone
                    if isGBDone:
                        self.toolBar.dcsAction.setEnabled(True)
                        self.mode2_widget.updateWidget()
                        self.updateWidget(2)

            if not stream.atEnd() and self.pC.mode > 1:
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    len_val1=int(stream.readDouble())
                    mechList=list()
                    for jj in range(len_val1):
                        mechList.append(stream.readQString())
                    len_val1=int(stream.readDouble())
                    reactionList=list()
                    for jj in range(len_val1):
                        reactionList.append(stream.readQString())
                    len_val1=int(stream.readDouble())
                    speciesList=list()
                    for jj in range(len_val1):
                        speciesList.append(stream.readQString())
                    self.pC.allRectList[ii].mechList=mechList
                    self.pC.allRectList[ii].reactionList=reactionList
                    self.pC.allRectList[ii].speciesList=speciesList
                    
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    len_val1=int(stream.readDouble())
                    mechList=list()
                    for jj in range(len_val1):
                        mechList.append(stream.readQString())
                    len_val1=int(stream.readDouble())
                    reactionList=list()
                    for jj in range(len_val1):
                        reactionList.append(stream.readQString())
                    len_val1=int(stream.readDouble())
                    speciesList=list()
                    for jj in range(len_val1):
                        speciesList.append(stream.readQString())
                    self.pC.allLineList[ii].mechList=mechList
                    self.pC.allLineList[ii].reactionList=reactionList
                    self.pC.allLineList[ii].speciesList=speciesList
                    
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    len_val1=int(stream.readDouble())
                    mechList=list()
                    for jj in range(len_val1):
                        mechList.append(stream.readQString())
                    len_val1=int(stream.readDouble())
                    reactionList=list()
                    for jj in range(len_val1):
                        reactionList.append(stream.readQString())
                    len_val1=int(stream.readDouble())
                    speciesList=list()
                    for jj in range(len_val1):
                        speciesList.append(stream.readQString())
                    self.pC.allPointList[ii].mechList=mechList
                    self.pC.allPointList[ii].reactionList=reactionList
                    self.pC.allPointList[ii].speciesList=speciesList
                    
                self.mode2_widget.updateDialog()
                if self.pC.mode > 2:
                    self.toolBar.dcmsAction.setEnabled(True)
#            print('updating the widget to mode 3 _1')    
            if not stream.atEnd() and self.pC.mode > 2:
#                print('updating the widget to mode 3')
                self.updateWidget(3)
                self.mode3_widget.updateWidget()
                # for RectList
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    cationChemPot=stream.readDouble()
                    cationVacancy=stream.readDouble()
                    anionVacancy=stream.readDouble()
                    eEffMass=stream.readDouble()
                    hEffMass=stream.readDouble()
                    latDen=stream.readDouble()
                    elecAff=stream.readDouble()
                    dielecConst=stream.readDouble()
                    radRateConst=stream.readDouble()
                    bgModelName=stream.readQString()
                    bgPar=stream.readQString()
                    eMobName=stream.readQString()
                    eMobPar=stream.readQString()
                    hMobName=stream.readQString()
                    hMobPar=stream.readQString()
#                    formEnergy=stream.readQString()
                    self.pC.allRectList[ii].matPropData.update(eEffMass,hEffMass,
                                       latDen,elecAff,dielecConst,radRateConst,
                                       bgModelName,bgPar,eMobName,eMobPar,
                                       hMobName,hMobPar)
                    
                    len_val1=int(stream.readDouble())
                    speciesPropDataList=list()
                    for jj in range(len_val1):
                        cationLoss=stream.readDouble()
                        anionLoss=stream.readDouble()
                        diffModel=stream.readQString()
                        diffParList=stream.readQString()
                        siteDenModel=stream.readQString()
                        siteDenParList=stream.readQString()
                        formEnergyModel=stream.readQString()
                        formEnergyParList=stream.readQString()
                        if len(formEnergyParList)==0:
                            formEnergyParList=None
                        q=stream.readDouble()
                        isNotNone=stream.readBool()
                        elemCountLit=None
                        if isNotNone:
                            elemCountLit=stream.readQString()
                        speciesPropData=PVRD_speciesPropData()
#                        skip=False
#                        if isElectron(species) or isHole(species):
#                            skip=True
#                        if isCationAtCationSite(matProp.cation,species) or isAnionAtAnionSite(matProp.anion,species):
#                            skip=True
#                        if isReservior(species):
#                            skip=True
#                        if not skip:
#                            correction=self.getCorrectedPotential(matName,species,matProp.cationChemPot)
#                        else:
#                            correction=0
                        correction=0
                        speciesPropData.update(diffModel,diffParList,siteDenModel,siteDenParList,
                                               formEnergyModel,formEnergyParList,q,elemCountLit,
                                               self.pC.allRectList[ii].matPropData,
                                               correction)
#                        speciesPropData.cationLoss=cationLoss
#                        speciesPropData.anionLoss=anionLoss
                        speciesPropDataList.append(speciesPropData)
                    self.pC.allRectList[ii].updateSpeciesPropDataList(speciesPropDataList)
                    self.pC.allRectList[ii].matPropData.cationChemPot=cationChemPot
                    self.pC.allRectList[ii].matPropData.cationVacancy=cationVacancy
                    self.pC.allRectList[ii].matPropData.anionVacancy=anionVacancy
                    
                    len_val1=int(stream.readDouble())
                    reactionPropDataList=list()
                    for jj in range(len_val1):
                        rateModel=stream.readQString()
                        rateParList=stream.readQString()
                        limitingSide=int(stream.readDouble())
                        len_val2=int(stream.readDouble())
                        LHSlist=list()
                        for kk in range(len_val2):
                            lhs=stream.readQString()
                            LHSlist.append(lhs)
                        len_val2=int(stream.readDouble())
                        RHSlist=list()
                        for kk in range(len_val2):
                            rhs=stream.readQString()
                            RHSlist.append(rhs)
                        reactionPropData=PVRD_reactionPropData()
                        reactionPropData.update(rateModel,rateParList,limitingSide,LHSlist,RHSlist,
                                                self.pC.allRectList[ii].speciesList,
                                                self.pC.allRectList[ii].speciesPropDataList,
                                                self.pC.allRectList[ii].matPropData)
                        reactionPropDataList.append(reactionPropData)
                    self.pC.allRectList[ii].updateReactionPropDataList(reactionPropDataList)
                    
                # for LineList
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    cationChemPot=stream.readDouble()
                    cationVacancy=stream.readDouble()
                    anionVacancy=stream.readDouble()
                    eEffMass=stream.readDouble()
                    hEffMass=stream.readDouble()
                    latDen=stream.readDouble()
                    elecAff=stream.readDouble()
                    dielecConst=stream.readDouble()
                    radRateConst=stream.readDouble()
                    bgModelName=stream.readQString()
                    bgPar=stream.readQString()
                    eMobName=stream.readQString()
                    eMobPar=stream.readQString()
                    hMobName=stream.readQString()
                    hMobPar=stream.readQString()
                    self.pC.allLineList[ii].matPropData.update(eEffMass,hEffMass,
                                       latDen,elecAff,dielecConst,radRateConst,
                                       bgModelName,bgPar,eMobName,eMobPar,
                                       hMobName,hMobPar)
                    self.pC.allLineList[ii].matPropData.cationChemPot=cationChemPot
                    self.pC.allLineList[ii].matPropData.cationVacancy=cationVacancy
                    self.pC.allLineList[ii].matPropData.anionVacancy=anionVacancy
                    len_val1=int(stream.readDouble())
                    speciesPropDataList=list()
                    for jj in range(len_val1):
                        cationLoss=stream.readDouble()
                        anionLoss=stream.readDouble()
                        diffModel=stream.readQString()
                        diffParList=stream.readQString()
                        siteDenModel=stream.readQString()
                        siteDenParList=stream.readQString()
                        formEnergyModel=stream.readQString()
                        formEnergyParList=stream.readQString()
                        if len(formEnergyParList)==0:
                            formEnergyParList=None
                        q=stream.readDouble()
                        isNotNone=stream.readBool()
                        elemCountLit=None
                        if isNotNone:
                            elemCountLit=stream.readQString()
                        speciesPropData=PVRD_speciesPropData()
                        speciesPropData.update(diffModel,diffParList,siteDenModel,siteDenParList,
                                               formEnergyModel,formEnergyParList,q,elemCountLit,
                                               self.pC.allLineList[ii].matPropData,
                                               cationLoss,anionLoss)
                        speciesPropDataList.append(speciesPropData)
                    self.pC.allLineList[ii].updateSpeciesPropDataList(speciesPropDataList)
                    
                    len_val1=int(stream.readDouble())
                    reactionPropDataList=list()
                    for jj in range(len_val1):
                        rateModel=stream.readQString()
                        rateParList=stream.readQString()
                        limitingSide=int(stream.readDouble())
                        len_val2=int(stream.readDouble())
                        LHSlist=list()
                        for kk in range(len_val2):
                            lhs=stream.readQString()
                            LHSlist.append(lhs)
                        len_val2=int(stream.readDouble())
                        RHSlist=list()
                        for kk in range(len_val2):
                            rhs=stream.readQString()
                            RHSlist.append(rhs)
                        reactionPropData=PVRD_reactionPropData()
                        reactionPropData.update(rateModel,rateParList,limitingSide,LHSlist,RHSlist,
                                                self.pC.allLineList[ii].speciesList,
                                                self.pC.allLineList[ii].speciesPropDataList,
                                                self.pC.allLineList[ii].matPropData)
                        reactionPropDataList.append(reactionPropData)
                    self.pC.allLineList[ii].updateReactionPropDataList(reactionPropDataList)
                        
                # for PointList
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    cationChemPot=stream.readDouble()
                    cationVacancy=stream.readDouble()
                    anionVacancy=stream.readDouble()
                    eEffMass=stream.readDouble()
                    hEffMass=stream.readDouble()
                    latDen=stream.readDouble()
                    elecAff=stream.readDouble()
                    dielecConst=stream.readDouble()
                    radRateConst=stream.readDouble()
                    bgModelName=stream.readQString()
                    bgPar=stream.readQString()
                    eMobName=stream.readQString()
                    eMobPar=stream.readQString()
                    hMobName=stream.readQString()
                    hMobPar=stream.readQString()
                    self.pC.allPointList[ii].matPropData.update(eEffMass,hEffMass,
                                       latDen,elecAff,dielecConst,radRateConst,
                                       bgModelName,bgPar,eMobName,eMobPar,
                                       hMobName,hMobPar)
                    self.pC.allPointList[ii].matPropData.cationChemPot=cationChemPot
                    self.pC.allPointList[ii].matPropData.cationVacancy=cationVacancy
                    self.pC.allPointList[ii].matPropData.anionVacancy=anionVacancy
                    len_val1=int(stream.readDouble())
                    speciesPropDataList=list()
                    for jj in range(len_val1):
                        cationLoss=stream.readDouble()
                        anionLoss=stream.readDouble()
                        diffModel=stream.readQString()
                        diffParList=stream.readQString()
                        siteDenModel=stream.readQString()
                        siteDenParList=stream.readQString()
                        formEnergyModel=stream.readQString()
                        formEnergyParList=stream.readQString()
                        if len(formEnergyParList)==0:
                            formEnergyParList=None
                        q=stream.readDouble()
                        isNotNone=stream.readBool()
                        elemCountLit=None
                        if isNotNone:
                            elemCountLit=stream.readQString()
                        speciesPropData=PVRD_speciesPropData()
                        speciesPropData.update(diffModel,diffParList,siteDenModel,siteDenParList,
                                               formEnergyModel,formEnergyParList,q,elemCountLit,
                                               self.pC.allPointList[ii].matPropData,
                                               cationLoss,anionLoss)
                        speciesPropDataList.append(speciesPropData)
                    self.pC.allPointList[ii].updateSpeciesPropDataList(speciesPropDataList)
                    
                    len_val1=int(stream.readDouble())
                    reactionPropDataList=list()
                    for jj in range(len_val1):
                        rateModel=stream.readQString()
                        rateParList=stream.readQString()
                        limitingSide=int(stream.readDouble())
                        len_val2=int(stream.readDouble())
                        LHSlist=list()
                        for kk in range(len_val2):
                            lhs=stream.readQString()
                            LHSlist.append(lhs)
                        len_val2=int(stream.readDouble())
                        RHSlist=list()
                        for kk in range(len_val2):
                            rhs=stream.readQString()
                            RHSlist.append(rhs)
                        reactionPropData=PVRD_reactionPropData()
                        reactionPropData.update(rateModel,rateParList,limitingSide,LHSlist,RHSlist,
                                                self.pC.allPointList[ii].speciesList,
                                                self.pC.allPointList[ii].speciesPropDataList,
                                                self.pC.allPointList[ii].matPropData)
                        reactionPropDataList.append(reactionPropData)
                    self.pC.allPointList[ii].updateReactionPropDataList(reactionPropDataList)

            self.mode3_widget.updateDialog()
            # somehow the above is changing self.pC.mode to 3
            self.pC.mode=pC_mode
            
            print("is stream at End ={0}, pCmode={1}".format(stream.atEnd(),self.pC.mode))
            if not stream.atEnd() and self.pC.mode > 3:
                self.updateWidget(4)
                self.toolBar.simAction.setEnabled(True)
                self.mode4_widget.mode0_widget.updateWidget()
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    typeVal=int(stream.readDouble())
                    len_val1=int(stream.readDouble())
                    listSp=list()
                    for jj in range(len_val1):
                        len_val2=int(stream.readDouble())
                        list0=list()
                        list1=list()
                        list2=list()
                        for kk in range(len_val2):
                            list0.append(stream.readDouble())
                            list1.append(stream.readDouble())
                            list2.append(stream.readDouble())
                        listSp.append([list0,list1,list2])
                    len_val1=int(stream.readDouble())
                    isFirstList=list()
                    for jj in range(len_val1):
                        isFirstList.append(stream.readBool())
                    len_val1=int(stream.readDouble())
                    list0=list()
                    list1=list()
                    list2=list()
                    for jj in range(len_val1):
                        list0.append(stream.readDouble())
                        list1.append(stream.readDouble())
                        list2.append(stream.readDouble())
                    potDataList=[list0,list1,list2]
                    isPotFirst=stream.readBool()
                    
                    self.pC.allRectList[ii].IC.typeVal=typeVal
                    self.pC.allRectList[ii].IC.icDataList=listSp
                    self.pC.allRectList[ii].IC.isFirst=isFirstList
                    self.pC.allRectList[ii].IC.potentialData=potDataList
                    self.pC.allRectList[ii].IC.isFirstPotential=isPotFirst
                    
                    isBoundary=stream.readBool()
                    if isBoundary:
                        typeVal=int(stream.readDouble())
                        len_val1=int(stream.readDouble())
                        listSp=list()
                        for jj in range(len_val1):
                            len_val2=int(stream.readDouble())
                            list0=list()
                            list1=list()
                            list2=list()
                            list3=list()
                            for kk in range(len_val2):
                                list0.append(stream.readDouble())
                                list1.append(stream.readDouble())
                                list2.append(stream.readDouble())
                                list3.append(stream.readDouble())
                            listSp.append([list0,list1,list2,list3])
                        len_val1=int(stream.readDouble())
                        isFirstList=list()
                        for jj in range(len_val1):
                            isFirstList.append(stream.readBool())
                        len_val1=int(stream.readDouble())
                        list0=list()
                        list1=list()
                        list2=list()
                        list3=list()
                        for jj in range(len_val1):
                            list0.append(stream.readDouble())
                            list1.append(stream.readDouble())
                            list2.append(stream.readDouble())
                            list3.append(stream.readDouble())
                        potDataList=[list0,list1,list2,list3]
                        isPotFirst=stream.readBool()
                        
                        self.pC.allRectList[ii].BC.typeVal=typeVal
                        self.pC.allRectList[ii].BC.bcDataList=listSp
                        self.pC.allRectList[ii].BC.isFirst=isFirstList
                        self.pC.allRectList[ii].BC.potentialData=potDataList
                        self.pC.allRectList[ii].BC.isFirstPotential=isPotFirst
                        
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    typeVal=int(stream.readDouble())
                    len_val1=int(stream.readDouble())
                    listSp=list()
                    for jj in range(len_val1):
                        len_val2=int(stream.readDouble())
                        list0=list()
                        list1=list()
                        list2=list()
                        for kk in range(len_val2):
                            list0.append(stream.readDouble())
                            list1.append(stream.readDouble())
                            list2.append(stream.readDouble())
                        listSp.append([list0,list1,list2])
                    len_val1=int(stream.readDouble())
                    isFirstList=list()
                    for jj in range(len_val1):
                        isFirstList.append(stream.readBool())
                    len_val1=int(stream.readDouble())
                    list0=list()
                    list1=list()
                    list2=list()
                    for jj in range(len_val1):
                        list0.append(stream.readDouble())
                        list1.append(stream.readDouble())
                        list2.append(stream.readDouble())
                    potDataList=[list0,list1,list2]
                    isPotFirst=stream.readBool()
                    
                    self.pC.allLineList[ii].IC.typeVal=typeVal
                    self.pC.allLineList[ii].IC.icDataList=listSp
                    self.pC.allLineList[ii].IC.isFirst=isFirstList
                    self.pC.allLineList[ii].IC.potentialData=potDataList
                    self.pC.allLineList[ii].IC.isFirstPotential=isPotFirst
                    
                    isBoundary=stream.readBool()
                    if isBoundary:
                        typeVal=int(stream.readDouble())
                        len_val1=int(stream.readDouble())
                        listSp=list()
                        for jj in range(len_val1):
                            len_val2=int(stream.readDouble())
                            list0=list()
                            list1=list()
                            list2=list()
                            list3=list()
                            for kk in range(len_val2):
                                list0.append(stream.readDouble())
                                list1.append(stream.readDouble())
                                list2.append(stream.readDouble())
                                list3.append(stream.readDouble())
                            listSp.append([list0,list1,list2,list3])
                        len_val1=int(stream.readDouble())
                        isFirstList=list()
                        for jj in range(len_val1):
                            isFirstList.append(stream.readBool())
                        len_val1=int(stream.readDouble())
                        list0=list()
                        list1=list()
                        list2=list()
                        list3=list()
                        for jj in range(len_val1):
                            list0.append(stream.readDouble())
                            list1.append(stream.readDouble())
                            list2.append(stream.readDouble())
                            list3.append(stream.readDouble())
                        potDataList=[list0,list1,list2,list3]
                        isPotFirst=stream.readBool()
                        
                        self.pC.allLineList[ii].BC.typeVal=typeVal
                        self.pC.allLineList[ii].BC.bcDataList=listSp
                        self.pC.allLineList[ii].BC.isFirst=isFirstList
                        self.pC.allLineList[ii].BC.potentialData=potDataList
                        self.pC.allLineList[ii].BC.isFirstPotential=isPotFirst
                        
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    typeVal=int(stream.readDouble())
                    len_val1=int(stream.readDouble())
                    listSp=list()
                    for jj in range(len_val1):
                        len_val2=int(stream.readDouble())
                        list0=list()
                        list1=list()
                        list2=list()
                        for kk in range(len_val2):
                            list0.append(stream.readDouble())
                            list1.append(stream.readDouble())
                            list2.append(stream.readDouble())
                        listSp.append([list0,list1,list2])
                    len_val1=int(stream.readDouble())
                    isFirstList=list()
                    for jj in range(len_val1):
                        isFirstList.append(stream.readBool())
                    len_val1=int(stream.readDouble())
                    list0=list()
                    list1=list()
                    list2=list()
                    for jj in range(len_val1):
                        list0.append(stream.readDouble())
                        list1.append(stream.readDouble())
                        list2.append(stream.readDouble())
                    potDataList=[list0,list1,list2]
                    isPotFirst=stream.readBool()
                    
                    self.pC.allPointList[ii].IC.typeVal=typeVal
                    self.pC.allPointList[ii].IC.icDataList=listSp
                    self.pC.allPointList[ii].IC.isFirst=isFirstList
                    self.pC.allPointList[ii].IC.potentialData=potDataList
                    self.pC.allPointList[ii].IC.isFirstPotential=isPotFirst
                    
                    isBoundary=stream.readBool()
                    if isBoundary:
                        typeVal=int(stream.readDouble())
                        len_val1=int(stream.readDouble())
                        listSp=list()
                        for jj in range(len_val1):
                            len_val2=int(stream.readDouble())
                            list0=list()
                            list1=list()
                            list2=list()
                            list3=list()
                            for kk in range(len_val2):
                                list0.append(stream.readDouble())
                                list1.append(stream.readDouble())
                                list2.append(stream.readDouble())
                                list3.append(stream.readDouble())
                            listSp.append([list0,list1,list2,list3])
                        len_val1=int(stream.readDouble())
                        isFirstList=list()
                        for jj in range(len_val1):
                            isFirstList.append(stream.readBool())
                        len_val1=int(stream.readDouble())
                        list0=list()
                        list1=list()
                        list2=list()
                        list3=list()
                        for jj in range(len_val1):
                            list0.append(stream.readDouble())
                            list1.append(stream.readDouble())
                            list2.append(stream.readDouble())
                            list3.append(stream.readDouble())
                        potDataList=[list0,list1,list2,list3]
                        isPotFirst=stream.readBool()
                        
                        self.pC.allPointList[ii].BC.typeVal=typeVal
                        self.pC.allPointList[ii].BC.bcDataList=listSp
                        self.pC.allPointList[ii].BC.isFirst=isFirstList
                        self.pC.allPointList[ii].BC.potentialData=potDataList
                        self.pC.allPointList[ii].BC.isFirstPotential=isPotFirst
                
                self.pC.tempParList=list()
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    typeVal=int(stream.readDouble())
                    sTVal=stream.readDouble()
                    eTVal=stream.readDouble()
                    sPVal=stream.readDouble()
                    ePVal=stream.readDouble()
                    nPVal=stream.readDouble()
                    if typeVal==1:
                        cRate=stream.readDouble()
                    else:
                        cRate=0.1
                    tempPar=PVRD_ParTimeData(typeVal=typeVal,
                            startTime=sTVal,
                            startPar=sPVal,
                            endTime=eTVal,
                            endPar=ePVal,
                            nParVal=nPVal,
                            cRate=cRate)
                    self.pC.tempParList.append(tempPar)
                
                self.pC.lightParList=list()
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    typeVal=int(stream.readDouble())
                    sTVal=stream.readDouble()
                    eTVal=stream.readDouble()
                    sPVal=stream.readDouble()
                    ePVal=stream.readDouble()
                    nPVal=stream.readDouble()
                    lightPar=PVRD_ParTimeData(typeVal=typeVal,
                            startTime=sTVal,
                            startPar=sPVal,
                            endTime=eTVal,
                            endPar=ePVal,
                            nParVal=nPVal)
                    self.pC.lightParList.append(lightPar)
                
                self.pC.biasParList=list()
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    typeVal=int(stream.readDouble())
                    sTVal=stream.readDouble()
                    eTVal=stream.readDouble()
                    sPVal=stream.readDouble()
                    ePVal=stream.readDouble()
                    nPVal=stream.readDouble()
                    isFloating=stream.readBool()
                    biasPar=PVRD_ParTimeData(typeVal=typeVal,
                            startTime=sTVal,
                            startPar=sPVal,
                            endTime=eTVal,
                            endPar=ePVal,
                            nParVal=nPVal,
                            isFloating=isFloating)
                    self.pC.biasParList.append(biasPar)
                        
                self.mode4_widget.mode0_widget.updateWidgetDialog()
                self.mode4_widget.mode1_widget.updateWidgetDialog()
                self.mode4_widget.mode2_widget.updateWidgetDialog()
                self.mode4_widget.mode3_widget.updateWidgetDialog()
                
            if not stream.atEnd() and self.pC.mode > 4:
                self.updateWidget(5)
                self.mode5_widget.updateWidget()
                self.toolBar.meshAction.setEnabled(True)
                len_val=int(stream.readDouble())
                for ii in range(len_val):
                    nY=int(stream.readDouble())
                    nYType=int(stream.readDouble())
                    yLen=int(stream.readDouble())
                    yMeshList=list()
                    for jj in range(yLen):
                        val=stream.readDouble()
                        yMeshList.append(val)
                    nX=int(stream.readDouble())
                    nXType=int(stream.readDouble())
                    xLen=int(stream.readDouble())
                    xMeshList=list()
                    for jj in range(xLen):
                        val=stream.readDouble()
                        xMeshList.append(val)
                    
                    self.pC.allRectList[ii].nY=nY
                    self.pC.allRectList[ii].nYType=nYType
                    self.pC.allRectList[ii].yMeshPointList=yMeshList
                    self.pC.allRectList[ii].nX=nX
                    self.pC.allRectList[ii].nXType=nXType
                    self.pC.allRectList[ii].xMeshPointList=xMeshList
                    
                self.mode5_widget.updateDialogProp()
            
            
            self.setModified(False)
            self.updateStatus("Successfully Loaded {0} Project".format(self.fileName))
            fh.close()
    
        
    def updateWidget(self,mode=None):
        if mode is not None and mode !=1:
            self.stackWidget.setCurrentIndex(mode)
        elif mode ==1:
            
            self.stackWidget.setCurrentIndex(mode)
        else:
            self.stackWidget.setCurrentIndex(self.pC.mode)
            
    def callNumEngwInputs(self):
#        QMessageBox.about(self,"Under Development","Run is not yet implemented")
        self.mode6_widget.outLog.write('Initializing...\n')
        
#        self.runThread=QThread()
        
        # set Data to Numerical Engine
#        self.pC.updateDataForNumEng()

        nDims,nX,nY,M,K,species,charge,reactions,X,Y=self.pC.getDimData()
        
        if not X:
            X=[1e-4]
            nX=1
        
        if not Y:
            Y=[1e-4]
            nY=1
        
        U0,fi0,LHS,RHS=self.pC.getMeshDataForNumEng()
        
        # Temporary
#        U0=np.zeros((M,1))
        
        nMesh=nX*nY
        
#        QMessageBox.about(self,"Under Development",
#                          "nDims={0}<br>".format(nDims)+
#                          "nX={0}<br>".format(nX)+
#                          "nY={0}<br>".format(nY)+
#                          "M={0}<br>".format(M)+
#                          "K={0}<br>".format(K)+
#                          "species={0}<br>".format(species)+
#                          "reactions={0}<br>".format(reactions)+
#                          "X={0}<br>".format(X)+
#                          "Y={0}<br>".format(Y[-1])+
#                          "charge={0}<br>".format(charge)+
#                          "U0={0}<br>".format(U0)+
#                          "fi0={0}<br>".format(fi0)+
#                          "LHS={0}<br>".format(LHS)+
#                          "RHS={0}<br>".format(RHS)
#                          )
#        QMessageBox.about(self,"Under Development","U0={0}<br>".format(U0))
        
#        timeDataList=self.pC.timeDataList
        
#        QMessageBox.about(self,"Testing","length of timeDataList={0}".format(len(timeDataList)))
        
#        for timeData in timeDataList:
#            QMessageBox.about(self,"Testing",
#                 "time={0}<br>".format(timeData.time)+
#                 "temp={0}<br>".format(timeData.temp)+
#                 "Kf={0}<br>".format(timeData.Kf)
#                 )
#            QMessageBox.about(self,"Testing","Kb={0}<br>".format(timeData.Kb))
#            QMessageBox.about(self,"Testing","D={0}<br>".format(timeData.D))
#            QMessageBox.about(self,"Testing","G={0}<br>".format(timeData.G))
#            QMessageBox.about(self,"Testing","Ns={0}<br>".format(timeData.Ns))
#            QMessageBox.about(self,"Testing","Eps={0}<br>".format(timeData.Eps))
#            QMessageBox.about(self,"Testing","TopA={0}<br>".format(timeData.TopA))
#            QMessageBox.about(self,"Testing","TopB={0}<br>".format(timeData.TopB))
#            QMessageBox.about(self,"Testing","TopC={0}<br>".format(timeData.TopC))
#            QMessageBox.about(self,"Testing","BotA={0}<br>".format(timeData.BottomA))
#            QMessageBox.about(self,"Testing","BotB={0}<br>".format(timeData.BottomB))
#            QMessageBox.about(self,"Testing","BotC={0}<br>".format(timeData.BottomC))
        X=np.reshape(X,(len(X),1))*1e-4 # Assuming GUI is always giving them in um
        Y=np.reshape(Y,(len(Y),1))*1e-4 # Assuming GUI is always giving them in um
        if not len(X)==1:
            dX_diff=np.diff(X,n=1,axis=0)
        else:
            dX_diff=np.array([])
            dX_diff=np.reshape(dX_diff,(0,1))
        dY_diff=np.diff(Y,n=1,axis=0)
#        print("dY_diff={0}".format(dY_diff))
#        QMessageBox.about(self,"Testing","dY_diff={0}<br>".format(dY_diff))
#        QMessageBox.about(self,"Testing","dY_diff[0]={0}<br>".format(dY_diff[0]))
        
        if nDims==2:
            dX1=np.vstack((dX_diff[0],dX_diff))
            dX2=np.vstack((dX_diff,dX_diff[-1]))
            
            dY1=np.vstack((dY_diff[0],dY_diff))
            dY2=np.vstack((dY_diff,dY_diff[-1]))
        elif nDims==1:
            dX1=0.5 #Units are in cms
            dX2=0.5 #Units are in cms
            dY1=np.vstack((dY_diff[0],dY_diff))
            dY2=np.vstack((dY_diff,dY_diff[-1]))
        
        if nDims:
            dX=(dX1+dX2)/2
            dY=(dY1+dY2)/2
            
        ############## setting to Num Engine Object ###########################
        
        self.mode6_widget.outLog.write('Setting the Data to Numerical Engine\n')
        
        self.numEng.is0D = (nDims==0)
        self.numEng.nDims= nDims
        self.numEng.nX = nX
        self.numEng.nY = nY
        self.numEng.M = M
        self.numEng.K = K
        self.numEng.iter_tol = 1e-3
        
        self.numEng.mGrid.nX = nX
        self.numEng.mGrid.nY = nY
        self.numEng.mGrid.X = X
        self.numEng.mGrid.Y = Y
        
        if nDims:
            self.numEng.mGrid.dX=np.transpose(dX)
            self.numEng.mGrid.dY=np.transpose(dY)
            self.numEng.mGrid.Hx=np.tile(dX,[1,self.numEng.mGrid.nY])
            self.numEng.mGrid.Hy=np.tile(self.numEng.mGrid.dY,[self.numEng.mGrid.nX,1])
            self.numEng.mGrid.hx=np.tile(dX_diff,[1,self.numEng.mGrid.nY])
            self.numEng.mGrid.hy=np.tile(np.transpose(dY_diff),[self.numEng.mGrid.nX,1])
            
        self.numEng.qVec=np.array(charge)
        self.numEng.Species=species
        
        eIndx,hIndx=getIndCarriers(species)
        self.numEng.eIndx=eIndx
        self.numEng.hIndx=hIndx
        
        self.numEng.U0=U0
        self.numEng.fi0=np.zeros((nMesh,1))
        self.numEng.Dop=np.zeros((nMesh,1))
        self.numEng.LHS=np.int32(LHS)
        self.numEng.RHS=np.int32(RHS)
        
#        self.numEng.fIO.write('\nU0\n')
#        np.savetxt(self.numEng.fIO,self.numEng.U0,fmt='%2.2e')
#        
#        self.numEng.fIO.write('\nLHS\n')
#        np.savetxt(self.numEng.fIO,self.numEng.LHS,fmt='%2.2e')
#        
#        self.numEng.fIO.write('\nRHS\n')
#        np.savetxt(self.numEng.fIO,self.numEng.RHS,fmt='%2.2e')
#        
#        self.numEng.fIO.write('\nD0\n')
#        np.savetxt(self.numEng.fIO,self.pC.timeDataList[0].D,fmt='%2.2e')
#        
#        self.numEng.fIO.write('\nG0\n')
#        np.savetxt(self.numEng.fIO,self.pC.timeDataList[0].G,fmt='%2.2e')
#        
#        self.numEng.fIO.write('\nNs\n')
#        np.savetxt(self.numEng.fIO,self.pC.timeDataList[0].Ns,fmt='%2.2e')
#        
#        self.numEng.fIO.write('\nKf\n')
#        np.savetxt(self.numEng.fIO,self.pC.timeDataList[0].Kf,fmt='%2.2e')
#        
#        self.numEng.fIO.write('\nKb\n')
#        np.savetxt(self.numEng.fIO,self.pC.timeDataList[0].Kb,fmt='%2.2e')
        
#        self.numEng.fIO.close()
#        exit()
        
        
        
        self.mode6_widget.outLog.write('Opening the Solution File\n')
        
        self.hdf5_fileName=str.replace(self.fileName,'.ppd','_sol.out')        
        print('HDF5 fileName={0}'.format(self.hdf5_fileName))
        self.hdf5_file=h5py.File(self.hdf5_fileName, 'a')
        baseName=os.path.basename(self.fileName)
        baseName=str.replace(baseName,'.ppd','')
        baseName1=baseName
        groups=list(self.hdf5_file.keys())
        if baseName not in groups:
            self.rootGrp=self.hdf5_file.create_group(baseName)
        else:
#            baseName="/"+baseName
            self.rootGrp=self.hdf5_file["/"+baseName]
            
        groupLinks=list(self.rootGrp.keys())
#        print('group Links={0}'.format(groupLinks))
        if 'latestRun' in groupLinks:
            del self.rootGrp['latestRun']
        
        timeStr=time.strftime('%Y%m%d_%H%M%S')
        runName='run_{0}'.format(timeStr)
        timeStruct=time.strptime(timeStr,'%Y%m%d_%H%M%S')
        
        self.runGrp=self.rootGrp.create_group(runName)
        self.rootGrp["latestRun"]=h5py.SoftLink('/'+baseName+'/'+runName)
        self.runGrp.attrs['title']='PyCDTS Simulation Run for the Project {0} on {1} at {2}'.format(
                baseName1,time.strftime('%d %B %Y',timeStruct),time.strftime('%H:%M:%S'))
        self.runGrp.attrs['timeStamp']=timeStr
        self.runGrp.attrs['version']=1.0
        
        self.runGrpInfo=self.runGrp.create_group('Info')
        self.runGrpSnapShot=self.runGrp.create_group('SnapShot')
        self.runGrpSol=self.runGrp.create_group('Solution')
        
        self.runGrpInfo.attrs['nX']=nX
        self.runGrpInfo.attrs['nY']=nY
        self.runGrpInfo.attrs['nMesh']=nMesh
        self.runGrpInfo.attrs['nDims']=nDims
        self.runGrpInfo.attrs['nSpecies']=M
        self.runGrpInfo.attrs['nReactions']=K
        self.runGrpInfo.attrs['eIndx']=eIndx
        self.runGrpInfo.attrs['hIndx']=hIndx
        
        dt = h5py.special_dtype(vlen=str) 
#        print('species Type={0}'.format(type(species)))
        
        self.runGrpInfo.create_dataset('X',data=X)
        self.runGrpInfo.create_dataset('X_um',data=X*1e4)
        self.runGrpInfo.create_dataset('Y',data=Y)
        self.runGrpInfo.create_dataset('Y_um',data=Y*1e4)
        
        self.runGrpInfo.create_dataset('dX',data=self.numEng.mGrid.dX)
        self.runGrpInfo.create_dataset('dX_um',data=self.numEng.mGrid.dX*1e4)
        self.runGrpInfo.create_dataset('dY',data=self.numEng.mGrid.dY)
        self.runGrpInfo.create_dataset('dY_um',data=self.numEng.mGrid.dY*1e4)
        
        self.runGrpInfo.create_dataset('Hx',data=self.numEng.mGrid.Hx)
        self.runGrpInfo.create_dataset('Hx_um',data=self.numEng.mGrid.Hx*1e4)
        self.runGrpInfo.create_dataset('Hy',data=self.numEng.mGrid.Hy)
        self.runGrpInfo.create_dataset('Hy_um',data=self.numEng.mGrid.Hy*1e4)
        
        self.runGrpInfo.create_dataset('hx',data=self.numEng.mGrid.hx)
        self.runGrpInfo.create_dataset('hx_um',data=self.numEng.mGrid.hx*1e4)
        self.runGrpInfo.create_dataset('hy',data=self.numEng.mGrid.hy)
        self.runGrpInfo.create_dataset('hy_um',data=self.numEng.mGrid.hy*1e4)
        
        self.runGrpInfo.create_dataset('initConc',data=self.numEng.U0)
        self.runGrpInfo.create_dataset('initFi',data=self.numEng.fi0)
        
        self.runGrpInfo.create_dataset('reaction_LHS',data=self.numEng.LHS)
        self.runGrpInfo.create_dataset('reaction_RHS',data=self.numEng.RHS)
        
        self.runGrpInfo.create_dataset('species',data=np.array(species,dtype=dt))
        self.runGrpInfo.create_dataset('reactions',data=np.array(reactions,dtype=dt))
        self.runGrpInfo.create_dataset('charge',data=np.array(self.numEng.qVec))
        
        self.dSet_Ns = self.runGrpSnapShot.create_dataset('Ns',(1,nX,nY,M),maxshape=(len(self.pC.timeDataList),nX,nY,M),dtype=np.double)
        self.dSet_G = self.runGrpSnapShot.create_dataset('G',(1,nX,nY,M),maxshape=(len(self.pC.timeDataList),nX,nY,M),dtype=np.double)
        self.dSet_D = self.runGrpSnapShot.create_dataset('D',(1,nX,nY,M),maxshape=(len(self.pC.timeDataList),nX,nY,M),dtype=np.double)
        self.dSet_Kf = self.runGrpSnapShot.create_dataset('Kf',(1,nX,nY,K),maxshape=(len(self.pC.timeDataList),nX,nY,K),dtype=np.double)
        self.dSet_Kb = self.runGrpSnapShot.create_dataset('Kb',(1,nX,nY,K),maxshape=(len(self.pC.timeDataList),nX,nY,K),dtype=np.double)
        self.dSet_FC_BC = self.runGrpSnapShot.create_dataset('FC_BC',(1,3,nX,M+1),maxshape=(len(self.pC.timeDataList),3,nX,M+1),dtype=np.double)
        self.dSet_BC_BC = self.runGrpSnapShot.create_dataset('BC_BC',(1,3,nX,M+1),maxshape=(len(self.pC.timeDataList),3,nX,M+1),dtype=np.double)
        self.dSet_Eps = self.runGrpSnapShot.create_dataset('Eps',(1,nX,nY),maxshape=(len(self.pC.timeDataList),nX,nY),dtype=np.double)
        self.dSet_iConc = self.runGrpSnapShot.create_dataset('initConc',(1,nX,nY,M),maxshape=(len(self.pC.timeDataList),nX,nY,M),dtype=np.double)
        self.dSet_fConc = self.runGrpSnapShot.create_dataset('finalConc',(1,nX,nY,M),maxshape=(len(self.pC.timeDataList),nX,nY,M),dtype=np.double)
        self.dSet_iFi = self.runGrpSnapShot.create_dataset('initFi',(1,nX,nY),maxshape=(len(self.pC.timeDataList),nX,nY),dtype=np.double)
        self.dSet_fFi = self.runGrpSnapShot.create_dataset('finalFi',(1,nX,nY),maxshape=(len(self.pC.timeDataList),nX,nY),dtype=np.double)
        self.dSet_iTime = self.runGrpSnapShot.create_dataset('initTime',(1,1),maxshape=(len(self.pC.timeDataList),1),dtype=np.double)
        self.dSet_fTime = self.runGrpSnapShot.create_dataset('finalTime',(1,1),maxshape=(len(self.pC.timeDataList),1),dtype=np.double)
        self.dSet_vT = self.runGrpSnapShot.create_dataset('Vt',(1,1),maxshape=(len(self.pC.timeDataList),1),dtype=np.double)
        self.dSet_isFloating = self.runGrpSnapShot.create_dataset('isFloating',(1,1),maxshape=(len(self.pC.timeDataList),1),dtype=np.double)
        
        self.dSet_Conc = self.runGrpSol.create_dataset('Conc',(1,nX,nY,M),maxshape=(None,nX,nY,M),dtype=np.double)
        self.dSet_Fi = self.runGrpSol.create_dataset('Fi',(1,nX,nY),maxshape=(None,nX,nY),dtype=np.double)
        self.dSet_Time = self.runGrpSol.create_dataset('Time',(1,1),maxshape=(None,1),dtype=np.double)
        
        
#        self.hdf5_file.close()
#        exit()
        
        self.setSnapShotData(self.pC.timeDataList[0],0)
        
        self.mode6_widget.outLog.write('Initializing the Numerical Engine\n')
        
        self.numEng.outLog=self.mode6_widget.outLog
        
        self.numEng.initialize()
        
        self.mode6_widget.outLog.write('Running the Recipe\n Please Wait\n')
        
#        self.saveSolution
        
#        self.runThread.started.connect(self.runRecipe)
#        self.runThread.start()
        
#        self.mode6_widget.outLog.write('Completed the Run\n')
        
        self.runRecipe()
        
    def setSnapShotData(self,SnapShot,indx):
#        print('indx={0}'.format(indx))
        nX,nY,M,K=self.numEng.nX,self.numEng.nY,self.numEng.M,self.numEng.K
        self.numEng.Vt=SnapShot.temp*scipy.constants.k/ scipy.constants.e
        self.numEng.Ns=SnapShot.Ns
        self.numEng.G=SnapShot.G
        self.numEng.D=SnapShot.D
        self.numEng.Eps=SnapShot.Eps*scipy.constants.epsilon_0*1e-2
        
        Kf=np.asarray(SnapShot.Kf)
        Kb=np.asarray(SnapShot.Kb)
        
        
#        print('Vt :{0}'.format(self.numEng.Vt.shape))
#        print('Ns :{0}'.format(self.numEng.Ns.shape))
#        print('G :{0}'.format(self.numEng.G.shape))
#        print('D :{0}'.format(self.numEng.D.shape))
#        print('Eps :{0}'.format(self.numEng.Eps.shape))
        
        
        Kf=np.reshape(Kf,(self.numEng.nX*self.numEng.nY,self.numEng.K))
        Kb=np.reshape(Kb,(self.numEng.nX*self.numEng.nY,self.numEng.K))
        self.numEng.Kf=Kf
        self.numEng.Kb=Kb
        
        
#        print('Kf :{0}'.format(self.numEng.Kf.shape))
#        print('Kb :{0}'.format(self.numEng.Kb.shape))
        fc_bc=np.vstack((SnapShot.TopA,SnapShot.TopB,SnapShot.TopC))
        bc_bc=np.vstack((SnapShot.BottomA,SnapShot.BottomB,SnapShot.BottomC))
        self.numEng.FC_BC=fc_bc
        self.numEng.BC_BC=bc_bc
        
#        print('BC_BC :{0}'.format(self.numEng.BC_BC.shape))
#        print('FC_BC :{0}'.format(self.numEng.FC_BC.shape))
        # should get this from the GUI
        self.numEng.isFloating=SnapShot.isFloating
        
        if indx!=0:
            self.dSet_vT.resize(self.dSet_vT.shape[0]+1,axis=0)
            self.dSet_Ns.resize(self.dSet_Ns.shape[0]+1,axis=0)
            self.dSet_G.resize(self.dSet_G.shape[0]+1,axis=0)
            self.dSet_D.resize(self.dSet_D.shape[0]+1,axis=0)
            self.dSet_Eps.resize(self.dSet_Eps.shape[0]+1,axis=0)
            self.dSet_Kf.resize(self.dSet_Kf.shape[0]+1,axis=0)
            self.dSet_Kb.resize(self.dSet_Kb.shape[0]+1,axis=0)
            self.dSet_FC_BC.resize(self.dSet_FC_BC.shape[0]+1,axis=0)
            self.dSet_BC_BC.resize(self.dSet_BC_BC.shape[0]+1,axis=0)
            self.dSet_isFloating.resize(self.dSet_isFloating.shape[0]+1,axis=0)
            
        self.dSet_vT[-1:]=np.reshape(self.numEng.Vt,(1,1))
        self.dSet_Ns[-1:]=np.reshape(self.numEng.Ns,(1,nX,nY,M))
        self.dSet_G[-1:]=np.reshape(self.numEng.G,(1,nX,nY,M))
        self.dSet_D[-1:]=np.reshape(self.numEng.D,(1,nX,nY,M))
        self.dSet_Eps[-1:]=np.reshape(SnapShot.Eps,(1,nX,nY))
        self.dSet_Kf[-1:]=np.reshape(self.numEng.Kf,(1,nX,nY,K))
        self.dSet_Kb[-1:]=np.reshape(self.numEng.Kb,(1,nX,nY,K))
        self.dSet_FC_BC[-1:]=np.reshape(self.numEng.FC_BC,(1,3,nX,M+1))
        self.dSet_BC_BC[-1:]=np.reshape(self.numEng.BC_BC,(1,3,nX,M+1))
        self.dSet_isFloating[-1:]=np.reshape(SnapShot.isFloating,(1,1))
        
#        self.hdf5_file.close()
#        exit()
        
    def runRecipe(self):
        nX,nY,M=self.numEng.nX,self.numEng.nY,self.numEng.M
        dtStart=1e-14
        tOut=np.array([[]])
        uOut=np.array([[]])
        uOut.shape=(self.numEng.nX*self.numEng.nY*self.numEng.M,0)
        fiOut=np.array([[]])
        fiOut.shape=(self.numEng.nX*self.numEng.nY,0)
        self.dSet_Time[-1:]=self.pC.timeDataList[0].time
        self.dSet_Fi[-1:]=np.reshape(self.numEng.fi0*self.numEng.Vt,(1,nX,nY))
        self.dSet_Conc[-1:]=np.reshape(self.numEng.U0,(1,nX,nY,M))
        for i in range(1,len(self.pC.timeDataList)):
            timeStart=self.pC.timeDataList[i-1].time
            timeEnd=self.pC.timeDataList[i].time
            
            self.dSet_iTime.resize(self.dSet_iTime.shape[0]+1,axis=0)
            self.dSet_iConc.resize(self.dSet_iConc.shape[0]+1,axis=0)
            self.dSet_iFi.resize(self.dSet_iFi.shape[0]+1,axis=0)
            
            self.dSet_iTime[-1:]=self.pC.timeDataList[i-1].time
            self.dSet_iConc[-1:]=np.reshape(self.numEng.U0,(1,nX,nY,M))
            self.dSet_iFi[-1:]=np.reshape(self.numEng.fi0*self.numEng.Vt,(1,nX,nY))
#            QMessageBox.about(self,"Testing","i={0},start={1},end={2}".format(i,timeStart,timeEnd))
#            print('timeStart={0}'.format(timeStart))
#            print('timeEnd={0}'.format(timeEnd))
#            print('dtStart={0}'.format(dtStart))
            tVec,UVec,fiVec=self.numEng.Run(timeStart,timeEnd,dtStart,self.dSet_Conc,self.dSet_Fi,self.dSet_Time)
#            print("tVec={0}".format(tVec))
#            print("UVec={0}".format(UVec))
#            print("fiVec={0}".format(fiVec))
            tOut=np.hstack((tOut,tVec))
            uOut=np.hstack((uOut,UVec))
            fiOut=np.hstack((fiOut,fiVec*self.pC.timeDataList[i-1].temp*scipy.constants.k/ scipy.constants.e))
            nextInitConc=np.reshape(UVec[:,-1],(self.numEng.nX*self.numEng.nY,self.numEng.M))
            nextInitFi=fiVec[:,-1]
            nextInitFi.shape=(self.numEng.nX*self.numEng.nY,1)
            self.setSnapShotData(self.pC.timeDataList[i],i)
            self.numEng.reInitialize()
            self.numEng.U0=nextInitConc
            self.numEng.fi0=nextInitFi
            
            if i>1:
                self.dSet_fTime.resize(self.dSet_fTime.shape[0]+1,axis=0)
                self.dSet_fConc.resize(self.dSet_fConc.shape[0]+1,axis=0)
                self.dSet_fFi.resize(self.dSet_fFi.shape[0]+1,axis=0)
            
            self.dSet_fTime[-1:]=self.pC.timeDataList[i].time
            self.dSet_fConc[-1:]=np.reshape(nextInitConc,(1,nX,nY,M))
            self.dSet_fFi[-1:]=np.reshape(nextInitFi*self.numEng.Vt,(1,nX,nY))
            
            dtStart=tVec[0,-1]-tVec[0,-2]
            dtStart=1e-14
        self.tOut=tOut
        self.fiOut=fiOut
        self.uOut=uOut
        
        
        self.hdf5_file.close()
        print('Completed the Simulation')
#        print('Should start the Visualization Browser')
        
        self.toolBar.resultsAction.setEnabled(True)
        self.pC.mode=7
        self.mode7_widget.updateHDF5Name(self.hdf5_fileName)
        self.mode7_widget.updateData()
#        exit()
#        self.SB.startInteractive()
        
        
