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
Created on Mon Mar 12 16:40:31 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""
#from PVRD_geoMode_2 import prec
prec=6
initEndTime=10

from .PVRD_models import PVRD_models

from .generalFunctions import (
        parseString, getInterpolatedVal, getBCInterpolatedVal
        )

from .Database import Database

import ast

import numpy as np

class PVRD_projectContainer():
    def __init__(self):
        self.nDims=-1
        self.mode=-1
        self.db=Database()
        self.dbFname=None
        
        self.geoMode=-1
        self.boundaryX0=0
        self.boundaryY0=0
        self.boundaryWidth=0
        self.boundaryHeight=0
        self.topBoundaryLineList=list()
        self.topBoundaryPointList=list()
        
        self.bottomBoundaryLineList=list()
        self.bottomBoundaryPointList=list()
        
        self.leftBoundaryLineList=list()
        self.leftBoundaryPointList=list()
        
        self.rightBoundaryLineList=list()
        self.rightBoundaryPointList=list()
        
        self.matRectList=list()
        self.matBrushDict={}
        self.matColorDict={}
        
        self.GBLineList=list()
        self.interfaceLineList=list()
        self.autoGBLineList=list()
        
        self.isGeoModeDone=False
        
        self.allRectList=list()
        self.allLineList=list()
        self.allPointList=list()
        
        self.tempParList=list()
        self.biasParList=list()
        self.lightParList=list()
        
        self.timeDataList=list()
        self.timeList=list()
        
#        self.tempParList.append(PVRD_ParTimeData(typeVal=0,startPar=300,endTime=10,endPar=300))
#        self.lightParList.append(PVRD_ParTimeData(typeVal=1,endTime=10))
#        self.biasParList.append(PVRD_ParTimeData(typeVal=2,endTime=10))
        
    def simplifyBoudaries(self):
        # Segment Bottom Boundary into sub boundaries
        xl,xr=round(self.boundaryX0,prec),round(self.boundaryX0+self.boundaryWidth,prec)
        for matRect in self.matRectList:
            if round(matRect.Y0+matRect.H,prec) == round(self.boundaryY0+self.boundaryHeight,prec):
                if xl<= round(matRect.X0,prec) <= xr:
                    x1=round(matRect.X0,prec)
                if xl <= round(matRect.X0+matRect.W,prec) <= xr:
                    x2=round(matRect.X0+matRect.W,prec)
                y1=round(matRect.Y0+matRect.H,prec)
                y2=y1
                self.bottomBoundaryLineList.append(PVRD_lineData(x1,y1,x2,y2,matRect.matName))
                if self.nDims==2:
                    self.bottomBoundaryPointList.append(PVRD_pointData(x1,y1,matRect.matName))
                    self.bottomBoundaryPointList.append(PVRD_pointData(x2,y2,matRect.matName))
                
        # Segment Top Boundary into sub boundaries
        xl,xr=round(self.boundaryX0,prec),round(self.boundaryX0+self.boundaryWidth,prec)
        for matRect in self.matRectList:
            if round(matRect.Y0,prec) == round(self.boundaryY0,prec):
                if xl<= round(matRect.X0,prec) <= xr:
                    x1=round(matRect.X0,prec)
                if xl <= round(matRect.X0+matRect.W,prec) <= xr:
                    x2=round(matRect.X0+matRect.W,prec)
                y1=round(matRect.Y0,prec)
                y2=y1
                self.topBoundaryLineList.append(PVRD_lineData(x1,y1,x2,y2,matRect.matName))
                if self.nDims==2:
                    self.topBoundaryPointList.append(PVRD_pointData(x1,y1,matRect.matName))
                    self.topBoundaryPointList.append(PVRD_pointData(x2,y2,matRect.matName))
                
        # Segment Left Boundary into sub boundaries
        yb,yt=round(self.boundaryY0,prec),round(self.boundaryY0+self.boundaryHeight,prec)
        for matRect in self.matRectList:
            if round(matRect.X0,prec) == round(self.boundaryX0,prec):
                if yb <= round(matRect.Y0,prec) <= yt:
                    y1=round(matRect.Y0,prec)
                if yb <= round(matRect.Y0+matRect.H,prec) <=yt:
                    y2=round(matRect.Y0+matRect.H,prec)
                x1=round(matRect.X0,prec)
                x2=x1
                self.leftBoundaryLineList.append(PVRD_lineData(x1,y1,x2,y2,matRect.matName))
                if self.nDims==2:
                    self.leftBoundaryPointList.append(PVRD_pointData(x1,y1,matRect.matName))
                    self.leftBoundaryPointList.append(PVRD_pointData(x2,y2,matRect.matName))
        
        # Segment Right Boundary into sub boundaries
        yb,yt=round(self.boundaryY0,prec),round(self.boundaryY0+self.boundaryHeight,prec)
        for matRect in self.matRectList:
            if round(matRect.X0+matRect.W,prec) == round(self.boundaryX0+self.boundaryWidth,prec):
                if yb <= round(matRect.Y0,prec) <= yt:
                    y1=round(matRect.Y0,prec)
                if yb <= round(matRect.Y0+matRect.H,prec) <=yt:
                    y2=round(matRect.Y0+matRect.H,prec)
                x1=round(matRect.X0+matRect.W,prec)
                x2=x1
                self.rightBoundaryLineList.append(PVRD_lineData(x1,y1,x2,y2,matRect.matName))
                if self.nDims==2:
                    self.rightBoundaryPointList.append(PVRD_pointData(x1,y1,matRect.matName))
                    self.rightBoundaryPointList.append(PVRD_pointData(x2,y2,matRect.matName))
                
        listName=self.bottomBoundaryPointList
        listOut=list()
        for ii in range(len(listName)):
            p1=listName[ii]
            jj=ii+1
            matName=p1.matName
            shouldAddPoint=False
            while jj < len(listName):
                p2=listName[jj]
                if p1.x1==p2.x1 and p1.y1==p2.y1:
                    shouldAddPoint=True
                    matName=matName+"/"+p2.matName
                jj=jj+1                                
            if shouldAddPoint:
                pointItem=PVRD_pointData(p1.x1,p1.y1,matName)
                listOut.append(pointItem)
        self.bottomBoundaryPointList=listOut
        
        listName=self.topBoundaryPointList
        listOut=list()
        for ii in range(len(listName)):
            p1=listName[ii]
            jj=ii+1
            matName=p1.matName
            shouldAddPoint=False
            while jj < len(listName):
                p2=listName[jj]
                if p1.x1==p2.x1 and p1.y1==p2.y1:
                    shouldAddPoint=True
                    matName=matName+"/"+p2.matName
                jj=jj+1                                
            if shouldAddPoint:
                pointItem=PVRD_pointData(p1.x1,p1.y1,matName)
                listOut.append(pointItem)
        self.topBoundaryPointList=listOut
        
        listName=self.leftBoundaryPointList
        listOut=list()
        for ii in range(len(listName)):
            p1=listName[ii]
            jj=ii+1
            matName=p1.matName
            shouldAddPoint=False
            while jj < len(listName):
                p2=listName[jj]
                if p1.x1==p2.x1 and p1.y1==p2.y1:
                    shouldAddPoint=True
                    matName=matName+"/"+p2.matName
                jj=jj+1                                
            if shouldAddPoint:
                pointItem=PVRD_pointData(p1.x1,p1.y1,matName)
                listOut.append(pointItem)
        self.leftBoundaryPointList=listOut
        
        listName=self.rightBoundaryPointList
        listOut=list()
        for ii in range(len(listName)):
            p1=listName[ii]
            jj=ii+1
            matName=p1.matName
            shouldAddPoint=False
            while jj < len(listName):
                p2=listName[jj]
                if p1.x1==p2.x1 and p1.y1==p2.y1:
                    shouldAddPoint=True
                    matName=matName+"/"+p2.matName
                jj=jj+1                                
            if shouldAddPoint:
                pointItem=PVRD_pointData(p1.x1,p1.y1,matName)
                listOut.append(pointItem)
        self.rightBoundaryPointList=listOut
        
        if self.nDims==1:
            self.rightBoundaryPointList=list()
            self.rightBoundaryLineList=list()
            self.leftBoundaryLineList=list()
            
        if self.nDims==0:
            self.rightBoundaryLineList=list()
            self.leftBoundaryLineList=list()
            self.topBoundaryLineList=list()
            self.bottomBoundaryLineList=list()
            
            self.rightBoundaryPointList=list()
            self.leftBoundaryPointList=list()
            self.topBoundaryPointList=list()
            self.bottomBoundaryPointList=list()
            
    def getSpeciesInAllGraphicsItem(self):
        out=list()
        charge=list()
        for data in self.allRectList:
            ii=0
            for speciesName in data.speciesList:
                speciesProp=data.speciesPropDataList[ii]
                if speciesName  not in out:
                    out.append(speciesName)
                    charge.append(speciesProp.q)
                ii=ii+1
                    
        for data in self.allLineList:
            ii=0
            for speciesName in data.speciesList:
                speciesProp=data.speciesPropDataList[ii]
                if speciesName  not in out:
                    out.append(speciesName)
                    charge.append(speciesProp.q)
                ii=ii+1
                    
        for data in self.allPointList:
            ii=0
            for speciesName in data.speciesList:
                speciesProp=data.speciesPropDataList[ii]
                if speciesName  not in out:
                    out.append(speciesName)
                    charge.append(speciesProp.q)
                ii=ii+1
                    
        return out,charge
    
    def getReactionsInAllGraphicsItem(self,Temp=None):
        out=list()
        lhs=list()
        rhs=list()
        KF=list()
        KB=list()
#        print("Inside GetReactions Temp={0}".format(Temp))
        for data in self.allRectList:
            ii=0
            for reactionName in data.reactionList:
                reactionProp=data.reactionPropDataList[ii]
                if reactionName not in out:
                    out.append(reactionName)
                    lhs.append(reactionProp.LHS)
                    rhs.append(reactionProp.RHS)
                    if Temp is None:
                        KF.append(reactionProp.KF)
                        KB.append(reactionProp.KB)
                    else:
#                        print("inside Else******")
                        KF.append(reactionProp.KF(Temp))
                        KB.append(reactionProp.KB(Temp))
                ii=ii+1
                    
        for data in self.allLineList:
            ii=0
            for reactionName in data.reactionList:
                reactionProp=data.reactionPropDataList[ii]
                if reactionName not in out:
                    out.append(reactionName)
                    lhs.append(reactionProp.LHS)
                    rhs.append(reactionProp.RHS)
                    if Temp is None:
                        KF.append(reactionProp.KF)
                        KB.append(reactionProp.KB)
                    else:
                        KF.append(reactionProp.KF(Temp))
                        KB.append(reactionProp.KB(Temp))
                ii=ii+1
                    
        for data in self.allPointList:
            ii=0
            for reactionName in data.reactionList:
                reactionProp=data.reactionPropDataList[ii]
                if reactionName not in out:
                    out.append(reactionName)
                    lhs.append(reactionProp.LHS)
                    rhs.append(reactionProp.RHS)
                    if Temp is None:
                        KF.append(reactionProp.KF)
                        KB.append(reactionProp.KB)
                    else:
                        KF.append(reactionProp.KF(Temp))
                        KB.append(reactionProp.KB(Temp))
                ii=ii+1
                    
        return out,lhs,rhs,KF,KB
    
    def updateDataForNumEng(self):
        self.X,self.Y=self.getMeshData()
        self.nX=len(self.X)
        self.nY=len(self.Y)
        self.nMesh=self.nX*self.nY
        
        self.species,self.charge=self.getSpeciesInAllGraphicsItem()
        self.M=len(self.species)
        self.reactions,_,_,_,_=self.getReactionsInAllGraphicsItem()
        self.K=len(self.reactions)
        
    
    def getDimData(self):
        return self.nDims,self.nX,self.nY,self.M,self.K,self.species,self.charge,self.reactions, self.X, self.Y
    
    
    def getMeshData(self):
        outX=list()
        outY=list()
        for data in self.allRectList:
            outY.extend(data.yMeshPointList)
            outX.extend(data.xMeshPointList)
        X=sorted(set(outX))
        Y=sorted(set(outY))
        outList=list()
        indx=0
        for xVal in X:
            for yVal in Y:
                outList.append([indx,xVal,yVal])
                indx=indx+1
#        for yVal in Y:
#            for xVal in X:
#                outList.append([indx,xVal,yVal])
#                indx=indx+1
        self.iXY=outList
        return X,Y
    
    def getMeshDataForNumEng(self):
        U0=0
        fi0=0
        U0,fi0=self.getMeshDataInitialConditions()
        reactions,lhs,rhs,KF,KB=self.getReactionsInAllGraphicsItem()
        species,charge=self.getSpeciesInAllGraphicsItem()

        lhs_out=list()
        for pair in lhs:
            tempList=list()
            if len(pair)==0:
                tempList.append(0)
                tempList.append(0)
            elif len(pair)==1:
                tempList.append(species.index(pair[0])+1)
                tempList.append(0)
            else:
                tempList.append(species.index(pair[0])+1)
                tempList.append(species.index(pair[1])+1)
            lhs_out.append(tempList)
                
        rhs_out=list()
        for pair in rhs:
            tempList=list()
            if len(pair)==0:
                tempList.append(0)
                tempList.append(0)
            elif len(pair)==1:
                tempList.append(species.index(pair[0])+1)
                tempList.append(0)
            else:
                tempList.append(species.index(pair[0])+1)
                tempList.append(species.index(pair[1])+1)
            rhs_out.append(tempList)
                                
        return U0,fi0,lhs_out,rhs_out
        
    def getMeshDataInitialConditions(self):
        outICData=np.zeros([self.nMesh,self.M])
        outPotData=np.zeros([self.nMesh,1])
        for iXYVal in self.iXY:
            if self.isDataInPointList(iXYVal[1],iXYVal[2]):
                species,data,potData=self.getICFromList(iXYVal[1],iXYVal[2],0)
            elif self.isDataInLineList(iXYVal[1],iXYVal[2]):
                species,data,potData=self.getICFromList(iXYVal[1],iXYVal[2],1)
            elif self.isDataInRectList(iXYVal[1],iXYVal[2]):
                species,data,potData=self.getICFromList(iXYVal[1],iXYVal[2],2)
            else:
                species=list()
                data=list()
                potData=list()
            ii=0
            for speciesName in species:
                indx=self.species.index(speciesName)
                icVal=getInterpolatedVal(data[ii],iXYVal[1],iXYVal[2])
                outICData[iXYVal[0],indx]=icVal
                ii=ii+1
            
            potVal=getInterpolatedVal(potData,iXYVal[1],iXYVal[2])
            outPotData[iXYVal[0],0]=potVal
            
        return outICData,outPotData
    
    def getMeshDataReactionRates(self,temp):
        outKFData=np.zeros([self.nMesh,self.K])
        outKBData=np.zeros([self.nMesh,self.K])
        
        for iXYVal in self.iXY:
            if self.isDataInPointList(iXYVal[1],iXYVal[2]):
                reactionList,reactionPropDataList=self.getReactionDataFromList(iXYVal[1],iXYVal[2],0)
            elif self.isDataInLineList(iXYVal[1],iXYVal[2]):
                reactionList,reactionPropDataList=self.getReactionDataFromList(iXYVal[1],iXYVal[2],1)
            elif self.isDataInRectList(iXYVal[1],iXYVal[2]):
                reactionList,reactionPropDataList=self.getReactionDataFromList(iXYVal[1],iXYVal[2],2)
            ii=0
            for reactionName in reactionList:
                reactionProp=reactionPropDataList[ii]
                rIndx=self.reactions.index(reactionName)
                outKFData[iXYVal[0],rIndx]=reactionProp.KF(temp)
                outKBData[iXYVal[0],rIndx]=reactionProp.KB(temp)
                ii=ii+1
        return outKFData,outKBData
    
    def getMeshDataMatSpeciesProp(self,temp):
        outDData=np.zeros([self.nMesh,self.M])
        outGData=np.zeros([self.nMesh,self.M])
        outNsData=np.zeros([self.nMesh,self.M])
        outEpsData=np.zeros([self.nMesh,1])
        
        for iXYVal in self.iXY:
            if self.isDataInPointList(iXYVal[1],iXYVal[2]):
                matList,speciesList,speciesPropDataList=self.getMatSpeciesDataFromList(iXYVal[1],iXYVal[2],0)
            elif self.isDataInLineList(iXYVal[1],iXYVal[2]):
                matList,speciesList,speciesPropDataList=self.getMatSpeciesDataFromList(iXYVal[1],iXYVal[2],1)
            elif self.isDataInRectList(iXYVal[1],iXYVal[2]):
                matList,speciesList,speciesPropDataList=self.getMatSpeciesDataFromList(iXYVal[1],iXYVal[2],2)
            
            outEpsData[iXYVal[0],0]=matList.dielecConst
            ii=0
            for speciesName in speciesList:
                speciesProp=speciesPropDataList[ii]
                sIndx=self.species.index(speciesName)
                outDData[iXYVal[0],sIndx]=speciesProp.diff(temp)
                outGData[iXYVal[0],sIndx]=speciesProp.formEnergy(temp)
                outNsData[iXYVal[0],sIndx]=speciesProp.siteDen(temp)
                ii=ii+1
        return outDData,outGData,outNsData,outEpsData
    
    def getMeshDataBC(self,temp):
#        print('********')
        outTopA=np.zeros([self.nX,self.M+1])
        outTopB=np.ones([self.nX,self.M+1])
        outTopC=np.zeros([self.nX,self.M+1])
        outBotA=np.zeros([self.nX,self.M+1])
        outBotB=np.ones([self.nX,self.M+1])
        outBotC=np.zeros([self.nX,self.M+1])
        
        for iXYVal in self.iXY:
            if self.isDataInPointList(iXYVal[1],iXYVal[2]):
                species,data,potData,isBoundary,isTop=self.getBCFromList(iXYVal[1],iXYVal[2],0)
            elif self.isDataInLineList(iXYVal[1],iXYVal[2]):
                species,data,potData,isBoundary,isTop=self.getBCFromList(iXYVal[1],iXYVal[2],1)
            elif self.isDataInRectList(iXYVal[1],iXYVal[2]):
                species,data,potData,isBoundary,isTop=self.getBCFromList(iXYVal[1],iXYVal[2],2)
            
#            print("*** isBoundary={0},xVal={1},yVal={2}".format(isBoundary,iXYVal[1],iXYVal[2]))
            if isBoundary:
                ii=0
                for speciesName in species:
                    indx=self.species.index(speciesName)
                    indx1=self.X.index(iXYVal[1])
                    bcVal,bcType=getBCInterpolatedVal(data[ii],iXYVal[1],iXYVal[2])
#                    print("bcVal={0},bcType={1}".format(bcVal,bcType))
                    if bcType==0:
                        if isTop:
                            outTopA[indx1,indx]=0
                            outTopB[indx1,indx]=1
                            outTopC[indx1,indx]=bcVal
                        else:
                            outBotA[indx1,indx]=0
                            outBotB[indx1,indx]=1
                            outBotC[indx1,indx]=bcVal
                    if bcType==1:
                        if isTop:
                            outTopA[indx1,indx]=1
                            outTopB[indx1,indx]=0
                            outTopC[indx1,indx]=bcVal
                        else:
                            outBotA[indx1,indx]=1
                            outBotB[indx1,indx]=0
                            outBotC[indx1,indx]=bcVal
                    ii=ii+1
                
#                print('outTopA={0}'.format(outTopA))
#                print('outTopB={0}'.format(outTopB))
#                print('outTopC={0}'.format(outTopC))
#                print('outBotA={0}'.format(outBotA))
#                print('outBotB={0}'.format(outBotB))
#                print('outBotC={0}'.format(outBotC))
                
                potBCVal,potBCType=getBCInterpolatedVal(potData,iXYVal[1],iXYVal[2])
                if potBCType==0:
                    if isTop:
                        outTopA[indx1,self.M]=0
                        outTopB[indx1,self.M]=1
                        outTopC[indx1,self.M]=potBCVal
                    else:
                        outBotA[indx1,self.M]=0
                        outBotB[indx1,self.M]=1
                        outBotC[indx1,self.M]=potBCVal
                
                if potBCType==1:
                    if isTop:
                        outTopA[indx1,self.M]=1
                        outTopB[indx1,self.M]=0
                        outTopC[indx1,self.M]=potBCVal
                    else:
                        outBotA[indx1,self.M]=1
                        outBotB[indx1,self.M]=0
                        outBotC[indx1,self.M]=potBCVal
        
#        print('outTopA={0}'.format(outTopA))
#        print('outTopB={0}'.format(outTopB))
#        print('outTopC={0}'.format(outTopC))
#        print('outBotA={0}'.format(outBotA))
#        print('outBotB={0}'.format(outBotB))
#        print('outBotC={0}'.format(outBotC))
#        print('***END***')
        return outTopA,outTopB,outTopC,outBotA,outBotB,outBotC
                
    def getReactionDataFromList(self,xVal,yVal,listType):
        if listType==0:
            dataList=self.allPointList
        if listType==1:
            dataList=self.allLineList
        if listType==2:
            dataList=self.allRectList
            
        for data in dataList:
            if data.isPointInItem(xVal,yVal):
                return data.reactionList,data.reactionPropDataList
            
    def getMatSpeciesDataFromList(self,xVal,yVal,listType):
        if listType==0:
            dataList=self.allPointList
        if listType==1:
            dataList=self.allLineList
        if listType==2:
            dataList=self.allRectList
            
        for data in dataList:
            if data.isPointInItem(xVal,yVal):
                return data.matPropData,data.speciesList,data.speciesPropDataList

    def getICFromList(self,xVal,yVal,listType):
        if listType==0:
            for data in self.allPointList:
                if data.isPointInItem(xVal,yVal):
                    return data.speciesList,data.IC.icDataList,data.IC.potentialData
        
        if listType==1:
            for data in self.allLineList:
                if data.isPointInItem(xVal,yVal):
                    return data.speciesList,data.IC.icDataList,data.IC.potentialData
                
        if listType==2:
            for data in self.allRectList:
                if data.isPointInItem(xVal,yVal):
                    return data.speciesList,data.IC.icDataList,data.IC.potentialData
                
    def getBCFromList(self,xVal,yVal,listType):
        if listType==0:
            dataList=self.allPointList
        if listType==1:
            dataList=self.allLineList
        if listType==2:
            dataList=self.allRectList
#        print("Inside getBC")
        for data in dataList:
            if data.isPointInItem(xVal,yVal):
#                print("BC isBoundary={2},listType={3},xVal={0},yVal={1}".format(xVal,yVal,data.isBoundary,listType))
                if data.isBoundary:
                    return data.speciesList,data.BC.bcDataList,data.BC.potentialData,data.isBoundary,data.isTop
                else:
                    return list(),list(),list(),False,False
                
    def isDataInPointList(self,xVal,yVal):
        for data in self.allPointList:
            if data.isPointInItem(xVal,yVal):
                return True
        return False
    
    def isDataInLineList(self,xVal,yVal):
        for data in self.allLineList:
            if data.isPointInItem(xVal,yVal):
                return True
        return False
    
    def isDataInRectList(self,xVal,yVal):
        for data in self.allRectList:
            if data.isPointInItem(xVal,yVal):
                return True
        return False
        
    def isFloatingAtTime(self,time):
        for biasParData in self.biasParList:
            for ii in range(0,len(biasParData.xPointList)-1):
                if biasParData.xPointList[ii]<= time < biasParData.xPointList[ii+1]:
                    return biasParData.isFloating
            
        return False
     
    def updateTempBiasLightData(self):
        self.updateDataForNumEng()
        for tempParData in self.tempParList:
#            print('startTime={0}, endTime={1}'.format(tempParData.xPointList[0],tempParData.xPointList[-1]))
#            print('startTemp={0}, endTemp={1}'.format(tempParData.yPointList[0],tempParData.yPointList[-1]))
            for ii in range(0,len(tempParData.xPointList)):
                timeData=PVRD_timeData()
                timeData.time=tempParData.xPointList[ii]
                timeData.temp=tempParData.yPointList[ii]
                KF,KB=self.getMeshDataReactionRates(timeData.temp)
                timeData.Kf=KF
                timeData.Kb=KB
                D,G,Ns,Eps=self.getMeshDataMatSpeciesProp(timeData.temp)
                timeData.D=D
                timeData.G=G
                timeData.Ns=Ns
                timeData.Eps=Eps
                topA,topB,topC,botA,botB,botC=self.getMeshDataBC(timeData.temp)
                timeData.TopA=topA
                timeData.TopB=topB
                timeData.TopC=topC
                timeData.BottomA=botA
                timeData.BottomB=botB
                timeData.BottomC=botC
                timeData.isFloating=self.isFloatingAtTime(timeData.time)
                
                if timeData.time not in self.timeList:
                    self.timeList.append(timeData.time)
                    self.timeDataList.append(timeData)
            
            

class PVRD_timeData():
    def __init__(self):
        self.time=0
        self.temp=0
        self.light=0
        self.bias=0
        self.G=0
        self.D=0
        self.Ns=0
        self.Eps=0
        self.Kf=0
        self.Kb=0
        self.TopA=0
        self.TopB=0
        self.TopC=0
        self.BottomA=0
        self.BottomB=0
        self.BottomC=0
        self.isFloating=False
        
        
class PVRD_rectData():
    def __init__(self,bX=0,bY=0,rW=0,rH=0,mat="",mechList=None,reactionList=None,speciesList=None):
        self.X0=bX
        self.Y0=bY
        self.W=rW
        self.H=rH
        self.matName=mat
        self.type=0
        self.dType=0
        self.isBoundary=False
        self.isTop=False
        if mechList is None:
            self.mechList=list()
        else:
            self.mechList=mechList
            
        if reactionList is None:
            self.reactionList=list()
        else:
            self.reactionList=reactionList
        
        if speciesList is None:
            self.speciesList=list()
        else:
            self.speciesList=speciesList
        
        self.matPropData=PVRD_matPropData()
        self.speciesPropDataList=None
        self.reactionPropDataList=None
        
        self.IC=None
        self.BC=None
        
        self.xMeshPointList=list()
        self.yMeshPointList=list()
        
        self.nX=0;
        self.nY=0;
        
        self.nXType=0;
        self.nYType=0;
        
    def getCenter(self):
        return self.X0+self.W/2,self.Y0+self.H/2
    
    def updateSpeciesPropDataList(self,datList):
        self.speciesPropDataList=datList
        
    def updateReactionPropDataList(self,datList):
        self.reactionPropDataList=datList
        
    def isPointInItem(self,xVal,yVal):
        xBool=self.X0 <= xVal <= self.X0+self.W or self.X0+self.W <= xVal <= self.X0
        yBool=self.Y0 <= yVal <= self.Y0+self.H or self.Y0+self.H <= yVal <= self.Y0
        return xBool and yBool
    
class PVRD_lineData():
    def __init__(self,x1=0,y1=0,x2=0,y2=0,mat="",mechList=None,reactionList=None,speciesList=None):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.matName=mat
        self.type=0
        self.dType=1
        self.isBoundary=False
        self.isTop=False
        if mechList is None:
            self.mechList=list()
        else:
            self.mechList=mechList
            
        if reactionList is None:
            self.reactionList=list()
        else:
            self.reactionList=reactionList
        
        if speciesList is None:
            self.speciesList=list()
        else:
            self.speciesList=speciesList
            
        self.matPropData=PVRD_matPropData()
        self.speciesPropDataList=None
        self.reactionPropDataList=None
        
        self.IC=None
        self.BC=None
    
    def updateSpeciesPropDataList(self,datList):
        self.speciesPropDataList=datList
        
    def updateReactionPropDataList(self,datList):
        self.reactionPropDataList=datList
        
    def isPointInItem(self,xVal,yVal):
        xBool=self.x1 <= xVal <= self.x2 or self.x2 <= xVal <= self.x1
        yBool=self.y1 <= yVal <= self.y2 or self.y2 <= yVal <= self.y1
        return xBool and yBool
        
class PVRD_pointData():
    def __init__(self,x1=0,y1=0,mat="",mechList=None,reactionList=None,speciesList=None):
        self.x1=x1
        self.y1=y1
        self.matName=mat
        self.type=0
        self.dType=2
        self.isBoundary=False
        self.isTop=False
        if mechList is None:
            self.mechList=list()
        else:
            self.mechList=mechList
            
        if reactionList is None:
            self.reactionList=list()
        else:
            self.reactionList=reactionList
        
        if speciesList is None:
            self.speciesList=list()
        else:
            self.speciesList=speciesList
            
        self.matPropData=PVRD_matPropData()
        self.speciesPropDataList=None
        self.reactionPropDataList=None
        
        self.IC=None
        self.BC=None
    
    def updateSpeciesPropDataList(self,datList):
        self.speciesPropDataList=datList
        
    def updateReactionPropDataList(self,datList):
        self.reactionPropDataList=datList
        
    def isPointInItem(self,xVal,yVal):
        return self.x1==xVal and self.y1==yVal

class PVRD_matPropData():
    def __init__(self):
        self.formEnergy=0
        
        self.cationChemPot=0
        self.cationVacancy=0
        self.anionVacancy=0
        
        self.cation=''
        self.anion=''
        
#        self.dv_cationChemPot=0
#        self.dv_cationVacancy=0
#        self.dv_anionVacancy=0
        
        self.eEffMass=1
#        self.eEffMass_dbString='Electron Effective Mass'
        
        self.hEffMass=1
#        self.hEffMass_dbString='Hole Effective Mass'
        
        self.latDen=1e22
#        self.latDen_dbString='Lattice Density'
        
        self.elecAff=1
        
        self.dielecConst=1
        
        self.radRateConst=1
        
        self.bgModelName="kBG"
        self.bgPar="(0)"
        
#        self.eDos=lambda T:PVRD_models.eDOS(self.eEffMass,T)
#        self.hDos=lambda T:PVRD_models.eDOS(self.eEffMass,T)
#        self.kDos=lambda T:self.latDen
        self.bg=1
        
    def update(self,eMass,hMass,latDen,afnity,dielec,radRate,bgName,bgPar,eMobName,eMobPar,hMobName,hMobPar,formEnergy=None):
        if formEnergy is not None:
            self.formEnergy=formEnergy
        self.eEffMass=eMass
        self.hEffMass=hMass
        self.latDen=latDen
        self.elecAff=afnity
        self.dielecConst=dielec
        self.radRateConst=radRate
        self.bgModelName=bgName
        self.bgPar=bgPar
        bgFun=getattr(PVRD_models,bgName)
        parValList_bg=parseString(bgPar) # used in further calss to self.bg
        self.bg=lambda T:bgFun(parValList_bg,T)
        
        self.eMobName=eMobName
        self.eMobPar=eMobPar
        eMobFun=getattr(PVRD_models,eMobName)
        parValList_eMob=parseString(eMobPar)
        self.eMob=lambda T:eMobFun(parValList_eMob,T)
        
        self.hMobName=hMobName
        self.hMobPar=hMobPar
        hMobFun=getattr(PVRD_models,hMobName)
        parValList_hMob=parseString(hMobPar)
        self.hMob=lambda T:hMobFun(parValList_hMob,T)
        
        self.e_vel=lambda T: PVRD_models.thermalVel(self.eEffMass,T)
        self.h_vel=lambda T: PVRD_models.thermalVel(self.hEffMass,T)
        
#class PVRD_TemperatureDataList():
#    def __init__(self):
#        self.timeList=list()
#        self.timeUnitList=list()
#        
#        self.tempList=list()
#        self.tempUnitList=list()
#        self.tempNPoints=list()
        
#        self.timeList.append(0)
#        self.timeUnitList.append(0)
        
#        self.tempList.append(300)
#        self.tempUnitList.append(0)
        
class PVRD_ParTimeData():
    def __init__(self,typeVal=0,startTime=0,startTimeUnit=0,endTime=0,endTimeUnit=0,startPar=0,startParUnit=0,
                 endPar=0,endParUnit=0,nParVal=0,isFloating=False,cRate=0.1):
        
        # For type of time division. For example in temperature dlg can be point based or newton Cooling Based
        # typeVal=0 for linear Point of Temperature dlg
        # typeVal=1 for Newton Cooling of Temperature dlg
        # typeVal=100 for linear Point of Light dlg
        # typeVal=200 for linear Point of Bias dlg
        self.typeVal=typeVal 
        self.startTimeVal=startTime
        self.startTimeUnitVal=startTimeUnit
        self.endTimeVal=endTime
        self.endTimeUnitVal=endTimeUnit
        
        self.startParVal=startPar
        self.startParUnitVal=startParUnit
        self.endParVal=endPar
        self.endParUnitVal=endParUnit
        self.nParVal=nParVal
        
        self.isFloating=isFloating
        self.cRate=cRate
        
        self.xPointList=list()
        self.yPointList=list()
        
class PVRD_IC_Data():
    def __init__(self,typeVal=0,parentData=None):
        self.typeVal=typeVal
        self.parentData=parentData
        self.icDataList=list()
        self.isFirst=list()
        for ii in range(len(self.parentData.speciesList)):
            self.icDataList.append([[0],[0],[0]])
            self.isFirst.append(True)
            
        self.potentialData=[[0],[0],[0]]
        self.isFirstPotential=True
        
    def addData(self,speciesName,valList):
        """
        typeVal=1:
        valList should be a list of size 3 with first element being x coordinate
        2nd element as y coordinate and 3rd element as the value.
        """
        indx=self.parentData.speciesList.index(speciesName)
        if self.isFirst[indx]:
            self.isFirst[indx]=False
            if len(valList)>0:
                self.icDataList[indx][2][0]=valList[-1]
            if len(valList)>1:
                self.icDataList[indx][1][0]=valList[-2]
            if len(valList)>2:
                self.icDataList[indx][0][0]=valList[-3]
        else:
            if len(valList)>0:
                self.icDataList[indx][2].append(valList[-1])
            if len(valList)>1:
                self.icDataList[indx][1].append(valList[-2])
            if len(valList)>2:
                self.icDataList[indx][0].append(valList[-3])
                    
    def isDataAdded(self,speciesName,valList):    
        indx=self.parentData.speciesList.index(speciesName)
        if self.isFirst[indx]:
            return False
        else:
            out=False
            if len(valList)>0:
                out=valList[-1] in self.icDataList[indx][2]
                matchIndx=self.icDataList[indx][2].index(valList[-1])
            if len(valList)>1:
                out=out and (valList[-2] in self.icDataList[indx][1])
                out=out and (self.icDataList[indx][1][matchIndx]==valList[-2])
            if len(valList)>2:
                out=out and (valList[-3] in self.icDataList[indx][0])
                out=out and (self.icDataList[indx][0][matchIndx]==valList[-3])
            
            return out
    
    def setFirst(self,speciesName):
        indx=self.parentData.speciesList.index(speciesName)
        self.isFirst[indx]=True
        
    def addPotData(self,valList):
        if self.isFirstPotential:
            self.isFirstPotential=False
            if len(valList)>0:
                self.potentialData[2][0]=valList[-1]
            if len(valList)>1:
                self.potentialData[1][0]=valList[-2]
            if len(valList)>2:
                self.potentialData[0][0]=valList[-3]
        else:
            if len(valList)>0:
                self.potentialData[2].append(valList[-1])
            if len(valList)>1:
                self.potentialData[1].append(valList[-2])
            if len(valList)>2:
                self.potentialData[0].append(valList[-3])
                
    def isPotDataAdded(self,valList):
        if self.isFirstPotential:
            return False
        else:
            out=False
            if len(valList)>0:
                out=valList[-1] in self.potentialData[2]
                matchIndx=self.potentialData[2].index(valList[-1])
            if len(valList)>1:
                out=out and (valList[-2] in self.potentialData[1])
                out=out and (self.potentialData[1][matchIndx]==valList[-2])
            if len(valList)>2:
                out=out and (valList[-3] in self.potentialData[0])
                out=out and (self.potentialData[0][matchIndx]==valList[-3])
            
            return out
        
    def setFirstPotential(self):
        self.isFirstPotential=True
        
class PVRD_BC_Data():
    def __init__(self,typeVal=0,parentData=None):
        self.typeVal=typeVal
        self.parentData=parentData
        self.bcDataList=list()
        self.isFirst=list()
        for ii in range(len(self.parentData.speciesList)):
            self.bcDataList.append([[0],[0],[0],[0]])
            self.isFirst.append(True)
            
        self.potentialData=[[0],[0],[0],[0]]
        self.isFirstPotential=True
        
    def addData(self,speciesName,valList):
        """
        Boundary condition valList should be atleast of size 2.
        First element being the value and 2nd being the type (Neuman,Dirichlet,...)
        """
        indx=self.parentData.speciesList.index(speciesName)
        if self.isFirst[indx]:
            self.isFirst[indx]=False
            if len(valList)>1:
                self.bcDataList[indx][3][0]=valList[-1]
                self.bcDataList[indx][2][0]=valList[-2]
            if len(valList)>2:
                self.bcDataList[indx][1][0]=valList[-3]
            if len(valList)>3:
                self.bcDataList[indx][0][0]=valList[-4]
        else:
            if len(valList)>1:
                self.bcDataList[indx][3].append(valList[-1])
                self.bcDataList[indx][2].append(valList[-2])
            if len(valList)>2:
                self.bcDataList[indx][1].append(valList[-3])
            if len(valList)>3:
                self.bcDataList[indx][0].append(valList[-4])
                
    def isDataAdded(self,speciesName,valList):    
        indx=self.parentData.speciesList.index(speciesName)
        if self.isFirst[indx]:
            return False
        else:
            out=False
            if len(valList)>1:
                out=valList[-2] in self.bcDataList[indx][2]
                matchIndx=self.bcDataList[indx][2].index(valList[-2])
                out=out and (self.bcDataList[indx][3][matchIndx]==valList[-1])
            if len(valList)>2:
                out=out and (valList[-3] in self.bcDataList[indx][1])
                out=out and (self.bcDataList[indx][1][matchIndx]==valList[-3])
            if len(valList)>3:
                out=out and (valList[-4] in self.bcDataList[indx][0])
                out=out and (self.bcDataList[indx][0][matchIndx]==valList[-4])
            
            return out
    def setFirst(self,speciesName):
        indx=self.parentData.speciesList.index(speciesName)
        self.isFirst[indx]=True
        
    def addPotData(self,valList):
        if self.isFirstPotential:
            self.isFirstPotential=False
            if len(valList)>1:
                self.potentialData[3][0]=valList[-1]
                self.potentialData[2][0]=valList[-2]
            if len(valList)>2:
                self.potentialData[1][0]=valList[-3]
            if len(valList)>3:
                self.potentialData[0][0]=valList[-4]
        else:
            if len(valList)>1:
                self.potentialData[3].append(valList[-1])
                self.potentialData[2].append(valList[-2])
            if len(valList)>2:
                self.potentialData[1].append(valList[-3])
            if len(valList)>3:
                self.potentialData[0].append(valList[-4])
                
    def isPotDataAdded(self,valList):
        if self.isFirstPotential:
            return False
        else:
            out=False
            if len(valList)>1:
                out=valList[-2] in self.potentialData[2]
                matchIndx=self.potentialData[2].index(valList[-2])
                out=out and (self.potentialData[3][matchIndx]==valList[-1])
            if len(valList)>2:
                out=out and (valList[-3] in self.potentialData[1])
                out=out and (self.potentialData[1][matchIndx]==valList[-3])
            if len(valList)>3:
                out=out and (valList[-4] in self.potentialData[0])
                out=out and (self.potentialData[0][matchIndx]==valList[-4])
            
            return out
        
    def setFirstPotential(self):
        self.isFirstPotential=True
