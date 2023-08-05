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
Created on Sat Jun 30 23:21:48 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from scipy import constants as PhysCon
import ast
import numpy as np
from .generalFunctions import (isElectron,isHole)

class PVRD_models():
    def __init__(self):
        self.info="Supported Models are"

    def vBG(parList,T):
        valList=getValList(parList)
        return valList[0]-valList[1]*(pow(T,2)/(T+valList[2]))
    
    def eLFMob(parList,T):
        valList=getValList(parList)
        return valList[0]*pow(T/300,1.5)
    
    def hLFMob(parList,T):
        valList=getValList(parList)
        return valList[0]*pow(T/300,1.5)
    
    def eDOS(parList,T,matProp):
        return 2*pow(2*PhysCon.pi*matProp.eEffMass*PhysCon.m_e*PhysCon.k*T/PhysCon.h/PhysCon.h,1.5)*1e-6
    
    def hDOS(parList,T,matProp):
        return 2*pow(2*PhysCon.pi*matProp.hEffMass*PhysCon.m_e*PhysCon.k*T/PhysCon.h/PhysCon.h,1.5)*1e-6
    
    def kDOS(parList,T,matProp):
        return matProp.latDen
    
    def thermalVel(mass,T):
        return np.sqrt(3*PhysCon.k*T/(mass*PhysCon.m_e))
    
    def eGf(q,parList,T,matProp,correction):
        return q*matProp.elecAff
    
    def hGf(q,parList,T,matProp,correction):
        return q*(matProp.elecAff+matProp.bg(T))
    
    def iGf(q,parList,T,matProp,correction):
        Gf=0
#        if catLoss == 1:
#            ratio=(matProp.latDen-matProp.cationVacancy)/matProp.latDen
#            Gf=matProp.cationChemPot-PhysCon.k*T/PhysCon.e*np.log(ratio)
#        
#        if anLoss == 1:
#            ratio=(matProp.latDen-matProp.anionVacancy)/matProp.latDen
#            Gf=(matProp.formEnergy-matProp.cationChemPot)-PhysCon.k*T/PhysCon.e*np.log(ratio)
        
#        print('iGF={0}'.format(Gf))
        
        return Gf*0
    
    def sGf(q,parList,T,matProp,correction):
        valList=ast.literal_eval(parList)
        G0=valList[0]
        
        Gf=G0-correction;
        
#        print('G0={0},correction={1},chemPot={2},formEnergy={3},Gf={4}'.format(
#                G0,correction,matProp.cationChemPot,matProp.formEnergy,Gf))
#        print('valList={0}'.format(valList))

        ratio=matProp.bg(T)/matProp.bg(300)

        for ii in range(1,len(valList)):
            eVal=valList[ii][0]
            if valList[ii][1]==1:
                Gf=Gf-np.sign(q)*(eVal*ratio-matProp.elecAff-matProp.bg(T))
            elif valList[ii][1]==-1:
                Gf=Gf-np.sign(q)*(-eVal*ratio-matProp.elecAff)

                    
        return Gf
    
    def eD(parList,T,matProp):
        return matProp.eMob(T)*PhysCon.k*T/PhysCon.e
    
    def hD(parList,T,matProp):
        return matProp.hMob(T)*PhysCon.k*T/PhysCon.e
    
    def kD(parList,T,matProp):
        valList=ast.literal_eval(parList)
        return valList
    
    def bD(parList,T,matProp):
        valList=ast.literal_eval(parList)
        return valList[0]*np.exp(-valList[1]/(PhysCon.k*T/PhysCon.e))
    
    def dlwA(parList,T,speciesList,speciesProp,species,matProp):
        if species is not None:
            iSpeciesList=[speciesList.index(i) for i in species]
        else:
            iSpeciesList=list()
        diffSum=0
        z1_z2=1
        
        for indx in iSpeciesList:
            diffSum=diffSum+speciesProp[indx].diff(T)
            z1_z2=z1_z2*speciesProp[indx].q
        
        return PhysCon.e * abs(z1_z2) * diffSum / (matProp.dielecConst*PhysCon.epsilon_0*1e-2*PhysCon.k*T/PhysCon.e)
    
    def fcCC(parList,T,speciesList,speciesProp,species,matProp):
        valList=ast.literal_eval(parList)
        isElec=0
        isHol=0
        for speciesName in species:
            isElec=isElectron(speciesName)
            isHol=isHole(speciesName)
        if isElec==1:
            return valList*matProp.e_vel(T)
        elif isHol==1:
            return valList*matProp.h_vel(T)
        else:
            return 1
    def fcGR(parList,T,speciesList,speciesProp,species,matProp):
        return matProp.radRateConst
    
    def bl(parList,T,speciesList,speciesProp,species,matProp):
        valList=ast.literal_eval(parList)
        vt=PhysCon.k*T/PhysCon.e
        return valList[1]*1e12*np.exp(-valList[0]/vt)
    
    def getKeqRatio(LHS,RHS,speciesList,speciesProp,T):
        if LHS is not None:
            iLHSList=[speciesList.index(i) for i in LHS]
        else:
            iLHSList=list()
        if RHS is not None:
            iRHSList=[speciesList.index(i) for i in RHS]
        else:
            iRHSList=list()
        
        LHS_siteProd=1
        RHS_siteProd=1
        
        Gf_LHS=0
        Gf_RHS=0
        
        for indx in iLHSList:
            LHS_siteProd=LHS_siteProd*speciesProp[indx].siteDen(T)
            Gf_LHS=Gf_LHS+speciesProp[indx].formEnergy(T)
        for indx in iRHSList:
            RHS_siteProd=RHS_siteProd*speciesProp[indx].siteDen(T)
            Gf_RHS=Gf_RHS+speciesProp[indx].formEnergy(T)
#        print(
#                "LHS_siteProd={0}".format(LHS_siteProd)+
#                "RHS_siteProd={0}".format(RHS_siteProd)+
#                "Gf_LHS={0}".format(Gf_LHS)+
#                "Gf_RHS={0}".format(Gf_RHS)
#                )
        return RHS_siteProd/LHS_siteProd*np.exp((Gf_LHS-Gf_RHS)/(PhysCon.k*T/PhysCon.e))

def getValList(parList):
    valList=parList
    if isinstance(parList[0], str):
        ii=0
        for val in parList:
            valList[ii]=float(val)
            ii=ii+1
    return valList
