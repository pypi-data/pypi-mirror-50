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
Created on Sun Nov  4 15:09:36 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QRadioButton, QHBoxLayout, QPushButton, QLabel,
        QLineEdit, QDialogButtonBox, QGridLayout, QCheckBox, QComboBox,
        QMessageBox, QScrollArea, QWidget
        )

from .latexQLabel import latexQLabel

from PyQt5.QtGui import (
        QDoubleValidator
        )

from .generalFunctions import (
        parseString, getTimeInSeconds, getTempInKelvin, restoreString, tupleString,
        isCationVacancy, isAnionVacancy, isHostCation, isHostAnion
        )

import ast

import numpy as np

class NewProjectDlg(QDialog):
    def __init__(self, parent=None):
        super(NewProjectDlg,self).__init__(parent)
        self.temp_nDims=2
        self.nDims=-1
        
        layout_h1=QVBoxLayout()
        
        radioButton=QRadioButton("0D")
        radioButton.nDims=0
        radioButton.toggled.connect(self.update_nDimsTemp)
        layout_h1.addWidget(radioButton)
        
        radioButton=QRadioButton("1D")
        radioButton.nDims=1
        radioButton.toggled.connect(self.update_nDimsTemp)
        layout_h1.addWidget(radioButton)
        
        radioButton=QRadioButton("2D")
        radioButton.nDims=2
        radioButton.toggled.connect(self.update_nDimsTemp)
        layout_h1.addWidget(radioButton)
        
        layout_h2=QHBoxLayout()
        okButton=QPushButton("OK")
        okButton.clicked.connect(self.update_nDims)
        okButton.isOk=True;
        cancelButton=QPushButton("Cancel")
        cancelButton.isOk=False;
        cancelButton.clicked.connect(self.update_nDims)
        layout_h2.addWidget(okButton)
        layout_h2.addWidget(cancelButton)
        layout_h1.addLayout(layout_h2)
        self.setLayout(layout_h1)
        
    def update_nDimsTemp(self):
        radiobutton=self.sender()
        if radiobutton.isChecked():
            self.temp_nDims=radiobutton.nDims
            
    def update_nDims(self):
        button=self.sender()
        self.isOk=button.isOk
        if button.isOk:
            self.nDims=self.temp_nDims
        self.close()
        
class PVRD_RectangleDlg_Mode1_Boundary(QDialog):
    def __init__(self,X0=0,Y0=0,width=1,height=1,nDims=0,parent=None):
        super(PVRD_RectangleDlg_Mode1_Boundary,self).__init__(parent)
        self.rX0=X0
        self.rY0=Y0
        self.rWidth=width
        self.rHeight=height
        self.nDims=nDims
        if not self.nDims >=2:
            self.rWidth=0
        if not self.nDims >=1:
            self.rHeight=0
        self.propChanged=False
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    
    def create_widgets(self):
        
        self.bottomXLabel=QLabel("&Bottom X:")
        self.bottomXTB=QLineEdit("{0}".format(self.rX0))
        self.bottomXLabel.setBuddy(self.bottomXTB)
        self.bottomXTB.setValidator(QDoubleValidator())
        self.bottomXTB.setEnabled(False)
        
        self.bottomYLabel=QLabel("&Bottom Y:")
        self.bottomYTB=QLineEdit("{0}".format(self.rY0))
        self.bottomYLabel.setBuddy(self.bottomYTB)
        self.bottomYTB.setValidator(QDoubleValidator())
        self.bottomYTB.setEnabled(False)
        
        self.widthLabel=QLabel("&Width(um):")
        self.widthTB=QLineEdit("{0}".format(self.rWidth))
        self.widthLabel.setBuddy(self.widthTB)
        self.widthTB.setValidator(QDoubleValidator())
        self.widthTB.setEnabled(self.nDims >= 2)
        
        self.heightLabel=QLabel("&Height(um):")
        self.heightTB=QLineEdit("{0}".format(self.rHeight))
        self.heightLabel.setBuddy(self.heightTB)
        self.heightTB.setValidator(QDoubleValidator())
        self.heightTB.setEnabled(self.nDims >= 1)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        
    def layout_widgets(self):
        QCheckBox
        layout = QGridLayout()
        layout.addWidget(self.bottomXLabel, 0, 0)
        layout.addWidget(self.bottomXTB, 0, 1)
        layout.addWidget(self.bottomYLabel, 1, 0)
        layout.addWidget(self.bottomYTB, 1, 1)
        layout.addWidget(self.widthLabel, 2, 0)
        layout.addWidget(self.widthTB, 2, 1)
        layout.addWidget(self.heightLabel, 3, 0)
        layout.addWidget(self.heightTB, 3, 1)
        layout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
#        self.widthTB.textChanged[str].connect(self.checkIfNumber)
        
        self.setWindowTitle("Rectangle Creation Dialog")
        
    def result(self):
        return float(self.widthTB.text()),float(self.heightTB.text()),\
            float(self.bottomXTB.text()),float(self.bottomYTB.text())
            
class PVRD_RectangleDlg_Mode1_Material(QDialog):
    def __init__(self,X0=0,Y0=0,width=1,height=1,nDims=0,parent=None):
        super(PVRD_RectangleDlg_Mode1_Material,self).__init__(parent)
        self.rX0=X0
        self.rY0=Y0
        self.rWidth=width
        self.rHeight=height
        self.nDims=nDims
        if not self.nDims >=2:
            self.rWidth=0
        if not self.nDims >=1:
            self.rHeight=0
        self.propChanged=False
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
    
    def create_widgets(self):
        
        self.bottomXLabel=QLabel("&Bottom X:")
        self.bottomXTB=QLineEdit("{0}".format(self.rX0))
        self.bottomXLabel.setBuddy(self.bottomXTB)
        self.bottomXTB.setValidator(QDoubleValidator())
        self.bottomXTB.setEnabled(self.nDims >= 2)
        
        self.bottomYLabel=QLabel("&Bottom Y:")
        self.bottomYTB=QLineEdit("{0}".format(self.rY0))
        self.bottomYLabel.setBuddy(self.bottomYTB)
        self.bottomYTB.setValidator(QDoubleValidator())
        self.bottomYTB.setEnabled(self.nDims >= 1)
        
        self.widthLabel=QLabel("&Width(um):")
        self.widthTB=QLineEdit("{0}".format(self.rWidth))
        self.widthLabel.setBuddy(self.widthTB)
        self.widthTB.setValidator(QDoubleValidator())
        self.widthTB.setEnabled(self.nDims >= 2)
        
        self.heightLabel=QLabel("&Height(um):")
        self.heightTB=QLineEdit("{0}".format(self.rHeight))
        self.heightLabel.setBuddy(self.heightTB)
        self.heightTB.setValidator(QDoubleValidator())
        self.heightTB.setEnabled(self.nDims >= 1)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        
    def layout_widgets(self):
        
        layout = QGridLayout()
        layout.addWidget(self.bottomXLabel, 0, 0)
        layout.addWidget(self.bottomXTB, 0, 1)
        layout.addWidget(self.bottomYLabel, 1, 0)
        layout.addWidget(self.bottomYTB, 1, 1)
        layout.addWidget(self.widthLabel, 2, 0)
        layout.addWidget(self.widthTB, 2, 1)
        layout.addWidget(self.heightLabel, 3, 0)
        layout.addWidget(self.heightTB, 3, 1)
        layout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
#        self.widthTB.textChanged[str].connect(self.checkIfNumber)
        
        self.setWindowTitle("Rectangle Creation Dialog")
        
    def result(self):
        return float(self.widthTB.text()),float(self.heightTB.text()),\
    float(self.bottomXTB.text()),float(self.bottomYTB.text())
    
class PVRD_MaterialDlg_Mode1_GrainBoundary(QDialog):
    def __init__(self,mat1Name,parent=None):
        super(PVRD_MaterialDlg_Mode1_GrainBoundary,self).__init__(parent)
        self.label=QLabel("{0} sharing common line.\n Do you want to treat this as Grain Boundary?".format(
                mat1Name))
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Yes|
                                          QDialogButtonBox.No)
        self.checkBox = QCheckBox("Remember this for all others")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.buttonBox)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.setLayout(layout)
        
class PVRD_LineDlg_Mode1_GrainBoundary(QDialog):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,nDims=0,parent=None):
        super(PVRD_LineDlg_Mode1_GrainBoundary,self).__init__(parent)
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.nDims=nDims
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        
        self.X1_Label=QLabel("Start X:")
        self.X1_TB=QLineEdit("{0}".format(self.x1))
        self.X1_Label.setBuddy(self.X1_TB)
        self.X1_TB.setValidator(QDoubleValidator())
        self.X1_TB.setEnabled(self.nDims==2)
        
        self.Y1_Label=QLabel("Start Y:")
        self.Y1_TB=QLineEdit("{0}".format(self.y1))
        self.Y1_Label.setBuddy(self.Y1_TB)
        self.Y1_TB.setValidator(QDoubleValidator())
        self.Y1_TB.setEnabled(self.nDims>=1)
        
        self.X2_Label=QLabel("End X:")
        self.X2_TB=QLineEdit("{0}".format(self.x2))
        self.X2_Label.setBuddy(self.X2_TB)
        self.X2_TB.setValidator(QDoubleValidator())
        self.X2_TB.setEnabled(self.nDims==2)
        
        self.Y2_Label=QLabel("End Y:")
        self.Y2_TB=QLineEdit("{0}".format(self.y2))
        self.Y2_Label.setBuddy(self.Y2_TB)
        self.Y2_TB.setValidator(QDoubleValidator())
        self.Y2_TB.setEnabled(self.nDims==2)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        
    def layout_widgets(self):
        
        layout = QGridLayout()
        layout.addWidget(self.X1_Label, 0, 0)
        layout.addWidget(self.X1_TB, 0, 1)
        layout.addWidget(self.Y1_Label, 1, 0)
        layout.addWidget(self.Y1_TB, 1, 1)
        layout.addWidget(self.X2_Label, 2, 0)
        layout.addWidget(self.X2_TB, 2, 1)
        layout.addWidget(self.Y2_Label, 3, 0)
        layout.addWidget(self.Y2_TB, 3, 1)
        layout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
#        self.widthTB.textChanged[str].connect(self.checkIfNumber)
        
        self.setWindowTitle("Grain Boundary Creation Dialog")
        
    def result(self):
        return float(self.X1_TB.text()),float(self.Y1_TB.text()),\
    float(self.X2_TB.text()),float(self.Y2_TB.text())
    
    
class PVRD_RectangleDlg_Mode2(QDialog):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,Name="",matName="",parent=None):
        super(PVRD_RectangleDlg_Mode2,self).__init__(None)
        self.parent=parent
        self.bX=x1
        self.bY=x2
        self.w=y1
        self.h=y2
        self.name=Name
        self.matName=matName
#        self.mechList=list()
#        self.reactionList=list()
#        self.speciesList=list()
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
        self.checkMech=False
        self.checkReactions=False
        self.checkSpecies=False
        
    def create_widgets(self):
        
        self.Name_Label=QLabel("Name:")
        self.Name_TB=QLineEdit("{0}".format(self.name))
        self.Name_TB.setEnabled(False)
        self.Name_Label.setBuddy(self.Name_TB)
        
        self.Mat_Label=QLabel("Material:")
        self.Mat_TB=QLineEdit("{0}".format(self.matName))
        self.Mat_TB.setEnabled(False)
        self.Mat_Label.setBuddy(self.Mat_TB)
        
        self.X1_Label=QLabel("Bottom X:")
        self.X1_TB=QLineEdit("{0}".format(self.bX))
        self.X1_TB.setEnabled(False)
        self.X1_Label.setBuddy(self.X1_TB)
#        self.X1_TB.setValidator(QDoubleValidator())
        
        self.Y1_Label=QLabel("Bottom Y:")
        self.Y1_TB=QLineEdit("{0}".format(self.bY))
        self.Y1_TB.setEnabled(False)
        self.Y1_Label.setBuddy(self.Y1_TB)
#        self.Y1_TB.setValidator(QDoubleValidator())
        
        self.X2_Label=QLabel("Width:")
        self.X2_TB=QLineEdit("{0}".format(self.w))
        self.X2_TB.setEnabled(False)
        self.X2_Label.setBuddy(self.X2_TB)
#        self.X2_TB.setValidator(QDoubleValidator())
        
        self.Y2_Label=QLabel("Height:")
        self.Y2_TB=QLineEdit("{0}".format(self.h))
        self.Y2_TB.setEnabled(False)
        self.Y2_Label.setBuddy(self.Y2_TB)
#        self.Y2_TB.setValidator(QDoubleValidator())
        
        self.Mechanism_Label=QLabel("Mechanisms:")
        self.Mechanism_CB=QComboBox()
        self.Mechanism_Label.setBuddy(self.Mechanism_CB)
        
        self.MechanismText_Label=QLabel("Mechanisms(Text):")
        self.MechanismText_TB=QLineEdit()
        self.MechanismText_TB.setToolTip('Add or delete mechanisms seperated by comma')
        self.MechanismText_Label.setBuddy(self.MechanismText_TB)
        
        self.Reactions_Label=QLabel("Reactions:")
        self.Reactions_CB=QComboBox()
        self.Reactions_Label.setBuddy(self.Reactions_CB)
        
        self.ReactionsText_Label=QLabel("Reactions(Text):")
        self.ReactionsText_TB=QLineEdit()
        self.ReactionsText_Label.setBuddy(self.ReactionsText_TB)
        
        self.PointDefects_Label=QLabel("PointDefects:")
        self.PointDefects_CB=QComboBox()
        self.PointDefects_Label.setBuddy(self.PointDefects_CB)
        
        self.PointDefectsText_Label=QLabel("PointDefects(Text):")
        self.PointDefectsText_TB=QLineEdit()
        self.PointDefectsText_Label.setBuddy(self.PointDefectsText_TB)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Apply|
                                          QDialogButtonBox.Cancel)
        self.applyBotton=self.buttonBox.button(QDialogButtonBox.Apply)
        self.applyBotton.setEnabled(False)
        
    def layout_widgets(self):
        
        row=0
        layout = QGridLayout()
        
        layout.addWidget(self.Name_Label, row, 0)
        layout.addWidget(self.Name_TB, row, 1,1,3)
        row=row+1
        layout.addWidget(self.Mat_Label, row, 0)
        layout.addWidget(self.Mat_TB, row, 1,1,3)
        row=row+1
        layout.addWidget(self.X1_Label, row, 0)
        layout.addWidget(self.X1_TB, row, 1)
        layout.addWidget(self.X2_Label, row, 2)
        layout.addWidget(self.X2_TB, row, 3)
        row=row+1
        layout.addWidget(self.Y1_Label, row, 0)
        layout.addWidget(self.Y1_TB, row, 1)
        layout.addWidget(self.Y2_Label, row, 2)
        layout.addWidget(self.Y2_TB, row, 3)
        row=row+1
        layout.addWidget(self.Mechanism_Label,row,0)
        layout.addWidget(self.Mechanism_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.MechanismText_Label,row,0)
        layout.addWidget(self.MechanismText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.Reactions_Label,row,0)
        layout.addWidget(self.Reactions_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.ReactionsText_Label,row,0)
        layout.addWidget(self.ReactionsText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.PointDefects_Label,row,0)
        layout.addWidget(self.PointDefects_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.PointDefectsText_Label,row,0)
        layout.addWidget(self.PointDefectsText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.buttonBox, row, 2, 1, 2)
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Material Defect Chemistry Properties Dialog")
        self.MechanismText_TB.textEdited[str].connect(self.checkMechanisms)
        self.ReactionsText_TB.textEdited[str].connect(self.checkReactions)
        self.PointDefectsText_TB.textEdited[str].connect(self.checkSpecies)
        self.applyBotton.clicked.connect(self.updateDialog)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.rejectEdits)
        
    def result(self):
        return float(self.X1_TB.text()),float(self.Y1_TB.text()),\
    float(self.X2_TB.text()),float(self.Y2_TB.text())
        
    def addMechanisms(self,mechName,toStr=True):
        if not mechName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList:
            QMessageBox.about(self,'warning',"In Add Mechanisms 0")            
            if len(self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList):
                if toStr:
                    self.MechanismText_TB.setText(self.MechanismText_TB.text()+','+mechName)
            else:
                self.Mechanism_CB.addItem('')
                if toStr:
                    self.MechanismText_TB.setText(self.MechanismText_TB.text()+mechName)
            self.Mechanism_CB.addItem(mechName)
            self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList.append(mechName)
            self.addReactionsNSpeciesForMechanisms(mechName)
#            QMessageBox.about(self,'warning','pC Indx "{0}"'.format(self.parent.pCindx))
            
    def addReactions(self,reactionName,toStr=True):
        if not reactionName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
            if len(self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList):
                if toStr:
                    self.ReactionsText_TB.setText(self.ReactionsText_TB.text()+','+reactionName)
            else:
                self.Reactions_CB.addItem('')
                if toStr:
                    self.ReactionsText_TB.setText(self.ReactionsText_TB.text()+reactionName)
            self.Reactions_CB.addItem(reactionName)
            self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList.append(reactionName)
            self.addSpeciesForReactions(reactionName)
            
    def addSpecies(self,speciesName,toStr=True):
        if not speciesName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
            if len(self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList):
                if toStr:
                    self.PointDefectsText_TB.setText(self.PointDefectsText_TB.text()+','+speciesName)
            else:
                self.PointDefects_CB.addItem('')
                if toStr:
                    self.PointDefectsText_TB.setText(self.PointDefectsText_TB.text()+speciesName)
            self.PointDefects_CB.addItem(speciesName)
            self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList.append(speciesName)
        
    
        
    def rejectEdits(self):
        self.MechanismText_TB.setText(','.join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList))
        self.ReactionsText_TB.setText(','.join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList))
        self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList))
        self.applyBotton.setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.reject()
        
    def addReactionsNSpeciesForMechanisms(self,mechName):
        if mechName is None:
            for mechName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList:
                reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
                for ii in range(len(reactionsTuple)):
                    reactionName=reactionsTuple[ii]
                    if not reactionName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
                        self.addReactions(reactionName)
                        speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                        for jj in range(len(speciesTuple)):
                            speciesName=speciesTuple[jj]
                            if not speciesName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
                                self.addSpecies(speciesName)
        else:
            reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
#            QMessageBox.about(self,'warning',"In Add Mechanisms {0}".format(reactionsTuple))
            for ii in range(len(reactionsTuple)):
                reactionName=reactionsTuple[ii]
                if not reactionName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
                    self.addReactions(reactionName)
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                    for jj in range(len(speciesTuple)):
                        speciesName=speciesTuple[jj]
                        if not speciesName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
                            self.addSpecies(speciesName)
                            
    def addSpeciesForReactions(self,reactionName):
        if reactionName is not None:
            speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
            for jj in range(len(speciesTuple)):
                speciesName=speciesTuple[jj]
                if not speciesName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
                    self.addSpecies(speciesName)
        
    def closeEvent(self,event):
        self.rejectEdits()
        
    def updateDialog(self):
        disableFlg=True
        if self.checkMech:
            self.checkMech=False
            newStr=self.MechanismText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newMechList=list()
            deletionList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.mechanisms:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" mechanism Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList:
                        ii=ii+1
                    else:
                       newMechList.append(editStr) 
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList):
                    jj=1
                    for mechStr in self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList:
                        if not mechStr in newStrList:
                            deletionList.append(jj)
                        jj=jj+1
                deletionList.sort(reverse=True)
                for jj in deletionList:
                    self.Mechanism_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList[jj-1]
                for newMechName in newMechList:
                    self.addMechanisms(newMechName,False)
#                    self.mechList.append(newMechName)
#                    self.Mechanism_CB.addItem(newMechName)
                    
                    
        if self.checkReactions:
            self.checkReactions=False
            newStr=self.ReactionsText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newList=list()
            delList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.reactions:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" reaction Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
                        ii=ii+1
                    else:
                        newList.append(editStr)
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList):
                    jj=1
                    for reactionStr in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
                        if not reactionStr in newStrList:
                            delList.append(jj)
                        jj=jj+1
                delList.sort(reverse=True)
                speciesDelList=list()
                for jj in delList:
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList[jj-1])
                    for speciesName in speciesTuple:
                        speciesDelList.append(speciesName)
                speciesDelList=list(set(speciesDelList))
                
                delMechList=list()
                
                for jj in delList:
                    reactionName=self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList[jj-1]
                    for mechName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList:
                        reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
                        if reactionName in reactionsTuple:
                            delMechList.append(self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList.index(mechName))
                delMechList=list(set(delMechList))
                delMechList.sort(reverse=True)
                for jj in delMechList:
                    self.Mechanism_CB.removeItem(jj+1)
                    del self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList[jj]
                self.MechanismText_TB.setText(",".join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList))
                    
                for jj in delList:
                    self.Reactions_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList[jj-1]
                for newReactionName in newList:
                    self.addReactions(newReactionName,False)
                
                speciesUpdateList=list()
                for reactionName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                    for speciesName in speciesTuple:
                        speciesUpdateList.append(speciesName)
                speciesUpdateList=list(set(speciesUpdateList))
                
                speciesDelIndx=list()
                for speciesName in speciesDelList:
                    if not speciesName in speciesUpdateList:
                        speciesDelIndx.append(self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList.index(speciesName))
                        
                speciesDelIndx.sort(reverse=True)
                for jj in speciesDelIndx:
                    self.PointDefects_CB.removeItem(jj+1)
                    del self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList[jj]
                    
                self.PointDefectsText_TB.setText(",".join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList))
                
                    
#                    self.reactionList.append(newReactionName)
#                    self.Reactions_CB.addItem(newReactionName)
    
        if self.checkSpecies:
            self.checkSpecies=False
            newStr=self.PointDefectsText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newList=list()
            delList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.species:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" species Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
                        ii=ii+1
                    else:
                        newList.append(editStr)
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList):
                    jj=1
                    for speciesStr in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
                        if not speciesStr in newStrList:
                            delList.append(jj)
                        jj=jj+1
                delList.sort(reverse=True)
                delRemoveList=list()
                for jj in delList:
                    speciesFound=False
                    speciesName=self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList[jj-1]
                    for reactionName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
                        speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                        if speciesName in speciesTuple:
                            QMessageBox.about(self,'warning','Cannot delete "{0}" \n\
                                              as it is involved in the reaction\n\
                                              {1}'.format(speciesName,reactionName))
                            speciesFound=True
#                            delRemoveList.append(jj)
                            break
                    if speciesFound:
                        delRemoveList.append(jj)
                
                for jj in delRemoveList:
                    delList.remove(jj)
                
                for jj in delList:
                    self.PointDefects_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList[jj-1]
                for newSpeciesName in newList:
                    self.addSpecies(newSpeciesName,False)
                    
                self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList))
#                    self.speciesList.append(newSpeciesName)
#                    self.PointDefects_CB.addItem(newSpeciesName)
        
        if disableFlg:
            self.applyBotton.setEnabled(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            
#        self.accept()
    def checkMechanisms(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkMech=True
        
    def checkReactions(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkReactions=True
        
    def checkSpecies(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkSpecies=True
        
    def setCB_and_TB(self):
        for ii in range(self.Mechanism_CB.count()):
            self.Mechanism_CB.removeItem(ii)
        self.Mechanism_CB.addItem('')
        for mechName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList:
            self.Mechanism_CB.addItem(mechName)
        self.MechanismText_TB.setText(','.join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList))
        
        for ii in range(self.Reactions_CB.count()):
            self.Reactions_CB.removeItem(ii)
        self.Reactions_CB.addItem('')
        for reactionName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
            self.Reactions_CB.addItem(reactionName)
        self.ReactionsText_TB.setText(','.join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList))
        
        for ii in range(self.PointDefects_CB.count()):
            self.PointDefects_CB.removeItem(ii)
        self.PointDefects_CB.addItem('')
        for speciesName in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
            self.PointDefects_CB.addItem(speciesName)
        self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList))
        
###############################################################################

class PVRD_LineDlg_Mode2(QDialog):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,Name="",matName="",parent=None):
        super(PVRD_LineDlg_Mode2,self).__init__(None)
        self.parent=parent
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.name=Name
        self.matName=matName
#        self.mechList=list()
#        self.reactionList=list()
#        self.speciesList=list()
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
        self.checkMech=False
        self.checkReactions=False
        self.checkSpecies=False
        
    def create_widgets(self):
        
#        font = QFont(pointSize=15, weight=QFont.Bold)
        
        self.Name_Label=QLabel("Name:")
        self.Name_TB=QLineEdit("{0}".format(self.name))
#        self.Name_TB.setFont(font)
        self.Name_TB.setEnabled(False)
        self.Name_Label.setBuddy(self.Name_TB)
        
        self.Mat_Label=QLabel("Material:")
        self.Mat_TB=QLineEdit("{0}".format(self.matName))
#        self.Mat_TB.setFont(font)
        self.Mat_TB.setEnabled(False)
        self.Mat_Label.setBuddy(self.Mat_TB)
        
        self.X1_Label=QLabel("Start X:")
        self.X1_TB=QLineEdit("{0}".format(self.x1))
        self.X1_TB.setEnabled(False)
        self.X1_Label.setBuddy(self.X1_TB)
#        self.X1_TB.setValidator(QDoubleValidator())
        
        self.Y1_Label=QLabel("Start Y:")
        self.Y1_TB=QLineEdit("{0}".format(self.y1))
        self.Y1_TB.setEnabled(False)
        self.Y1_Label.setBuddy(self.Y1_TB)
#        self.Y1_TB.setValidator(QDoubleValidator())
        
        self.X2_Label=QLabel("End X:")
        self.X2_TB=QLineEdit("{0}".format(self.x2))
        self.X2_TB.setEnabled(False)
        self.X2_Label.setBuddy(self.X2_TB)
#        self.X2_TB.setValidator(QDoubleValidator())
        
        self.Y2_Label=QLabel("End Y:")
        self.Y2_TB=QLineEdit("{0}".format(self.y2))
        self.Y2_TB.setEnabled(False)
        self.Y2_Label.setBuddy(self.Y2_TB)
#        self.Y2_TB.setValidator(QDoubleValidator())
        
        self.Mechanism_Label=QLabel("Mechanisms:")
        self.Mechanism_CB=QComboBox()
        self.Mechanism_Label.setBuddy(self.Mechanism_CB)
        
        self.MechanismText_Label=QLabel("Mechanisms(Text):")
        self.MechanismText_TB=QLineEdit()
        self.MechanismText_Label.setBuddy(self.MechanismText_TB)
        
        self.Reactions_Label=QLabel("Reactions:")
        self.Reactions_CB=QComboBox()
        self.Reactions_Label.setBuddy(self.Reactions_CB)
        
        self.ReactionsText_Label=QLabel("Reactions(Text):")
        self.ReactionsText_TB=QLineEdit()
        self.ReactionsText_Label.setBuddy(self.ReactionsText_TB)
        
        self.PointDefects_Label=QLabel("PointDefects:")
        self.PointDefects_CB=QComboBox()
        self.PointDefects_Label.setBuddy(self.PointDefects_CB)
        
        self.PointDefectsText_Label=QLabel("PointDefects(Text):")
        self.PointDefectsText_TB=QLineEdit()
        self.PointDefectsText_Label.setBuddy(self.PointDefectsText_TB)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Apply|
                                          QDialogButtonBox.Cancel)
        self.applyBotton=self.buttonBox.button(QDialogButtonBox.Apply)
        self.applyBotton.setEnabled(False)
        
    def layout_widgets(self):
        
        row=0
        layout = QGridLayout()
        
        layout.addWidget(self.Name_Label, row, 0)
        layout.addWidget(self.Name_TB, row, 1,1,3)
        row=row+1
        layout.addWidget(self.Mat_Label, row, 0)
        layout.addWidget(self.Mat_TB, row, 1,1,3)
        row=row+1
        layout.addWidget(self.X1_Label, row, 0)
        layout.addWidget(self.X1_TB, row, 1)
        layout.addWidget(self.X2_Label, row, 2)
        layout.addWidget(self.X2_TB, row, 3)
        row=row+1
        layout.addWidget(self.Y1_Label, row, 0)
        layout.addWidget(self.Y1_TB, row, 1)
        layout.addWidget(self.Y2_Label, row, 2)
        layout.addWidget(self.Y2_TB, row, 3)
        row=row+1
        layout.addWidget(self.Mechanism_Label,row,0)
        layout.addWidget(self.Mechanism_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.MechanismText_Label,row,0)
        layout.addWidget(self.MechanismText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.Reactions_Label,row,0)
        layout.addWidget(self.Reactions_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.ReactionsText_Label,row,0)
        layout.addWidget(self.ReactionsText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.PointDefects_Label,row,0)
        layout.addWidget(self.PointDefects_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.PointDefectsText_Label,row,0)
        layout.addWidget(self.PointDefectsText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.buttonBox, row, 2, 1, 2)
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("GB/Interface Defect Chemistry Properties Dialog")
        self.MechanismText_TB.textEdited[str].connect(self.checkMechanisms)
        self.ReactionsText_TB.textEdited[str].connect(self.checkReactions)
        self.PointDefectsText_TB.textEdited[str].connect(self.checkSpecies)
        self.applyBotton.clicked.connect(self.updateDialog)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.rejectEdits)
        
    def result(self):
        return float(self.X1_TB.text()),float(self.Y1_TB.text()),\
    float(self.X2_TB.text()),float(self.Y2_TB.text())
    
    def addMechanisms(self,mechName,toStr=True):        
        if not mechName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList:
            
            if len(self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList):
                if toStr:
                    self.MechanismText_TB.setText(self.MechanismText_TB.text()+','+mechName)
            else:
                self.Mechanism_CB.addItem('')
                if toStr:
                    self.MechanismText_TB.setText(self.MechanismText_TB.text()+mechName)
            self.Mechanism_CB.addItem(mechName)
            self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList.append(mechName)
            self.addReactionsNSpeciesForMechanisms(mechName)
            
    def addReactions(self,reactionName,toStr=True):
        if not reactionName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
            if len(self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList):
                if toStr:
                    self.ReactionsText_TB.setText(self.ReactionsText_TB.text()+','+reactionName)
            else:
                self.Reactions_CB.addItem('')
                if toStr:
                    self.ReactionsText_TB.setText(self.ReactionsText_TB.text()+reactionName)
            self.Reactions_CB.addItem(reactionName)
            self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList.append(reactionName)
            self.addSpeciesForReactions(reactionName)
            
    def addSpecies(self,speciesName,toStr=True):
        if not speciesName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
            if len(self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList):
                if toStr:
                    self.PointDefectsText_TB.setText(self.PointDefectsText_TB.text()+','+speciesName)
            else:
                self.PointDefects_CB.addItem('')
                if toStr:
                    self.PointDefectsText_TB.setText(self.PointDefectsText_TB.text()+speciesName)
            self.PointDefects_CB.addItem(speciesName)
            self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList.append(speciesName)
        
    
        
    def rejectEdits(self):
        self.MechanismText_TB.setText(','.join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList))
        self.ReactionsText_TB.setText(','.join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList))
        self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList))
        self.applyBotton.setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.reject()
        
    def addReactionsNSpeciesForMechanisms(self,mechName):
        if mechName is None:
            for mechName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList:
                reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
                for ii in range(len(reactionsTuple)):
                    reactionName=reactionsTuple[ii]
                    if not reactionName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
                        self.addReactions(reactionName)
                        speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                        for jj in range(len(speciesTuple)):
                            speciesName=speciesTuple[jj]
                            if not speciesName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
                                self.addSpecies(speciesName)
        else:
            reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
            if len(reactionsTuple)==0:
                QMessageBox.about(self,'warning','No reactions found for mech="{0}"\n\
                                  in "{1}"'.format(mechName,self.matName))
            for ii in range(len(reactionsTuple)):
                reactionName=reactionsTuple[ii]
                if not reactionName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
                    self.addReactions(reactionName)
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                    for jj in range(len(speciesTuple)):
                        speciesName=speciesTuple[jj]
                        if not speciesName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
                            self.addSpecies(speciesName)
                            
                            
    def addSpeciesForReactions(self,reactionName):
        if reactionName is not None:
            speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
            for jj in range(len(speciesTuple)):
                speciesName=speciesTuple[jj]
                if not speciesName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
                    self.addSpecies(speciesName)
                    

        
    def closeEvent(self,event):
        self.rejectEdits()
        
    def updateDialog(self):
        disableFlg=True
        if self.checkMech:
            self.checkMech=False
            newStr=self.MechanismText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newMechList=list()
            deletionList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.mechanisms:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" mechanism Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList:
                        ii=ii+1
                    else:
                       newMechList.append(editStr) 
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList):
                    jj=1
                    for mechStr in self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList:
                        if not mechStr in newStrList:
                            deletionList.append(jj)
                        jj=jj+1
                deletionList.sort(reverse=True)
                for jj in deletionList:
                    self.Mechanism_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList[jj-1]
                for newMechName in newMechList:
                    self.addMechanisms(newMechName,False)
#                    self.mechList.append(newMechName)
#                    self.Mechanism_CB.addItem(newMechName)
                    
                    
        if self.checkReactions:
            self.checkReactions=False
            newStr=self.ReactionsText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newList=list()
            delList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.reactions:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" reaction Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
                        ii=ii+1
                    else:
                        newList.append(editStr)
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList):
                    jj=1
                    for reactionStr in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
                        if not reactionStr in newStrList:
                            delList.append(jj)
                        jj=jj+1
                delList.sort(reverse=True)
                speciesDelList=list()
                for jj in delList:
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList[jj-1])
                    for speciesName in speciesTuple:
                        speciesDelList.append(speciesName)
                speciesDelList=list(set(speciesDelList))
                
                delMechList=list()
                
                for jj in delList:
                    reactionName=self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList[jj-1]
                    for mechName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList:
                        reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
                        if reactionName in reactionsTuple:
                            delMechList.append(self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList.index(mechName))
                delMechList=list(set(delMechList))
                delMechList.sort(reverse=True)
                for jj in delMechList:
                    self.Mechanism_CB.removeItem(jj+1)
                    del self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList[jj]
                self.MechanismText_TB.setText(",".join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList))
                    
                for jj in delList:
                    self.Reactions_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList[jj-1]
                for newReactionName in newList:
                    self.addReactions(newReactionName,False)
                
                speciesUpdateList=list()
                for reactionName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                    for speciesName in speciesTuple:
                        speciesUpdateList.append(speciesName)
                speciesUpdateList=list(set(speciesUpdateList))
                
                speciesDelIndx=list()
                for speciesName in speciesDelList:
                    if not speciesName in speciesUpdateList:
                        speciesDelIndx.append(self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList.index(speciesName))
                        
                speciesDelIndx.sort(reverse=True)
                for jj in speciesDelIndx:
                    self.PointDefects_CB.removeItem(jj+1)
                    del self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList[jj]
                    
                self.PointDefectsText_TB.setText(",".join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList))
                
                    
#                    self.reactionList.append(newReactionName)
#                    self.Reactions_CB.addItem(newReactionName)
    
        if self.checkSpecies:
            self.checkSpecies=False
            newStr=self.PointDefectsText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newList=list()
            delList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.species:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" species Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
                        ii=ii+1
                    else:
                        newList.append(editStr)
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList):
                    jj=1
                    for speciesStr in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
                        if not speciesStr in newStrList:
                            delList.append(jj)
                        jj=jj+1
                delList.sort(reverse=True)
                delRemoveList=list()
                for jj in delList:
                    speciesFound=False
                    speciesName=self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList[jj-1]
                    for reactionName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
                        speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                        if speciesName in speciesTuple:
                            QMessageBox.about(self,'warning','Cannot delete "{0}" \n\
                                              as it is involved in the reaction\n\
                                              {1}'.format(speciesName,reactionName))
                            speciesFound=True
#                            delRemoveList.append(jj)
                            break
                    if speciesFound:
                        delRemoveList.append(jj)
                
                for jj in delRemoveList:
                    delList.remove(jj)
                
                for jj in delList:
                    self.PointDefects_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList[jj-1]
                for newSpeciesName in newList:
                    self.addSpecies(newSpeciesName,False)
                    
                self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList))
#                    self.speciesList.append(newSpeciesName)
#                    self.PointDefects_CB.addItem(newSpeciesName)
        
        if disableFlg:
            self.applyBotton.setEnabled(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            
#        self.accept()
    def checkMechanisms(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkMech=True
        
    def checkReactions(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkReactions=True
        
    def checkSpecies(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkSpecies=True
        
    def setCB_and_TB(self):
        for ii in range(self.Mechanism_CB.count()):
            self.Mechanism_CB.removeItem(ii)
        self.Mechanism_CB.addItem('')
        for mechName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList:
            self.Mechanism_CB.addItem(mechName)
        self.MechanismText_TB.setText(','.join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList))
        
        for ii in range(self.Reactions_CB.count()):
            self.Reactions_CB.removeItem(ii)
        self.Reactions_CB.addItem('')
        for reactionName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
            self.Reactions_CB.addItem(reactionName)
        self.ReactionsText_TB.setText(','.join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList))
        
        for ii in range(self.PointDefects_CB.count()):
            self.PointDefects_CB.removeItem(ii)
        self.PointDefects_CB.addItem('')
        for speciesName in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
            self.PointDefects_CB.addItem(speciesName)
        self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList))
        
###############################################################################

class PVRD_PointDlg_Mode2(QDialog):
    def __init__(self,x1=0,y1=0,Name="",matName="",parent=None):
        super(PVRD_PointDlg_Mode2,self).__init__(None)
        self.parent=parent
        self.x1=x1
        self.y1=y1
        self.name=Name
        self.matName=matName
#        self.mechList=list()
#        self.reactionList=list()
#        self.speciesList=list()
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
        self.checkMech=False
        self.checkReactions=False
        self.checkSpecies=False
        
    def create_widgets(self):
        
        self.Name_Label=QLabel("Name:")
        self.Name_TB=QLineEdit("{0}".format(self.name))
        self.Name_TB.setEnabled(False)
        self.Name_Label.setBuddy(self.Name_TB)
        
        self.Mat_Label=QLabel("Material:")
        self.Mat_TB=QLineEdit("{0}".format(self.matName))
        self.Mat_TB.setEnabled(False)
        self.Mat_Label.setBuddy(self.Mat_TB)
        
        self.X1_Label=QLabel("Point X:")
        self.X1_TB=QLineEdit("{0}".format(self.x1))
        self.X1_TB.setEnabled(False)
        self.X1_Label.setBuddy(self.X1_TB)

        
        self.Y1_Label=QLabel("Point Y:")
        self.Y1_TB=QLineEdit("{0}".format(self.y1))
        self.Y1_TB.setEnabled(False)
        self.Y1_Label.setBuddy(self.Y1_TB)

        
        self.Mechanism_Label=QLabel("Mechanisms:")
        self.Mechanism_CB=QComboBox()
        self.Mechanism_Label.setBuddy(self.Mechanism_CB)
        
        self.MechanismText_Label=QLabel("Mechanisms(Text):")
        self.MechanismText_TB=QLineEdit()
        self.MechanismText_Label.setBuddy(self.MechanismText_TB)
        
        self.Reactions_Label=QLabel("Reactions:")
        self.Reactions_CB=QComboBox()
        self.Reactions_Label.setBuddy(self.Reactions_CB)
        
        self.ReactionsText_Label=QLabel("Reactions(Text):")
        self.ReactionsText_TB=QLineEdit()
        self.ReactionsText_Label.setBuddy(self.ReactionsText_TB)
        
        self.PointDefects_Label=QLabel("PointDefects:")
        self.PointDefects_CB=QComboBox()
        self.PointDefects_Label.setBuddy(self.PointDefects_CB)
        
        self.PointDefectsText_Label=QLabel("PointDefects(Text):")
        self.PointDefectsText_TB=QLineEdit()
        self.PointDefectsText_Label.setBuddy(self.PointDefectsText_TB)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Apply|
                                          QDialogButtonBox.Cancel)
        self.applyBotton=self.buttonBox.button(QDialogButtonBox.Apply)
        self.applyBotton.setEnabled(False)
        
    def layout_widgets(self):
        
        row=0
        layout = QGridLayout()
        
        layout.addWidget(self.Name_Label, row, 0)
        layout.addWidget(self.Name_TB, row, 1,1,3)
        row=row+1
        layout.addWidget(self.Mat_Label, row, 0)
        layout.addWidget(self.Mat_TB, row, 1,1,3)
        row=row+1
        layout.addWidget(self.X1_Label, row, 0)
        layout.addWidget(self.X1_TB, row, 1)
        layout.addWidget(self.Y1_Label, row, 2)
        layout.addWidget(self.Y1_TB, row, 3)
        row=row+1
        layout.addWidget(self.Mechanism_Label,row,0)
        layout.addWidget(self.Mechanism_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.MechanismText_Label,row,0)
        layout.addWidget(self.MechanismText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.Reactions_Label,row,0)
        layout.addWidget(self.Reactions_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.ReactionsText_Label,row,0)
        layout.addWidget(self.ReactionsText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.PointDefects_Label,row,0)
        layout.addWidget(self.PointDefects_CB,row,1,1,3)
        row=row+1
        layout.addWidget(self.PointDefectsText_Label,row,0)
        layout.addWidget(self.PointDefectsText_TB,row,1,1,3)
        row=row+1
        layout.addWidget(self.buttonBox, row, 2, 1, 2)
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("GB/Interface Defect Chemistry Properties Dialog")
        self.MechanismText_TB.textEdited[str].connect(self.checkMechanisms)
        self.ReactionsText_TB.textEdited[str].connect(self.checkReactions)
        self.PointDefectsText_TB.textEdited[str].connect(self.checkSpecies)
        self.applyBotton.clicked.connect(self.updateDialog)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.rejectEdits)
        
    def result(self):
        return float(self.X1_TB.text()),float(self.Y1_TB.text()),\
    float(self.X2_TB.text()),float(self.Y2_TB.text())
    
    def addMechanisms(self,mechName,toStr=True):
        if not mechName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList:
            
            if len(self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList):
                if toStr:
                    self.MechanismText_TB.setText(self.MechanismText_TB.text()+','+mechName)
            else:
                self.Mechanism_CB.addItem('')
                if toStr:
                    self.MechanismText_TB.setText(self.MechanismText_TB.text()+mechName)
            self.Mechanism_CB.addItem(mechName)
            self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList.append(mechName)
            self.addReactionsNSpeciesForMechanisms(mechName)
            
    def addReactions(self,reactionName,toStr=True):
        if not reactionName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
            if len(self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList):
                if toStr:
                    self.ReactionsText_TB.setText(self.ReactionsText_TB.text()+','+reactionName)
            else:
                self.Reactions_CB.addItem('')
                if toStr:
                    self.ReactionsText_TB.setText(self.ReactionsText_TB.text()+reactionName)
            self.Reactions_CB.addItem(reactionName)
            self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList.append(reactionName)
            self.addSpeciesForReactions(reactionName)
            
    def addSpecies(self,speciesName,toStr=True):
        if not speciesName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
            if len(self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList):
                if toStr:
                    self.PointDefectsText_TB.setText(self.PointDefectsText_TB.text()+','+speciesName)
            else:
                self.PointDefects_CB.addItem('')
                if toStr:
                    self.PointDefectsText_TB.setText(self.PointDefectsText_TB.text()+speciesName)
            self.PointDefects_CB.addItem(speciesName)
            self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList.append(speciesName)
        
    
        
    def rejectEdits(self):
        self.MechanismText_TB.setText(','.join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList))
        self.ReactionsText_TB.setText(','.join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList))
        self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList))
        self.applyBotton.setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.reject()
        
    def addReactionsNSpeciesForMechanisms(self,mechName):
        if mechName is None:
            for mechName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList:
                reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
                for ii in range(len(reactionsTuple)):
                    reactionName=reactionsTuple[ii]
                    if not reactionName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
                        self.addReactions(reactionName)
                        speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                        for jj in range(len(speciesTuple)):
                            speciesName=speciesTuple[jj]
                            if not speciesName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
                                self.addSpecies(speciesName)
        else:
            reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
            for ii in range(len(reactionsTuple)):
                reactionName=reactionsTuple[ii]
                if not reactionName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
                    self.addReactions(reactionName)
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                    for jj in range(len(speciesTuple)):
                        speciesName=speciesTuple[jj]
                        if not speciesName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
                            self.addSpecies(speciesName)
                            
    def addSpeciesForReactions(self,reactionName):
        if reactionName is not None:
            speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
            for jj in range(len(speciesTuple)):
                speciesName=speciesTuple[jj]
                if not speciesName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
                    self.addSpecies(speciesName)
                    

        
    def closeEvent(self,event):
        self.rejectEdits()
        
    def updateDialog(self):
        disableFlg=True
        if self.checkMech:
            self.checkMech=False
            newStr=self.MechanismText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newMechList=list()
            deletionList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.mechanisms:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" mechanism Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList:
                        ii=ii+1
                    else:
                       newMechList.append(editStr) 
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList):
                    jj=1
                    for mechStr in self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList:
                        if not mechStr in newStrList:
                            deletionList.append(jj)
                        jj=jj+1
                deletionList.sort(reverse=True)
                for jj in deletionList:
                    self.Mechanism_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList[jj-1]
                for newMechName in newMechList:
                    self.addMechanisms(newMechName,False)
#                    self.mechList.append(newMechName)
#                    self.Mechanism_CB.addItem(newMechName)
                    
                    
        if self.checkReactions:
            self.checkReactions=False
            newStr=self.ReactionsText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newList=list()
            delList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.reactions:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" reaction Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
                        ii=ii+1
                    else:
                        newList.append(editStr)
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList):
                    jj=1
                    for reactionStr in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
                        if not reactionStr in newStrList:
                            delList.append(jj)
                        jj=jj+1
                delList.sort(reverse=True)
                speciesDelList=list()
                for jj in delList:
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList[jj-1])
                    for speciesName in speciesTuple:
                        speciesDelList.append(speciesName)
                speciesDelList=list(set(speciesDelList))
                
                delMechList=list()
                
                for jj in delList:
                    reactionName=self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList[jj-1]
                    for mechName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList:
                        reactionsTuple=self.parent.projWindow.pC.db.getReactionsForMechanism(mechName,mat=self.matName)
                        if reactionName in reactionsTuple:
                            delMechList.append(self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList.index(mechName))
                delMechList=list(set(delMechList))
                delMechList.sort(reverse=True)
                for jj in delMechList:
                    self.Mechanism_CB.removeItem(jj+1)
                    del self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList[jj]
                self.MechanismText_TB.setText(",".join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList))
                    
                for jj in delList:
                    self.Reactions_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList[jj-1]
                for newReactionName in newList:
                    self.addReactions(newReactionName,False)
                
                speciesUpdateList=list()
                for reactionName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
                    speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                    for speciesName in speciesTuple:
                        speciesUpdateList.append(speciesName)
                speciesUpdateList=list(set(speciesUpdateList))
                
                speciesDelIndx=list()
                for speciesName in speciesDelList:
                    if not speciesName in speciesUpdateList:
                        speciesDelIndx.append(self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList.index(speciesName))
                        
                speciesDelIndx.sort(reverse=True)
                for jj in speciesDelIndx:
                    self.PointDefects_CB.removeItem(jj+1)
                    del self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList[jj]
                    
                self.PointDefectsText_TB.setText(",".join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList))
                
                    
#                    self.reactionList.append(newReactionName)
#                    self.Reactions_CB.addItem(newReactionName)
    
        if self.checkSpecies:
            self.checkSpecies=False
            newStr=self.PointDefectsText_TB.text()
            newStrList=newStr.split(',')
            ii=0
            newList=list()
            delList=list()
            for editStr in newStrList:
                if not editStr in self.parent.projWindow.pC.db.species:
                    disableFlg=False
                    QMessageBox.about(self,'warning','"{0}" species Not found.\n\
                                      Please check it\n\
                                      Note: names should be seperated by comma \n\
                                      without any spaces'.format(editStr))
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    break
                else:
                    if editStr in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
                        ii=ii+1
                    else:
                        newList.append(editStr)
            if disableFlg:
                if ii<len(self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList):
                    jj=1
                    for speciesStr in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
                        if not speciesStr in newStrList:
                            delList.append(jj)
                        jj=jj+1
                delList.sort(reverse=True)
                delRemoveList=list()
                for jj in delList:
                    speciesFound=False
                    speciesName=self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList[jj-1]
                    for reactionName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
                        speciesTuple=self.parent.projWindow.pC.db.getSpeciesForReaction(reactionName)
                        if speciesName in speciesTuple:
                            QMessageBox.about(self,'warning','Cannot delete "{0}" \n\
                                              as it is involved in the reaction\n\
                                              {1}'.format(speciesName,reactionName))
                            speciesFound=True
#                            delRemoveList.append(jj)
                            break
                    if speciesFound:
                        delRemoveList.append(jj)
                
                for jj in delRemoveList:
                    delList.remove(jj)
                
                for jj in delList:
                    self.PointDefects_CB.removeItem(jj)
                    del self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList[jj-1]
                for newSpeciesName in newList:
                    self.addSpecies(newSpeciesName,False)
                    
                self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList))
#                    self.speciesList.append(newSpeciesName)
#                    self.PointDefects_CB.addItem(newSpeciesName)
        
        if disableFlg:
            self.applyBotton.setEnabled(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            
#        self.accept()
    def checkMechanisms(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkMech=True
        
    def checkReactions(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkReactions=True
        
    def checkSpecies(self,newStr):
        self.applyBotton.setEnabled(True)
        self.checkSpecies=True
        
    def setCB_and_TB(self):
        for ii in range(self.Mechanism_CB.count()):
            self.Mechanism_CB.removeItem(ii)
        self.Mechanism_CB.addItem('')
        for mechName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList:
            self.Mechanism_CB.addItem(mechName)
        self.MechanismText_TB.setText(','.join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList))
        
        for ii in range(self.Reactions_CB.count()):
            self.Reactions_CB.removeItem(ii)
        self.Reactions_CB.addItem('')
        for reactionName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
            self.Reactions_CB.addItem(reactionName)
        self.ReactionsText_TB.setText(','.join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList))
        
        for ii in range(self.PointDefects_CB.count()):
            self.PointDefects_CB.removeItem(ii)
        self.PointDefects_CB.addItem('')
        for speciesName in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
            self.PointDefects_CB.addItem(speciesName)
        self.PointDefectsText_TB.setText(','.join(self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList))
        
###############################################################################
        
class PVRD_Dlg_Mode3(QDialog):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,Name="",matName="",parent=None):
        super(PVRD_Dlg_Mode3,self).__init__(None)
        self.parent=parent
        self.bX=x1
        self.bY=x2
        self.w=y1
        self.h=y2
        self.name=Name
        self.matName=matName
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        
        self.scrollArea = QScrollArea(self)
#        self.scrollArea.setWidget(self)
#        self.scrollArea.setFixedSize(250, 6000)
        self.scrollArea.setWidgetResizable(True)
        
        self.Name_Label=QLabel("Name:")
        self.Name_TB=QLineEdit("{0}".format(self.name))
        self.Name_TB.setEnabled(False)
        self.Name_Label.setBuddy(self.Name_TB)
        
        self.Mat_Label=QLabel("Material:")
        self.Mat_TB=QLineEdit("{0}".format(self.matName))
        self.Mat_TB.setEnabled(False)
        self.Mat_Label.setBuddy(self.Mat_TB)
        self.Mat_prop_PB=QPushButton("Properties")
#        self.Mat_prop_PB.pWindow=PVRD_PropWindowDlg(0,0,self)
        
        self.X1_Label=QLabel("Bottom X:")
        self.X1_TB=QLineEdit("{0}".format(self.bX))
        self.X1_TB.setEnabled(False)
        self.X1_Label.setBuddy(self.X1_TB)
        
        self.Y1_Label=QLabel("Bottom Y:")
        self.Y1_TB=QLineEdit("{0}".format(self.bY))
        self.Y1_TB.setEnabled(False)
        self.Y1_Label.setBuddy(self.Y1_TB)
        
        self.X2_Label=QLabel("Width:")
        self.X2_TB=QLineEdit("{0}".format(self.w))
        self.X2_TB.setEnabled(False)
        self.X2_Label.setBuddy(self.X2_TB)
        
        self.Y2_Label=QLabel("Height:")
        self.Y2_TB=QLineEdit("{0}".format(self.h))
        self.Y2_TB.setEnabled(False)
        self.Y2_Label.setBuddy(self.Y2_TB)
        
        self.Mechanism_Label=QLabel("Mechanisms:")
        self.Mechanism_CB=QComboBox()
        self.Mechanism_Label.setBuddy(self.Mechanism_CB)
        self.Mechanism_prop_PB=QPushButton("Properties")
        self.Mechanism_prop_PB.setEnabled(False)
#        self.Mechanism_prop_PB.pWindow=PVRD_sim_PropWindow(1,self)
        
        self.Reactions_Label=QLabel("Reactions:")
        self.Reactions_CB=QComboBox()
        self.Reactions_Label.setBuddy(self.Reactions_CB)
        self.Reactions_prop_PB=QPushButton("Properties")
#        self.Reactions_prop_PB.pWindow=PVRD_PropWindowDlg(1,0,self)
        
        self.PointDefects_Label=QLabel("PointDefects:")
        self.PointDefects_CB=QComboBox()
        self.PointDefects_Label.setBuddy(self.PointDefects_CB)
        self.PointDefects_prop_PB=QPushButton("Properties")
#        self.PointDefects_prop_PB.pWindow=PVRD_PropWindowDlg(2,0,self)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Apply|
                                          QDialogButtonBox.Cancel)
        self.qInfoWidget=latexQLabel("Information")
        
    def layout_widgets(self):
        row=0
        
        viewPort=QWidget(self)
        self.scrollArea.setWidget(viewPort)
        
        vLayout=QVBoxLayout()
        viewPort.setLayout(vLayout)
        
        layout = QGridLayout()
        
        layout.addWidget(self.Name_Label, row, 0)
        layout.addWidget(self.Name_TB, row, 1,1,2)
        
        row=row+1
        layout.addWidget(self.Mat_Label, row, 0)
        layout.addWidget(self.Mat_TB, row, 1,1,2)
        layout.addWidget(self.Mat_prop_PB, row, 3,1,1)
        
        row=row+1
        layout.addWidget(self.X1_Label, row, 0)
        layout.addWidget(self.X1_TB, row, 1)
        layout.addWidget(self.X2_Label, row, 2)
        layout.addWidget(self.X2_TB, row, 3)
        
        row=row+1
        layout.addWidget(self.Y1_Label, row, 0)
        layout.addWidget(self.Y1_TB, row, 1)
        layout.addWidget(self.Y2_Label, row, 2)
        layout.addWidget(self.Y2_TB, row, 3)
        
        row=row+1
        layout.addWidget(self.Mechanism_Label, row, 0)
        layout.addWidget(self.Mechanism_CB, row, 1,1,2)
        layout.addWidget(self.Mechanism_prop_PB, row, 3,1,1)
        
        row=row+1
        layout.addWidget(self.Reactions_Label, row, 0)
        layout.addWidget(self.Reactions_CB, row, 1,1,2)
        layout.addWidget(self.Reactions_prop_PB, row, 3,1,1)
        
        row=row+1
        layout.addWidget(self.PointDefects_Label, row, 0)
        layout.addWidget(self.PointDefects_CB, row, 1,1,2)
        layout.addWidget(self.PointDefects_prop_PB, row, 3,1,1)
        
        row=row+1
        layout.addWidget(self.buttonBox, row, 1, 1, 3)
        
#        row=row+1
        vLayout.addLayout(layout)
        vLayout.addWidget(self.qInfoWidget)
        vLayout.addStretch(1)
        
        vlayout=QVBoxLayout(self)
        vlayout.addWidget(self.scrollArea)
#        vlayout.addStretch(1)s
        
#        vlayout.addWidget(self.scrollArea)
        self.setLayout(vlayout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Simulation Setup Properties Dialog")
        
        self.Mechanism_CB.currentIndexChanged[int].connect(self.mechUpdateInfoDisplay)
        self.Reactions_CB.currentIndexChanged[int].connect(self.reactionUpdateInfoDisplay)
        self.PointDefects_CB.currentIndexChanged[int].connect(self.speciesUpdateInfoDisplay)
        self.Mat_prop_PB.clicked.connect(self.openPropWindow)
        self.Reactions_prop_PB.clicked.connect(self.openPropWindow)
        self.PointDefects_prop_PB.clicked.connect(self.openPropWindow)
        
    def openPropWindow(self):
        pb=self.sender()
        pb.pWindow.show()
#        pb.pWindow.raise_()
        
    def mechUpdateInfoDisplay(self,indx):
        if indx >0:
#            QMessageBox.about(self,'warning','indx= "{0}"'.format(indx))
            mechName=self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList[indx-1]
            mechDescription=self.parent.projWindow.pC.db.getMechInfo(mechName,self.matName)
            mechDescription=mechDescription.replace(r"<=>","\\rightleftharpoons")
#            QMessageBox.about(self,'warning','r= "{0}"'.format(qq))
            allStr='\n Mechanism Information\n\n'+mechDescription
            self.qInfoWidget.updateText(allStr)
        else:
            self.qInfoWidget.updateText("Information")
    
    def reactionUpdateInfoDisplay(self,indx):
        if indx > 0:
            reactionName=self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList[indx-1]
            reactionDescription=self.parent.projWindow.pC.db.getReactionInfo(reactionName,self.matName)
#            QMessageBox.about(self,'warning','indx= "{0}"'.format(reactionDescription))
            self.qInfoWidget.updateText(reactionDescription)
        else:
            self.qInfoWidget.updateText("Information")
    def speciesUpdateInfoDisplay(self,indx):
        if indx > 0:
            speciesName=self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList[indx-1]
            speciesDescription=self.parent.projWindow.pC.db.getSpeciesInfo(speciesName,self.matName)
            self.qInfoWidget.updateText(speciesDescription)
        else:
            self.qInfoWidget.updateText("Information")

            
###############################################################################
class PVRD_RectangleDlg_Mode3(PVRD_Dlg_Mode3):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,Name="",matName="",parent=None):
        super(PVRD_RectangleDlg_Mode3,self).__init__(x1,y1,x2,y2,Name,matName,parent)
        self.Mat_prop_PB.pWindow=PVRD_PropWindowDlg(0,0,self)
        self.Reactions_prop_PB.pWindow=PVRD_PropWindowDlg(1,0,self)
        self.PointDefects_prop_PB.pWindow=PVRD_PropWindowDlg(2,0,self)
        
    def updateDialog(self,isInit=False):
        self.Mechanism_CB.addItem('')
        for mech in self.parent.projWindow.pC.allRectList[self.parent.pCindx].mechList:
            self.Mechanism_CB.addItem(mech)

        self.Reactions_CB.addItem('')
        for mech in self.parent.projWindow.pC.allRectList[self.parent.pCindx].reactionList:
            self.Reactions_CB.addItem(mech)

        self.PointDefects_CB.addItem('')
        for mech in self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList:
            self.PointDefects_CB.addItem(mech)
        
        self.Mat_prop_PB.pWindow.resetPCdata(isInit)
        self.Reactions_prop_PB.pWindow.resetPCdata(isInit)
        self.PointDefects_prop_PB.pWindow.resetPCdata(isInit)
        
class PVRD_LineDlg_Mode3(PVRD_Dlg_Mode3):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,Name="",matName="",parent=None):
        super(PVRD_LineDlg_Mode3,self).__init__(x1,y1,x2,y2,Name,matName,parent)
        
        self.X1_Label=QLabel("X1:")
        self.Y1_Label=QLabel("Y1:")
        self.X2_Label=QLabel("X2:")
        self.Y2_Label=QLabel("Y2:")
        
        self.Mat_prop_PB.pWindow=PVRD_PropWindowDlg(0,1,self)
        self.Reactions_prop_PB.pWindow=PVRD_PropWindowDlg(1,1,self)
        self.PointDefects_prop_PB.pWindow=PVRD_PropWindowDlg(2,1,self)
        
    def updateDialog(self,isInit=False):
        self.Mechanism_CB.addItem('')
        for mech in self.parent.projWindow.pC.allLineList[self.parent.pCindx].mechList:
            self.Mechanism_CB.addItem(mech)

        self.Reactions_CB.addItem('')
        for mech in self.parent.projWindow.pC.allLineList[self.parent.pCindx].reactionList:
            self.Reactions_CB.addItem(mech)

        self.PointDefects_CB.addItem('')
        for mech in self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList:
            self.PointDefects_CB.addItem(mech)
            
        self.Mat_prop_PB.pWindow.resetPCdata(isInit)
        self.Reactions_prop_PB.pWindow.resetPCdata(isInit)
        self.PointDefects_prop_PB.pWindow.resetPCdata(isInit)
        
class PVRD_PointDlg_Mode3(PVRD_Dlg_Mode3):
    def __init__(self,x1=0,y1=0,Name="",matName="",parent=None):
        super(PVRD_PointDlg_Mode3,self).__init__(x1,y1,x1,y1,Name,matName,parent)
        
        self.X1_Label=QLabel("X1:")
        self.Y1_Label=QLabel("Y1:")

        self.X2_Label.hide()
        self.X2_TB.hide()
        self.Y2_Label.hide()
        self.Y2_TB.hide()
        
        self.Mat_prop_PB.pWindow=PVRD_PropWindowDlg(0,2,self)
        self.Reactions_prop_PB.pWindow=PVRD_PropWindowDlg(1,2,self)
        self.PointDefects_prop_PB.pWindow=PVRD_PropWindowDlg(2,2,self)        
        
    def updateDialog(self,isInit=False):
        self.Mechanism_CB.addItem('')
        for mech in self.parent.projWindow.pC.allPointList[self.parent.pCindx].mechList:
            self.Mechanism_CB.addItem(mech)

        self.Reactions_CB.addItem('')
        for mech in self.parent.projWindow.pC.allPointList[self.parent.pCindx].reactionList:
            self.Reactions_CB.addItem(mech)

        self.PointDefects_CB.addItem('')
        for mech in self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList:
            self.PointDefects_CB.addItem(mech)
            
        self.Mat_prop_PB.pWindow.resetPCdata(isInit)
        self.Reactions_prop_PB.pWindow.resetPCdata(isInit)
        self.PointDefects_prop_PB.pWindow.resetPCdata(isInit)
    
###############################################################################
            
class PVRD_PropWindowDlg(QDialog):
    def __init__(self,propType=0, objType=0, parent=None):
        super(PVRD_PropWindowDlg, self).__init__(parent)
        self.propType=propType
        self.root=parent.parent
        self.objType=objType
        
        if (objType==0):
            self.allList=self.root.projWindow.pC.allRectList
            self.root.projWindow.pC.db.updateProjMatModelData(self.allList[self.root.pCindx])
            self.root.projWindow.pC.db.updateProjSpeciesModelData(self.allList[self.root.pCindx])
            self.root.projWindow.pC.db.updateProjReactionModelData(self.allList[self.root.pCindx])
        
        if (objType==1):
            self.allList=self.root.projWindow.pC.allLineList
            self.root.projWindow.pC.db.updateProjMatModelData(self.allList[self.root.pCindx])
            self.root.projWindow.pC.db.updateProjSpeciesModelData(self.allList[self.root.pCindx])
            self.root.projWindow.pC.db.updateProjReactionModelData(self.allList[self.root.pCindx])
            
        if (objType==2):
            self.allList=self.root.projWindow.pC.allPointList
            self.root.projWindow.pC.db.updateProjMatModelData(self.allList[self.root.pCindx])
            self.root.projWindow.pC.db.updateProjSpeciesModelData(self.allList[self.root.pCindx])
            self.root.projWindow.pC.db.updateProjReactionModelData(self.allList[self.root.pCindx])
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        if self.propType==0: # For Material Properties
            self.Mat_Label=QLabel("Properties of the Material {0}:".format(self.allList[self.root.pCindx].matName))
            
            self.matFormEnergy=QLabel("Formation Energy: {0}".format(self.allList[self.root.pCindx].matPropData.formEnergy))
            
            self.cationChemPot_Label=QLabel("Cation Chemical Potential:")
            self.cationChemPot_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.cationChemPot))
            self.cationChemPot_Label.setBuddy(self.cationChemPot_TB)
            
            self.cationVacancy_Label=QLabel("Cation Vacancy Concentration(neutral):")
            self.cationVacancy_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.cationVacancy))
            self.cationVacancy_Label.setBuddy(self.cationVacancy_TB)
            
            self.anionVacancy_Label=QLabel("Anion Vacancy Concentration(neutral):")
            self.anionVacancy_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.anionVacancy))
            self.anionVacancy_Label.setBuddy(self.anionVacancy_TB)
            
            self.eMass_Label=QLabel("Electron Effective Mass:")
            self.eMass_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.eEffMass))
            self.eMass_Label.setBuddy(self.eMass_TB)
            
            self.hMass_Label=QLabel("Hole Effective Mass:")
            self.hMass_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.hEffMass))
            self.hMass_Label.setBuddy(self.hMass_TB)
            
            self.latDen_Label=QLabel("Lattice Density [1/(cm^3)]:")
            self.latDen_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.latDen))
            self.latDen_Label.setBuddy(self.latDen_TB)
            
            self.afnity_Label=QLabel("Electron Affinity:")
            self.afnity_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.elecAff))
            self.afnity_Label.setBuddy(self.afnity_TB)
            
            self.dielec_Label=QLabel("Dielectric Constant:")
            self.dielec_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.dielecConst))
            self.dielec_Label.setBuddy(self.dielec_TB)
            
            self.radRate_Label=QLabel("Radiative Rate Constant [1/(cm^3 s)]:")
            self.radRate_TB=QLineEdit("{0}".format(self.allList[self.root.pCindx].matPropData.radRateConst))
            self.radRate_Label.setBuddy(self.afnity_TB)
            
            self.bgModel_Label=QLabel("Band Gap Model:")
            self.bgModel_CB=QComboBox()
            for bgName in self.root.projWindow.pC.db.bgModels:
                self.bgModel_CB.addItem(bgName)
            self.bgModel_Label.setBuddy(self.bgModel_CB)
            bgName=self.allList[self.root.pCindx].matPropData.bgModelName
            indx = self.root.projWindow.pC.db.bgModels.index(bgName)
            self.bgModel_CB.setCurrentIndex(indx)
            
            # Model change in the Project is not supported now.
            # Will be implemented in future versions
            
            # Model change implementation Require
            self.bgModel_CB.setEnabled(False) 
            
            self.bgParam_Label_list=list()
            self.bgParam_TB_list=list()
            
            parList=parseString(self.root.projWindow.pC.db.bgModelsParList[indx])
            parValList=parseString(self.allList[self.root.pCindx].matPropData.bgPar)
            
            ii=0
            for parName in parList:
                label=QLabel("{0}:".format(parName))
                TB=QLineEdit("{0}".format(parValList[ii]))
                label.setBuddy(TB)
                self.bgParam_Label_list.append(label)
                self.bgParam_TB_list.append(TB)
                ii=ii+1
            
            self.bgVal300_Label=QLabel("Band Gap (eV) @ 300K :")
            self.bgVal300_TB=QLineEdit("{0:.4f}".format(self.allList[self.root.pCindx].matPropData.bg(300)))
#            self.bgVal300_TB=QLineEdit("temp")
            self.bgVal300_Label.setBuddy(self.bgVal300_TB)
            self.bgVal300_TB.setEnabled(False)
            
            self.eMobModel_Label=QLabel("Electron Mobility Model:")
            self.eMobModel_CB=QComboBox()
            for eMobName in self.root.projWindow.pC.db.freeCarrMobModels:
                self.eMobModel_CB.addItem(eMobName)
            self.eMobModel_Label.setBuddy(self.eMobModel_CB)
            eMobName=self.allList[self.root.pCindx].matPropData.eMobName
            indx = self.root.projWindow.pC.db.freeCarrMobModels.index(eMobName)
            self.eMobModel_CB.setCurrentIndex(indx)
            # Model change implementation Require
            self.eMobModel_CB.setEnabled(False) 
            
            self.eMobParam_Label_list=list()
            self.eMobParam_TB_list=list()
            
            parList=parseString(self.root.projWindow.pC.db.freeCarrMobModelsParList[indx])
            parValList=parseString(self.allList[self.root.pCindx].matPropData.eMobPar)
            
            ii=0
            for parName in parList:
                label=QLabel("{0}:".format(parName))
                TB=QLineEdit("{0}".format(parValList[ii]))
                label.setBuddy(TB)
                self.eMobParam_Label_list.append(label)
                self.eMobParam_TB_list.append(TB)
                ii=ii+1
            
            self.eMobVal300_Label=QLabel("Electron Mobility (cm^2/Vs) @ 300K :")
            self.eMobVal300_TB=QLineEdit("{0:.2f}".format(self.allList[self.root.pCindx].matPropData.eMob(300)))
            self.eMobVal300_Label.setBuddy(self.eMobVal300_TB)
            self.eMobVal300_TB.setEnabled(False)
            
            self.hMobModel_Label=QLabel("Hole Mobility Model:")
            self.hMobModel_CB=QComboBox()
            for hMobName in self.root.projWindow.pC.db.freeCarrMobModels:
                self.hMobModel_CB.addItem(hMobName)
            self.hMobModel_Label.setBuddy(self.hMobModel_CB)
            hMobName=self.allList[self.root.pCindx].matPropData.hMobName
            indx = self.root.projWindow.pC.db.freeCarrMobModels.index(hMobName)
            self.hMobModel_CB.setCurrentIndex(indx)
            # Model change implementation Require
            self.hMobModel_CB.setEnabled(False) 
            
            self.hMobParam_Label_list=list()
            self.hMobParam_TB_list=list()
            
            parList=parseString(self.root.projWindow.pC.db.freeCarrMobModelsParList[indx])
            parValList=parseString(self.allList[self.root.pCindx].matPropData.hMobPar)
            
            ii=0
            for parName in parList:
                label=QLabel("{0}:".format(parName))
                TB=QLineEdit("{0}".format(parValList[ii]))
                label.setBuddy(TB)
                self.hMobParam_Label_list.append(label)
                self.hMobParam_TB_list.append(TB)
                ii=ii+1
            
            self.hMobVal300_Label=QLabel("Hole Mobility (cm^2/Vs) @ 300K :")
            self.hMobVal300_TB=QLineEdit("{0:.2f}".format(self.allList[self.root.pCindx].matPropData.hMob(300)))
            self.hMobVal300_Label.setBuddy(self.hMobVal300_TB)
            self.hMobVal300_TB.setEnabled(False)
            
            self.photoAbsorpModel_Label=QLabel("Photo Absorption Coefficient Model:")
            self.photoAbsorpModel_TB=QLineEdit("Not Supported Now")
            self.photoAbsorpModel_Label.setBuddy(self.photoAbsorpModel_TB)
            self.photoAbsorpModel_TB.setEnabled(False)
            
        if self.propType==1:
            self.Mat_Label=QLabel("Properties of Reactions in the Material {0}:".format(self.allList[self.root.pCindx].matName))
            
            self.reactionName_Label_list=list()
            self.reactionModel_CB_list=list()
            self.reactionParamLabelList=list()
            self.reactionParamTBList=list()
            ii=0
            for reaction in self.allList[self.root.pCindx].reactionList:
                rLatex=reaction.replace(r"<=>","\\rightleftharpoons")
                label=latexQLabel("test")
                label.updateText('$ '+rLatex+' $')
                CB=QComboBox()
                CB.addItems(self.root.projWindow.pC.db.reactionRateModels)
                rPropData=self.allList[self.root.pCindx].reactionPropDataList[ii]
                rModel=rPropData.rateModel
                indx=self.root.projWindow.pC.db.reactionRateModels.index(rModel)
                CB.setCurrentIndex(indx)
                # Model change implementation Require
                CB.setEnabled(False) 
                
                pName=self.root.projWindow.pC.db.reactionRateModelsParList[indx]
                pNPar=self.root.projWindow.pC.db.reactionRateModelsnParList[indx]
                
                pNameVal=parseString(pName)
                pVal=parseString(rPropData.rateParList)
                jj=0
                tempLabelList=list()
                tempTBList=list()
                while jj<pNPar:
                    pLabel=QLabel(pNameVal[jj])
                    TB=QLineEdit(pVal[jj])
                    tempLabelList.append(pLabel)
                    tempTBList.append(TB)
                    jj=jj+1
                
                if pName is None:
                    pLabel=QLabel("")
                    TB=QLabel("")
                    tempLabelList.append(pLabel)
                    tempTBList.append(TB)
                
                self.reactionName_Label_list.append(label)
                self.reactionModel_CB_list.append(CB)
                self.reactionParamLabelList.append(tempLabelList)
                self.reactionParamTBList.append(tempTBList)
                
                ii=ii+1
                
        if self.propType==2:
            self.Mat_Label=QLabel("Properties of Species in the Material {0}:".format(self.allList[self.root.pCindx].matName))
            
            self.speciesLabelList=list()
            self.speciesDiffModelList=list()
            self.speciesDiffParamLabelList=list()
            self.speciesDiffParamTBList=list()
            
            self.speciesSiteDenModelList=list()
            self.speciesSiteDenParamLabelList=list()
            self.speciesSiteDenParamTBList=list()
            
            self.speciesFormEnergyModelList=list()
            self.speciesFormEnergyParamLabelList=list()
            self.speciesFormEnergyParamTBList=list()
            
            DiffModelList=self.root.projWindow.pC.db.speciesDiffModels
            SiteDenModelList=self.root.projWindow.pC.db.speciesSiteDenModels
            FormEnergyModelList=self.root.projWindow.pC.db.speciesFormEnergyModels
            
            ii=0
            speciesPropList=self.allList[self.root.pCindx].speciesPropDataList
            for species in self.allList[self.root.pCindx].speciesList:
                label=latexQLabel("test")
                label.updateText('$ '+species+' $')
                
                speciesDiffModelName=speciesPropList[ii].diffModel
                CB=QComboBox()
                CB.addItems(DiffModelList)
                indx=DiffModelList.index(speciesDiffModelName)
                CB.setCurrentIndex(indx)
                # Model change implementation Require
                CB.setEnabled(False) 
                pName=self.root.projWindow.pC.db.speciesDiffModelsParList[indx]
                pNPar=self.root.projWindow.pC.db.speciesDiffModelsnParList[indx]
                
                pNameVal=parseString(pName)
                pVal=parseString(speciesPropList[ii].diffParList)
                jj=0
                tempLabelList=list()
                tempTBList=list()
                while jj<pNPar:
                    pLabel=QLabel(pNameVal[jj])
                    TB=QLineEdit(pVal[jj])
                    tempLabelList.append(pLabel)
                    tempTBList.append(TB)
                    jj=jj+1
                
                if pName is None:
                    pLabel=QLabel("")
                    TB=QLabel("")
                    tempLabelList.append(pLabel)
                    tempTBList.append(TB)
                
                self.speciesLabelList.append(label)
                self.speciesDiffModelList.append(CB)
                self.speciesDiffParamLabelList.append(tempLabelList)
                self.speciesDiffParamTBList.append(tempTBList)
                
                speciesSiteDenModelName=speciesPropList[ii].siteDenModel
                CB=QComboBox()
                CB.addItems(SiteDenModelList)
                indx = SiteDenModelList.index(speciesSiteDenModelName)
                CB.setCurrentIndex(indx)
                # Model change implementation Require
                CB.setEnabled(False) 
                pName=self.root.projWindow.pC.db.speciesSiteDenModelsParList[indx]
                pNPar=self.root.projWindow.pC.db.speciesSiteDenModelsnParList[indx]
                
                pNameVal=parseString(pName)
                pVal=parseString(speciesPropList[ii].siteDenParList)
                jj=0
                tempLabelList=list()
                tempTBList=list()
                while jj<pNPar:
                    pLabel=QLabel(pNameVal[jj])
                    TB=QLineEdit(pVal[jj])
                    tempLabelList.append(pLabel)
                    tempTBList.append(TB)
                    jj=jj+1
                
                if pName is None:
                    pLabel=QLabel("")
                    TB=QLabel("")
                    tempLabelList.append(pLabel)
                    tempTBList.append(TB)
                
                self.speciesSiteDenModelList.append(CB)
                self.speciesSiteDenParamLabelList.append(tempLabelList)
                self.speciesSiteDenParamTBList.append(tempTBList)

                speciesFormEnergyModelName=speciesPropList[ii].formEnergyModel                
                CB=QComboBox()
                CB.addItems(FormEnergyModelList)
                indx=FormEnergyModelList.index(speciesFormEnergyModelName)
                CB.setCurrentIndex(indx)
                # Model change implementation Require
                CB.setEnabled(False) 
                pName=self.root.projWindow.pC.db.speciesSiteDenModelsParList[indx]
                pNPar=self.root.projWindow.pC.db.speciesSiteDenModelsnParList[indx]
                
                pNameVal=parseString(pName)
                pVal=list()
                if speciesPropList[ii].formEnergyParList is not None:
                    pVal=ast.literal_eval(speciesPropList[ii].formEnergyParList)
                
                # Should form our own parameter Name and values
                pNPar=len(pVal)
                
                jj=0
                tempLabelList=list()
                tempTBList=list()
                while jj<pNPar:
                    if jj==0:
                        pLabel=QLabel('G0')
                        TB=QLineEdit('{0}'.format(pVal[jj]))
                    else:
                        val=pVal[jj][0]
                        vbStr=''
                        if pVal[jj][1]==1:
                            vbStr=' (wrt VB)'
                        elif pVal[jj][1]==-1:
                            vbStr=' (wrt CB)'
                        pLabel=QLabel('E'+str(jj)+vbStr)
                        TB=QLineEdit('{0}'.format(val))
                    tempLabelList.append(pLabel)
                    tempTBList.append(TB)
                    jj=jj+1
                
                self.speciesFormEnergyModelList.append(CB)
                self.speciesFormEnergyParamLabelList.append(tempLabelList)
                self.speciesFormEnergyParamTBList.append(tempTBList)
                
                ii=ii+1
                
#            self.speciesCB=QCombobox()
#            self.speciesCB.addItems()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Apply|
                                          QDialogButtonBox.Cancel|
                                          QDialogButtonBox.Reset)
        
    def layout_widgets(self):
        viewPort=QWidget(self)
        self.scrollArea.setWidget(viewPort)
        
        vLayout=QVBoxLayout()
        viewPort.setLayout(vLayout)
        
        row=0
        
        layout = QGridLayout()
        if self.propType==0:
            layout.addWidget(self.Mat_Label, row, 0,1,4)
            
            row=row+1
            layout.addWidget(self.matFormEnergy,row,0,1,4)
            
            row=row+1
            layout.addWidget(self.cationChemPot_Label, row, 0,1,2)
            layout.addWidget(self.cationChemPot_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.cationVacancy_Label, row, 0,1,2)
            layout.addWidget(self.cationVacancy_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.anionVacancy_Label, row, 0,1,2)
            layout.addWidget(self.anionVacancy_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.eMass_Label, row, 0,1,2)
            layout.addWidget(self.eMass_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.hMass_Label, row, 0,1,2)
            layout.addWidget(self.hMass_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.latDen_Label, row, 0,1,2)
            layout.addWidget(self.latDen_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.afnity_Label, row, 0,1,2)
            layout.addWidget(self.afnity_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.dielec_Label, row, 0,1,2)
            layout.addWidget(self.dielec_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.radRate_Label, row, 0,1,2)
            layout.addWidget(self.radRate_TB, row, 3,1,2)
            
            row=row+1
            layout.addWidget(self.bgModel_Label, row, 0,1,2)
            layout.addWidget(self.bgModel_CB, row, 3,1,2)
            
            ii=0
            for label in self.bgParam_Label_list:
                row=row+1
                layout.addWidget(self.bgParam_Label_list[ii],row,0,1,2)
                layout.addWidget(self.bgParam_TB_list[ii],row,3,1,2)
                ii=ii+1
                
            row=row+1
            layout.addWidget(self.bgVal300_Label,row,0,1,2)
            layout.addWidget(self.bgVal300_TB,row,3,1,2)
            
            row=row+1
            layout.addWidget(self.eMobModel_Label, row, 0,1,2)
            layout.addWidget(self.eMobModel_CB, row, 3,1,2)
            
            ii=0
            for label in self.eMobParam_Label_list:
                row=row+1
                layout.addWidget(self.eMobParam_Label_list[ii],row,0,1,2)
                layout.addWidget(self.eMobParam_TB_list[ii],row,3,1,2)
                ii=ii+1
                
            row=row+1
            layout.addWidget(self.eMobVal300_Label,row,0,1,2)
            layout.addWidget(self.eMobVal300_TB,row,3,1,2)
            
            row=row+1
            layout.addWidget(self.hMobModel_Label, row, 0,1,2)
            layout.addWidget(self.hMobModel_CB, row, 3,1,2)
            
            ii=0
            for label in self.hMobParam_Label_list:
                row=row+1
                layout.addWidget(self.hMobParam_Label_list[ii],row,0,1,2)
                layout.addWidget(self.hMobParam_TB_list[ii],row,3,1,2)
                ii=ii+1
                
            row=row+1
            layout.addWidget(self.hMobVal300_Label,row,0,1,2)
            layout.addWidget(self.hMobVal300_TB,row,3,1,2)
            
            row=row+1
            layout.addWidget(self.photoAbsorpModel_Label,row,0,1,2)
            layout.addWidget(self.photoAbsorpModel_TB,row,3,1,2)
        
        if self.propType==1:
            layout.addWidget(self.Mat_Label, row, 0,1,4)
            
            ii=0
            for label in self.reactionName_Label_list:
                row=row+1
                layout.addWidget(self.reactionName_Label_list[ii],row,0,1,2)
                layout.addWidget(self.reactionModel_CB_list[ii],row,3,1,1)
                
                jj=0
                for label1 in self.reactionParamLabelList[ii]:
                    pLabel=self.reactionParamLabelList[ii][jj]
                    TB=self.reactionParamTBList[ii][jj]
                    layout.addWidget(pLabel,row+jj,4,1,1)
                    layout.addWidget(TB,row+jj,5,1,1)
                    jj=jj+1
                
                row=row+jj-1
                
                ii=ii+1
        
        if self.propType==2:
            layout.addWidget(self.Mat_Label, row, 0,1,4)
            
            row=row+1
            layout.addWidget(QLabel("Species"),row,0,1,1)
            layout.addWidget(QLabel("Diffusion"),row,1,1,3)
            layout.addWidget(QLabel("Site Density"),row,4,1,3)
            layout.addWidget(QLabel("Formation Energy"),row,7,1,3)
            
            row=row+1
            layout.addWidget(QLabel("Name"),row,0,1,1)
            layout.addWidget(QLabel("Model"),row,1,1,1)
            layout.addWidget(QLabel("Param"),row,2,1,2)
            layout.addWidget(QLabel("Model"),row,4,1,1)
            layout.addWidget(QLabel("Param"),row,5,1,2)
            layout.addWidget(QLabel("Model"),row,7,1,1)
            layout.addWidget(QLabel("Param"),row,8,1,2)
            
            
            ii=0
            for sLabel in self.speciesLabelList:
                row=row+1
                layout.addWidget(self.speciesLabelList[ii],row,0,1,1)
                
                layout.addWidget(self.speciesDiffModelList[ii],row,1,1,1)
                
                
                layout.addWidget(self.speciesSiteDenModelList[ii],row,4,1,1)
                
                layout.addWidget(self.speciesFormEnergyModelList[ii],row,7,1,1)
                
                jj=0
                for label in self.speciesDiffParamLabelList[ii]:
                    pLabel=self.speciesDiffParamLabelList[ii][jj]
                    TB=self.speciesDiffParamTBList[ii][jj]
                    layout.addWidget(pLabel,row+jj,2,1,1)
                    layout.addWidget(TB,row+jj,3,1,1)
                    jj=jj+1
                
                jj=0
                for label in self.speciesSiteDenParamLabelList[ii]:
                    pLabel=self.speciesSiteDenParamLabelList[ii][jj]
                    TB=self.speciesSiteDenParamTBList[ii][jj]
                    layout.addWidget(pLabel,row+jj,5,1,1)
                    layout.addWidget(TB,row+jj,6,1,1)
                    jj=jj+1
                    
                jj=0
                for label in self.speciesFormEnergyParamLabelList[ii]:
                    pLabel=self.speciesFormEnergyParamLabelList[ii][jj]
                    TB=self.speciesFormEnergyParamTBList[ii][jj]
                    layout.addWidget(pLabel,row+jj,8,1,1)
                    layout.addWidget(TB,row+jj,9,1,1)
                    jj=jj+1
                rowAdd=max(len(self.speciesDiffParamLabelList[ii]),
                           len(self.speciesSiteDenParamLabelList[ii]),
                           len(self.speciesFormEnergyParamLabelList[ii])
                           )-1
                row=row+rowAdd
                
                ii=ii+1
                
                
        
        row=row+1
        if self.propType==0:
            layout.addWidget(self.buttonBox, row, 1, 1, 4)
        elif self.propType==1:
            layout.addWidget(self.buttonBox, row, 3, 1, 4)
        elif self.propType==2:
            layout.addWidget(self.buttonBox, row, 6, 1, 4)
        
        vLayout.addLayout(layout)
#        vLayout.addWidget(self.qInfoWidget)
        vLayout.addStretch(1)
        
        vlayout=QVBoxLayout(self)
        vlayout.addWidget(self.scrollArea)

        self.setLayout(vlayout)
        
    def create_connections(self):
        if self.propType==0:
            self.setWindowTitle("Simulation Setup Material Properties Dialog")
        if self.propType==1:
            self.setWindowTitle("Simulation Setup Reaction Properties Dialog")
        if self.propType==2:
            self.setWindowTitle("Simulation Setup Species Properties Dialog")
            
        self.buttonBox.accepted.connect(self.updatePCdata)
        applyBtn=self.buttonBox.button(QDialogButtonBox.Apply)
        applyBtn.clicked.connect(self.updatePCdata)
        resetBtn=self.buttonBox.button(QDialogButtonBox.Reset)
        resetBtn.clicked.connect(self.resetPCdata)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        
    def updatePCdata(self):
#        QMessageBox.about(self,'warning',"In update PC method")
        if self.propType==0:
            if float(self.cationChemPot_TB.text())!=self.allList[self.root.pCindx].matPropData.cationChemPot:
                self.allList[self.root.pCindx].matPropData.cationChemPot=float(self.cationChemPot_TB.text())
            if float(self.cationVacancy_TB.text())!=self.allList[self.root.pCindx].matPropData.cationVacancy:
                self.allList[self.root.pCindx].matPropData.cationVacancy=float(self.cationVacancy_TB.text())
            if float(self.anionVacancy_TB.text())!=self.allList[self.root.pCindx].matPropData.anionVacancy:
                self.allList[self.root.pCindx].matPropData.anionVacancy=float(self.anionVacancy_TB.text())
            if float(self.eMass_TB.text())!=self.allList[self.root.pCindx].matPropData.eEffMass:
                self.allList[self.root.pCindx].matPropData.eEffMass=float(self.eMass_TB.text())
            if float(self.hMass_TB.text())!=self.allList[self.root.pCindx].matPropData.hEffMass:
                self.allList[self.root.pCindx].matPropData.hEffMass=float(self.hMass_TB.text())
            if float(self.latDen_TB.text())!=self.allList[self.root.pCindx].matPropData.latDen:
                self.allList[self.root.pCindx].matPropData.latDen=float(self.latDen_TB.text())
            if float(self.afnity_TB.text())!=self.allList[self.root.pCindx].matPropData.elecAff:
                self.allList[self.root.pCindx].matPropData.elecAff=float(self.afnity_TB.text())
            if float(self.dielec_TB.text())!=self.allList[self.root.pCindx].matPropData.dielecConst:
                self.allList[self.root.pCindx].matPropData.dielecConst=float(self.dielec_TB.text())
            if float(self.radRate_TB.text())!=self.allList[self.root.pCindx].matPropData.radRateConst:
                self.allList[self.root.pCindx].matPropData.radRateConst=float(self.radRate_TB.text())
                
            parValList=parseString(self.allList[self.root.pCindx].matPropData.bgPar)
#            QMessageBox.about(self,'warning',"bgPar={0}".format(self.allList[self.root.pCindx].matPropData.bgPar))
            ii=0
            for parVal in parValList:
                if float(self.bgParam_TB_list[ii].text())!=float(parValList[ii]):
                    parValList[ii]=self.bgParam_TB_list[ii].text()
                ii=ii+1
            self.allList[self.root.pCindx].matPropData.bgPar=restoreString(parValList)
            
            parValList=parseString(self.allList[self.root.pCindx].matPropData.eMobPar)
            ii=0
            for parVal in parValList:
                if float(self.eMobParam_TB_list[ii].text())!=float(parValList[ii]):
                    parValList[ii]=self.eMobParam_TB_list[ii].text()
                ii=ii+1
            self.allList[self.root.pCindx].matPropData.eMobPar=restoreString(parValList)
            
            parValList=parseString(self.allList[self.root.pCindx].matPropData.hMobPar)
            ii=0
            for parVal in parValList:
                if float(self.hMobParam_TB_list[ii].text())!=float(parValList[ii]):
                    parValList[ii]=self.hMobParam_TB_list[ii].text()
                ii=ii+1
            self.allList[self.root.pCindx].matPropData.hMobPar=restoreString(parValList)
            
        if self.propType==1:
            ii=0
            for reaction in self.allList[self.root.pCindx].reactionList:
                rPropData=self.allList[self.root.pCindx].reactionPropDataList[ii]
                rModel=rPropData.rateModel
                indx=self.root.projWindow.pC.db.reactionRateModels.index(rModel)
                
                pNPar=self.root.projWindow.pC.db.reactionRateModelsnParList[indx]                
                pVal=parseString(rPropData.rateParList)
                
                jj=0
                while jj<pNPar:
                    if float(self.reactionParamTBList[ii][jj].text())!=float(pVal[jj]):
                        pVal[jj]=self.reactionParamTBList[ii][jj].text()
                    jj=jj+1
#                QMessageBox.about(self,'warning',"pVal={0}".format(pVal))    
                self.allList[self.root.pCindx].reactionPropDataList[ii].rateParList=restoreString(pVal)
                ii=ii+1
        
        if self.propType==2:
            ii=0
            DiffModelList=self.root.projWindow.pC.db.speciesDiffModels
            SiteDenModelList=self.root.projWindow.pC.db.speciesSiteDenModels
#            FormEnergyModelList=self.root.projWindow.pC.db.speciesFormEnergyModels
            speciesPropList=self.allList[self.root.pCindx].speciesPropDataList
            for species in self.allList[self.root.pCindx].speciesList:
                speciesDiffModelName=speciesPropList[ii].diffModel
                indx=DiffModelList.index(speciesDiffModelName)
                pNPar=self.root.projWindow.pC.db.speciesDiffModelsnParList[indx]
                pVal=parseString(speciesPropList[ii].diffParList)
                jj=0
                while jj<pNPar:
                    if float(self.speciesDiffParamTBList[ii][jj].text())!=float(pVal[jj]):
                        pVal[jj]=self.speciesDiffParamTBList[ii][jj].text()
                    jj=jj+1
                self.allList[self.root.pCindx].speciesPropDataList[ii].diffParList=restoreString(pVal)
                
                speciesSiteDenModelName=speciesPropList[ii].siteDenModel
                indx = SiteDenModelList.index(speciesSiteDenModelName)
                pNPar=self.root.projWindow.pC.db.speciesSiteDenModelsnParList[indx]
                pVal=parseString(speciesPropList[ii].siteDenParList)
                jj=0
                while jj<pNPar:
                    if float(self.speciesSiteDenParamTBList[ii][jj].text())!=float(pVal[jj]):
                        pVal[jj]=self.speciesSiteDenParamTBList[ii][jj].text()
                    jj=jj+1
                self.allList[self.root.pCindx].speciesPropDataList[ii].siteDenParList=restoreString(pVal)
                
                pVal=list()
                if speciesPropList[ii].formEnergyParList is not None:
                    pVal=ast.literal_eval(speciesPropList[ii].formEnergyParList)
                    
                pNPar=len(pVal)
                
                
                jj=0
                while jj<pNPar:
                    if jj==0:
                        pVal=list(pVal)
                        if float(self.speciesFormEnergyParamTBList[ii][jj].text())!=float(pVal[jj]):
                            pVal[jj]=float(self.speciesFormEnergyParamTBList[ii][jj].text())
                    else:
                        pVal[jj]=list(pVal[jj])
                        if float(self.speciesFormEnergyParamTBList[ii][jj].text())!=float(pVal[jj][0]):
                            pVal[jj][0]=float(self.speciesFormEnergyParamTBList[ii][jj].text())
                    jj=jj+1
                self.allList[self.root.pCindx].speciesPropDataList[ii].formEnergyParList=tupleString(pVal)
                        
                ii=ii+1
                
        
    def resetPCdata(self,isInit=False):
#        QMessageBox.about(self,'warning',"In reset PC method")
#        aaa=1
        if self.propType==0:
            if not isInit:
                self.root.projWindow.pC.db.updateProjMatModelData(self.allList[self.root.pCindx])
#                print('Resetting data to database values')
#                print("ChemPot {0}".format(self.allList[self.root.pCindx].matPropData.cationChemPot))
            self.cationChemPot_TB.setText("{0}".format(self.allList[self.root.pCindx].matPropData.cationChemPot))
            self.eMass_TB.setText("{0}".format(self.allList[self.root.pCindx].matPropData.eEffMass))
            self.hMass_TB.setText("{0}".format(self.allList[self.root.pCindx].matPropData.hEffMass))
            self.latDen_TB.setText("{0}".format(self.allList[self.root.pCindx].matPropData.latDen))
            self.afnity_TB.setText("{0}".format(self.allList[self.root.pCindx].matPropData.elecAff))
            self.dielec_TB.setText("{0}".format(self.allList[self.root.pCindx].matPropData.dielecConst))
            self.radRate_TB.setText("{0}".format(self.allList[self.root.pCindx].matPropData.radRateConst))
            
            parValList=parseString(self.allList[self.root.pCindx].matPropData.bgPar)
            ii=0
            for parName in parValList:
                self.bgParam_TB_list[ii].setText("{0}".format(parValList[ii]))
                ii=ii+1
            
            parValList=parseString(self.allList[self.root.pCindx].matPropData.eMobPar)
            ii=0
            for parName in parValList:
                self.eMobParam_TB_list[ii].setText("{0}".format(parValList[ii]))
                ii=ii+1
            
            parValList=parseString(self.allList[self.root.pCindx].matPropData.hMobPar)
            ii=0
            for parName in parValList:
                self.hMobParam_TB_list[ii].setText("{0}".format(parValList[ii]))
                ii=ii+1
            
        if self.propType==1:
            if not isInit:
                self.root.projWindow.pC.db.updateProjReactionModelData(self.allList[self.root.pCindx])
            ii=0
            for reaction in self.allList[self.root.pCindx].reactionList:
                rPropData=self.allList[self.root.pCindx].reactionPropDataList[ii]
                rModel=rPropData.rateModel
                indx=self.root.projWindow.pC.db.reactionRateModels.index(rModel)
                
                pNPar=self.root.projWindow.pC.db.reactionRateModelsnParList[indx]                
                pVal=parseString(rPropData.rateParList)
                
                jj=0
                while jj<pNPar:
                    self.reactionParamTBList[ii][jj].setText("{0}".format(pVal[jj]))
                    jj=jj+1
                    
                ii=ii+1
            
        if self.propType==2:
            if not isInit:
                self.root.projWindow.pC.db.updateProjSpeciesModelData(self.allList[self.root.pCindx])
            ii=0
            DiffModelList=self.root.projWindow.pC.db.speciesDiffModels
            SiteDenModelList=self.root.projWindow.pC.db.speciesSiteDenModels
            speciesPropList=self.allList[self.root.pCindx].speciesPropDataList
            for species in self.allList[self.root.pCindx].speciesList:
                speciesDiffModelName=speciesPropList[ii].diffModel
                indx=DiffModelList.index(speciesDiffModelName)
                pNPar=self.root.projWindow.pC.db.speciesDiffModelsnParList[indx]
                pVal=parseString(speciesPropList[ii].diffParList)
                jj=0
                while jj<pNPar:
                    self.speciesDiffParamTBList[ii][jj].setText("{0}".format(pVal[jj]))
                    jj=jj+1
                
                speciesSiteDenModelName=speciesPropList[ii].siteDenModel
                indx = SiteDenModelList.index(speciesSiteDenModelName)
                pNPar=self.root.projWindow.pC.db.speciesSiteDenModelsnParList[indx]
                pVal=parseString(speciesPropList[ii].siteDenParList)
                jj=0
                while jj<pNPar:
                    self.speciesSiteDenParamTBList[ii][jj].setText("{0}".format(pVal[jj]))
                    jj=jj+1
                
                pVal=list()
                if speciesPropList[ii].formEnergyParList is not None:
                    pVal=ast.literal_eval(speciesPropList[ii].formEnergyParList)
                    
                pNPar=len(pVal)
                jj=0
                while jj<pNPar:
                    if jj==0:
                        self.speciesFormEnergyParamTBList[ii][jj].setText("{0}".format(pVal[jj]))
                    else:
                        self.speciesFormEnergyParamTBList[ii][jj].setText("{0}".format(pVal[jj][0]))
                    jj=jj+1
                
                ii=ii+1
        
    def closeEvent(self, event):
        self.hide()
        
class PVRD_Dlg_Mode4(QDialog):
    def __init__(self,typeVal=0,parent=None):
        super(PVRD_Dlg_Mode4,self).__init__(None)
        self.parent=parent
        self.typeVal=typeVal
        self.tbList=list()
        self.cbList=list()
        self.tbBList=list()
        self.cbBList=list()
        
        if typeVal==0:
            self.pcData=self.parent.projWindow.pC.allPointList[self.parent.pCindx]
#            self.species=self.parent.projWindow.pC.allPointList[self.parent.pCindx].speciesList
#            self.isBoundary=self.parent.projWindow.pC.allPointList[self.parent.pCindx].isBoundary
        elif typeVal==1:
            self.pcData=self.parent.projWindow.pC.allLineList[self.parent.pCindx]
#            self.species=self.parent.projWindow.pC.allLineList[self.parent.pCindx].speciesList
#            self.isBoundary=self.parent.projWindow.pC.allLineList[self.parent.pCindx].isBoundary
        elif typeVal==2:
            self.pcData=self.parent.projWindow.pC.allRectList[self.parent.pCindx]
#            self.species=self.parent.projWindow.pC.allRectList[self.parent.pCindx].speciesList
#            self.isBoundary=self.parent.projWindow.pC.allRectList[self.parent.pCindx].isBoundary
        else:
            self.pcData=None
        
        if self.pcData is not None:
            self.species=self.pcData.speciesList
            self.isBoundary=self.pcData.isBoundary
        else:
            self.species=list()
            self.isBoundary=False
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
#                                          QDialogButtonBox.Apply|
                                          QDialogButtonBox.Cancel)
    
    def layout_widgets(self):
        row=0
        
        viewPort=QWidget(self)
        self.scrollArea.setWidget(viewPort)
        
        vLayout=QVBoxLayout()
        viewPort.setLayout(vLayout)
        
        layout = QGridLayout()
        
        name=QLabel("species")
        tb=QLabel("Initial Condition")
        cb=QLabel("Type")
        layout.addWidget(name,row,0,1,1)
        layout.addWidget(tb,row,1,1,1)
        layout.addWidget(cb,row,2,1,1)
        if self.isBoundary:
            tb1=QLabel("Boundary Condition")
            cb1=QLabel("Type")
            layout.addWidget(tb1,row,3,1,1)
            layout.addWidget(cb1,row,4,1,1)
        row=row+1
        
#        print('cation={0}'.format(self.pcData.matPropData.cation))
#        print('anion={0}'.format(self.pcData.matPropData.anion))
        
        for speciesName in self.species:
            name=QLabel(speciesName)
            cb=QComboBox()
            cb.addItem("Constant")
            
#            print('Spcies={1},isHostCation={0}'.format(isHostCation(speciesName,self.pcData),speciesName))
            
            if isCationVacancy(speciesName):
                tb=QLineEdit('{0:1.3e}'.format(self.pcData.matPropData.cationVacancy))
                tb.setEnabled(True)
            elif isAnionVacancy(speciesName):
                tb=QLineEdit('{0:1.3e}'.format(self.pcData.matPropData.anionVacancy))
                tb.setEnabled(True)
            elif isHostCation(speciesName,self.pcData):
                val=self.pcData.matPropData.latDen-self.pcData.matPropData.cationVacancy
                tb=QLineEdit('{0:1.3e}'.format(val))
                tb.setEnabled(False)
            elif isHostAnion(speciesName,self.pcData):
                val=self.pcData.matPropData.latDen-self.pcData.matPropData.anionVacancy
                tb=QLineEdit('{0:1.3e}'.format(val))
                tb.setEnabled(False)
            else:
                tb=QLineEdit("0")
            
            
                
            layout.addWidget(name,row,0,1,1)
            layout.addWidget(tb,row,1,1,1)
            layout.addWidget(cb,row,2,1,1)
            self.tbList.append(tb)
            self.cbList.append(cb)
            if self.isBoundary:
                tb1=QLineEdit("0")
                cb1=QComboBox()
                cb1.addItems(["Constant Neumann","Constant Dirichlet"])
                layout.addWidget(tb1,row,3,1,1)
                layout.addWidget(cb1,row,4,1,1)
                self.tbBList.append(tb1)
                self.cbBList.append(cb1)
            row=row+1
        
        name=QLabel("Potential")
        self.potTB=QLineEdit("0")
        self.potCB=QComboBox()
        self.potCB.addItem("Constant")
        layout.addWidget(name,row,0,1,1)
        layout.addWidget(self.potTB,row,1,1,1)
        layout.addWidget(self.potCB,row,2,1,1)
        if self.isBoundary:
            self.potTBB=QLineEdit("0")
            self.potCBB=QComboBox()
            self.potCBB.addItems(["Constant Neumann","Constant Dirichlet"])
            layout.addWidget(self.potTBB,row,3,1,1)
            layout.addWidget(self.potCBB,row,4,1,1)
            
        row=row+1
            
        layout.addWidget(self.buttonBox, row, 1, 1, 3)
        row=row+1
        
        vLayout.addLayout(layout)
        vLayout.addStretch(1)
        
        vlayout=QVBoxLayout(self)
        vlayout.addWidget(self.scrollArea)
        
        self.setLayout(vlayout)
            
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Simulation IC BC Setup Properties Dialog")
        
    def accept(self):
#        QMessageBox.about(self,'warning',"In accept method")
        if self.pcData is not None:
            for ii in range(len(self.species)):
                userVal=self.processInput(ii,self.tbList[ii].text(),self.cbList[ii].currentText())
                for val in userVal:
                    isDataAdded=self.pcData.IC.isDataAdded(self.species[ii],val)
                    if not isDataAdded:
                        self.pcData.IC.addData(self.species[ii],val)
                if self.isBoundary:
                    userVal=self.processInput(ii,self.tbBList[ii].text(),self.cbBList[ii].currentText())
                    for val in userVal:
                        isDataAdded=self.pcData.BC.isDataAdded(self.species[ii],val)
                        if not isDataAdded:
                            self.pcData.BC.addData(self.species[ii],val)
                    
            userVal=self.processInput(-1,self.potTB.text(),self.potCB.currentText())
            for val in userVal:
                isPotDataAdded=self.pcData.IC.isPotDataAdded(val)
                if not isPotDataAdded:
                    self.pcData.IC.addPotData(val)
            
            if self.isBoundary:
                userVal=self.processInput(-1,self.potTBB.text(),self.potCBB.currentText())
                for val in userVal:
                    isPotDataAdded=self.pcData.BC.isPotDataAdded(val)
                    if not isPotDataAdded:
                        self.pcData.BC.addPotData(val)
            
#            QMessageBox.about(self,'warning',"ICDataList={0}<br>PotData={1}".format(self.pcData.IC.icDataList,self.pcData.IC.potentialData))
#            if self.isBoundary:
#                QMessageBox.about(self,'warning',"BCDataList={0}<br>PotData={1}".format(self.pcData.BC.bcDataList,self.pcData.BC.potentialData))
                
        super(PVRD_Dlg_Mode4,self).accept()
        
    def processInput(self,indx,valStr,typeStr):
        if typeStr.lower()=="Constant".lower():
            if indx>=0:
                self.pcData.IC.setFirst(self.species[indx])
            else:
                self.pcData.IC.setFirstPotential()
            return [[float(valStr)]]
        if typeStr.lower()=="Constant Neumann".lower():
            if indx>=0:
                self.pcData.BC.setFirst(self.species[indx])
            else:
                self.pcData.BC.setFirstPotential()
            return [[float(valStr),0]]
        
        if typeStr.lower()=="Constant Dirichlet".lower():
            if indx>=0:
                self.pcData.BC.setFirst(self.species[indx])
            else:
                self.pcData.BC.setFirstPotential()
            return [[float(valStr),1]]
        
    def updateDialog(self):
        if self.pcData is not None:
            for ii in range(len(self.species)):
                val=self.pcData.IC.icDataList[ii][2][0] # Assuming only Constant is supported
                self.tbList[ii].setText("{0}".format(val))
            # Assuming only Constant is supported
            val=self.pcData.IC.potentialData[2][0]
            self.potTB.setText("{0}".format(val))
            if self.isBoundary:
                for ii in range(len(self.species)):
                    val1=self.pcData.BC.bcDataList[ii][2][0] # actual Value
                    val2=self.pcData.BC.bcDataList[ii][3][0] # Type of boundary Condition
                    self.tbBList[ii].setText("{0}".format(val1))
                    self.cbBList[ii].setCurrentIndex(val2)
                val1=self.pcData.BC.potentialData[2][0]
                val2=self.pcData.BC.potentialData[3][0]
                self.potTBB.setText("{0}".format(val1))
                self.potCBB.setCurrentIndex(val2)
                
            
        
class PVRD_Mode4_TemperatureDlg_Point(QDialog):
    def __init__(self,curTime=0,curTemp=0,curTimeIndx=0,curTempIndx=0):
        super(PVRD_Mode4_TemperatureDlg_Point,self).__init__(None)
        self.curTime=curTime
        self.curTemp=curTemp
        self.curTimeIndx=curTimeIndx
        self.curTempIndx=curTempIndx
        
        self.nextTime=None
        self.nextTemp=None
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        
        self.curTimeName=QLabel("Start Time:")
        self.curTempName=QLabel("Start Temp:")
        
        self.curTimeTB=QLineEdit("{0}".format(self.curTime))
        self.curTimeName.setBuddy(self.curTimeTB)
        self.curTimeTB.setValidator(QDoubleValidator())
        self.curTimeTB.setEnabled(False)
        
        self.curTempTB=QLineEdit("{0}".format(self.curTemp))
        self.curTempName.setBuddy(self.curTempTB)
        self.curTempTB.setValidator(QDoubleValidator())
        self.curTempTB.setEnabled(self.curTime == 0)
        
        self.curTimeCB=QComboBox()
        self.curTempCB=QComboBox()
        
        self.curTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        self.curTimeCB.setCurrentIndex(self.curTimeIndx)
        self.curTimeCB.setEnabled(False)
        
        self.curTempCB.addItems(["K","C"])
        self.curTempCB.setCurrentIndex(self.curTempIndx)
        self.curTempCB.setEnabled(self.curTime == 0)
        
        
        self.nextTimeName=QLabel("Duration:")
        self.nextTempName=QLabel("New Temp:")
        
        self.nextTimeTB=QLineEdit("")
        self.nextTimeName.setBuddy(self.nextTimeTB)
        self.nextTimeTB.setValidator(QDoubleValidator())
        
        self.nextTempTB=QLineEdit("")
        self.nextTempName.setBuddy(self.nextTempTB)
        self.nextTempTB.setValidator(QDoubleValidator())
        
        self.nextTimeCB=QComboBox()
        self.nextTempCB=QComboBox()
        
        self.nextTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        self.nextTempCB.addItems(["K","C"])
        
        self.nPointName=QLabel("Number of Points:")
        self.nPointTB=QLineEdit("0")
        
        self.deleteButton=QRadioButton("Delete:")
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        
    def layout_widgets(self):
        
        layout = QGridLayout()
        row=0
        layout.addWidget(self.curTimeName,row,0,1,1)
        layout.addWidget(self.curTimeTB,row,1,1,1)
        layout.addWidget(self.curTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.curTempName,row,0,1,1)
        layout.addWidget(self.curTempTB,row,1,1,1)
        layout.addWidget(self.curTempCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextTimeName,row,0,1,1)
        layout.addWidget(self.nextTimeTB,row,1,1,1)
        layout.addWidget(self.nextTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextTempName,row,0,1,1)
        layout.addWidget(self.nextTempTB,row,1,1,1)
        layout.addWidget(self.nextTempCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nPointName,row,0,1,1)
        layout.addWidget(self.nPointTB,row,1,1,1)
        
        row=row+1
        layout.addWidget(self.deleteButton,row,1,1,2)
        
        row=row+1
        layout.addWidget(self.buttonBox,row,0,1,3)
        
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Add/Modify Temperature Point in Time")
        
#        self.nextTimeTB.textEdited[str].connect(self.updateNextTime)
#        self.nextTempTB.textEdited[str].connect(self.updateNexTemp)
#        
#    def updateNextTime(self):
        
        
    def result(self):
        nextTimeOut=getTimeInSeconds(float(self.nextTimeTB.text()),
                                     self.nextTimeCB.currentText())
        nextTempOut=getTempInKelvin(float(self.nextTempTB.text()),
                                    self.nextTempCB.currentText())
        curTempOut=getTempInKelvin(float(self.curTempTB.text()),
                                    self.curTempCB.currentText())
        return nextTimeOut, nextTempOut, float(self.nPointTB.text()), self.deleteButton.isChecked(), curTempOut
    
    
class PVRD_Mode4_TemperatureDlg_NCooling(QDialog):
    def __init__(self,curTime=0,curTemp=0,curTimeIndx=0,curTempIndx=0):
        super(PVRD_Mode4_TemperatureDlg_NCooling,self).__init__(None)
        self.curTime=curTime
        self.curTemp=curTemp
        self.curTimeIndx=curTimeIndx
        self.curTempIndx=curTempIndx
        
        self.nextTime=None
        self.nextTemp=None
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        
        self.curTimeName=QLabel("Start Time:")
        self.curTempName=QLabel("Start Temp:")
        
        self.curTimeTB=QLineEdit("{0}".format(self.curTime))
        self.curTimeName.setBuddy(self.curTimeTB)
        self.curTimeTB.setValidator(QDoubleValidator())
        self.curTimeTB.setEnabled(False)
        
        self.curTempTB=QLineEdit("{0}".format(self.curTemp))
        self.curTempName.setBuddy(self.curTempTB)
        self.curTempTB.setValidator(QDoubleValidator())
        self.curTempTB.setEnabled(self.curTime == 0)
        
        self.curTimeCB=QComboBox()
        self.curTempCB=QComboBox()
        
        self.curTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        self.curTimeCB.setCurrentIndex(self.curTimeIndx)
        self.curTimeCB.setEnabled(False)
        
        self.curTempCB.addItems(["K","C"])
        self.curTempCB.setCurrentIndex(self.curTempIndx)
        self.curTempCB.setEnabled(self.curTime == 0)
        
        
        self.nextTimeName=QLabel("Duration:")
        self.nextTempName=QLabel("Surrounding Temp:")
        
        self.nextTimeTB=QLineEdit("")
        self.nextTimeName.setBuddy(self.nextTimeTB)
        self.nextTimeTB.setValidator(QDoubleValidator())
        self.nextTimeTB.setEnabled(False)
        
        self.nextTempTB=QLineEdit("")
        self.nextTempName.setBuddy(self.nextTempTB)
        self.nextTempTB.setValidator(QDoubleValidator())
        
        self.nextTimeCB=QComboBox()
        self.nextTempCB=QComboBox()
        
        self.nextTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        self.nextTimeCB.setEnabled(False)
        self.nextTempCB.addItems(["K","C"])
        
        self.rateName=QLabel("Cooling Rate:")
        self.rateTB=QLineEdit("0.1")
        self.rateName.setBuddy(self.rateTB)
        self.rateTB.setValidator(QDoubleValidator())
        self.rateCB=QLabel("1/s")
        
        self.nPointName=QLabel("Number of Points:")
        self.nPointTB=QLineEdit("0")
        
        self.deleteButton=QRadioButton("Delete:")
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        
        self.setDuration()
        
    def setDuration(self):
        rate=float(self.rateTB.text())
        dur=1/rate*9.2103403719761818 # dur=-1/k*ln(0.0001)
        self.nextTimeTB.setText("{0}".format(round(dur,2)))
        
    def getRate(self):
        return float(self.rateTB.text())
        
        
    def layout_widgets(self):
        
        layout = QGridLayout()
        row=0
        layout.addWidget(self.curTimeName,row,0,1,1)
        layout.addWidget(self.curTimeTB,row,1,1,1)
        layout.addWidget(self.curTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.curTempName,row,0,1,1)
        layout.addWidget(self.curTempTB,row,1,1,1)
        layout.addWidget(self.curTempCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextTimeName,row,0,1,1)
        layout.addWidget(self.nextTimeTB,row,1,1,1)
        layout.addWidget(self.nextTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextTempName,row,0,1,1)
        layout.addWidget(self.nextTempTB,row,1,1,1)
        layout.addWidget(self.nextTempCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.rateName,row,0,1,1)
        layout.addWidget(self.rateTB,row,1,1,1)
        layout.addWidget(self.rateCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nPointName,row,0,1,1)
        layout.addWidget(self.nPointTB,row,1,1,1)
        
        row=row+1
        layout.addWidget(self.deleteButton,row,1,1,2)
        
        row=row+1
        layout.addWidget(self.buttonBox,row,0,1,3)
        
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Add/Modify Temperature Point in Time")
        self.rateTB.textChanged[str].connect(self.setDuration)
        
    def result(self):
        nextTimeOut=getTimeInSeconds(float(self.nextTimeTB.text()),
                                     self.nextTimeCB.currentText())
        nextTempOut=getTempInKelvin(float(self.nextTempTB.text()),
                                    self.nextTempCB.currentText())
        curTempOut=getTempInKelvin(float(self.curTempTB.text()),
                                    self.curTempCB.currentText())
        return nextTimeOut, nextTempOut, float(self.nPointTB.text()), self.deleteButton.isChecked(), curTempOut
    
class PVRD_Mode4_LightDlg_Point(QDialog):
    def __init__(self,curTime=0,curLight=0):
        super(PVRD_Mode4_LightDlg_Point,self).__init__(None)
        self.curTime=curTime
        self.curLight=curLight
        
        self.nextTime=None
        self.nextLight=None
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        self.curTimeName=QLabel("Start Time:")
        self.curTimeTB=QLineEdit("{0}".format(self.curTime))
        self.curTimeName.setBuddy(self.curTimeTB)
        self.curTimeTB.setValidator(QDoubleValidator())
        self.curTimeTB.setEnabled(False)
        self.curTimeCB=QComboBox()        
        self.curTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        self.curTimeCB.setEnabled(False)
        
        self.curLightName=QLabel("Start Suns:")
        self.curLightTB=QLineEdit("{0}".format(self.curLight))
        self.curLightName.setBuddy(self.curLightTB)
        self.curLightTB.setValidator(QDoubleValidator())
        self.curLightTB.setEnabled(False)
        
        self.nextTimeName=QLabel("Duration:")
        self.nextTimeTB=QLineEdit("")
        self.nextTimeName.setBuddy(self.nextTimeTB)
        self.nextTimeTB.setValidator(QDoubleValidator())
        self.nextTimeCB=QComboBox()
        self.nextTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        
        self.nextLightName=QLabel("New Suns:")
        self.nextLightTB=QLineEdit("")
        self.nextLightName.setBuddy(self.nextLightTB)
        self.nextLightTB.setValidator(QDoubleValidator())
        
        self.nPointName=QLabel("Number of Points:")
        self.nPointTB=QLineEdit("0")
        
        self.deleteButton=QRadioButton("Delete:")
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        
    def layout_widgets(self):
        
        layout = QGridLayout()
        row=0
        layout.addWidget(self.curTimeName,row,0,1,1)
        layout.addWidget(self.curTimeTB,row,1,1,1)
        layout.addWidget(self.curTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.curLightName,row,0,1,1)
        layout.addWidget(self.curLightTB,row,1,1,1)
#        layout.addWidget(self.curTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextTimeName,row,0,1,1)
        layout.addWidget(self.nextTimeTB,row,1,1,1)
        layout.addWidget(self.nextTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextLightName,row,0,1,1)
        layout.addWidget(self.nextLightTB,row,1,1,1)
        
        row=row+1
        layout.addWidget(self.nPointName,row,0,1,1)
        layout.addWidget(self.nPointTB,row,1,1,1)
        
        row=row+1
        layout.addWidget(self.deleteButton,row,1,1,2)
        
        row=row+1
        layout.addWidget(self.buttonBox,row,0,1,3)
        
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Add/Modify Light Point in Time")
        
    def result(self):
        nextTimeOut=getTimeInSeconds(float(self.nextTimeTB.text()),
                                     self.nextTimeCB.currentText())
        nextTempOut=float(self.nextLightTB.text())
                                    
        return nextTimeOut, nextTempOut, float(self.nPointTB.text()), self.deleteButton.isChecked()
    
class PVRD_Mode4_BiasDlg_Point(QDialog):
    def __init__(self,curTime=0,curBias=0):
        super(PVRD_Mode4_BiasDlg_Point,self).__init__(None)
        self.curTime=curTime
        self.curBias=curBias
        
        self.nextTime=None
        self.nextBias=None
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        self.curTimeName=QLabel("Start Time:")
        self.curTimeTB=QLineEdit("{0}".format(self.curTime))
        self.curTimeName.setBuddy(self.curTimeTB)
        self.curTimeTB.setValidator(QDoubleValidator())
        self.curTimeTB.setEnabled(False)
        self.curTimeCB=QComboBox()        
        self.curTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        self.curTimeCB.setEnabled(False)
        
        self.curBiasName=QLabel("Start Bias:")
        self.curBiasTB=QLineEdit("{0}".format(self.curBias))
        self.curBiasName.setBuddy(self.curBiasTB)
        self.curBiasTB.setValidator(QDoubleValidator())
        self.curBiasTB.setEnabled(False)
        self.curBiasCB=QLabel("V")
        
        self.nextTimeName=QLabel("Duration:")
        self.nextTimeTB=QLineEdit("")
        self.nextTimeName.setBuddy(self.nextTimeTB)
        self.nextTimeTB.setValidator(QDoubleValidator())
        self.nextTimeCB=QComboBox()
        self.nextTimeCB.addItems(["s","min","hrs","days","weeks","months","Years","Decades"])
        
        self.nextBiasName=QLabel("New Bias:")
        self.nextBiasTB=QLineEdit("")
        self.nextBiasName.setBuddy(self.nextBiasTB)
        self.nextBiasTB.setValidator(QDoubleValidator())
        self.nextBiasCB=QLabel("V")
        
        self.floatButton=QRadioButton("isFloating:")
        
        self.nPointName=QLabel("Number of Points:")
        self.nPointTB=QLineEdit("0")
        
        self.deleteButton=QRadioButton("Delete:")
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)
        
    def layout_widgets(self):
        layout = QGridLayout()
        row=0
        layout.addWidget(self.curTimeName,row,0,1,1)
        layout.addWidget(self.curTimeTB,row,1,1,1)
        layout.addWidget(self.curTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.curBiasName,row,0,1,1)
        layout.addWidget(self.curBiasTB,row,1,1,1)
        layout.addWidget(self.curBiasCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextTimeName,row,0,1,1)
        layout.addWidget(self.nextTimeTB,row,1,1,1)
        layout.addWidget(self.nextTimeCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nextBiasName,row,0,1,1)
        layout.addWidget(self.nextBiasTB,row,1,1,1)
        layout.addWidget(self.nextBiasCB,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.nPointName,row,0,1,1)
        layout.addWidget(self.nPointTB,row,1,1,1)
        
        row=row+1
        layout.addWidget(self.floatButton,row,1,1,2)
        
        row=row+1
        layout.addWidget(self.deleteButton,row,1,1,2)
        
        row=row+1
        layout.addWidget(self.buttonBox,row,0,1,3)
        
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Add/Modify Light Point in Time")
        
    def result(self):
        nextTimeOut=getTimeInSeconds(float(self.nextTimeTB.text()),
                                     self.nextTimeCB.currentText())
        nextTempOut=float(self.nextBiasTB.text())
                                    
        return nextTimeOut, nextTempOut, float(self.nPointTB.text()), self.deleteButton.isChecked(), self.isFloating()
    
    def isFloating(self):
        return self.floatButton.isChecked()
        
    
class PVRD_Dlg_Mode5(QDialog):
    def __init__(self,parent=None,typeVal=0):
        super(PVRD_Dlg_Mode5,self).__init__(None)
        self.parent=parent
        self.typeVal=typeVal
        
        if typeVal==0:
            self.pcData=self.parent.projWindow.pC.allPointList[self.parent.pCindx]
        elif typeVal==1:
            self.pcData=self.parent.projWindow.pC.allLineList[self.parent.pCindx]
        elif typeVal==2:
            self.pcData=self.parent.projWindow.pC.allRectList[self.parent.pCindx]
        else:
            self.pcData=None
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        
    def create_widgets(self):
        self.nPointsXName=QLabel("N points(X):")
        self.nPointsXTB=QLineEdit("0")
        self.nPointsXName.setBuddy(self.nPointsXTB)
        self.nPointsXTB.setValidator(QDoubleValidator())
        self.nPointsXTB.setEnabled(self.parent.nDims>1)
        self.nPointsXCB=QComboBox()
        self.nPointsXCB.addItems(["linear","Geometric","Sym Geo"])
        self.nPointsXCB.setEnabled(self.parent.nDims>1)
        
        
        self.nPointsXSuggestName=QLabel("Debye Suggested Value {0}".format(1))
        
        self.dXName=QLabel("dX:")
        self.dXTB=QLineEdit("1")
        self.dXName.setBuddy(self.dXTB)
        self.dXTB.setValidator(QDoubleValidator())
        self.dXTB.setEnabled(self.parent.nDims>1)
        
        self.dXStartName=QLabel("Start dX:")
        self.dXStartTB=QLineEdit("{0}".format(self.pcData.W/100))
        self.dXStartName.setBuddy(self.dXStartTB)
        self.dXStartTB.setValidator(QDoubleValidator())
        self.dXStartTB.setEnabled(self.parent.nDims>1 and not self.nPointsXCB.currentIndex()==0)
        
        self.dXEndName=QLabel("End dX:")
        self.dXEndTB=QLineEdit("{0}".format(self.pcData.W/10))
        self.dXEndName.setBuddy(self.dXEndTB)
        self.dXEndTB.setValidator(QDoubleValidator())
        self.dXEndTB.setEnabled(self.parent.nDims>1 and not self.nPointsXCB.currentIndex()==0)
        
        self.dXSuggestName=QLabel("Debye Suggested Value {0}".format(1))
        
        self.nPointsYName=QLabel("N points(Y):")
        self.nPointsYTB=QLineEdit("0")
        self.nPointsYName.setBuddy(self.nPointsYTB)
        self.nPointsYTB.setValidator(QDoubleValidator())
        self.nPointsYTB.setEnabled(self.parent.nDims>0)
        self.nPointsYCB=QComboBox()
        self.nPointsYCB.addItems(["linear","Geometric","Sym Geo"])
        self.nPointsYCB.setEnabled(self.parent.nDims>0)
        
        self.nPointsYSuggestName=QLabel("Debye Suggested Value {0}".format(1))
        
        self.dYName=QLabel("dY:")
        self.dYTB=QLineEdit("{0}".format(self.pcData.H))
        self.dYName.setBuddy(self.dYTB)
        self.dYTB.setValidator(QDoubleValidator())
        self.dYTB.setEnabled(self.parent.nDims>0)
        
        self.dYStartName=QLabel("Start dY:")
        self.dYStartTB=QLineEdit("{0}".format(self.pcData.H/100))
        self.dYStartName.setBuddy(self.dYStartTB)
        self.dYStartTB.setValidator(QDoubleValidator())
        self.dYStartTB.setEnabled(self.parent.nDims>0 and not self.nPointsYCB.currentIndex()==0)
        
        self.dYEndName=QLabel("End dY:")
        self.dYEndTB=QLineEdit("{0}".format(self.pcData.H/10))
        self.dYEndName.setBuddy(self.dYEndTB)
        self.dYEndTB.setValidator(QDoubleValidator())
        self.dYEndTB.setEnabled(self.parent.nDims>0 and not self.nPointsYCB.currentIndex()==0)
        
        self.dYSuggestName=QLabel("Debye Suggested Value {0}".format(1))
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
#                                          QDialogButtonBox.Apply|
                                          QDialogButtonBox.Cancel)
        
    def layout_widgets(self):
        
        layout = QGridLayout()
        row=0
        layout.addWidget(self.nPointsYName,row,0,1,1)
        layout.addWidget(self.nPointsYTB,row,1,1,1)
        layout.addWidget(self.nPointsYCB,row,2,1,1)
#        layout.addWidget(self.nPointsYSuggestName,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.dYName,row,0,1,1)
        layout.addWidget(self.dYTB,row,1,1,1)
#        layout.addWidget(self.dYSuggestName,row,2,1,1)
        
        row=row+1
        layout.addWidget(self.dYStartName,row,0,1,1)
        layout.addWidget(self.dYStartTB,row,1,1,1)
        
#        row=row+1
        layout.addWidget(self.dYEndName,row,2,1,1)
        layout.addWidget(self.dYEndTB,row,3,1,1)
        
        if self.typeVal ==2:
            row=row+1
            layout.addWidget(self.nPointsXName,row,0,1,1)
            layout.addWidget(self.nPointsXTB,row,1,1,1)
            layout.addWidget(self.nPointsXCB,row,2,1,1)
#            layout.addWidget(self.nPointsXSuggestName,row,2,1,1)
            
            row=row+1
            layout.addWidget(self.dXName,row,0,1,1)
            layout.addWidget(self.dXTB,row,1,1,1)
#            layout.addWidget(self.dXSuggestName,row,2,1,1)
            
            row=row+1
            layout.addWidget(self.dXStartName,row,0,1,1)
            layout.addWidget(self.dXStartTB,row,1,1,1)
            
#            row=row+1
            layout.addWidget(self.dXEndName,row,2,1,1)
            layout.addWidget(self.dXEndTB,row,3,1,1)
            
        row=row+1
        layout.addWidget(self.buttonBox,row,2,1,2)
        
        self.setLayout(layout)
        
    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Mesh Properties")
        self.nPointsXTB.textEdited[str].connect(self.updateDx)
        self.dXTB.textEdited[str].connect(self.updateNpointX)
        self.nPointsXCB.currentIndexChanged.connect(self.updateXWidget)
        self.nPointsYCB.currentIndexChanged.connect(self.updateYWidget)
        
        self.nPointsYTB.textEdited[str].connect(self.updateDy)
        self.dYTB.textEdited[str].connect(self.updateNpointY)
        
#        self.dXStartTB.textEdited[str].connect(self.updateStartDx)
#        self.dXEndTB.textEdited[str].connect(self.updateEndDx)
#        
#        self.dYStartTB.textEdited[str].connect(self.updateStartDy)
#        self.dYEndTB.textEdited[str].connect(self.updateEndDy)
        
    def updateXWidget(self,indx):
        if not indx==0:
            self.dXTB.setEnabled(False)
            self.nPointsXTB.setEnabled(False)
            self.dXStartTB.setEnabled(True)
            self.dXEndTB.setEnabled(True)
        else:
            self.dXTB.setEnabled(True)
            self.nPointsXTB.setEnabled(True)
            self.dXStartTB.setEnabled(False)
            self.dXEndTB.setEnabled(False)
            
    def updateYWidget(self,indx):
        if not indx==0:
            self.dYTB.setEnabled(False)
            self.nPointsYTB.setEnabled(False)
            self.dYStartTB.setEnabled(True)
            self.dYEndTB.setEnabled(True)
        else:
            self.dXTB.setEnabled(True)
            self.nPointsYTB.setEnabled(True)
            self.dYStartTB.setEnabled(False)
            self.dYEndTB.setEnabled(False)
        
    def updateDx(self):
        if self.nPointsXTB.text() != "":
            nPoint=int(self.nPointsXTB.text())
        else:
            nPoint=0
        dX=self.pcData.W/(nPoint+1)
        self.dXTB.setText("{0}".format(dX))
    def updateNpointX(self):
        if self.dXTB.text() != "":
            dX=float(self.dXTB.text())
        else:
            dX=self.pcData.W
        
        nPoint=int(round(self.pcData.W/dX))
        self.nPointsXTB.setText("{0}".format(nPoint))
    def updateDy(self):
        if self.nPointsYTB.text() != "":
            nPoint=int(self.nPointsYTB.text())
        else:
            nPoint=0
        dY=self.pcData.H/(nPoint+1)
        self.dYTB.setText("{0}".format(dY))
    def updateNpointY(self):
        if self.dYTB.text() != "":
            dY=float(self.dYTB.text())
        else:
            dY=self.pcData.H
        nPoint=int(round(self.pcData.H/dY))
        self.nPointsYTB.setText("{0}".format(nPoint))
        
    def updateStartDx(self):
        if self.dXStartTB.text() != "":
            dXStart=float(self.dXStartTB.text())
        else:
            dXStart=self.pcData.W/10
        
        if dXStart == float(self.dXEndTB.text()):
            QMessageBox.about(self,'warning',"start dX and end dX should be different")
        if dXStart >= self.pcData.W:
            QMessageBox.about(self,'warning',"start dX should not be greater than width")
            
    def updateEndDx(self):
        if self.dXEndTB.text() != "":
            dXEnd=float(self.dXEndTB.text())
        else:
            dXEnd=self.pcData.W/100
        
        if dXEnd == float(self.dXStartTB.text()):
            QMessageBox.about(self,'warning',"end dX and start dX should be different")
        if dXEnd >= self.pcData.W:
            QMessageBox.about(self,'warning',"end dX should not be greater than width")
            
    def updateStartDy(self):
        if self.dYStartTB.text() != "":
            dYStart=float(self.dYStartTB.text())
        else:
            dYStart=self.pcData.H/10
        
        if dYStart == float(self.dYEndTB.text()):
            QMessageBox.about(self,'warning',"start dY and end dY should be different")
        if dYStart >= self.pcData.H:
            QMessageBox.about(self,'warning',"start dY should not be greater than Height")
            
    def updateEndDy(self):
        if self.dYEndTB.text() != "":
            dYEnd=float(self.dYEndTB.text())
        else:
            dYEnd=self.pcData.H/100
        
        if dYEnd == float(self.dYStartTB.text()):
            QMessageBox.about(self,'warning',"end dY and start dY should be different")
        if dYEnd >= self.pcData.H:
            QMessageBox.about(self,'warning',"end dY should not be greater than Height")
    
    def accept(self):
        if self.pcData is not None:
            if self.typeVal>0:
                self.pcData.yMeshPointList=self.getYMeshPointList()
                self.pcData.nY=int(self.nPointsYTB.text())
                self.pcData.nYType=self.nPointsYCB.currentIndex()
            if self.typeVal>1:
                self.pcData.xMeshPointList=self.getXMeshPointList()
                self.pcData.nX=int(self.nPointsXTB.text())
                self.pcData.nXType=self.nPointsXCB.currentIndex()
                for rectData in self.parent.projWindow.pC.allRectList:
                    rectData.xMeshPointList=self.getXMeshPointList()
                    rectData.nX=int(self.nPointsXTB.text())
                    rectData.nXType=self.nPointsXCB.currentIndex()
            self.parent.parent.updateDialogProp()
                
        super(PVRD_Dlg_Mode5,self).accept()
        
    def getYMeshPointList(self):
        out=list()
        if self.nPointsYCB.currentIndex()==0:
            Yarr=np.linspace(self.pcData.Y0,self.pcData.Y0+self.pcData.H,int(self.nPointsYTB.text())+2)
            out=Yarr.tolist()
        if self.nPointsYCB.currentIndex()==1:
            dYStart=float(self.dYStartTB.text())
            dYEnd=float(self.dYEndTB.text())
            ratio,num=self.getRatioNumber(self.pcData.H,dYStart,dYEnd)
            prevPoint=self.pcData.Y0
            out.append(prevPoint)
            for ii in range(0,num-2):
                newPoint=prevPoint+dYStart*ratio**ii
                out.append(newPoint)
                prevPoint=newPoint
            out.append(self.pcData.Y0+self.pcData.H-dYEnd)
            out.append(self.pcData.Y0+self.pcData.H)
            
        if self.nPointsYCB.currentIndex()==2:
            dYStart=float(self.dYStartTB.text())
            dYEnd=float(self.dYEndTB.text())
            ratio,num=self.getRatioNumber(self.pcData.H/2,dYStart,dYEnd)
            prevPoint=self.pcData.Y0
            out.append(prevPoint)
            for ii in range(0,num-2):
                newPoint=prevPoint+dYStart*ratio**ii
                out.append(newPoint)
                prevPoint=newPoint
            out.append(self.pcData.Y0+self.pcData.H/2-dYEnd)
            out.append(self.pcData.Y0+self.pcData.H/2)
            Yarr=np.array(out)
            Yarr1=2*self.pcData.Y0+self.pcData.H-np.flipud(Yarr[:-1])
            for val in Yarr1:
                out.append(val)
            out[-1]=self.pcData.Y0+self.pcData.H
#            QMessageBox.about(self,'warning',"out={0}".format(out))
        return out
    def getXMeshPointList(self):
        out=list()
        if self.nPointsXCB.currentIndex()==0:
            Xarr=np.linspace(self.pcData.X0,self.pcData.X0+self.pcData.W,int(self.nPointsXTB.text())+2)
            out=Xarr.tolist()
        if self.nPointsXCB.currentIndex()==1:
            dXStart=float(self.dXStartTB.text())
            dXEnd=float(self.dXEndTB.text())
            ratio,num=self.getRatioNumber(self.pcData.W,dXStart,dXEnd)
            prevPoint=self.pcData.X0
            out.append(prevPoint)
            for ii in range(0,num-2):
                newPoint=prevPoint+dXStart*ratio**ii
                out.append(newPoint)
                prevPoint=newPoint
            out.append(self.pcData.X0+self.pcData.W-dXEnd)
            out.append(self.pcData.X0+self.pcData.W)
        if self.nPointsXCB.currentIndex()==2:
            dXStart=float(self.dXStartTB.text())
            dXEnd=float(self.dXEndTB.text())
            ratio,num=self.getRatioNumber(self.pcData.H/2,dXStart,dXEnd)
            prevPoint=self.pcData.X0
            out.append(prevPoint)
            for ii in range(0,num-2):
                newPoint=prevPoint+dXStart*ratio**ii
                out.append(newPoint)
                prevPoint=newPoint
            out.append(self.pcData.X0+self.pcData.W/2-dXEnd)
            out.append(self.pcData.X0+self.pcData.W/2)
            Xarr=np.array(out)
            Xarr1=2*self.pcData.X0+self.pcData.W-np.flipud(Xarr[:-1])
            for val in Xarr1:
                out.append(val)
            out[-1]=self.pcData.X0+self.pcData.W
        return out
    
    def getRatioNumber(self,W,S,E):
        ratio=(W-S)/(W-E)
        num=int(np.log(E/S)/np.log(ratio))+1
        return ratio,num
    
    def updateDialog(self):
        if self.typeVal>0:
            self.nPointsYTB.setText("{0}".format(self.pcData.nY))
            self.updateDy()
            self.nPointsYCB.setCurrentIndex(self.pcData.nYType)
            self.updateYWidget(self.pcData.nYType)
        if self.typeVal>1:
            self.nPointsXTB.setText("{0}".format(self.pcData.nX))
            self.updateDx()
            self.nPointsXCB.setCurrentIndex(self.pcData.nXType)
            self.updateXWidget(self.pcData.nXType)
        
#class PVRD_DBPropWindowDlg(QDialog):
#    def __init__(self, parent=None):
#        super(PVRD_DBPropWindowDlg, self).__init__(parent)
#        self.root=parent.parent