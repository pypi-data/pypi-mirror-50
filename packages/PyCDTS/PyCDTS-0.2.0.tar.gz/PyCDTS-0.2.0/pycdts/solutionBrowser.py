#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 23:04:35 2018

@author: abdul
"""
#from Project import Project
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.switch_backend('Qt5Agg')
import matplotlib as mpl
import numpy as np
from cycler import cycler
import sys
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import h5py

import os

fac=10

from PyQt5.QtWidgets import (
        QAction, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
        QSizePolicy, QSlider, QSpacerItem, QMainWindow, QLineEdit, QApplication,
        QCheckBox,QListWidget,QListWidgetItem,QAbstractItemView, QFileDialog
        )

from PyQt5.QtGui import (
        QKeySequence, QIcon
        )

from PyQt5.QtCore import (
        Qt,pyqtSignal
        )

class SolutionBrowser(QMainWindow):
    def __init__(self,hdf5Name=None,projWindow=None,parent=None):
        super(SolutionBrowser,self).__init__(parent)
        from .PVRD import MdiArea
        self.projWindow=projWindow
        self.parent=parent
        self.mdi = MdiArea()
        self.setCentralWidget(self.mdi)
#        self.mainWidget=
#        self.mainWidget.updateData()
        
        
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen", "Open a project file")
        self.fileMenuActions = (fileOpenAction,)
        self.fileMenu = self.menuBar().addMenu("&File")
        self.addActions(self.fileMenu,self.fileMenuActions)
#        self.proj=project
#        self.numEng=project.numEng
        
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False):
        """
        This method is used for creating QActions for each of the file menu
        operations.
        """
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action
        
    def addActions(self, target, actions):
        """
        Method to create Actions in a loop.
        """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
        
    def fileOpen(self):
        """
        Opens previous PVRD Projects
        """
#        QMessageBox.about(self,"Under Development","Under Development")
        filename,_ = QFileDialog.getOpenFileName(self,"PVRD Project -- Open File",'',"PVRD Project Solution Data files (*_sol.out)")
        if filename:
            for proj in self.mdi.subWindowList():
                if proj.widget().hdf5Name==filename:
                    self.mdi.setActiveSubWindow(proj)
                    break
            else:
                self.loadFile(filename)
                
    def loadFile(self,filename):
        from .PVRD_ModeWidgets import PVRD_Mode7_Widget
        proj=PVRD_Mode7_Widget(projWindow=self.projWindow,hdf5Name=filename,parent=self.parent)
        proj.updateData()
#        print('hdf5Name={0}'.format(proj.hdf5Name))
        self.mdi.addSubWindow(proj)
        proj.setWindowTitle(os.path.basename(filename))
        proj.show()
        
        
        
#    def startInteractive(self):
#        print("Starting Interactive Plotting\n")
#        plt.rc('axes', prop_cycle=(cycler('linestyle', ['-', '--', ':', '-.']))*cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']))
#        fig,ax=plt.subplots()
#        for jj in range(0,self.numEng.M):
#            ax.loglog(self.proj.tOut[0,:],self.proj.uOut[jj,:]+np.spacing(1),label=self.numEng.Species[jj],linewidth=3.0)
#        plt.legend(loc='upper right',bbox_to_anchor=(1.04,1)).draggable()
#        plt.grid(True)
#        plt.show()
#    def show(self):
#        self.show()
#        self.mainWidget.show()
        
#class PVRD_DataPlotter():
#    def __init__(self,hdf5_dataSet=None,nDims=0):
#        self.dataSet=hdf5_dataSet
#        self.nDims=nDims
#        self.window=PVRD_SB_Window(nDims)
#        self.window.show()
        
        
class PVRD_QWidget3D(QWidget):
    def __init__(self,parent=None):
        super(PVRD_QWidget3D,self).__init__(parent=parent)
        self.w = gl.GLViewWidget(self)
        self.w.resize(self.size())
        self.w.move(self.pos())
        self.w.show()
        self.w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
        self.w.setCameraPosition(distance=75)
        self.w.resize(self.sizeHint())
        
    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)
        self.w.resize(self.size())
        
class PVRD_SB_Window(QWidget):
    speciesChangeSignal=pyqtSignal(bool)
    def __init__(self,nDims=0,rows=0,cols=0,parent=None):
        super(PVRD_SB_Window,self).__init__(parent=parent)
        self.nDims=nDims
        self.rows=rows
        self.cols=cols
#        self.nPlots=(self.rows+1)*(self.cols+1)
        
        self.speciesList=list()
        
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.curveList=list()
        self.itemList=list()
        self.colorList=list(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
        self.styleList=list([Qt.SolidLine,Qt.DashLine,Qt.DotLine,Qt.DashDotLine,Qt.DashDotLine])
        
    def create_widgets(self):
        self.slider=PVRD_SB_Slider('Time',0,99) # Default inititalization.
        self.anim_ChkBox=QCheckBox("Animation")
        self.plotArea=pg.GraphicsWindow(title="Simple Plot")
        self.listBoxLabel=QLabel('Select')
        self.listBox=QListWidget()
        self.window3D=PVRD_QWidget3D(self)
        self.window3D.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.window3D.w.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.plotArea.setMinimumSize(720,480)
        self.window3D.setMinimumSize(720,480)
        self.p1List=list()
        self.legendList=list()
#        print('rows={0},cols={1}'.format(self.rows,self.cols))
        for row in range(self.rows+1):
            for col in range(self.cols+1):
                p1=self.plotArea.addPlot(row=row,col=col)
                self.p1List.append(p1)
                l1=pg.LegendItem()
                l1.setParentItem(p1)
                self.legendList.append(l1)
                
        self.p1=self.p1List[0]
        self.l1=self.legendList[0]
#        print('p1List ={0}'.format(len(self.p1List)))
        
    def layout_widgets(self):
        hLayout_bot=QHBoxLayout()

        hLayout_bot.addWidget(self.slider)
        hLayout_bot.addWidget(self.anim_ChkBox)
        vLayout_right=QVBoxLayout()
        
        
        vLayout_left=QVBoxLayout()
        
        vLayout_left.addWidget(self.listBoxLabel)
        vLayout_left.addWidget(self.listBox)
        vLayout_left.addStretch()
        
        hLayout_top=QHBoxLayout()        
        hLayout_top.addLayout(vLayout_left)
        hLayout_top.addLayout(vLayout_right)

        vLayout=QVBoxLayout()

        vLayout.addLayout(hLayout_top)
        vLayout.addLayout(hLayout_bot)
        
        self.setLayout(vLayout)
        if self.nDims==2:            
            vLayout_right.addWidget(self.window3D)
            self.plotArea.hide()
            self.speciesList.append("")
        else:
            vLayout_right.addWidget(self.plotArea)
            self.window3D.hide()
            
        if self.nDims==0:
            self.anim_ChkBox.hide()
            self.slider.hide()
        
        
    def create_connections(self):
        self.listBox.clicked.connect(self.updateSpeciesList)
        
    def plot(self,plotData):
        if self.nDims==0 or self.nDims==1:
#            self.p1=self.plotArea.addPlot(plotData.x,plotData.y)
#        elif :
            pen=self.getPen()
            p1=self.p1List[plotData.row*(self.cols+1)+plotData.col]
            if plotData.name in "":
                curve=p1.plot(plotData.y,plotData.z,pen=pen,row=plotData.row,col=plotData.col)
            else:
                curve=p1.plot(plotData.y,plotData.z,pen=pen,row=plotData.row,col=plotData.col,name=plotData.name)
            p1.setLabel('bottom',plotData.xLabel)
            p1.setLabel('left',plotData.yLabel)
            p1.setTitle(plotData.title)
            self.curveList.append(curve)
            self.speciesList.append(plotData.name)
        else:
            if len(self.curveList)==0:
                item=gl.GLSurfacePlotItem(x=plotData.x*fac, y=plotData.y*fac, z=plotData.z, shader='normalColor')
                self.window3D.w.addItem(item)
                self.curveList.append(item)
                ax = gl.GLAxisItem()
                ax.setSize(2*fac,2*fac,2*fac)
                self.window3D.w.addItem(ax)
                gx = gl.GLGridItem()
                gx.rotate(90, 0, 1, 0)
                gx.translate(-10, 0, 0)
                self.window3D.w.addItem(gx)
                gy = gl.GLGridItem()
                gy.rotate(90, 1, 0, 0)
                gy.translate(0, -10, 0)
                self.window3D.w.addItem(gy)
                gz = gl.GLGridItem()
                gz.translate(0, 0, -10)
                self.window3D.w.addItem(gz)
            else:
                self.curveList[0].setData(x=plotData.x*fac, y=plotData.y*fac, z=plotData.z)
            
    def updateSpeciesList(self):
#        item=self.listBox.currentItem()
#        print('Name:{0}'.format(item.text()))
#        outList=list()
#        self.l1.items=[]
            
        ii=0
        for item in self.itemList:
            self.l1.removeItem(item.text())
            if self.nDims !=2:
                if not item.isSelected():
                    self.p1.removeItem(self.curveList[ii])
                else:
                    self.p1.addItem(self.curveList[ii])
                    self.l1.addItem(self.curveList[ii],item.text())
            else:
                if item.isSelected():
                    self.speciesList[0]=item.text()
#                    self.window3D.w.removeItem(self.curveList[ii])
#                else:
#                    self.window3D.w.addItem(self.curveList[ii])
#                self.speciesList[0]=item.
            ii=ii+1
            
        if self.nDims ==2:
            self.speciesChangeSignal.emit(True)
            
            
            
    def addSpeciesList(self,speciesList):
        if self.nDims != 2:
            self.listBox.setSelectionMode(QAbstractItemView.ExtendedSelection)
#            self.listBox.setSelectionMode(QListWidget.MultiSelection)
        for species in speciesList:
            item=QListWidgetItem(species)
            self.listBox.addItem(item)
            self.itemList.append(item)
            if self.nDims !=2:
                item.setSelected(True)
            
        if self.nDims == 2:
            item.setSelected(True)
            self.speciesList[0]=species
            
    def getPen(self):
        ii=len(self.curveList)
        pen=pg.mkPen(self.colorList[ii%len(self.colorList)],width=2,
                                    style=self.styleList[int(ii/len(self.colorList))])
        return pen
        
class PVRD_GenericVisualizer(QMainWindow):
    def __init__(self,hdf5_FP,nDims=0, parent=None):
        super(PVRD_GenericVisualizer, self).__init__(parent=parent)
        self.parent=parent
        self.hdf5File=hdf5_FP
        self.nDims=nDims
        self.plotWindow=PVRD_SB_Window(nDims)
        self.setCentralWidget(self.plotWindow)
        self.tIndx=0
        self.plotWindow.slider.timeIndxChangeSignal.connect(self.updateTimeIndx)
        self.plotWindow.speciesChangeSignal.connect(self.updatePlots)
        
    def updateTimeIndx(self,indx):
        self.tIndx=indx
        self.updatePlots()
        
    def updatePlots():
        pass
    
    def setTimeList(self,tVec):
        self.plotWindow.slider.minimum=0
        self.plotWindow.slider.maximum=len(tVec)-1
        self.plotWindow.slider.slider.setMinimum(0)
        self.plotWindow.slider.slider.setMaximum(len(tVec)-1)
        self.plotWindow.slider.vector=tVec
        
    def closeEvent(self,event):
        self.hide()
        event.ignore()
        
class PVRD_FormEnergyVisualizer(PVRD_GenericVisualizer):
    def __init__(self,matName,db,hdf5_FP,nDims=1, parent=None):
        super(PVRD_FormEnergyVisualizer, self).__init__(hdf5_FP,nDims,parent=parent)
        self.selectList=list()
        self.species=None
        self.matName=matName
        self.speciesList=list()
        self.plotWindow.slider.label.setText('Cation\nPotential')
        self.db=db
        self.cation,self.anion=self.db.getCationAnion(matName)
        self.G0List=list()
        self.qList=list()
        self.associatedIndx=list()
        self.aList=list()
        
        matFormEnergy=self.db.getFormEnergy(matName)
        
#        print("mat={0},Hf={1}".format(matName,matFormEnergy))
        
        self.tVec=np.arange(0,matFormEnergy,-0.01)
        
#        print("tVec={0}".format(self.tVec))
        
        self.setTimeList(self.tVec)
        
        from .PVRD_models import PVRD_models
        from .generalFunctions import (
                parseString, isElectron, isHole, isCationAtCationSite,
                isAnionAtAnionSite, getSpeciesNameSite, isReservior
                )
        import ast
        
        bgName,bgPar=self.db.getBandGap(matName)
        bgFun=getattr(PVRD_models,bgName)
        parValList_bg=parseString(bgPar) # used in further calss to self.bg
        bgLambda=lambda T:bgFun(parValList_bg,T)
        self.Eg=bgLambda(300)
        
        
        allSpecies=self.db.getAllSpecies(matName)
#        ii=0
        for species in allSpecies:
            if isElectron(species[0]) or isHole(species[0]):
                continue
            if isCationAtCationSite(self.cation,species[0]) or isAnionAtAnionSite(self.anion,species[0]):
                continue
            if isReservior(species[0]):
                continue
            
            formEnergy=self.db.getSpeciesFormEnergyData(matName,species[0])
            q=self.db.getSpeciesCharge(species[0])
            pVal=ast.literal_eval(formEnergy)
            
            jj=0
            while jj<len(pVal):
                if jj==0:
                    G0=pVal[jj]
                    tLevel=list()
                else:
                    val=pVal[jj][0]
                    if pVal[jj][1]==1:
                        tLevel.append(val)
                    elif pVal[jj][1]==-1:
                        val=self.Eg-val
                        tLevel.append(val)
                jj=jj+1
            
            speciesNameSite=getSpeciesNameSite(species[0])
            if speciesNameSite not in self.speciesList:
                self.speciesList.append(speciesNameSite)
                self.G0List.append(G0-np.sign(q)*sum(tLevel))
                self.qList.append(q)
            else:
                indx=self.speciesList.index(speciesNameSite)
                self.associatedIndx=np.append(self.associatedIndx,indx)
                self.aList.append(list([G0-np.sign(q)*sum(tLevel),q]))
        
        self.addSpeciesList(self.speciesList)
        
        
    def addSpeciesList(self,species):
        self.plotWindow.addSpeciesList(species)
        self.species=species        
        self.selectList=[ii for ii in range(len(species))]
        self.updatePlots()
#        self.plotWindow.p1List[0].addLegend()
        
    def updatePlots(self):
        jj=0;
#        legend=list()
#        update=0;
        for ii in self.selectList:
            indx=self.selectList[ii]
            species=self.species[indx]
#            legend.append(species)
            x=np.arange(0,self.Eg,0.0005) # Irrelavent for form energy diagrams
            y=np.arange(0,self.Eg,0.0005)
            Gf=lambda Ef : self.G0List[jj]+self.qList[jj]*Ef
#            data=Gf(x)+a*self.cationLoss[jj]+(self.formEnergy-a)*self.anionLoss[jj]
#            z=Gf(x)+self.db.getCorrectedPotential(self.matName,species,self.tVec[self.tIndx])
            data=Gf(x)-self.db.getCorrectedPotential(self.matName,species,self.tVec[self.tIndx])
            indx1=np.where(self.associatedIndx==jj)
            for idx in indx1[0]:
#                print('ii={0}'.format(ii))
#                print('aList[ii][0]={0}'.format(self.aList[ii][0]))
                Gft=lambda Ef: self.aList[idx][0]+self.aList[idx][1]*Ef
                data1=Gft(x)-self.db.getCorrectedPotential(self.matName,species,self.tVec[self.tIndx])
#                print('data={0},data1={1}'.format(data,data1))
                data=np.minimum(data,data1)
                
            z=data
            jj=jj+1
            
            pData=PVRD_plotData(x=x,y=y,z=z,name=species,xLabel='Fermi Level (eV)',
                                yLabel='Formation Energy (eV)',
                                title='Formation Energy Diagram for {0}'.format(self.matName))
            if species not in self.plotWindow.speciesList:
                self.plotWindow.plot(pData)
            else:
#                update=1
                self.plotWindow.curveList[indx].setData(x=y,y=z)
        
#        if update==0:
#            self.plotWindow.p1List[0].addLegend()
        
        
        
class PVRD_ConcVisualizer(PVRD_GenericVisualizer):
    def __init__(self,hdf5_FP,nDims=0, parent=None):
        super(PVRD_ConcVisualizer, self).__init__(hdf5_FP,nDims,parent=parent)
        self.selectList=list()
        self.species=None
        
#        print('Time indx={0}'.format(indx))
        
    def addSpeciesList(self,species):
        self.plotWindow.addSpeciesList(species)
        self.species=species
#        if self.nDims!=2:
#            self.selectList=[ii for ii in range(len(species))]
#        else:
#            self.selectList=list([0])
        self.selectList=[ii for ii in range(len(species))]
        self.updatePlots()
#        if self.nDims==2:
#            self.selectList=list([0])
#            self.plotWindow.updateSpeciesList()
        
    def updatePlots(self):
        for ii in self.selectList:
            indx=self.selectList[ii]
            species=self.species[indx]
            x=np.reshape(self.parent.X,(-1,))*1e4
            y=np.reshape(self.parent.Y,(-1,))*1e4
            z=np.log10(np.reshape(self.parent.conc[self.tIndx,:,:,indx],(-1,))+np.spacing(1))
            if self.nDims==2:
#                print('order=f')
                z=np.log10(np.reshape(self.parent.conc[self.tIndx,:,:,indx],(self.parent.nX,self.parent.nY))+np.spacing(1))
#                z=np.reshape(z,(-1,1))
#                z=np.reshape(z.T,(self.parent.nX,self.parent.nY),order='C')
            pData=PVRD_plotData(x=x,y=y,z=z,name=species,xLabel='Y(um)',
                                yLabel='Concentration (1/cm^3)',
                                title='Concentration Profile Plots')
#            if self.nDims!=2:
#                if species not in self.plotWindow.speciesList:
#                    self.plotWindow.plot(pData)
#                else:
#                    self.plotWindow.curveList[indx].setData(x=y,y=z)
#            else:
#                if species in self.plotWindow.speciesList:
#                    self.plotWindow.plot(pData)
                    
            if self.nDims==2:
                if species in self.plotWindow.speciesList:
                    self.plotWindow.plot(pData)
            elif self.nDims==1:
                if species not in self.plotWindow.speciesList:
                    self.plotWindow.plot(pData)
                else:
                    self.plotWindow.curveList[indx].setData(x=y,y=z)
            else:
#               y=np.log10(self.parent.tVec+np.spacing(1))
               y=self.parent.tVec+np.spacing(1)
               z=np.log10(np.reshape(self.parent.conc[:,:,:,indx],(-1,))+np.spacing(1))
               pData=PVRD_plotData(x=x,y=y,z=z,name=species,xLabel='time(s)',
                                yLabel='Concentration (1/cm^3)',
                                title='Concentration Profile Plots')
               if species not in self.plotWindow.speciesList:
                   self.plotWindow.plot(pData)
               else:
                   self.plotWindow.curveList[indx].setData(x=y,y=z)
            
                        
                
        
class PVRD_FiVisualizer(PVRD_GenericVisualizer):
    def __init__(self,hdf5_FP,nDims=0, parent=None):
        super(PVRD_FiVisualizer, self).__init__(hdf5_FP,nDims,parent=parent)
        if parent is not None:
            self.parent.calculateRho()
#        print('before asign')
        self.plotWindow=PVRD_SB_Window(nDims,rows=1,cols=1)
        self.setCentralWidget(self.plotWindow)
        self.plotWindow.slider.timeIndxChangeSignal.connect(self.updateTimeIndx)
        self.plotWindow.listBox.hide()
        self.plotWindow.listBoxLabel.hide()
        
    def updatePlots(self):
        y=np.reshape(self.parent.Y,(-1,))*1e4
        z=np.reshape(self.parent.fi[self.tIndx,:,:],(-1,))
        sName='Potential'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Potential (V)',
                                title='Potential Profile Plot',
                                row=0,col=0)
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[0].setData(x=y,y=z)
            
        rho=np.reshape(self.parent.rho[self.tIndx,:,:],(-1,))
        z=rho
        sName='Rho'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Concentration (1/cm^3)',
                                title='Charge Density Profile Plots',
                                row=1,col=0)
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[1].setData(x=y,y=z)
        
        z=np.reshape(self.parent.conc[self.tIndx,:,:,self.parent.eIndx],(-1,))
        z=np.log10(z+np.spacing(1))
        sName='FreeCarrier_e'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Concentration (1/cm^3)',
                                title='Free Carrier Concentration Profile Plots',
                                row=0,col=1)
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[2].setData(x=y,y=z)
        
        z=np.reshape(self.parent.conc[self.tIndx,:,:,self.parent.hIndx],(-1,))
        z=np.log10(z+np.spacing(1))
        sName='FreeCarrier_h'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Concentration (1/cm^3)',
                                title='Free Carrier Concentration Profile Plots',
                                row=0,col=1)
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[3].setData(x=y,y=z)
            
        z=np.reshape(self.parent.netNd[self.tIndx,:,:],(-1,))
        z=np.log10(z+np.spacing(1))
        sName='NetDonor'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Concentration (1/cm^3)',
                                title='Net Donor Acceptor Concentration Profile Plots',
                                row=1,col=1)
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[4].setData(x=y,y=z)
            
        z=np.reshape(self.parent.netNa[self.tIndx,:,:],(-1,))
        z=np.log10(z+np.spacing(1))
        sName='NetAcceptor'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Concentration (1/cm^3)',
                                title='Net Donor Acceptor Concentration Profile Plots',
                                row=1,col=1)
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[5].setData(x=y,y=z)
        
        
class PVRD_FieldVisualizer(PVRD_GenericVisualizer):
    def __init__(self,hdf5_FP,nDims=0, parent=None):
        super(PVRD_FieldVisualizer, self).__init__(hdf5_FP,nDims,parent=parent)
        
class PVRD_FluxVisualizer(PVRD_GenericVisualizer):
    def __init__(self,hdf5_FP,nDims=0, parent=None):
        super(PVRD_FluxVisualizer, self).__init__(hdf5_FP,nDims,parent=parent)
        
class PVRD_BandsVisualizer(PVRD_GenericVisualizer):
    def __init__(self,hdf5_FP,nDims=0, parent=None):
        super(PVRD_BandsVisualizer, self).__init__(hdf5_FP,nDims,parent=parent)
        if parent is not None:
            self.parent.calculateBands()
        self.plotWindow.listBox.hide()
        self.plotWindow.listBoxLabel.hide()
        
    def updatePlots(self):
        y=np.reshape(self.parent.Y,(-1,))*1e4
        z=np.reshape(self.parent.Ev[self.tIndx,:,:],(-1,))
        sName='ValenceBand'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Energy (eV)',
                                title='Band Profile Plot')
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[0].setData(x=y,y=z)
            
        z=np.reshape(self.parent.Ec[self.tIndx,:,:],(-1,))
        sName='ConductionBand'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Energy (eV)',
                                title='Band Profile Plot')
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[1].setData(x=y,y=z)
            
        z=np.reshape(self.parent.Efp[self.tIndx,:,:],(-1,))
        sName='QFL_hole'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Energy (eV)',
                                title='Band Profile Plot')
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[2].setData(x=y,y=z)
            
        z=np.reshape(self.parent.Efn[self.tIndx,:,:],(-1,))
        sName='QFL_electron'
        pData=PVRD_plotData(y=y,z=z,name=sName,xLabel='Y(um)',
                                yLabel='Energy (eV)',
                                title='Band Profile Plot')
        if sName not in self.plotWindow.speciesList:
            self.plotWindow.plot(pData)
        else:
            self.plotWindow.curveList[3].setData(x=y,y=z)
        

class PVRD_SB_Slider(QWidget):
    timeIndxChangeSignal=pyqtSignal(int)
    def __init__(self,labelName,minimum,maximum,parent=None):
        super(PVRD_SB_Slider,self).__init__(parent=parent)
        self.vector=None
#        self.timeIndxChangeSignal=
        self.hLayout = QHBoxLayout(self)
        vLayout=QVBoxLayout()
        self.label = QLabel(labelName,self)
        self.labelVal=QLabel('',self)
        vLayout.addStretch()
        vLayout.addWidget(self.label)
        vLayout.addWidget(self.labelVal)
        vLayout.addStretch()
        self.hLayout.addLayout(vLayout)
        self.vLayout = QVBoxLayout()
        spacerItem = QSpacerItem(10, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.vLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.vLayout.addWidget(self.slider)
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.vLayout.addItem(spacerItem1)
        self.hLayout.addLayout(self.vLayout)
        self.resize(self.sizeHint())

        self.minimum = minimum
        self.maximum = maximum
        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())
        
        
    def setLabelValue(self, value):
#        print('value={0}'.format(type(value)))
        self.x = self.minimum + (np.float(value) / (self.slider.maximum() - self.slider.minimum())) * (self.maximum - self.minimum)
#        print('Vector={0}'.format(self.vector))
#        print('xVal={0}'.format(self.x))
        if self.vector is not None:
            self.labelVal.setText("{0:1.2e}".format(self.vector[int(self.x)]))
            self.tIndx=int(self.x)
            self.timeIndxChangeSignal.emit(self.tIndx)
        else:
            self.labelVal.setText("{0:1.1f}".format(self.x))
        
class PVRD_plotData():
    def __init__(self,x=None,y=None,z=None,xLabel="",yLabel="",zLabel="",title="",name="",row=0,col=0):
        self.x=x
        self.y=y
        self.z=z
        self.xLabel=xLabel
        self.yLabel=yLabel
        self.zLabel=zLabel
        self.labels={'left':'','bottom':''}
        if zLabel == "":
            self.labels['left']=yLabel
            self.labels['bottom']=xLabel
        
        self.title=title
        self.name=name
        self.row=row
        self.col=col    
    
#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    fName = '../Projects/PN1D_sol.out'
#    sb = SolutionBrowser(fName,None,None)
#    hdf5_file=h5py.File('../Projects/PN1D_sol.out', 'r')
#    dataSet=hdf5_file["PN1D/latestRun/Solution/Conc"]
#    nX=hdf5_file["PN1D/latestRun/Info"].attrs['nX']
#    nY=hdf5_file["PN1D/latestRun/Info"].attrs['nY']
#    species=list(hdf5_file["PN1D/latestRun/Info/species"])
#    x=np.reshape(np.array(hdf5_file["PN1D/latestRun/Info/X_um"]),(nX,))*50
#    y=np.reshape(np.array(hdf5_file["PN1D/latestRun/Info/Y_um"]),(nY,))
#    sIndx=0
#    z=np.log(np.reshape(np.array(dataSet[1,:,:,sIndx]),(nY,))+1)
#    pd=PVRD_plotData(y=y,z=z)
#    print('species={0}'.format(species[sIndx]))
#    print('conc shape={0}'.format(dataSet.shape))
#    np.savetxt('debug.txt',z,fmt='%2.2e')
#    window = PVRD_SB_Window(1)
##    w.setWindowTitle('Simple')
#    window.show()
#    window.plot(pd)
#    print('x shape={0}'.format(x.shape))
#    print('y shape={0}'.format(y.shape))
#    print('z shape={0}'.format(z.shape))
#    p1 = gl.GLSurfacePlotItem(x=x,y=y,z=z, shader='normalColor')
#    p1.translate(-10,-10,0)
    
#    g = gl.GLGridItem()
#    g.scale(2,2,1)
#    g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
#    self.window3D.w.addItem(g)
    
#    window.window3D.w.addItem(p1)
    
#    hdf5_file.close()
#    sys.exit(app.exec_())