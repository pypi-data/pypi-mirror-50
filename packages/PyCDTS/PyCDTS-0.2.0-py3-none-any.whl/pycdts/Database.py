#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 03:34:17 2018

@author: abdul
"""

import sqlite3 as sqlite

#from PVRD_projectContainer import PVRD_speciesPropData
#from PVRD_projectContainer import PVRD_reactionPropData

from .PVRD_models import PVRD_models

import ast

from .generalFunctions import (
        getCationLoss,getAnionLoss,isElectron,isHole, isCationAtCationSite,
        isAnionAtAnionSite, isReservior
        )

class Database:
    
    def __init__(self,fileName=None):
        self.dbName=fileName
        self.materials=list()
        if fileName is not None:
            self.update()
            
    def getElementPotential(self,mat,element,x):
        potFun=self.getElementPhaseFormEnergyFunction(mat,element)
        val=potFun(x)
        if val>0:
            return 0
        else:
            return val
            
    def getElementPhaseFormEnergyFunction(self,mat,element):
        formEnergy=self.getFormEnergy(mat)
        cation,anion=self.getCationAnion(mat)
        if element in cation:
            return lambda x:x
        elif element in anion:
            return lambda x:formEnergy-x
        else:
            self.cursor.execute("SELECT \"Formation Energy\" FROM MATERIALPHASE where Material='{0}' and Element='{1}'".format(mat,element))
            all_rows=self.cursor.fetchall()
            if len(all_rows)==0:
                return lambda x: 0
            else:
                fe=all_rows[0][0]
                self.cursor.execute("SELECT Composition FROM MATERIALPHASE where Material='{0}' and Element='{1}'".format(mat,element))
                all_rows=self.cursor.fetchall()
                comp=ast.literal_eval(all_rows[0][0])
                cationVal=0
                anionVal=0
                elementVal=1
                for data in comp:
                    if data[0] in cation:
                        cationVal=data[1]
                    if data[0] in anion:
                        anionVal=data[1]
                    if data[0] in element:
                        elementVal=data[1]
                return lambda x: (fe-cationVal*x-anionVal*(formEnergy-x))/elementVal
            
    def getCorrectedPotential(self,matName,species,potential):
        if not '^' in species:
            species=species+'^{0}'
        self.cursor.execute("SELECT elementscount FROM SPECIES where Name='{0}'".format(species))
        all_rows=self.cursor.fetchall()
#        print('species={0},row={1}'.format(species,all_rows))
        comp=ast.literal_eval(all_rows[0][0])
        pot=0
        for data in comp:
            element=data[0]
            count=data[1]
            pot=pot+count*self.getElementPotential(matName,element,potential)
            
        return pot
            
        
    def update(self):
        self.connect=sqlite.connect("file:{fName}?mode=ro".format(fName=self.dbName),uri=True)
        self.cursor=self.connect.cursor()
        
        # Read the database for list of Materials From MATERIALS TABLE
        # self.materials is used as primary key value for retriving data from database.
        self.cursor.execute("SELECT Name FROM MATERIALS")
        all_rows=self.cursor.fetchall()
        self.materials=[' '.join(item) for item in all_rows]
        self.materialPhaseElements=list()
        self.matFormEnergy=list()
        
        for mat in self.materials:
            cation,anion=self.getCationAnion(mat)
            formEnergy=self.getFormEnergy(mat)
            self.matFormEnergy.append(formEnergy)
            self.cursor.execute("SELECT Element FROM MATERIALPHASE where Material='{0}'".format(mat))
            all_rows=self.cursor.fetchall()
            eList=[''.join(item) for item in all_rows]
            eList.insert(0,anion)
            eList.insert(0,cation)
            self.materialPhaseElements.append(eList)
            
#        ii=0
#        self.matPhaseFormEnergyList=list()
#        for ii,mat in enumerate(self.materials):
#            formEnergyFunList=list()
#            jj=0
#            for element in self.materialPhaseElements[ii]:
#                if jj==0:
#                    formEnergyFunList.append(lambda x: x)
#                elif jj==1:
#                    formEnergyFunList.append(lambda x: self.matFormEnergy[ii]-x)
#                else:
#                    self.cursor.execute("SELECT \"Formation Energy\" FROM MATERIALPHASE where Material='{0}' and Element='{1}'".format(mat,element))
#                    all_rows=self.cursor.fetchall()
#                    fe=all_rows[0][0]
#                    self.cursor.execute("SELECT Composition FROM MATERIALPHASE where Material='{0}' and Element='{1}'".format(mat,element))
#                    all_rows=self.cursor.fetchall()
#                    comp=ast.literal_eval(all_rows[0][0])
##                    fVal=lambda x: fe
#                    cationVal=0
#                    anionVal=0
#                    elementVal=0
#                    for data in comp:
#                        if data[0]==self.materialPhaseElements[0]:
#                            cationVal=data[1]
#                        if data[0]==self.materialPhaseElements[1]:
#                            anionVal=data[1]
#                        if data[0]==element:
#                            elementVal=data[1]
#                    formEnergyFunList.append(lambda x: (fe-cationVal*x-anionVal*(formEnergy-x))/elementVal)
#                jj=jj+1
#            self.matPhaseFormEnergyList.append(formEnergyFunList)        
##            ii=ii+1
        
        self.cursor.execute("SELECT Name,Description FROM SPECIES")
        all_rows=self.cursor.fetchall()
        self.species=[row[0] for row in all_rows]
        self.speciesText=[row[1] for row in all_rows]
        
        self.cursor.execute("SELECT Name,Description FROM MECHANISMS")
        all_rows=self.cursor.fetchall()
        self.mechanisms=[row[0] for row in all_rows]
        self.mechanismsText=[row[1] for row in all_rows]
        
        self.cursor.execute("SELECT Name,Description FROM REACTIONS")
        all_rows=self.cursor.fetchall()
        self.reactions=[row[0] for row in all_rows]
        self.reactionsText=[row[1] for row in all_rows]
        
        self.cursor.execute("SELECT Name from BGMODELS")
        all_rows=self.cursor.fetchall()
        self.bgModels=[row[0] for row in all_rows]
        
        self.bgModelsText=list()
        self.bgModelsParList=list()
        self.bgModelsnParList=list()
        self.bgModelsParUnitsList=list()
        for bgModelName in self.bgModels:
            self.cursor.execute("SELECT Description,nParam,paramNameList,paramUnits from MODELS where Name='{0}'".format(bgModelName))
            all_rows=self.cursor.fetchall()
#            modelsText=[row[0] for row in all_rows]
#            modelnParam=[row[1] for row in all_rows]
#            modelParamName=[row[2] for row in all_rows]
#            modelParamUnits=[row[3] for row in all_rows]
            
            modelsText=all_rows[0][0]
            modelnParam=all_rows[0][1]
            modelParamName=all_rows[0][2]
            modelParamUnits=all_rows[0][3]
            
            self.bgModelsText.append(modelsText)
            self.bgModelsParList.append(modelParamName)
            self.bgModelsnParList.append(ast.literal_eval(modelnParam))
            self.bgModelsParUnitsList.append(modelParamUnits)
        
        self.cursor.execute("SELECT Name from FREECARRIERMOBMODEL")
        all_rows=self.cursor.fetchall()
        self.freeCarrMobModels=[row[0] for row in all_rows]
        
        self.freeCarrMobModelsText=list()
        self.freeCarrMobModelsParList=list()
        self.freeCarrMobModelsnParList=list()
        self.freeCarrMobModelsParUnitsList=list()
        for freeCarrMobModelName in self.freeCarrMobModels:
            self.cursor.execute("SELECT Description,nParam,paramNameList,paramUnits from MODELS where Name='{0}'".format(freeCarrMobModelName))
            all_rows=self.cursor.fetchall()
            
            modelsText=all_rows[0][0]
            modelnParam=all_rows[0][1]
            modelParamName=all_rows[0][2]
            modelParamUnits=all_rows[0][3]
            
            self.freeCarrMobModelsText.append(modelsText)
            self.freeCarrMobModelsParList.append(modelParamName)
            self.freeCarrMobModelsnParList.append(ast.literal_eval(modelnParam))
            self.freeCarrMobModelsParUnitsList.append(modelParamUnits)
        
        self.cursor.execute("SELECT Name from REACTIONRATEMODELS")
        all_rows=self.cursor.fetchall()
        self.reactionRateModels=[row[0] for row in all_rows]
        
        self.reactionRateModelsText=list()
        self.reactionRateModelsParList=list()
        self.reactionRateModelsnParList=list()
        self.reactionRateModelsParUnitsList=list()
        for reactionRateModelName in self.reactionRateModels:
            self.cursor.execute("SELECT Description,nParam,paramNameList,paramUnits from MODELS where Name='{0}'".format(reactionRateModelName))
            all_rows=self.cursor.fetchall()
            
            modelsText=all_rows[0][0]
            modelnParam=all_rows[0][1]
            modelParamName=all_rows[0][2]
            modelParamUnits=all_rows[0][3]
            
            self.reactionRateModelsText.append(modelsText)
            self.reactionRateModelsParList.append(modelParamName)
            self.reactionRateModelsnParList.append(ast.literal_eval(modelnParam))
            self.reactionRateModelsParUnitsList.append(modelParamUnits)
        
        self.cursor.execute("SELECT Name from SPECIESDIFFMODELS")
        all_rows=self.cursor.fetchall()
        self.speciesDiffModels=[row[0] for row in all_rows]
        
        self.speciesDiffModelsText=list()
        self.speciesDiffModelsParList=list()
        self.speciesDiffModelsnParList=list()
        self.speciesDiffModelsParUnitsList=list()
        for speciesDiffModelName in self.speciesDiffModels:
            self.cursor.execute("SELECT Description,nParam,paramNameList,paramUnits from MODELS where Name='{0}'".format(speciesDiffModelName))
            all_rows=self.cursor.fetchall()
            
            modelsText=all_rows[0][0]
            modelnParam=all_rows[0][1]
            modelParamName=all_rows[0][2]
            modelParamUnits=all_rows[0][3]
            
            self.speciesDiffModelsText.append(modelsText)
            self.speciesDiffModelsParList.append(modelParamName)
            self.speciesDiffModelsnParList.append(ast.literal_eval(modelnParam))
            self.speciesDiffModelsParUnitsList.append(modelParamUnits)
        
        self.cursor.execute("SELECT Name from SPECIESNSMODELS")
        all_rows=self.cursor.fetchall()
        self.speciesSiteDenModels=[row[0] for row in all_rows]
        
        self.speciesSiteDenModelsText=list()
        self.speciesSiteDenModelsParList=list()
        self.speciesSiteDenModelsnParList=list()
        self.speciesSiteDenModelsParUnitsList=list()
        for speciesSiteDenModelName in self.speciesSiteDenModels:
            self.cursor.execute("SELECT Description,nParam,paramNameList,paramUnits from MODELS where Name='{0}'".format(speciesSiteDenModelName))
            all_rows=self.cursor.fetchall()
            
            modelsText=all_rows[0][0]
            modelnParam=all_rows[0][1]
            modelParamName=all_rows[0][2]
            modelParamUnits=all_rows[0][3]
            
            self.speciesSiteDenModelsText.append(modelsText)
            self.speciesSiteDenModelsParList.append(modelParamName)
            self.speciesSiteDenModelsnParList.append(ast.literal_eval(modelnParam))
            self.speciesSiteDenModelsParUnitsList.append(modelParamUnits)
            
        self.cursor.execute("SELECT Name from SPECIESGFMODELS")
        all_rows=self.cursor.fetchall()
        self.speciesFormEnergyModels=[row[0] for row in all_rows]
        
        self.speciesFormEnergyModelsText=list()
        self.speciesFormEnergyModelsParList=list()
        self.speciesFormEnergyModelsnParList=list()
        self.speciesFormEnergyModelsParUnitsList=list()
        for speciesFormEnergyModelName in self.speciesFormEnergyModels:
            self.cursor.execute("SELECT Description,nParam,paramNameList,paramUnits from MODELS where Name='{0}'".format(speciesFormEnergyModelName))
            all_rows=self.cursor.fetchall()
            
            modelsText=all_rows[0][0]
            modelnParam=all_rows[0][1]
            modelParamName=all_rows[0][2]
            modelParamUnits=all_rows[0][3]
            
            self.speciesFormEnergyModelsText.append(modelsText)
            self.speciesFormEnergyModelsParList.append(modelParamName)
            self.speciesFormEnergyModelsnParList.append(modelnParam)
            self.speciesFormEnergyModelsParUnitsList.append(modelParamUnits)
            
    def getReactionsForMechanism(self,mechName,mat=None):
        isInterface=0
        if mat is not None:
            if mat in self.materials:
                eString="SELECT reaction FROM MATERIALMECHANISMREACTIONS WHERE mechanism='{0}' AND material='{1}'".format(mechName,mat)
            elif "/" in mat:
                self.cursor.execute("SELECT prefer FROM INTERFACES WHERE Name='{0}'".format(mat))
                all_rows=self.cursor.fetchall()
                mat=all_rows[0][0]
#                eString1="SELECT reaction FROM MATERIALMECHANISMREACTIONS WHERE mechanism='{0}' AND material='{1}'".format(mechName,mat)
                isInterface=1
                eString="SELECT reaction FROM INTERFACEMECHANISMREACTIONS WHERE mechanism='{0}' AND material='{1}'".format(mechName,mat)
        else:
            eString="SELECT reaction,material FROM MATERIALMECHANISMREACTIONS WHERE mechanism='{0}'".format(mechName)
        self.cursor.execute(eString)
                
#        self.cursor.execute(eString)
        all_rows=self.cursor.fetchall()
        if mat is None:
            reactionTuple=tuple([row[0] for row in all_rows])
            materialTuple=tuple([row[1] for row in all_rows])
            return reactionTuple,materialTuple
        else:
            return tuple([row[0] for row in all_rows])
        
    def getSpeciesForReaction(self,reactionName):
        eString="SELECT LHSspecies1,LHSspecies2,RHSspecies1,RHSspecies2 FROM REACTIONS WHERE Name='{0}'".format(reactionName)
        self.cursor.execute(eString)
        all_rows=self.cursor.fetchall()
        speciesTuple=tuple(xi for xi in all_rows[0] if xi is not None)
        return speciesTuple
    
    def getMechInfo(self,mechName,mat=None):
        if mat is not None:
            reactionTuple=self.getReactionsForMechanism(mechName,mat)
        else:
            reactionTuple,matTuple=self.getReactionsForMechanism(mechName,mat)
        
        self.cursor.execute("SELECT Description FROM MECHANISMS WHERE Name='{0}'".format(mechName))
        all_rows=self.cursor.fetchall()
        description=[row[0] for row in all_rows]
        out=list()
        out.append(description[0])
        for ii in range(len(reactionTuple)):
            reaction=reactionTuple[ii]
#            reaction.replace("<=>","\\rightleftharpoons")
            rOut='$ '+reaction+' $'
            out.append(rOut)
        return "\n".join(out)
    
    def getReactionInfo(self,reactionName,matName):
        if "/" in matName:
            self.cursor.execute("SELECT prefer FROM INTERFACES WHERE Name='{0}'".format(matName))
            all_rows=self.cursor.fetchall()
            matName=all_rows[0][0]
        self.cursor.execute("SELECT LHSspecies1 FROM REACTIONS WHERE Name='{0}'".format(reactionName))
        all_rows=self.cursor.fetchall()
        lhs1=all_rows[0][0]
        self.cursor.execute("SELECT LHSspecies2 FROM REACTIONS WHERE Name='{0}'".format(reactionName))
        all_rows=self.cursor.fetchall()
        lhs2=all_rows[0][0]
        self.cursor.execute("SELECT RHSspecies1 FROM REACTIONS WHERE Name='{0}'".format(reactionName))
        all_rows=self.cursor.fetchall()
        rhs1=all_rows[0][0]
        self.cursor.execute("SELECT RHSspecies2 FROM REACTIONS WHERE Name='{0}'".format(reactionName))
        all_rows=self.cursor.fetchall()
        rhs2=all_rows[0][0]
        if lhs1 is None: lhs1=""
        if lhs2 is None: lhs2=""
        if rhs1 is None: rhs1=""
        if rhs2 is None: rhs2=""
        
        if lhs1=="" and lhs2=="":
            lhs1_lhs2="NULL"
        else:
            if lhs1=="":
                lhs1_lhs2=lhs2
            elif lhs2=="":
                lhs1_lhs2=lhs1
            else:
                lhs1_lhs2=lhs1+","+lhs2
        
        if rhs1=="" and rhs2=="":
            rhs1_rhs2="NULL"
        else:
            if rhs1=="":
                rhs1_rhs2=rhs2
            elif rhs2=="":
                rhs1_rhs2=rhs1
            else:
                rhs1_rhs2=rhs1+","+rhs2        
        
        out="LHS Species:\n"+lhs1_lhs2+"\n"+"RHS Species:\n"+rhs1_rhs2+"\n"
        self.cursor.execute("SELECT reactionRateModel,reactionRateModelParam,rateDirection FROM MATERIALREACTIONS WHERE reaction='{0}' AND material='{1}'".format(reactionName,matName))
        all_rows=self.cursor.fetchall()
        rrModelName=all_rows[0][0]
        rrParams=all_rows[0][1]
        rDirection=all_rows[0][2]
        self.cursor.execute("SELECT Description FROM MODELS WHERE Name='{0}'".format(rrModelName))
        all_rows=self.cursor.fetchall()
        rrDes=all_rows[0][0]
        
        if rrParams is None: rrParams="Nil"
        
        return out+"Model Name:\n"+rrModelName+"\n"\
                  +"Description:\n"+rrDes+"\n"\
                  +"Parameters:\n"+rrParams+"\n"\
                  +"Direction:"+rDirection
                  
    def getSpeciesInfo(self,speciesName,matName):
#        matName=PC_rectData.matName
        if "/" in matName:
            self.cursor.execute("SELECT prefer FROM INTERFACES WHERE Name='{0}'".format(matName))
            all_rows=self.cursor.fetchall()
            matName=all_rows[0][0]
            
        self.cursor.execute("SELECT NsModelName,NsModelParam,GfModelName,GfModelParam,DModelName,DModelParam\
                            FROM MATERIALSPECIES WHERE species='{0}' AND material='{1}'".format(speciesName,matName))
        all_rows=self.cursor.fetchall()
        NsName=all_rows[0][0]
        NsParam=all_rows[0][1]
        if NsParam is None: NsParam="Nil"
        GfName=all_rows[0][2]
        GfParam=all_rows[0][3]
        if GfParam is None: GfParam="Nil"
        DName=all_rows[0][4]
        DParam=all_rows[0][5]
        if DParam is None: DParam="Nil"
        
        self.cursor.execute("SELECT Description FROM MODELS WHERE Name='{0}'".format(NsName))
        all_rows=self.cursor.fetchall()
        NsDescptn=all_rows[0][0]
        
        self.cursor.execute("SELECT Description FROM MODELS WHERE Name='{0}'".format(GfName))
        all_rows=self.cursor.fetchall()
        GfDescptn=all_rows[0][0]
        
        self.cursor.execute("SELECT Description FROM MODELS WHERE Name='{0}'".format(DName))
        all_rows=self.cursor.fetchall()
        DDescptn=all_rows[0][0]
        
        out= "Ns Model Name:\n"+NsName+"\n"\
            +"Description:\n"+NsDescptn+"\n"\
            +"Parameters:\n"+NsParam+"\n"\
            +"Gf Model Name:\n"+GfName+"\n"\
            +"Description:\n"+GfDescptn+"\n"\
            +"Parameters:\n"+GfParam+"\n"\
            +"D Model Name:\n"+DName+"\n"\
            +"Description:\n"+DDescptn+"\n"\
            +"Parameters:\n"+DParam
            
        return out
    
    def getFormEnergy(self,matName):
        self.cursor.execute("SELECT \"Formation Energy\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        formEnergy=all_rows[0][0]
        return formEnergy
    
    def getAllSpecies(self,matName):
        self.cursor.execute("SELECT \"species\" FROM MATERIALSPECIES WHERE material='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        species=all_rows
        return species
    
    def getSpeciesFormEnergyData(self,matName,speciesName):
        self.cursor.execute("SELECT GfModelParam FROM MATERIALSPECIES WHERE species='{0}' AND material='{1}'".format(speciesName,matName))
        all_rows=self.cursor.fetchall()
        formEnergy=all_rows[0][0]
        return formEnergy
    
    def getSpeciesCharge(self,speciesName):
        self.cursor.execute("SELECT Charge FROM SPECIES WHERE Name='{0}'".format(speciesName))
        all_rows=self.cursor.fetchall()
        charge=all_rows[0][0]
        return charge
    
    def getSpeciesComposition(self,speciesName):
        self.cursor.execute("SELECT elementscount FROM SPECIES WHERE Name='{0}'".format(speciesName))
        all_rows=self.cursor.fetchall()
        charge=all_rows[0][0]
        return charge
    
#    def getMaterialPhaseElements(self,matName):
#        self.cursor.execute("SELECT Composition FROM MATERIALPHASE WHERE material='{0}'".format(matName))
#        all_rows=self.cursor.fetchall()
#        charge=all_rows[0][0]
#        return charge
    
    def getBandGap(self,matName):
        self.cursor.execute("SELECT \"Band Gap Model\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        bgModelName=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Band Gap Params\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        bgModelPar=all_rows[0][0]
        
        return bgModelName,bgModelPar
    
    def getCationAnion(self,matName):
        self.cursor.execute("SELECT Cation FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        cation=all_rows[0][0]
        
        self.cursor.execute("SELECT Anion FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        anion=all_rows[0][0]
        
        return cation,anion
    
    def updateProjMatModelData(self,PC_rectData):
        matName=PC_rectData.matName
        if "/" in matName:
            self.cursor.execute("SELECT prefer FROM INTERFACES WHERE Name='{0}'".format(PC_rectData.matName))
            all_rows=self.cursor.fetchall()
            matName=all_rows[0][0]

#        if PC_rectData.dType==0:
#        print("SELECT \"Electron Effective Mass\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        self.cursor.execute("SELECT \"Electron Effective Mass\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        eMass=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Hole Effective Mass\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        hMass=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Lattice Density\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        latDen=all_rows[0][0]

        self.cursor.execute("SELECT \"Electron Affinity\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        afnity=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Dielectric Permittivity\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        dielec=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Radiative Rate Constant\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        radRate=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Band Gap Model\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        bgModelName=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Band Gap Params\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        bgModelPar=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Electron Mobility Model\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        eMobModelName=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Electron Mobility Params\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        eMobModelPar=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Hole Mobility Model\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        hMobModelName=all_rows[0][0]
        
        self.cursor.execute("SELECT \"Hole Mobility Params\" FROM MATERIALS WHERE Name='{0}'".format(matName))
        all_rows=self.cursor.fetchall()
        hMobModelPar=all_rows[0][0]
        
        formEnergy=self.getFormEnergy(matName)
        
        cation,anion=self.getCationAnion(matName)
        
#        print('Inside DB function mat={0}, formEnergy={1}'.format(matName,formEnergy))
        
        PC_rectData.matPropData.update(eMass,hMass,latDen,afnity,dielec,radRate,bgModelName,bgModelPar,
                                   eMobModelName,eMobModelPar,hMobModelName,hMobModelPar,formEnergy)
        
        PC_rectData.matPropData.cation=cation
        PC_rectData.matPropData.anion=anion
    

    def updateProjSpeciesModelData(self,PC_rectData):
        matName=PC_rectData.matName
        isInterface=0        
        if "/" in matName:
            self.cursor.execute("SELECT prefer FROM INTERFACES WHERE Name='{0}'".format(PC_rectData.matName))
            all_rows=self.cursor.fetchall()
            matName=all_rows[0][0]
            isInterface=1
        
        matProp=PC_rectData.matPropData
        speciesPropDataList=list()
        for species in PC_rectData.speciesList:
            print('species={0}'.format(species))
            all_rows=list()
            if isInterface==1:
                self.cursor.execute("SELECT NsModelName,NsModelParam,GfModelName,GfModelParam,DModelName,DModelParam\
                            FROM INTERFACESPECIES WHERE species='{0}' AND material='{1}'".format(species,PC_rectData.matName))
                all_rows=self.cursor.fetchall()
            
            if len(all_rows)==0:
                self.cursor.execute("SELECT NsModelName,NsModelParam,GfModelName,GfModelParam,DModelName,DModelParam\
                            FROM MATERIALSPECIES WHERE species='{0}' AND material='{1}'".format(species,matName))
                all_rows=self.cursor.fetchall()
            
            NsName=all_rows[0][0]
            NsParam=all_rows[0][1]
            GfName=all_rows[0][2]
            GfParam=all_rows[0][3]
            DName=all_rows[0][4]
            DParam=all_rows[0][5]
            
            self.cursor.execute("SELECT Charge,elementscount FROM SPECIES WHERE Name='{0}'".format(species))
            all_rows=self.cursor.fetchall()
            q=all_rows[0][0]
            elements=all_rows[0][1]
            
#            cationLoss=getCationLoss(matProp.cation,species)
#            anionLoss=getAnionLoss(matProp.anion,species)
            skip=False
            if isElectron(species) or isHole(species):
                skip=True
            if isCationAtCationSite(matProp.cation,species) or isAnionAtAnionSite(matProp.anion,species):
                skip=True
            if isReservior(species):
                skip=True
            if not skip:
                correction=self.getCorrectedPotential(matName,species,matProp.cationChemPot)
            else:
                correction=0
#            print('species={0}'.format(species))
#            print('correction1={0}'.format(correction))
#            print('chemPot={0}'.format(matProp.cationChemPot))
            speciesPropData=PVRD_speciesPropData()
            speciesPropData.update(DName,DParam,NsName,NsParam,GfName,GfParam,q,elements,matProp,correction)
            
            speciesPropDataList.append(speciesPropData)
        PC_rectData.updateSpeciesPropDataList(speciesPropDataList)
    
    def updateProjReactionModelData(self,PC_rectData):
        matName=PC_rectData.matName
        isInterface=0
        if "/" in matName:
            self.cursor.execute("SELECT prefer FROM INTERFACES WHERE Name='{0}'".format(PC_rectData.matName))
            all_rows=self.cursor.fetchall()
            matName=all_rows[0][0]
            isInterface=1
        
        matProp=PC_rectData.matPropData
        speciesPropData=PC_rectData.speciesPropDataList
        speciesList=PC_rectData.speciesList
        reactionsPropDataList=list()
        for reaction in PC_rectData.reactionList:
#            print('reaction={0}'.format(reaction))
#            print('material={0}'.format(matName))
            all_rows=list()
            if isInterface==1:
                self.cursor.execute("SELECT reactionRateModel,reactionRateModelParam,rateDirection\
                            FROM INTERFACEREACTIONS WHERE reaction='{0}' AND material='{1}'".format(reaction,PC_rectData.matName))
                all_rows=self.cursor.fetchall()
            if len(all_rows)==0:
                self.cursor.execute("SELECT reactionRateModel,reactionRateModelParam,rateDirection\
                            FROM MATERIALREACTIONS WHERE reaction='{0}' AND material='{1}'".format(reaction,matName))
                all_rows=self.cursor.fetchall()
                
#            all_rows=self.cursor.fetchall()
            rrModel=all_rows[0][0]
            rrParam=all_rows[0][1]
            rrSide=all_rows[0][2]
            if rrSide=='F':
                rVal=1
            elif rrSide=='B':
                rVal=-1
            else:
                rVal=0
            
            self.cursor.execute("SELECT LHSspecies1,LHSspecies2,RHSspecies1,RHSspecies2\
                            FROM REACTIONS WHERE Name='{0}'".format(reaction))
            all_rows=self.cursor.fetchall()
            lhs1=all_rows[0][0]
            lhs2=all_rows[0][1]
            rhs1=all_rows[0][2]
            rhs2=all_rows[0][3]
            
            LHSlist=list()
            RHSlist=list()
            
            if lhs1 is not None:
                LHSlist.append(lhs1)
            if lhs2 is not None:
                LHSlist.append(lhs2)
            
            if rhs1 is not None:
                RHSlist.append(rhs1)
            if rhs2 is not None:
                RHSlist.append(rhs2)
                
            reactionPropData=PVRD_reactionPropData()
            reactionPropData.update(rrModel,rrParam,rVal,LHSlist,RHSlist,speciesList,speciesPropData,matProp)
            reactionsPropDataList.append(reactionPropData)
        
        PC_rectData.updateReactionPropDataList(reactionsPropDataList)
    
    def updateDatabase(self,fileName):
        self.dbName=fileName
        self.update()
        
class PVRD_speciesPropData():
    def __init__(self):
        self.diffModel=1
        self.diffParList=1
        
        self.siteDenModel=1
        self.siteDenParList=1
        
        self.formEnergyModel=1
        self.formEnergyParList=1
        
        self.cationLoss=0
        self.anionLoss=0
        self.correction=0
        
    def update(self,diffModel,diffPar,siteDenModel,siteDenPar,formEnergyModel,formEnergyPar,q,elemCount,matProp,correction):
        self.diffModel=diffModel
        self.diffParList=diffPar
        
        self.siteDenModel=siteDenModel
        self.siteDenParList=siteDenPar
        
        self.formEnergyModel=formEnergyModel
        self.formEnergyParList=formEnergyPar
        
        self.q=q
        self.elemCountLit=elemCount
        self.correction=correction
        
#        print('formEnergyParList={0}'.format(self.formEnergyParList))
#        print('Correction={0}'.format(self.correction))
        
#        self.cationLoss=catLoss
#        self.anionLoss=anLoss
        
        diffFun=getattr(PVRD_models,diffModel)
        self.diff=lambda T:diffFun(self.diffParList,T,matProp)
        
        siteDenFun=getattr(PVRD_models,siteDenModel)
        self.siteDen=lambda T:siteDenFun(self.siteDenParList,T,matProp)
        
        formEnergyFun=getattr(PVRD_models,formEnergyModel)
        self.formEnergy=lambda T:formEnergyFun(self.q,self.formEnergyParList,T,matProp,self.correction)
        
        self.elementNameList=list()
        self.elementCountList=list()
        if self.elemCountLit is not None:
            elem=ast.literal_eval(self.elemCountLit)
            for element in elem:
                self.elementNameList.append(element[0])
                self.elementCountList.append(element[1])

class PVRD_reactionPropData():
    def __init__(self):
        self.rateModel=1
        self.rateParList=1
        self.limitingSide=1
#        
    def update(self,rateModel,ratePar,rateSide,LHS,RHS,speciesList,speciesProp,matProp):
        self.rateModel=rateModel
        self.rateParList=ratePar
        self.limitingSide=rateSide
#        self.rateSide=rateSide
        self.LHS=LHS
        self.RHS=RHS
        
        self.eqRatio=lambda T:PVRD_models.getKeqRatio(LHS,RHS,speciesList,speciesProp,T)
#        self.eqRatio=lambda T:
        
        rateFun=getattr(PVRD_models,rateModel)
        if self.limitingSide==1: #Forward is limiting
            self.KF=lambda T:rateFun(self.rateParList,T,speciesList,speciesProp,LHS,matProp)
            self.KB=lambda T:self.KF(T)/self.eqRatio(T)
        elif self.limitingSide==-1:
            self.KB=lambda T:rateFun(self.rateParList,T,speciesList,speciesProp,RHS,matProp)
            self.KF=lambda T:self.KB(T)*self.eqRatio(T)
            
        
        
#        ii=0
#        self.KF_list=list()
#        self.KB_list=list()
#        for rName in self.rateModelName:
#            rName=self.rateModelName[ii]
#            rPar=self.rateModelPar[ii]
#            parValList=parseString(rPar)
#            rSide=self.rateSide[ii]
#            lhs=self.LHS[ii]
#            rhs=self.RHS[ii]
#            
#            ratio=getEntropyChange(lhs,rhs) # entropy(lhs) / entropy(rhs)
#            
#            rateFun=getattr(PVRD_models,rName)
#            
#            if rSide==0: # Forward Limited
#                KF=lambda T:rateFun(rPar)
#            ii=ii+1
