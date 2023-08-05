#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 12:39:30 2019

@author: abdul
"""

from .diffusionSolver import DiffusionSolver
from .Berfun import Berfun
import numpy as np
import scipy.constants
import scipy.sparse as sps
import scipy.sparse.linalg as spsl

class simul_DS_ber_FOP(DiffusionSolver):
    def Solve(self,dt):
#        print('inside DS FOP\n')
        out=np.array([])
        fi=self.numEng.fi_sol
        mG=self.numEng.mGrid
        Hx=mG.Hx
        Hy=mG.Hy
        hx=mG.hx
        hy=mG.hy
        
        u0=self.numEng.uD_solInit.copy()
        
        uSol=np.zeros((mG.nX*mG.nY,self.numEng.M))
        T_uSol=np.zeros((mG.nX*mG.nY,self.numEng.M))
        self.tOperator = sps.lil_matrix((mG.nX*mG.nY*self.numEng.M,mG.nX*mG.nY*self.numEng.M))
        
        sF_bc=np.zeros((mG.nX*mG.nY*self.numEng.M,1))
        vol=np.zeros((mG.nX*mG.nY*self.numEng.M,1))
        
        for ii in range(0,self.numEng.M):
            indx=(ii)*mG.nX*mG.nY+np.arange(0,mG.nX*mG.nY)
#            print('before vol assignment')
            vol[indx]=np.reshape(Hx*Hy,(mG.nX*mG.nY,1),order='C')
#            ppp=np.reshape(Hx*Hy,(mG.nX*mG.nY,1),order='C')
#            print('after vol assignment')
#            self.numEng.fIO.write('\nvol\n')
#            np.savetxt(self.numEng.fIO,ppp,fmt='%2.2e')
#            self.numEng.fIO.close()
#            exit()
            if max(self.numEng.D[:,ii])==0:
                uSol[:,ii]=u0[:,ii]
                continue
#            print('ii={0}'.format(ii))
            uT=np.reshape(u0[:,ii],(mG.nX,mG.nY))
            sF=Hx*Hy*uT*0/dt

#            Bottom=np.reshape(self.numEng.BC_BC[:,ii],(mG.nX,3),order='F')
#            Top=np.reshape(self.numEng.FC_BC[:,ii],(mG.nX,3),order='F')
            
            Bottom=np.reshape(self.numEng.FC_BC[:,ii],(mG.nX,3),order='F')
            Top=np.reshape(self.numEng.BC_BC[:,ii],(mG.nX,3),order='F')

            D_2D=np.reshape(self.numEng.D[:,ii],(mG.nX,mG.nY))
            
            Dh_x=1/hx*2/(1/D_2D[1:,:]+1/D_2D[0:-1,:])
            Dh_y=1/hy*2/(1/D_2D[:,1:]+1/D_2D[:,0:-1])

            G_2D=np.reshape(self.numEng.G[:,ii]/self.numEng.Vt,(mG.nX,mG.nY))
            Ns_2D=np.reshape(self.numEng.Ns[:,ii],(mG.nX,mG.nY))
            QFL_2D=G_2D-np.log(Ns_2D)+self.numEng.qVec[ii]*fi

            dPhi_x=QFL_2D[1:,:]-QFL_2D[0:-1,:]
            dPhi_y=QFL_2D[:,1:]-QFL_2D[:,0:-1]
            
            berVal_plus_dPhi_x,berVal_minus_dPhi_x=Berfun(dPhi_x)
            berVal_plus_dPhi_y,berVal_minus_dPhi_y=Berfun(dPhi_y)
            
#            self.numEng.fIO.write('Hy {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,Hy,fmt='%2.2e')
#            
#            self.numEng.fIO.write('D_2D {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,D_2D,fmt='%2.2e')
#            
#            self.numEng.fIO.write('Dh_y {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,Dh_y,fmt='%2.2e')

            sN=0*Hx;
            sS=0*Hx;
            sW=0*Hx;
            sE=0*Hx;
            
            sN[:,1:  ] =-Hx[:,0:-1]*Dh_y*berVal_minus_dPhi_y
            sS[:,0:-1] =-Hx[:,1:  ]*Dh_y*berVal_plus_dPhi_y
            
            sE[1:  ,:] =-Hy[0:-1,:]*Dh_x*berVal_minus_dPhi_x
            sW[0:-1,:] =-Hy[1:  ,:]*Dh_x*berVal_plus_dPhi_x
            
            sC=0*Hx*Hy/dt
#            sC1=Hx*Hy/dt

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

            sF[:,0]=sF[:,0]*Bottom[:,1]+Hx[:,0]*Bottom[:,2]
            sF[:,-1]=sF[:,-1]*Top[:,1]-Hx[:,-1]*Top[:,2]
            
            if ii==self.numEng.eIndx or ii==self.numEng.hIndx:
                sC[:,0]=0
                sN[:,1]=0
                sE[:,0]=0
                sW[:,0]=0
                
                sC[:,-1]=0
                sS[:,-2]=0
                sE[:,-1]=0
                sW[:,-1]=0
                
                sF[:,0]=0
                sF[:,-1]=0
                
#            self.numEng.fIO.write('sC Before {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,sC,fmt='%2.2e')
#            
#            self.numEng.fIO.write('sN Before {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,sN,fmt='%2.2e')
            
            sF=np.reshape(sF,(-1,1),order='C')

            sCent=np.reshape(sC,(1,-1),order='C')
#            sCent1=np.reshape(sC1,(1,-1),order='F')
            sN=np.reshape(sN,(1,-1),order='C')
            sS=np.reshape(sS,(1,-1),order='C')
            sE=np.reshape(sE,(1,-1),order='C')
            sW=np.reshape(sW,(1,-1),order='C')
            

            if self.numEng.nDims==2:
#                diagLoc = [0,-1,-mG.nX,mG.nX,1]
#                diags = np.vstack((sCent,sW,sS,sN,sE))
                
                diagLoc = [0,-1,-mG.nY,mG.nY,1]
                diags = np.vstack((sCent,sS,sW,sE,sN))
                
            else:
                diagLoc = [0,-1,1]
                diags = np.vstack((sCent,sS,sN))
                
#            self.numEng.fIO.write('\nsC After {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,sCent,fmt='%2.2e')
#            
#            self.numEng.fIO.write('\nsN After {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,sN,fmt='%2.2e')
#                
#            self.numEng.fIO.close()
#            exit()

            temp_Ap=sps.spdiags(diags,diagLoc,mG.nX*mG.nY,mG.nX*mG.nY)
            T_operator=temp_Ap
            
#            self.numEng.fIO.write('T_operator {0}\n'.format(ii))
#            np.savetxt(self.numEng.fIO,T_operator.todense(),fmt='%2.2e')
#            self.numEng.fIO.close()
#            exit()
#            print('near tOperator assignment')
#            print('indx={0}'.format(indx))
#            print('T_operator size={0}'.format(T_operator.shape))
#            print('self_tOpertor shape={0}'.format(self.tOperator.shape))
#            ppp=self.tOperator[indx,indx]
#            print('self_tOperator ={0}'.format(ppp))
#            print('ppp ={0}'.format(ppp.shape))
            sIndx=ii*mG.nX*mG.nY+0
            eIndx=ii*mG.nX*mG.nY+mG.nX*mG.nY
            
#            print('T_operator shape={0}'.format(T_operator.shape))
            
            self.tOperator[sIndx:eIndx,sIndx:eIndx]=T_operator
            
            
#            temp_A=sps.spdiags(sCent1,0,mG.nX*mG.nY,mG.nX*mG.nY)+temp_Ap
#            print('after tOperator assignment')
            sF_bc[indx]=sF
#            print('final')
#            exit()
#            uSolTemp=spsl.spsolve(temp_Ap,sF)
#            uSolTemp1=np.reshape(uSolTemp,(mG.nX,mG.nY),order='F')
#
#            uSolOut=np.reshape(uSolTemp1,(1,mG.nX*mG.nY))
#
#            uSol[:,ii]=uSolOut


        self.numEng.tOperator=-self.tOperator
        self.numEng.sF_BC=-sF_bc
        self.numEng.Vol=vol
        
#        self.numEng.fIO.write('T_operator {0}\n'.format(ii))
#        np.savetxt(self.numEng.fIO,self.tOperator.todense(),fmt='%2.5e')
#        
##        exit()
#        self.numEng.fIO.close()
#        exit()
        
        out=uSol 
        return out
    def updateFields(self):
        numEng=self.numEng
