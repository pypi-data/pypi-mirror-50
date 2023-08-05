#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:36:41 2018

@author: abdul
"""

from .poissonSolver import PoissonSolver
import numpy as np
import scipy.constants
import scipy.sparse as sps
import scipy.sparse.linalg as spsl

class simple_PS(PoissonSolver):
    Ap=np.array([])
    def __init__(self,numEng):
        self.numEng=numEng
        self.Top=0
        self.Bottom=0
        self.formAp()

    def updateFields(self):
        numEng=self.numEng
    
    def formAp(self):
        mG=self.numEng.mGrid
        Hx=mG.Hx
        Hy=mG.Hy
        hx=mG.hx
        hy=mG.hy
        self.Top=np.reshape(self.numEng.FC_BC[:,-1],(mG.nX,3))
        self.Bottom=np.reshape(self.numEng.BC_BC[:,-1],(mG.nX,3))
        
        Eps2D=np.reshape(self.numEng.Eps,(mG.nX,mG.nY))
        
        eps_x=1/hx*(2/(1/Eps2D[1:,:] + 1/Eps2D[0:-1,:]))
        eps_y=1/hy*(2/(1/Eps2D[:,1:] + 1/Eps2D[:,0:-1]))
        
        sN=0*Hx;
        sS=0*Hx;
        sW=0*Hx;
        sE=0*Hx;
        
        sN[:,1:  ] =-Hx[:,0:-1]*eps_y
        sS[:,0:-1] =-Hx[:,1:  ]*eps_y
        
        sE[1:  ,:]=-Hy[0:-1,:]*eps_x
        sW[0:-1,:]=-Hy[1:  ,:]*eps_x
        
        sN=np.reshape(sN,(1,-1))
        sS=np.reshape(sS,(1,-1))
        
        sE=np.reshape(sE,(1,-1))
        sW=np.reshape(sW,(1,-1))
        
        sC=np.zeros((mG.nX,mG.nY))
        
        sC[1:,:]=sC[1:,:]+Hy[1:,:]*eps_x
        sC[0:-1,:]=sC[0:-1,:]+Hy[0:-1,:]*eps_x 
        
        sC[:,1:]=sC[:,1:]+Hx[:,1:]*eps_y
        sC[:,0:-1]=sC[:,0:-1]+Hx[:,0:-1]*eps_y
        
        sC[:,0]=sC[:,0]+Hx[:,0]*self.Bottom[:,0]/self.Bottom[:,1]
        sC[:,-1]=sC[:,-1]-Hx[:,-1]*self.Top[:,0]/self.Top[:,1]
        
        sCent = np.reshape(sC,(1,-1))
        
        # center(0), South(-1),North(1),West[-(mG.nX-1)],East(mG.nX-1)
        diagLoc = [0,-1,1,-mG.nY,mG.nY]
#        diags = [sCent,sS,sN,sW,sE]
#        print('sN type={0}'.format(sN.shape))
#        print('sN={0}'.format(sN))
        
#        print('sS type={0}'.format(sS.shape))
#        print('sS={0}'.format(sS))
        
#        print('sE type={0}'.format(sE.shape))
#        print('sE={0}'.format(sE))
        
#        print('sW type={0}'.format(sW.shape))
#        print('sW={0}'.format(sW))
        
#        print('sCent type={0}'.format(sCent.shape))
#        print('sCent={0}'.format(sCent))
#        print("nX={0},nY={1}".format(mG.nX,mG.nY))
        diags = np.vstack((sCent,sS,sN,sW,sE))
        
#        print("diags={0},\n diagLoc={1}".format(type(diags),diagLoc))
#        if not sW.size==0:
        self.Ap=sps.diags(diags,diagLoc,shape=(mG.nX*mG.nY,mG.nX*mG.nY))
#        else:
#            self.Ap = sps.diags([sCent,sS,sN],[0,-1,1],shape=(mG.nX*mG.nY,mG.nX*mG.nY))
        return
    
    def Solve(self,dt):
        mG=self.numEng.mGrid
        Hx=mG.Hx
        Hy=mG.Hy
        
        # negative sign is absorbed in the discretization matrix.
        sF= scipy.constants.e*np.reshape(np.dot(self.numEng.uD_sol,self.numEng.qVec)+self.numEng.Dop,(mG.nX,mG.nY))*mG.Hx*mG.Hy
        
        sF[:,0]=sF[:,0]+Hx[:,0]*self.Bottom[:,2]/self.Bottom[:,1]
        sF[:,-1]=sF[:,-1]-Hx[:,-1]*self.Top[:,2]/self.Top[:,1]
        
        sF=np.reshape(sF,(-1,1))
        
        out=spsl.spsolve(self.Ap,sF)
        
        out=np.reshape(out,(mG.nX,mG.nY))
        return out
    
