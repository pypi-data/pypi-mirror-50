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
Created on Mon Jul  2 23:37:28 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from PyQt5.QtWidgets import (
        QAction, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
        QSizePolicy, QSlider, QSpacerItem, QMainWindow, QLineEdit
        )

from PyQt5.QtGui import (
        QIcon,QTextCursor
        )

from PyQt5.QtCore import (
        Qt
        )
import numpy as np
import scipy.sparse as sps
import time

import pyqtgraph as pg

import ast

fac=100

prec=6

colorList=[Qt.red,Qt.green,Qt.blue,Qt.cyan,
           Qt.magenta,Qt.yellow]
bStyleList=[Qt.SolidPattern,Qt.Dense7Pattern,Qt.HorPattern,Qt.VerPattern,
            Qt.CrossPattern,Qt.BDiagPattern,Qt.FDiagPattern,Qt.DiagCrossPattern]

def parseString(inputStr):
    if inputStr is not None:
        str1=inputStr.replace("(","")
        str2=str1.replace(")","")
        return str2.split(",")
    else:
        return None

def restoreString(listVal):
    if listVal is not None:
        tempStr=','.join(listVal)
        return "("+tempStr+")"
    else:
        return None
    
def tupleString(tupleVal):
    out=""
    if tupleVal is not None:
        out="("
        for ii in range(len(tupleVal)):
            if ii==0:
                out=out+"{0},".format(tupleVal[ii])
            else:
                out=out+"({0},{1})".format(tupleVal[ii][0],tupleVal[ii][1])
        out=out+")"
    return out
    
def isElectron(inputStr):
    eList=['e_{c}^{-}'
            ]
    return inputStr in eList

def isHole(inputStr):
    eList=['h_{v}^{+}'
            ]
    return inputStr in eList

def isCationVacancy(species):
    return species in 'V_{C}^{0}'

def isAnionVacancy(species):
    return species in 'V_{A}^{0}'

def isHostCation(species,pcData):
    cation=pcData.matPropData.cation
    name,site,charge=getSpeciesInfo(species)
#    print('spcies={0}'.format(species))
#    print('cation={0},name={1},site={2},charge={3}'.format(cation,name,site,charge))
#    print('{0}=={1}({4}),{2}==C({5}),{3}==0({6})'.format(cation,name,site,charge,(cation in name),(site in 'C'),(charge in '0')))
    return (cation in name) and (site in 'C') and (charge in '0')

def isHostAnion(species,pcData):
    anion=pcData.matPropData.anion
    name,site,charge=getSpeciesInfo(species)
    return (anion in name) and (site in 'A') and (charge in '0')

def getSpeciesInfo(species):
#    species=species.replace('{','')
#    species=species.replace('}','')
    t1=species.split('^')
    charge=t1[1]
    charge=charge.replace('{','')
    charge=charge.replace('}','')
    name=t1[0]
    if '[' in species and ']' in species:
        Name=name
        Name=Name.replace('[','')
        Name=Name.replace(']','')
        Name=Name.replace('{','')
        Name=Name.replace('}','')
        t2=Name.split('-')
        species1=t2[0]
        species2=t2[1]
        t3=species1.split('_')
        t4=species2.split('_')
        site1=t3[1]
        site2=t4[1]
        if 'C' in site1 or 'C' in site2:
            site='C'
        elif 'A' in site1 or 'A' in site2:
            site='A'
        elif 'i' in site1 or 'i' in site2:
            site='i'
        else:
            site='i'
        
    else:
        name=name.replace('{','')
        name=name.replace('}','')
        t2=name.split('_')
        name=t2[0]
        site=t2[1]
    
    
    return name,site,charge

def getReactionLHS(reaction):
#    reaction=reaction.replace(' ','')
    t1=reaction.split('<')
    
    t2=t1[0].split(' + ')
    
#    print('t2={0}'.format(t2))
    
    ii=0
    for val in t2:
        t2[ii]=val.replace(' ','')
        ii=ii+1
    
#    print('t2={0}'.format(t2))    
    
    if len(t2)==2:
        return list([t2[0],t2[1]])
    else:
        return list(t2)
    
def getReactionRHS(reaction):
#    reaction=reaction.replace(' ','')
    t1=reaction.split('>')
    
    t2=t1[1].split(' + ')
    
    ii=0
    for val in t2:
        t2[ii]=val.replace(' ','')
        ii=ii+1
        
    
    if len(t2)==2:
        return list([t2[0],t2[1]])
    else:
        return list(t2)
    

def getSpeciesNameSite(species):
    name,site,charge=getSpeciesInfo(species)
    if not '[' in name:
        return name+"_{"+site+"}"
    else:
        return name

def isSiteAssociatedWithCation(site):
    cationSiteList=['C'
            ]
    return site in cationSiteList

def isSiteAssociatedWithAnion(site):
    cationSiteList=['A'
            ]
    return site in cationSiteList

def isCationAtCationSite(cation,species):
    name,site,charge=getSpeciesInfo(species)
    return (cation in name) and (site in 'C')

def isAnionAtAnionSite(anion,species):
    name,site,charge=getSpeciesInfo(species)
    return (anion in name) and (site in 'A')

def isReservior(species):
    return "{res}" in species
    
def getCationLoss(cation,species):
    out=0
    if isCationAtCationSite(cation,species):
        return 0
    
    name,site,charge=getSpeciesInfo(species)
    if cation in name:
        out=out-1
    
    if isSiteAssociatedWithCation(site):
        out=out+1
    
    return out

def getAnionLoss(anion,species):
    out=0
    if isAnionAtAnionSite(anion,species):
        return 0
    
    name,site,charge=getSpeciesInfo(species)
    if anion in name:
        out=out-1
    
    if isSiteAssociatedWithAnion(site):
        out=out+1
        
    return out
    
def getIndCarriers(inList):
    eOut=[]
    hOut=[]
    ii=0
    for car in inList:
        if isElectron(car):
            eOut=ii
        if isHole(car):
            hOut=ii
        ii=ii+1
    
    return eOut,hOut

def createTBAction(iconImageName,tbName,statusTip,
                                     toolTip,isEnabled,slotName,parent):
    
#        QMessageBox.about("Warning","Inside Mode 1 GeoMode 0 Widget")
#    print("Test")
    qa=QAction(QIcon(iconImageName),tbName,parent)
    if statusTip is not None:
        qa.setStatusTip(statusTip)
    if toolTip is not None:
        qa.setToolTip(toolTip)
    qa.setEnabled(isEnabled)
    if slotName is not None:
        qa.triggered.connect(slotName)
    return qa

def getTimeInSeconds(inVal,inUnits):
    outVal=inVal
    found=False
    
    if inUnits.lower() == "s".lower():
        outVal=inVal
        found=True
        
    if inUnits.lower() == "min".lower():
        outVal=inVal*60
        found=True
        
    if inUnits.lower() == "hrs".lower():
        outVal=inVal*60*60
        found=True
        
    if inUnits.lower() == "days".lower():
        outVal=inVal*60*60*24
        found=True
        
    if inUnits.lower() == "weeks".lower():
        outVal=inVal*60*60*24*7
        found=True
        
    if inUnits.lower() == "months".lower():
        outVal=inVal*60*60*24*30
        found=True
        
    if inUnits.lower() == "Years".lower():
        outVal=inVal*60*60*24*365
        found=True
        
    if inUnits.lower() == "Years".lower():
        outVal=inVal*60*60*24*3650
        found=True
        
    if not found:
        print("unknown units for time:{0}".format(inUnits))
    
    return outVal
        
        
def getTempInKelvin(inVal,inUnits):
    outVal=inVal
    found=False
    
    if inUnits.lower() == "K".lower():
        outVal=inVal
        found=True
        
    if inUnits.lower() == "C".lower():
        outVal=inVal+273
        found=True
        
    if not found:
        print("unknown units for time:{0}".format(inUnits))
        
    return outVal

def getInterpolatedVal(dataList,xVal,yVal):
    if len(dataList[0])==1:
        return dataList[2][0]
    
def getBCInterpolatedVal(dataList,xVal,yVal):
    if len(dataList[0])==1:
        return dataList[2][0],dataList[3][0]
    
def swapForReactions(inMat,nMesh,M):
#    Most time sensitive part of the solver. Matlab does this 100 times faster.    
#    tS=time.time()
    inMat=inMat.tocoo()
#    print('coo creation:{0}'.format(time.time()-tS))
#    tS=time.time()

#    normal=np.arange(0,nMesh*M)
#    trans=np.reshape(np.reshape(normal,(nMesh,M),order='F').transpose(),(nMesh*M,),order='F')
    
#    print('trans op:{0}'.format(time.time()-tS))
#    tS=time.time()
    
    rows=inMat.row

    cols=inMat.col

    data=inMat.data
#    print('data collection :{0}'.format(time.time()-tS))
#    tS=time.time()
    
#    transMat=np.tile(trans,(len(rows),1))
    
#    print('Trans tile :{0}'.format(time.time()-tS))
#    tS=time.time()
    
#    t1=np.zeros((len(trans),len(rows)))
#    transMat1=t1+np.reshape(trans,(-1,1))
    
#    print('Trans zero :{0}'.format(time.time()-tS))
#    tS=time.time()
    
#    rowsMat=np.tile(rows,(len(trans),1))
    
#    delta=rowsMat-transMat.T
    
#    print('rows tile and delta :{0}'.format(time.time()-tS))
#    tS=time.time()
    
#    delta=np.reshape(rows,(1,-1))-transMat.T
    
#    print('rows reshape and delta :{0}'.format(time.time()-tS))
#    tS=time.time()
    
#    delta=delta.T
#    r,c=np.where(delta==0)
    
    rows_1=(rows/nMesh).astype(int)+(rows%nMesh)*M
#    print('row search :{0}'.format(time.time()-tS))
#    tS=time.time()
    
#    delta=np.reshape(delta,(1,-1))
#    r=np.where(delta==0)
    
#    print('row search :{0}'.format(time.time()-tS))
#    exit()
    
#    colsMat=np.tile(cols,(len(trans),1))
#    delta=colsMat-transMat.T
#    delta=np.reshape(cols,(1,-1))-transMat.T
#    delta=delta.T
#    print('col tile and delta :{0}'.format(time.time()-tS))
#    tS=time.time()
    
#    r,c=np.where(delta==0)
    
    cols_1=(cols/nMesh).astype(int)+(cols%nMesh)*M
#    print('col search :{0}'.format(time.time()-tS))
#    tS=time.time()
    
    outMat=sps.coo_matrix((data, (rows_1,cols_1)),shape=inMat.shape)
    
#    print('coo out creation :{0}'.format(time.time()-tS))
#    tS=time.time()

    return outMat


class PVRD_Slider(QWidget):
    def __init__(self,minimum,maximum,parent=None):
        super(PVRD_Slider,self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
#        hLayout=QVBoxLayout()
        self.label_1 = QLabel('U(Cation)',self)
        self.label = QLabel('',self)
#        self.TB = QLineEdit(self)
#        self.label.setBuddy(self.TB)
#        hLayout.addWidget(self.label_1)
#        hLayout.addWidget(self.label)
#        hLayout.addWidget(self.TB)
#        hLayout.addStretch()
        self.verticalLayout.addWidget(self.label_1)
        self.verticalLayout.addWidget(self.label)
#        self.verticalLayout.addLayout(hLayout)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
#        self.slider.setOrientation(Qt.Horizontal)
        self.horizontalLayout.addWidget(self.slider)
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())

        self.minimum = minimum
        self.maximum = maximum
        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())
#        self.TB.editingFinished.connect(self.updateValue)
        
    def setLabelValue(self, value):
#        print('Value={0},type={1}'.format(value,type(value)))
        self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
        self.maximum - self.minimum)
#        self.TB.setText("{0:.4f}".format(self.x))
        self.label.setText("{0:.4f}".format(self.x))
        
    def updateValue(self):
        val=float(self.TB.text())
#        print('Val={0}'.format(val))
#        print('min={0},max={1}'.format(self.minimum,self.maximum))
#        print('self_val={0}'.format(self.x))
        if self.minimum <= val and val <=self.maximum:
#            self.x=val
            val1=np.round((val-self.minimum)*(self.slider.maximum()-self.slider.minimum())/(
                    self.maximum-self.minimum),1)
#            print('self_val(After)={0}'.format(self.x))
            self.slider.setValue(val1)
            self.x=val
#            self.slider.valueChanged.emit(val)
#            print('self_val(After,After)={0}'.format(self.x))
        
    
        
class PVRD_formEnergyWindow(QMainWindow):
    def __init__(self,matName="",db=None, parent=None):
        super(PVRD_formEnergyWindow, self).__init__(parent=parent)
        from .PVRD_models import PVRD_models
        self.db=db
        bgName,bgPar=self.db.getBandGap(matName)
        bgFun=getattr(PVRD_models,bgName)
        parValList_bg=parseString(bgPar) # used in further calss to self.bg
        bgLambda=lambda T:bgFun(parValList_bg,T)
        self.bg=bgLambda(300)
        self.cation,self.anion=self.db.getCationAnion(matName)
        
#        print('cation={0}, Anion={1}'.format(self.cation,self.anion))
        
        self.hLayout=QHBoxLayout(self)
        self.formEnergy=self.db.getFormEnergy(matName)
#        print('formEnergy={0}'.format(formEnergy))
        allSpecies=self.db.getAllSpecies(matName)
#        print('all Species={0}'.format(allSpecies))
        self.w1=PVRD_Slider(self.formEnergy,0,self)
        self.hLayout.addWidget(self.w1)
        self.win = pg.GraphicsWindow(title="Formation Energy Plot under Different Conditions at 300K")
        self.hLayout.addWidget(self.win)
        self.plt=self.win.addPlot(title="Formation Energy of Species in {0}".format(matName))
        self.curveList=list()
        self.speciesList=list()
#        self.GfList=list()
        self.G0List=list()
        self.qList=list()
        self.plt.addLegend()
        self.cationLoss=list()
        self.anionLoss=list()
        self.aList=list()
        self.associatedIndx=np.array([])
#        penList=list(['r','y','g','b','o','p'])
#        penList=list(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])
        penList=list(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
        styleList=list([Qt.SolidLine,Qt.DashLine,Qt.DotLine,Qt.DashDotLine,Qt.DashDotLine])
        ii=0
        for species in allSpecies:
#            print('species before Name={0}'.format(species[0]))
            if isElectron(species[0]) or isHole(species[0]):
                continue
            if isCationAtCationSite(self.cation,species[0]) or isAnionAtAnionSite(self.anion,species[0]):
                continue
            if isReservior(species[0]):
                continue
            print('species Name={0}'.format(species[0]))
            formEnergy=self.db.getSpeciesFormEnergyData(matName,species[0])
            q=self.db.getSpeciesCharge(species[0])
            pVal=ast.literal_eval(formEnergy)
#            print('pVal = {0}'.format(pVal))
            cationLoss=getCationLoss(self.cation,species[0])
            anionLoss=getAnionLoss(self.anion,species[0])
#            print('cationLoss={0}'.format(cationLoss))
#            print('anionLoss={0}'.format(anionLoss))
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
                        val=self.bg-val
                        tLevel.append(val)
                jj=jj+1
#            if len(tLevel)==0:
#                Gf=lambda x: G0+q*x
#            else:
#                G0=G0+sum(tLevel)
#                Gf=lambda x: G0+q*x
            
#            self.GfList.append(Gf)
            speciesNameSite=getSpeciesNameSite(species[0])
            if speciesNameSite not in self.speciesList:
                self.speciesList.append(speciesNameSite)
                self.cationLoss.append(cationLoss)
                self.anionLoss.append(anionLoss)
                self.G0List.append(G0-np.sign(q)*sum(tLevel))
                self.qList.append(q)
                pen=pg.mkPen(penList[ii%len(penList)],width=2,style=styleList[int(ii/len(penList))])
                curve=self.plt.plot(pen=pen,name=speciesNameSite)
                self.curveList.append(curve)
                ii=ii+1
            else:
                indx=self.speciesList.index(speciesNameSite)
                self.associatedIndx=np.append(self.associatedIndx,indx)
                self.aList.append(list([cationLoss,anionLoss,G0-np.sign(q)*sum(tLevel),q]))
        
        self.update_plot()
        self.widget=QWidget()
        self.widget.setLayout(self.hLayout)
        self.setCentralWidget(self.widget)
        self.w1.slider.valueChanged.connect(self.update_plot)
        
    def update_plot(self):
        a=self.w1.x
        x=np.linspace(0,self.bg,1000)
        data=np.cos(x+a)
        jj=0
        for curve in self.curveList:
            Gf=lambda Ef : self.G0List[jj]+self.qList[jj]*Ef
            data=Gf(x)+a*self.cationLoss[jj]+(self.formEnergy-a)*self.anionLoss[jj]
            indx=np.where(self.associatedIndx==jj)
#            print('aList={0}'.format(self.aList))
#            print('indx={0}'.format(indx))
            for ii in indx[0]:
#                print('ii={0}'.format(ii))
#                print('aList[ii][0]={0}'.format(self.aList[ii][0]))
                Gft=lambda Ef: self.aList[ii][2]+self.aList[ii][3]*Ef
                data1=Gft(x)+a*self.aList[ii][0]+(self.formEnergy-a)*self.aList[ii][1]
#                print('data={0},data1={1}'.format(data,data1))
                data=np.minimum(data,data1)
#            print('data={0}'.format(data))
            curve.setData(x,data)
            jj=jj+1
        

class OutLog:
    """
    Class for writing the output to QTextEdit.
    Taken from https://riverbankcomputing.com/pipermail/pyqt/2009-February/022025.html
    """
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)       
        