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
# Python porting done by Abdul Rawoof Shaik (ASU)
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 23:44:49 2019

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from .reactionSolver import ReactionSolver
import numpy as np
import scipy.constants
import scipy.sparse as sps
import scipy.sparse.linalg as spsl
from .generalFunctions import swapForReactions
#from scikits.umfpack import spsolve
import time

class simul_RS2_FOP(ReactionSolver):
    NetRates=0
    Jacobian=0
    def __init__(self,numEng):
        self.numEng=numEng
        self.nIterMax=40
        self.I=sps.eye(numEng.nX*numEng.nY*numEng.M,numEng.nX*numEng.nY*numEng.M)
        self.xEntries=0
        self.yEntires=0
        
        self.pWeight=0
        
        self.formQPK()
    
    def Solve(self,dt):
        out=np.array([])
        
#        if self.numEng.time>=1e-14:
#            uInit_1=self.numEng.uInit.copy()
#            self.numEng.fIO.write('\nuInit_1 \n')
#            np.savetxt(self.numEng.fIO,uInit_1,fmt='%2.2e')
#            print('dt={0}'.format(dt))
#            self.numEng.fIO.close()
#            exit()
#        nX=self.numEng.nX
#        nY=self.numEng.nY
#        normal=np.arange(0,nX*nY)
#        trans=np.reshape(np.transpose(np.reshape(normal,(nX,nY))),(nX*nY,))
        
#        self.numEng.fIO.write('\nuInit_1 \n')
#        np.savetxt(self.numEng.fIO,uInit_1,fmt='%2.2e')
        
        
#        print('normal={0}'.format(normal))
#        print('trans={0}'.format(trans))
#        print('uInit_1 ={0}'.format(uInit_1.shape))
#        self.numEng.fIO.close()
#        exit()
        
#        uInit_1[normal,:]=self.numEng.uInit[trans,:]
        
        
        u0=np.reshape(self.numEng.uInit.T,(self.numEng.nX*self.numEng.nY*self.numEng.M,1),order='F')
#        u0=np.reshape(uInit_1.T,(self.numEng.nX*self.numEng.nY*self.numEng.M,1),order='F')
        
        
        uReact=u0
        uReactPrev=u0
        uReactOld=u0
        
        nIterReact=0
        EReact=np.float64('inf')
        R=sps.csr_matrix([])
        Jac=sps.csr_matrix([])
        convergeReact=1
        nX=self.numEng.nX
        nY=self.numEng.nY
        M=self.numEng.M
        
        if not self.numEng.is0D:
#            tS=time.time()
#            print('before swap')
#            self.numEng.fIO.write('tOp before \n')
#            np.savetxt(self.numEng.fIO,self.numEng.tOperator.todense(),fmt='%2.2e')
            tOp=swapForReactions(self.numEng.tOperator,nX*nY,M) #should be in Fortran order
#            self.numEng.fIO.write('tOp after\n')
#            np.savetxt(self.numEng.fIO,tOp.todense(),fmt='%2.2e')
#            self.numEng.fIO.close()
#            exit()
#            print('time Elapsed for swap setup ={0}'.format(time.time()-tS))
#            exit()
#            tS=time.time()
            sF_BC=self.numEng.sF_BC
            sF_BC=np.reshape(np.transpose(np.reshape(sF_BC,(nX*nY,M),order='F')),(nX*nY*M,1),order='F')
            vol=np.reshape(np.transpose(np.reshape(self.numEng.Vol,(nX*nY,M),order='F')),(nX*nY*M,1),order='F')
            diagVol=sps.spdiags(vol.flatten(order='F'),0,nX*nY*M,nX*nY*M)
#            self.numEng.fIO.write('vol Vec\n')
#            np.savetxt(self.numEng.fIO,vol,fmt='%2.2e')
#            self.numEng.fIO.close()
#            exit()
#            print('time Elapsed for reshape setup ={0}'.format(time.time()-tS))
#            tS=time.time()
            diagVol.tocsr()
            tOp.tocsc()
#            print('time Elapsed for conversion ={0}'.format(time.time()-tS))
#            tS=time.time()
#            term3=spsl.spsolve(diagVol,dt*tOp,use_umfpack=False)
            term3=dt*tOp.multiply(1/vol.flatten(order='F'))
#            term3=spsl.spsolve_triangular(diagVol,dt*tOp.todense())
            term3=sps.csr_matrix(term3)
#            self.numEng.fIO.write('term3 \n')
#            np.savetxt(self.numEng.fIO,term3.todense(),fmt='%2.2e')
#            self.numEng.fIO.write('term3_1 \n')
#            np.savetxt(self.numEng.fIO,term3_1.todense(),fmt='%2.2e')
#            self.numEng.fIO.close()
#            print('time Elapsed for term3 and conversion ={0}'.format(time.time()-tS))
#            exit()
#            tS=time.time()
            
            term1=spsl.spsolve(diagVol,dt*sF_BC)
            term1=np.reshape(term1,(-1,1))
            
#            print('time Elapsed for term1 and conversion ={0}'.format(time.time()-tS))
            
#            print('time Elapsed for setup ={0}'.format(time.time()-tS))
            
        
        while convergeReact and nIterReact<self.nIterMax:
            nIterReact+=1
#            tS=time.time()
            self.CalculateNetRatesAndJacobian(uReactOld)
            R=self.NetRates
            Jac=self.Jacobian
            
#            ppp=np.transpose(np.reshape(uReactOld,(self.numEng.M,self.numEng.nX*self.numEng.nY),order='F'))
#            ppp=uReactOld
#            self.numEng.fIO.write('\nuReactOld \n')
#            np.savetxt(self.numEng.fIO,ppp,fmt='%2.2e')
####            
####            ppp=np.transpose(np.reshape(R,(self.numEng.M,self.numEng.nX*self.numEng.nY),order='F'))
#            ppp=R
#            self.numEng.fIO.write('\nRate \n')
#            np.savetxt(self.numEng.fIO,ppp,fmt='%2.2e')
            
            Jac.eliminate_zeros()
            
#            Jac1=Jac.tocoo(copy=True)
#            tOp1=tOp.tocoo(copy=True)
#            
#            self.numEng.fIO.write('\nJac \n')
#            for row, col, value in zip(Jac1.row, Jac1.col, Jac1.data):
#                self.numEng.fIO.write("({0}, {1}) {2}\n".format(row, col, value))
#                
#            self.numEng.fIO.write('\ntOp \n')
#            for row, col, value in zip(tOp1.row, tOp1.col, tOp1.data):
#                self.numEng.fIO.write("({0}, {1}) {2}\n".format(row, col, value))
            
#            self.numEng.fIO.write('uReactOld \n')
#            np.savetxt(self.numEng.fIO,uReactOld,fmt='%2.2e')
#            
#            self.numEng.fIO.write('Rate \n')
#            np.savetxt(self.numEng.fIO,R,fmt='%2.2e')
#            
#            self.numEng.fIO.write('\nJac \n')
#            np.savetxt(self.numEng.fIO,Jac.todense(),fmt='%2.2e')
            
#            self.numEng.fIO.write('\ntOp \n')
#            np.savetxt(self.numEng.fIO,tOp.todense(),fmt='%2.2e')
###            
#            self.numEng.fIO.close()
#            exit()
#            print('time Elapsed for Jacobian setup ={0}'.format(time.time()-tS))
#            tS=time.time()
            if self.numEng.is0D:
                uReact=uReactOld-np.reshape(spsl.spsolve(self.I-dt*Jac,(uReactOld-uReactPrev-dt*R)),(-1,1))
            else:
#                tS=time.time()
#                diagVol=diagVol.tocsr()
#                print('time Elapsed for diag CSR={0}'.format(time.time()-tS))
#                tS=time.time()
#                sF_BC=sps.csc_matrix(sF_BC)
                
#                term1=sps.csr_matrix(term1)
#                print('time Elapsed for term1 build={0}'.format(time.time()-tS))
#                tS=time.time()
                b_1=dt*tOp.dot(uReactOld)
                b_1=sps.csc_matrix(b_1)
                term2=spsl.spsolve(diagVol,b_1)
#                term2=sps.csr_matrix(term2)
#                print('time Elapsed for term2 build={0}'.format(time.time()-tS))
#                tS=time.time()
                
                term2=np.reshape(term2,(-1,1))
#                print('time Elapsed for term reshape={0}'.format(time.time()-tS))
#                tS=time.time()
                
#                print('time Elapsed for term3 build={0}'.format(time.time()-tS))
#                tS=time.time()
                A_mat=self.I-term3-dt*Jac
                A_mat.tocsr()
#                print('time Elapsed for A_mat build={0}'.format(time.time()-tS))
#                tS=time.time()
                B_vec=uReactOld-uReactPrev-term2-dt*R-term1
                B_vec=sps.csc_matrix(B_vec)
#                print('time Elapsed for B_vec build={0}'.format(time.time()-tS))
#                tS=time.time()
                mainSol=spsl.spsolve(A_mat,B_vec,use_umfpack=True)
                uReact=uReactOld-np.reshape(mainSol,(-1,1))
#                print('time Elapsed for RS main={0}'.format(time.time()-tS))
#                exit()
#                tS=time.time()
#                print('uReact = {0}'.format(type(dt)))
#                exit()
            
            iCheck=np.where(np.abs(uReactOld)>np.spacing(1)*0)
            if iCheck[0].size==0:
                EReact=np.float64('inf')
            else:
#                EReact=np.linalg.norm(uReact[iCheck]/uReactOld[iCheck]-1)/np.sqrt(iCheck[0].size)
                EReact=np.linalg.norm(uReact[iCheck]/uReactOld[iCheck]-1)/(iCheck[0].size)
            convergeReact = EReact>self.numEng.iter_tol
            
#            print('reaction Tol ={0}'.format(self.numEng.iter_tol))
            
#            self.numEng.fIO.write('\nuReactOld \n')
#            np.savetxt(self.numEng.fIO,np.transpose(np.reshape(uReactOld,(self.numEng.M,self.numEng.nX*self.numEng.nY),order='F')),fmt='%2.2e')
##            
#            self.numEng.fIO.write('\nuReactNew \n')
#            np.savetxt(self.numEng.fIO,np.transpose(np.reshape(uReact,(self.numEng.M,self.numEng.nX*self.numEng.nY),order='F')),fmt='%2.2e')
###            
#            self.numEng.fIO.close()
#            exit()
#            if self.numEng.time>=1e-14:
#            if dt>1e-8:
#                print('nIterReact={0}, Error={1}'.format(nIterReact,EReact))
#                
##                self.numEng.fIO.write('\n A_mat \n')
##                np.savetxt(self.numEng.fIO,A_mat.todense(),fmt='%2.6e')
##                
##                self.numEng.fIO.write('\n bVec \n')
##                np.savetxt(self.numEng.fIO,B_vec.todense(),fmt='%2.6e')
##                self.numEng.fIO.close()
#                
#                self.numEng.fIO.write('nIterReact={0}, Error={1}\n'.format(nIterReact,EReact))
#                
#                self.numEng.fIO.write('\n uReactOld({0})\n'.format(self.numEng.time))
#                np.savetxt(self.numEng.fIO,uReactOld,fmt='%2.6e')
#                
#                self.numEng.fIO.write('\n uReact({0})\n'.format(self.numEng.time))
#                np.savetxt(self.numEng.fIO,uReact,fmt='%2.6e')
#                
#                input('Press to Continue\n')
                

            uReactOld=uReact
        
        neg=0
        if np.amin(uReact)<0:
            neg=1
            self.numEng.outLog.write("Reaction Solution has negative values\n")
        
        nanInf=0
        if np.any(np.isnan(uReact)) or np.any(np.isinf(uReact)):
            nanInf=1
            self.numEng.outLog.write("Reaction Solution has NaN/Inf values\n")
        
        if nIterReact<self.nIterMax and nanInf==0 and neg==0 :
#            uOut=uReact.copy()
#            uOut[normal,:]=uReact[trans,:]
            out=np.transpose(np.reshape(uReact,(self.numEng.M,self.numEng.nX*self.numEng.nY),order='F'))
#            if self.numEng.time >=1e-14:
#                self.numEng.fIO.write('\nuReactSol\n')
#                np.savetxt(self.numEng.fIO,out,fmt='%2.5e')
#                self.numEng.fIO.close()
#                exit()
        else:
            self.numEng.outLog.write("Could not converge Reactions in {0} Iterations\n".format(self.nIterMax))
        
#        print('Rest time spend={0}'.format(time.time()-tS))
        return out
    def updateFields(self):
        self.formQPK()
    
    def formQPK(self):
        self.BuildAuxiliaryMatrices()
    
    def BuildAuxiliaryMatrices(self):
        vec=np.reshape(np.arange(0,self.numEng.M),(1,self.numEng.M))
        y0=np.reshape(np.tile(vec,(self.numEng.M,1)),(self.numEng.M*self.numEng.M,1))
        x0=np.reshape(np.transpose(np.tile(vec,(self.numEng.M,1))),(self.numEng.M*self.numEng.M,1))
        Add=self.numEng.M*np.tile(np.arange(0,self.numEng.nX*self.numEng.nY),(self.numEng.M*self.numEng.M,1))
        self.xEntries=np.reshape(Add+np.tile(x0,(1,self.numEng.nX*self.numEng.nY)),(1,-1),order='F')
        self.yEntries=np.reshape(Add+np.tile(y0,(1,self.numEng.nX*self.numEng.nY)),(1,-1),order='F')
        R=np.zeros((self.numEng.nX*self.numEng.nY,2*self.numEng.K))
        
        for ii in range(0,self.numEng.K):
#            print("ii={0},Kf={1}".format(ii,self.numEng.Kf))
            R[:,2*ii]=self.numEng.Kf[:,ii]
            R[:,2*ii+1]=self.numEng.Kb[:,ii]
        uni,iUni,iIni=np.unique(R,return_index=True,return_inverse=True,axis=0)
        
        # Order is not preserved in python and no option to preserve the order.
        iSort=np.sort(iUni)
        iIniSort=iIni.copy()
        
        for iVal in range(0,iUni.size):
            iIniSort[np.where(iIni==iVal)]=np.where(iSort==iUni[iVal])[0]
        
        iUni=iSort
        iIni=iIniSort
        
        self.Set=[None]*iUni.size
        self.SMat=np.zeros((self.numEng.K,self.numEng.M))
        
        for iSet in range(0,iUni.size):
            iRangeVal=np.where(iIni==iSet)
            Q=np.zeros((self.numEng.M,self.numEng.M,self.numEng.M))
            P=np.zeros((self.numEng.M,self.numEng.M))
            K=np.zeros((self.numEng.M,1))
            for j in range(0,self.numEng.K):
                # indexing is from 0 not from 1
#                print("j={0},LHS={1}".format(j,self.numEng.LHS))
                LHS=self.numEng.LHS[j,:]-1
                RHS=self.numEng.RHS[j,:]-1
                LHS=LHS[LHS>=0]
                RHS=RHS[RHS>=0]
                kIndx=iUni[iSet]
                Kb=self.numEng.Kb[kIndx,j]
                Kf=self.numEng.Kf[kIndx,j]
                self.ProcessSide(Q,P,K,LHS,Kb,RHS,Kf)
                self.ProcessSide(Q,P,K,RHS,Kf,LHS,Kb)
            Q=np.reshape(Q,(self.numEng.M**2,self.numEng.M),order='F')
            self.Set[iSet]={'iRange':iRangeVal,'Q':Q,'P':P,'K':K}
        
        if self.numEng.debugFlgEnableCorrections:
            self.pWeight=np.zeros((self.numEng.nX*self.numEng.nY*self.numEng.M,self.numEng.cMat.shape[1]))
            for ii in np.arange(self.numEng.cMat.shape[1]):
                self.pWeight[:,ii]=np.ones((self.numEng.nX*self.numEng.nY*self.numEng.M,))+np.tile(np.random.rand(self.numEng.M,),(self.numEng.nX*self.numEng.nY,))
        
    def ProcessSide(self,Q,P,K,Here,kHere,There,kThere):
        for jj in range(0,len(Here)):
            if len(There)==0:
                K[Here[jj]]=K[Here[jj]]+kHere
            elif len(There)==1:
                P[Here[jj],There]=P[Here[jj],There]+kHere
            elif len(There)==2:
                Q[There[0],Here[jj],There[1]]=Q[There[0],Here[jj],There[1]]+kHere/2
                Q[There[1],Here[jj],There[0]]=Q[There[0],Here[jj],There[1]]
                
            if len(Here)==1:
                P[Here,Here]=P[Here,Here]-kThere
            elif len(Here)==2:
                Q[Here[0],Here[jj],Here[1]]=Q[Here[0],Here[jj],Here[1]]-kThere/2
                Q[Here[1],Here[jj],Here[0]]=Q[Here[0],Here[jj],Here[1]]
        
    def CalculateNetRatesAndJacobian(self,U):
#        out=np.array([])
        RMat=np.zeros((self.numEng.M,self.numEng.M,self.numEng.nX*self.numEng.nY))
        JMat=np.zeros((self.numEng.M,self.numEng.M,self.numEng.nX*self.numEng.nY))
        KVec=np.zeros((self.numEng.nX*self.numEng.nY*self.numEng.M,1))
        for iSet in range(0,len(self.Set)):
            Q1=self.Set[iSet]['Q']
            P1=self.Set[iSet]['P']
            K1=self.Set[iSet]['K']
            Range=self.Set[iSet]['iRange']
            RangeVec=np.reshape(Range[0],(-1,1))
            vec=np.reshape(np.arange(0,self.numEng.M),(1,self.numEng.M))
            varMat=np.tile(self.numEng.M*RangeVec,(1,self.numEng.M))+np.tile(vec,(len(RangeVec),1))
            Vars=np.reshape(varMat.T,(-1,1),order='F')
            UBlock=np.reshape(U[Vars],(self.numEng.M,-1),order='F')
            aMat=np.matmul(Q1,UBlock)
            PMat=np.tile(np.reshape(P1.T,(self.numEng.M*self.numEng.M,1),order='F'),(1,len(RangeVec)))
            bMat=aMat+PMat
            
            RMat[:,:,RangeVec[:,0]]=np.reshape(bMat,(self.numEng.M,self.numEng.M,len(RangeVec)),order='F')
            JMat[:,:,RangeVec[:,0]]=np.reshape(aMat+bMat,(self.numEng.M,self.numEng.M,len(RangeVec)),order='F')
            KVec[Vars[:,0]]=np.tile(K1,(len(RangeVec),1))
            
        self.Jacobian = sps.csr_matrix((np.reshape(JMat,(1,-1),order='F')[0],(self.xEntries[0],self.yEntries[0])))
        RateMatrix = sps.csr_matrix((np.reshape(RMat,(1,-1),order='F')[0],(self.xEntries[0],self.yEntries[0])))
        self.NetRates = RateMatrix.dot(U)+KVec
        
