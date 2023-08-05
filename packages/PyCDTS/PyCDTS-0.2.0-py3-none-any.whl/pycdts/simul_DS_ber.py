#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:08:32 2018

@author: abdul
"""

from .diffusionSolver import DiffusionSolver
from .Berfun import Berfun
import numpy as np
import scipy.constants
import scipy.sparse as sps
import scipy.sparse.linalg as spsl

class simul_DS_ber(DiffusionSolver):
    def Solve(self,dt):
        out=np.array([])
        fi=self.numEng.fi_sol
        mG=self.numEng.mGrid
        Hx=mG.Hx
        Hy=mG.Hy
        hx=mG.hx
        hy=mG.hy
        
#        self.numEng.fIO.write('Hx\n')
#        np.savetxt(self.numEng.fIO,Hx,fmt='%2.2e')
#        self.numEng.fIO.write('Hy\n')
#        np.savetxt(self.numEng.fIO,Hy,fmt='%2.2e')
#        self.numEng.fIO.write('hx\n')
#        np.savetxt(self.numEng.fIO,hx,fmt='%2.2e')
#        self.numEng.fIO.write('hy\n')
#        np.savetxt(self.numEng.fIO,hy,fmt='%2.2e')
#        self.numEng.fIO.write('D\n')
#        np.savetxt(self.numEng.fIO,self.numEng.D,fmt='%2.2e')
#        exit()
#        self.numEng.fIO.write('U0\n')
#        np.savetxt(self.numEng.fIO,self.numEng.U0,fmt='%2.2e')
        
#        self.numEng.fIO.write('UR\n')
#        np.savetxt(self.numEng.fIO,self.numEng.uD_solInit,fmt='%2.2e')
        
        
        u0=self.numEng.uD_solInit.copy()
        
        uSol=np.zeros((mG.nX*mG.nY,self.numEng.M))
#        print("Inside simul_DS_ber solve() with dt={0}".format(dt))
#        print("M={0}".format(self.numEng.M))
        
        for ii in range(0,self.numEng.M):
#            print("start ii={0},dVal={1}".format(ii,max(self.numEng.D[:,ii])))
            if max(self.numEng.D[:,ii])==0:
                uSol[:,ii]=u0[:,ii]
                continue
#            print("After ii={0}".format(ii))
            uT=np.reshape(u0[:,ii],(mG.nX,mG.nY))
            sF=Hx*Hy*uT/dt
            
#            print("After_11 ii={0}".format(ii))
            
#            Bottom=np.reshape(self.numEng.BC_BC[:,ii],(mG.nX,3),order='F')
#            Top=np.reshape(self.numEng.FC_BC[:,ii],(mG.nX,3),order='F')
#            
#            Bottom_C=np.reshape(self.numEng.BC_BC[:,ii],(mG.nX,3),order='C')
#            Top_C=np.reshape(self.numEng.FC_BC[:,ii],(mG.nX,3),order='C')
            
            Bottom=np.reshape(self.numEng.BC_BC[:,ii],(mG.nX,3),order='F')
            Top=np.reshape(self.numEng.FC_BC[:,ii],(mG.nX,3),order='F')
            
#            Bottom_C=np.reshape(self.numEng.BC_BC[:,4],(mG.nX,3),order='C')
#            Top_C=np.reshape(self.numEng.FC_BC[:,4],(mG.nX,3),order='C')
#            
#            self.numEng.fIO.write('BC_BC\n')
#            np.savetxt(self.numEng.fIO,self.numEng.BC_BC,fmt='%2.2e')
#            self.numEng.fIO.write('FC_BC\n')
#            np.savetxt(self.numEng.fIO,self.numEng.FC_BC,fmt='%2.2e')
#            
#            self.numEng.fIO.write('Bottom(F)\n')
#            np.savetxt(self.numEng.fIO,Bottom,fmt='%2.2e')
#            self.numEng.fIO.write('Bottom(C)\n')
#            np.savetxt(self.numEng.fIO,Bottom_C,fmt='%2.2e')
#            
#            self.numEng.fIO.write('Top(F)\n')
#            np.savetxt(self.numEng.fIO,Top,fmt='%2.2e')
#            self.numEng.fIO.write('Top(C)\n')
#            np.savetxt(self.numEng.fIO,Top_C,fmt='%2.2e')
            
#            print("After_12 ii={0}".format(ii))
            
            D_2D=np.reshape(self.numEng.D[:,ii],(mG.nX,mG.nY))
            
            Dh_x=1/hx*2/(1/D_2D[1:,:]+1/D_2D[0:-1,:])
            Dh_y=1/hy*2/(1/D_2D[:,1:]+1/D_2D[:,0:-1])
            
#            print("After_13 ii={0}".format(ii))
#            print('Vt={0}'.format(self.numEng.Vt))
            G_2D=np.reshape(self.numEng.G[:,ii]/self.numEng.Vt,(mG.nX,mG.nY))
#            print("After_14 ii={0}".format(ii))
            Ns_2D=np.reshape(self.numEng.Ns[:,ii],(mG.nX,mG.nY))
            
#            print("After_15 ii={0}".format(ii))
#            print('Ns_2D:min={0},max={1}'.format(min(self.numEng.Ns[:,ii]),max(self.numEng.Ns[:,ii])))
#            print('Ns_2D is {0} and fi is {1}'.format(Ns_2D.shape,fi.shape))
            QFL_2D=G_2D-np.log(Ns_2D)+self.numEng.qVec[ii]*fi
            
#            print("After_1 ii={0}".format(ii))
            
            dPhi_x=QFL_2D[1:,:]-QFL_2D[0:-1,:]
            dPhi_y=QFL_2D[:,1:]-QFL_2D[:,0:-1]
            
            berVal_plus_dPhi_x,berVal_minus_dPhi_x=Berfun(dPhi_x)
            berVal_plus_dPhi_y,berVal_minus_dPhi_y=Berfun(dPhi_y)
            
#            print("After_2 ii={0}".format(ii))
            sN=0*Hx;
            sS=0*Hx;
            sW=0*Hx;
            sE=0*Hx;
            
            sN[:,1:  ] =-Hx[:,0:-1]*Dh_y*berVal_minus_dPhi_y
            sS[:,0:-1] =-Hx[:,1:  ]*Dh_y*berVal_plus_dPhi_y
            
            sE[1:  ,:] =-Hy[0:-1,:]*Dh_x*berVal_minus_dPhi_x
            sW[0:-1,:] =-Hy[1:  ,:]*Dh_x*berVal_plus_dPhi_x
            
            sC=Hx*Hy/dt
            
#            print("After_3 ii={0}".format(ii))
            
            sC[:,0:-1]=sC[:,0:-1]+Hx[:,0:-1]*Dh_y*berVal_plus_dPhi_y
            sC[:,1:]=sC[:,1:]+Hx[:,1:]*Dh_y*berVal_minus_dPhi_y
            sC[0:-1,:]=sC[0:-1,:]+Hy[0:-1,:]*Dh_x*berVal_plus_dPhi_x
            sC[1:,:]=sC[1:,:]+Hy[1:,:]*Dh_x*berVal_minus_dPhi_x
            
            sC[:,0]=sC[:,0]*Bottom[:,1]+Hx[:,0]*Bottom[:,0]
            sN[:,1]=sN[:,1]*Bottom[:,1]
            sE[:,0]=sE[:,0]*Bottom[:,1]
            sW[:,0]=sW[:,0]*Bottom[:,1]
            
            sC[:,-1]=sC[:,-1]*Top[:,1]-Hx[:,-1]*Top[:,0]
            sS[:,-2]=sS[:,-2]*Top[:,1]
            sE[:,-1]=sE[:,-1]*Top[:,1]
            sW[:,-1]=sW[:,-1]*Top[:,1]
            
#            print("After_4 ii={0}".format(ii))
            
            
            
            sF[:,0]=sF[:,0]*Bottom[:,1]+Hx[:,0]*Bottom[:,2]
            sF[:,-1]=sF[:,-1]*Top[:,1]-Hx[:,-1]*Top[:,2]
            
            sF=np.reshape(sF,(-1,1),order='F')
            
#            self.numEng.fIO.write('sN\n')
#            np.savetxt(self.numEng.fIO,sN,fmt='%2.2e')
#            self.numEng.fIO.write('sS\n')
#            np.savetxt(self.numEng.fIO,sS,fmt='%2.2e')
            
            sCent=np.reshape(sC,(1,-1),order='F')
            sN=np.reshape(sN,(1,-1),order='F')
            sS=np.reshape(sS,(1,-1),order='F')
            sE=np.reshape(sE,(1,-1),order='F')
            sW=np.reshape(sW,(1,-1),order='F')
#            print("After_5 ii={0}".format(ii))
            
            # center(0), South(-1),North(1),West[-(mG.nX-1)],East(mG.nX-1)
#            diagLoc = [0,-1,1,-mG.nY,mG.nY]
            if self.numEng.nDims==2:
                diagLoc = [0,-1,-mG.nX,mG.nX,1]
                diags = np.vstack((sCent,sW,sS,sN,sE))
            else:
                diagLoc = [0,-1,1]
                diags = np.vstack((sCent,sS,sN))
            
#            print("After_5_2 ii={0}".format(ii))
#            if not sW.size==0:
#            self.numEng.fIO.write('sN\n')
#            np.savetxt(self.numEng.fIO,sN,fmt='%2.2e')
#            self.numEng.fIO.write('sS\n')
#            np.savetxt(self.numEng.fIO,sS,fmt='%2.2e')
            temp_Ap=sps.spdiags(diags,diagLoc,mG.nX*mG.nY,mG.nX*mG.nY)
#            self.numEng.fIO.write('Mat\n')
#            np.savetxt(self.numEng.fIO,temp_Ap.todense(),fmt='%2.2e')
#            self.numEng.fIO.close()
#            exit()
#            print("1)ii={0}".format(ii))
            uSolTemp=spsl.spsolve(temp_Ap,sF)
#            print("2)ii={0}".format(ii))
            uSolTemp1=np.reshape(uSolTemp,(mG.nX,mG.nY),order='F')
#            print("3)ii={0}".format(ii))
            uSolOut=np.reshape(uSolTemp1,(1,mG.nX*mG.nY))
#            print("4)ii={0}".format(ii))
            
#            self.numEng.fIO.write('uT\n')
#            np.savetxt(self.numEng.fIO,u0[:,ii],fmt='%2.2e')
#            self.numEng.fIO.write('uSol\n')
#            np.savetxt(self.numEng.fIO,uSolOut,fmt='%2.2e')
#            self.numEng.fIO.close()
#            exit()
#            else:
#                temp_Ap = sps.diags([sCent,sS,sN],[0,-1,1],shape=(mG.nX*mG.nY,mG.nX*mG.nY))
#            print("ii={0}".format(ii))            
            uSol[:,ii]=uSolOut

        
        # Should check for nan, inf's and negative concentrations.
        out=uSol 
#        print('Before Return DS')
        return out
    def updateFields(self):
        numEng=self.numEng
