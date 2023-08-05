#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:00:09 2018

@author: abdul
"""

from .poissonSolver import PoissonSolver
import numpy as np
import scipy.constants as PhysConst
import scipy.sparse as sps
import scipy.sparse.linalg as spsl

class linearized_PS(PoissonSolver):
    Ap=np.array([])
    def __init__(self,numEng):
        self.numEng=numEng
        self.Top=0
        self.Bottom=0
        self.nIterMax=100
        self.formAp()
        
    
    def updateFields(self):
        numEng=self.numEng
        
    def formAp(self):
        mG=self.numEng.mGrid
        
    def Solve(self,dt):
        mG=self.numEng.mGrid
        Hx=mG.Hx
        Hy=mG.Hy
        hx=mG.hx
        hy=mG.hy
        self.Top=np.reshape(self.numEng.FC_BC[:,-1],(mG.nX,3),order='F')
        self.Bottom=np.reshape(self.numEng.BC_BC[:,-1],(mG.nX,3),order='F')
        
#        print("Inside linearized_PS solve() with dt={0}".format(dt))
        
        if self.numEng.isFloating:
#            print('PS_01')
            hIndx=self.numEng.hIndx
            eIndx=self.numEng.eIndx
            
            qVec=self.numEng.qVec.copy()
            qVec[hIndx]=0
            qVec[eIndx]=0
            
            netDop=np.reshape(np.dot(self.numEng.uD_sol,qVec),
                              (mG.nX,mG.nY))
#            print('uD_sol shape={0}'.format(self.numEng.uD_sol.shape))
#            print('qVec shape={0}'.format(qVec.shape))
#            exit()
            netDop_top=netDop[:,-1]
            netDop_bot=netDop[:, 0]
#            print('Top={0}'.format(netDop_top))
#            print('Bot={0}'.format(netDop_bot))
#            exit()
            
            uT_e =np.reshape(self.numEng.uD_sol[:,eIndx],(mG.nX,mG.nY))
            uNs_e=np.reshape(self.numEng.Ns[:,eIndx],(mG.nX,mG.nY))
            Gf_e =np.reshape(self.numEng.G[:,eIndx],(mG.nX,mG.nY))/self.numEng.Vt
#            print('PS_02')
            
            uT_h =np.reshape(self.numEng.uD_sol[:,hIndx],(mG.nX,mG.nY))
            uNs_h=np.reshape(self.numEng.Ns[:,hIndx],(mG.nX,mG.nY))
            Gf_h =np.reshape(self.numEng.G[:,hIndx],(mG.nX,mG.nY))/self.numEng.Vt
            
            vTop = 0*netDop_top
            vBot = 0*netDop_bot
            
            eTop = 0*netDop_top
            eBot = 0*netDop_bot
            
#            print('PS_03')
            
            for jj in range(0,len(netDop_top)):
                if netDop_top[jj]>0:
                    eTop[jj]=Gf_e[jj,-1]+np.log(uT_e[jj,-1]/uNs_e[jj,-1])
                else:
                    eTop[jj]=-Gf_h[jj,-1]-np.log(uT_h[jj,-1]/uNs_h[jj,-1])
            
            for jj in range(0,len(netDop_bot)):
                if netDop_bot[jj]>0:
                    eBot[jj]=Gf_e[jj,0]+np.log(uT_e[jj,0]/uNs_e[jj,0])
                else:
                    eBot[jj]=-Gf_h[jj,0]-np.log(uT_h[jj,0]/uNs_h[jj,0])
            
#            print('eTop={0},eBot={1}'.format(eTop,eBot))
#            print('Gf_e_top={0},Gf_e_bot={1}'.format(Gf_e[0,-1],Gf_e[0,0]))
#            print('Gf_h_top={0},Gf_h_bot={1}'.format(Gf_h[0,-1],Gf_h[0,0]))
            
            
            for jj in range(0,len(netDop_top)):
                midVal=(eBot[jj]-eTop[jj])/2
                vTop[jj]=-midVal
                vBot[jj]=midVal
            
#            print('vTop={0},vBot={1}'.format(vTop,vBot))
            
            self.Bottom[:,0]=1
            self.Bottom[:,1]=0
            self.Bottom[:,2]=vBot
            
            self.Top[:,0]=1
            self.Top[:,1]=0
            self.Top[:,2]=vTop
        
#        print('PS_0')
        
        Eps2D=np.reshape(self.numEng.Eps,(mG.nX,mG.nY))*self.numEng.Vt
        
        
        eps_x=1/hx*(2/(1/Eps2D[1:,:] + 1/Eps2D[0:-1,:]))
        eps_y=1/hy*(2/(1/Eps2D[:,1:] + 1/Eps2D[:,0:-1]))
        
        sN=0*Hx
        sS=0*Hx
        sW=0*Hx
        sE=0*Hx
        
#        print('PS_1')
                
        sN[:,1:  ] =-Hx[:,0:-1]*eps_y
        sS[:,0:-1] =-Hx[:,1:  ]*eps_y
        
        sE[1:  ,:]=-Hy[0:-1,:]*eps_x
        sW[0:-1,:]=-Hy[1:  ,:]*eps_x
        
        sC=np.zeros((mG.nX,mG.nY))
        
        sC[1:,:]=sC[1:,:]+Hy[1:,:]*eps_x
        sC[0:-1,:]=sC[0:-1,:]+Hy[0:-1,:]*eps_x 
        
        sC[:,1:]=sC[:,1:]+Hx[:,1:]*eps_y
        sC[:,0:-1]=sC[:,0:-1]+Hx[:,0:-1]*eps_y
        
        sC[:,0]=sC[:,0]*self.Bottom[:,1]+Hx[:,0]*self.Bottom[:,0]
        sN[:,1]=sN[:,1]*self.Bottom[:,1]
        sE[:,0]=sE[:,0]*self.Bottom[:,1]
        sW[:,0]=sW[:,0]*self.Bottom[:,1]
        
#        print('PS_2')
        
        sC[:,-1]=sC[:,-1]*self.Top[:,1]-Hx[:,-1]*self.Top[:,0]
        sS[:,-2]=sS[:,-2]*self.Top[:,1]
        sE[:,-1]=sE[:,-1]*self.Top[:,1]
        sW[:,-1]=sW[:,-1]*self.Top[:,1]
        
        sCent=np.reshape(sC,(1,-1),order='F')
        sW=np.reshape(sW,(1,-1),order='F')
        sE=np.reshape(sE,(1,-1),order='F')
        sN=np.reshape(sN,(1,-1),order='F')
        sS=np.reshape(sS,(1,-1),order='F')
        
#        print('PS_3')
        
#        diags=np.zeros((mG.nX*mG.nY,5))
#        print('PS_4')
#        print('diags={0}'.format(diags.shape))
#        print('sCent={0}'.format(sCent.shape))
#        diags[:,0]=sCent
#        print('PS_5')
#        diags[:,1]=sW
#        diags[:,2]=sS
#        print('PS_6')
#        diags[:,3]=sN
#        diags[:,4]=sE
        
#        diagLoc=[0,-1,-mG.nX,mG.nX,1]
        
#        diags = np.vstack((sCent,sW,sS,sN,sE))
        
        if self.numEng.nDims==2:
            diagLoc = [0,-1,-mG.nX,mG.nX,1]
            diags = np.vstack((sCent,sW,sS,sN,sE))
        else:
            diagLoc = [0,-1,1]
            diags = np.vstack((sCent,sS,sN))
        
#        print('PS_41')
#        print('sCent={0}'.format(sCent.shape))
#        print('diags={0}'.format(diags.shape))
        
        self.Ap=sps.spdiags(diags,diagLoc,mG.nX*mG.nY,mG.nX*mG.nY)
        
        out=np.array([])
#        np.savetxt(self.numEng.fIO,self.Ap.todense(),fmt='%2.2e')
#        self.numEng.fIO.close()
#        exit()
        nIter=0
        convFlg=0
        fi=self.numEng.fi_sol.copy()
        psi_old=self.numEng.fi_sol.copy()
        
#        print('PS_5')
        
        while convFlg==0 and nIter<self.nIterMax:
            nIter=nIter+1
            fiDiff=np.reshape(fi-psi_old,(-1,1))
#            self.numEng.fIO.write('fiDiff\n')
#            np.savetxt(self.numEng.fIO,fiDiff,fmt='%2.2e')
            qVec=np.reshape(self.numEng.qVec,(1,-1))
#            self.numEng.fIO.write('qVec\n')
#            np.savetxt(self.numEng.fIO,qVec,fmt='%2.2e')
            qVec2=qVec*qVec
#            self.numEng.fIO.write('qVec2\n')
#            np.savetxt(self.numEng.fIO,qVec2,fmt='%2.2e')
#            print('qVec shape={0}'.format(qVec.shape))
#            print('fiDiff shape={0}'.format(fiDiff.shape))
#            exit()
            expVal=np.dot(fiDiff,qVec)
#            self.numEng.fIO.write('expVal({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,expVal,fmt='%2.2e')
            uVal=np.exp(expVal)*self.numEng.uD_sol
#            self.numEng.fIO.write('uVal({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,uVal,fmt='%2.2e')
#            print('nIter={0}'.format(nIter))
#            uVal1=uVal.copy()
            
            
            
#            print('PS_0')
#            print('uVal shape={0}'.format(uVal.shape))
#            print('qVec shape={0}'.format(qVec.shape))
#            exit()
            rho_temp=np.dot(uVal,qVec.transpose())
#            self.numEng.fIO.write('rho_temp({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,rho_temp,fmt='%2.2e')
#            exit()
            rho = PhysConst.e*np.reshape(rho_temp+
                                         self.numEng.Dop,(mG.nX,mG.nY))*Hx*Hy
#            self.numEng.fIO.write('mG.X({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,mG.X,fmt='%2.2e')
#            self.numEng.fIO.write('mG.Y({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,mG.Y,fmt='%2.2e')
#            self.numEng.fIO.write('hx({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,hx,fmt='%2.2e')
#            self.numEng.fIO.write('hy({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,hy,fmt='%2.2e')
#            
#            self.numEng.fIO.write('Hx({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,Hx,fmt='%2.2e')
#            self.numEng.fIO.write('Hy({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,Hy,fmt='%2.2e')
            
#            print('PS_1')
            rho_temp1=np.dot(uVal,qVec2.transpose())
#            self.numEng.fIO.write('rhoTemp1({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,rho_temp1,fmt='%2.2e')
#            self.numEng.fIO.close()
#            exit()
            rhoAbs = PhysConst.e*np.reshape(rho_temp1+
                                            self.numEng.Dop,(mG.nX,mG.nY))*Hx*Hy
                                            
            rhoAbs[:,0]=0
            rhoAbs[:,-1]=0
            
#            print('shape uVal={0},rho={1},rhoAbs{2}'.format(uVal1.shape,rho.shape,rhoAbs.shape))
            
#            uVal1=np.hstack((uVal1,rho.transpose(),rhoAbs.transpose()))
#            exit()
            
#            print('PS_1')
#            self.numEng.fIO.write('uVal1({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,uVal1,fmt='%2.2e')
            
            Ap_new = self.Ap + sps.spdiags(rhoAbs.flatten(order='F'),0,mG.nX*mG.nY,mG.nX*mG.nY)
            
#            self.numEng.fIO.write('self.Ap({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,self.Ap.todense(),fmt='%2.2e')
#            self.numEng.fIO.write('Ap_new({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,Ap_new.todense(),fmt='%2.2e')
            
            sF = rho+psi_old*rhoAbs
            
            sF[:,0]=sF[:,0]*self.Bottom[:,1]+Hx[:,0]*self.Bottom[:,2]
            sF[:,-1]=sF[:,-1]*self.Bottom[:,1]-Hx[:,-1]*self.Top[:,2]
            
            sF=np.reshape(sF,(mG.nX*mG.nY,1),order='F')
#            print('PS_2')
            
#            self.numEng.fIO.write('sF({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,sF,fmt='%2.2e')
            
            tempSol=spsl.spsolve(Ap_new,sF)
            
#            if nIter>=2:  
#                self.numEng.fIO.close()
#                exit()
#            print('PS_3')
#            print('tempSol={0}'.format(tempSol.shape))
            psi_new=np.reshape(tempSol,(mG.nX,mG.nY),order='F')
            
#            self.numEng.fIO.write('psi_old({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,psi_old,fmt='%2.2e')
#            self.numEng.fIO.write('psi_new({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,psi_new,fmt='%2.2e')
            
            
#            print('psi_new={0}'.format(psi_new.shape))
#            print('psi_old={0}'.format(psi_old.shape))
#            print('psi_new={0}'.format(psi_new))
#            print('psi_old={0}'.format(psi_old))
#            print('diff={0}'.format(abs(psi_new-psi_old)))
#            print('max={0}'.format(np.max(abs(psi_new-psi_old))))
            error_P=np.max(abs(psi_new-psi_old))
            
#            print('error_p={0}'.format(error_P))
            
            if np.isnan(error_P):
                convFlg=0
            else:
                convFlg=(error_P<self.numEng.iter_tol)
            
#            self.numEng.fIO.write('\npsi_old({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,psi_old.T,fmt='%2.2e')
#            self.numEng.fIO.write('\npsi_new({0})\n'.format(nIter))
#            np.savetxt(self.numEng.fIO,psi_new.T,fmt='%2.2e')
#            
#            self.numEng.fIO.close()
#            exit()
            psi_old=psi_new
        
#        self.numEng.fIO.write('psi_old({0})\n'.format(nIter))
#        np.savetxt(self.numEng.fIO,psi_old,fmt='%2.2e')
#        self.numEng.fIO.write('psi_new({0}),Error={1}\n'.format(nIter,error_P))
#        np.savetxt(self.numEng.fIO,psi_new,fmt='%2.2e')
        
        
        
        
        out=psi_new
#        print('PS exit')
        return out