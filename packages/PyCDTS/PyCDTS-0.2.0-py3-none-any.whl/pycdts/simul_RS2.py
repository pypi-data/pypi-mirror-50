#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:10:21 2018

@author: abdul
"""

from .reactionSolver import ReactionSolver
import numpy as np
import scipy.constants
import scipy.sparse as sps
import scipy.sparse.linalg as spsl
#from scikits.umfpack import spsolve

class simul_RS2(ReactionSolver):
    NetRates=0
    Jacobian=0
    def __init__(self,numEng):
        self.numEng=numEng
        self.nIterMax=10
        self.I=sps.eye(numEng.nX*numEng.nY*numEng.M,numEng.nX*numEng.nY*numEng.M)
        self.xEntries=0
        self.yEntires=0
        
        self.pWeight=0
        
        self.formQPK()
    
    def Solve(self,dt):
        out=np.array([])
        
        u0=np.reshape(self.numEng.uInit.T,(self.numEng.nX*self.numEng.nY*self.numEng.M,1),order='F')
        
#        u0_5=np.reshape(self.numEng.uInit[:,4],(self.numEng.nX,self.numEng.nY))
#        u0_5f=np.reshape(self.numEng.uInit[:,4],(self.numEng.nX,self.numEng.nY),order='F')
#        
#        self.numEng.fIO.write('U0(Before Reshape in Reactions)\n')
#        np.savetxt(self.numEng.fIO,self.numEng.uInit,fmt='%2.2e')
#        self.numEng.fIO.write('U0_5(Before Reshape in Reactions)\n')
#        np.savetxt(self.numEng.fIO,u0_5,fmt='%2.2e')
#        self.numEng.fIO.write('U0_5f(Before Reshape in Reactions)\n')
#        np.savetxt(self.numEng.fIO,u0_5f,fmt='%2.2e')
#        self.numEng.fIO.write('U0(After Reshape in Reactions)\n')
#        np.savetxt(self.numEng.fIO,u0,fmt='%2.2e')
#        u0_1=np.transpose(np.reshape(u0,(self.numEng.M,self.numEng.nX*self.numEng.nY),order='F'))
#        self.numEng.fIO.write('U0(After After Reshape in Reactions)\n')
#        np.savetxt(self.numEng.fIO,u0_1,fmt='%2.2e')
#        self.numEng.fIO.close()
#        exit()
        
        uReact=u0
        uReactPrev=u0
        uReactOld=u0
        
        nIterReact=0
        EReact=np.float64('inf')
        R=sps.csr_matrix([])
        Jac=sps.csr_matrix([])
        convergeReact=1
        
        while convergeReact and nIterReact<self.nIterMax:
            nIterReact+=1
            self.CalculateNetRatesAndJacobian(uReactOld)
            R=self.NetRates
            Jac=self.Jacobian
            
            uReact=uReactOld-np.reshape(spsl.spsolve(self.I-dt*Jac,(uReactOld-uReactPrev-dt*R)),(-1,1))
            if self.numEng.debugFlgEnableCorrectionsInsideWhileLoop:
                u0=uReact/np.linalg.norm(uReact)
                pWght=self.pWeight
                p=pWght*np.tile(u0,(1,pWght.shape[1]))
                cMat=np.tile(self.numEng.cMat,(self.numEng.nX*self.numEng.nY,1))
                ctp=np.matmul(cMat.T,p)
                a=np.linalg.solve(ctp,np.matmul(cMat.T,(uReact-uReactPrev)))
                uReactNew=uReact-np.matmul(p,a)
                uReact=uReactNew
            
#            uReact=uReactOld-np.reshape(scipy.optimize.nnls(self.I-dt*Jac,(uReactOld-uReactPrev-dt*R)),(-1,1))
            
            iCheck=np.where(np.abs(uReactOld)>np.spacing(1)*0)
            if iCheck[0].size==0:
                EReact=np.float64('inf')
            else:
                EReact=np.linalg.norm(uReact[iCheck]/uReactOld[iCheck]-1)/np.sqrt(iCheck[0].size)
            convergeReact = EReact>self.numEng.iter_tol
            
#            convergeReact=np.allclose(uReact,uReactOld,atol=0,rtol=1e-6)
            uReactOld=uReact
#            print('time=%2.5e,\t dt=%2.5e,\tnIterReact=%d,\tEReact=%2.5e' % (self.numEng.time,dt,nIterReact,EReact))
        
        # Check for corrections, nan,inf, -ve concentrations and return out
        if self.numEng.debugFlgEnableCorrections:
            u0=uReact/np.linalg.norm(uReact)
            pWght=self.pWeight
            p=pWght*np.tile(u0,(1,pWght.shape[1]))
            cMat=np.tile(self.numEng.cMat,(self.numEng.nX*self.numEng.nY,1))
            ctp=np.matmul(cMat.T,p)
            a=np.linalg.solve(ctp,np.matmul(cMat.T,(uReact-uReactPrev)))
            uReactNew=uReact-np.matmul(p,a)
            uReact=uReactNew
        neg=0
        if np.amin(uReact)<0:
            neg=1
        
        nanInf=0
        if np.any(np.isnan(uReact)) or np.any(np.isinf(uReact)):
            nanInf=1
        
        if nIterReact<self.nIterMax and nanInf==0 and neg==0 :
            out=np.transpose(np.reshape(uReact,(self.numEng.M,self.numEng.nX*self.numEng.nY),order='F'))
        
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
        out=np.array([])
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
        
