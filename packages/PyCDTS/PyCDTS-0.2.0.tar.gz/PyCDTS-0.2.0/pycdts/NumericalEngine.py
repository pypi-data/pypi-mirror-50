
import numpy as np
from .mesh_class import Mesh_class
from .simple_PS import simple_PS
from .linearized_PS import linearized_PS
from .damping_PS import damping_PS
from .simpleLinearized_PS import simpleLinearized_PS
from .DAE_PS import DAE_PS
from .Newton_PS import Newton_PS
from .OPS_Gummel import OPS_Gummel
from .FOP_Gummel import FOP_Gummel

from .simul_RS import simul_RS
from .simul_RS2 import simul_RS2
from .simul_RS2_FOP import simul_RS2_FOP

from .simul_DS import simul_DS
from .simul_DS_ber import simul_DS_ber
from .Newton_DS_ber import Newton_DS_ber
from .DAE_DS_ber import DAE_DS_ber
from .simul_DS_ber_FOP import simul_DS_ber_FOP

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import pause
plt.switch_backend('Qt5Agg')
import os
import h5py
import warnings

#import warnings
#warnings.filterwarnings("error")

from PyQt5.QtWidgets import (QApplication)

class NumericalEngine:
    """
    All the computations are done in this class
    """
    def __init__(self):
        """
        Initializes the variables
        """
        self.nX=0
        self.nY=0
        self.M=0
        self.K=0
        self.iter_tol=0
        self.Kf=np.empty([])
        self.Kb=np.empty([])
        self.LHS=np.empty([])
        self.RHS=np.empty([])
        self.D=np.empty([])
        self.G=np.empty([])
        self.Ns=np.empty([])
        self.qVec=np.empty([])
        self.Eps=np.empty([])
        self.FC_BC=np.empty([])
        self.BC_BC=np.empty([])
        self.Dop=np.empty([])
        self.U0=np.empty([])
        self.fi0=np.empty([])
        self.kT=0
        self.vT=0
        self.Species=[]
        self.is0D=0
        self.nDims=0
        self.mGrid=Mesh_class()
#        Used in the internals of numerical engine.
#        Do not use them outside numerical engine except in solvers
        self.time=0
        self.timeEnd=0
        self.U=np.empty([])
        self.fi=np.empty([])
        self.fi_sol=np.empty([])
        self.uInit=np.empty([])
        self.uR_sol=np.array([])
        self.uD_sol=np.array([])
        self.uD_solInit=np.array([])
        self.gummelStart=1
        self.gummelRelTolForPotential=1e-3
        self.gummelRelTolForConc=1e-6
        
        self.nPoints=100
        
        self.maxGummelIter=4000
        
        self.enableRS=1
        self.enableDS=1
        self.enablePS=1
        
        self.typeDS=1
        self.typePS=1
        self.typeRS=1
        self.typeAlgo=1;
        
        self.PS=0
        self.DS=0
        self.RS=0
        self.algo=0
        
        self.eIndx=[]
        self.hIndx=[]
        
        
        self.PS_list={0:simple_PS,
                      1:linearized_PS,
                      2:damping_PS,
                      3:simpleLinearized_PS,
                      4:DAE_PS,
                      5:Newton_PS}
        
        self.DS_list={0:simul_DS,
                      1:simul_DS_ber,
                      2:Newton_DS_ber,
                      4:DAE_DS_ber,
                      5:simul_DS_ber_FOP}
        
        self.RS_list={0:simul_RS,
                      1:simul_RS2,
                      2:simul_RS2_FOP}
        
        self.algo_list={0:OPS_Gummel,
                        1:FOP_Gummel}
        
        self.debugFlgEnableCorrections=0
        self.debugFlgEnableCorrectionsInsideWhileLoop=0
        self.debugFile='runDebug.txt'
        self.fIO=open(self.debugFile,"w+")
        self.outLog=None
#        plt.ion()
#        self.fig=plt.figure()
#        self.ax=self.fig.add_subplot(221)
#        self.ax1=self.fig.add_subplot(222)
#        self.ax2=self.fig.add_subplot(223)
#        self.line1=0
#        self.line2=0
#        self.line3=0
        
    def updateGUI(self):
        QApplication.processEvents()
        
    def Run(self,timeStart,timeEnd,dtStart,dSet_Conc,dSet_Fi,dSet_Time):
#        os.remove('test.hdf5')
#        f = h5py.File('test.hdf5', 'w')
#        dset_conc = f.create_dataset('Conc',(1,self.nX,self.nY,self.M),maxshape=(None,self.nX,self.nY,self.M),dtype=np.double,compression="gzip", compression_opts=9)
#        dset_fi = f.create_dataset('Fi',(1,self.nX,self.nY),maxshape=(None,self.nX,self.nY),dtype=np.double,compression="gzip", compression_opts=9)
#        print("Inside Run with timeStart={0},timeEnd={1}".format(timeStart,timeEnd))
        tVec=np.array([timeStart])
        tVec.shape=(1,1)
        UVec=np.reshape(self.U0,(self.nX*self.nY*self.M,1))
        fiVec=self.fi0
        
        U_1=np.reshape(UVec,(self.nX,self.nY,self.M))
        fi_1=np.reshape(fiVec,(self.nX,self.nY))
#        dset_conc[:]=U_1
#        dset_fi[:]=fi_1
        
        self.time=np.double(timeStart)
        self.timeEnd=np.double(timeEnd)
        
        self.U=self.U0
        self.fi=self.fi0
        self.fi_sol=np.reshape(self.fi0,(self.nX,self.nY))
        self.uInit=self.U0
        self.uR_sol=self.uInit
#        print('Y={0}'.format(self.mGrid.Y))
#        print('fi0={0}'.format(self.fi0))
#        self.line1,=self.ax.plot(self.mGrid.Y,self.fi0,'r-')
#        self.line2,=self.ax1.plot(self.mGrid.Y,self.fi0,'r-')
#        self.line3,=self.ax2.plot(self.mGrid.Y,self.fi0,'r-')
        
        if dtStart < timeEnd-timeStart:
            dt=np.double(dtStart)
        else:
            dt=timeEnd-timeStart
        
        nIterTloop=0
        
        dtcounter=0
        tStart=0
        ratio=1
        
        warnings.filterwarnings("error")
        
        while self.time < self.timeEnd and nIterTloop<2000000:
#            print("time={0},nIterTloop={1}".format(self.time,nIterTloop))
            nIterTloop+=1
            uSol_t=self.uInit
            fiSol_t=self.fi_sol
            try:
                U,fi,nIter,Error=self.SolveTimeStep(dt)
            except Exception as error:
                U,fi,nIter,Error=np.array([]),np.array([]),0,0
                print(error)
            if not U.size==0:
#                U_1=np.reshape(U,(self.nX,self.nY,self.M))
#                fi_1=np.reshape(fi,(self.nX,self.nY))                
#                dset_conc.resize(dset_conc.shape[0]+1,axis=0)
#                dset_fi.resize(dset_fi.shape[0]+1,axis=0)
#                dset_conc[-1:]=U_1
#                dset_fi[-1:]=fi_1
#                f.close()
#                exit()
                if not tStart:
                    tStart=1
                    tSave=self.time+dt;
                    ratio= (self.timeEnd/tSave)**(1/self.nPoints)
                
                self.time=self.time+dt
#                print('time=%2.5e,\t dt=%2.5e\t GummelIter=%d' % (self.time,dt,nIter))
                self.outLog.write('time=%2.5e,\t dt=%2.5e\t GummelIter=%d \n' % (self.time,dt,nIter))
                self.updateGUI()
                
                
                if self.time==tSave or self.time==self.timeEnd:
                    dSet_Conc.resize(dSet_Conc.shape[0]+1,axis=0)
                    dSet_Fi.resize(dSet_Fi.shape[0]+1,axis=0)
                    dSet_Time.resize(dSet_Time.shape[0]+1,axis=0)
                    
                    dSet_Conc[-1:]=np.reshape(U,(self.nX,self.nY,self.M))
                    dSet_Fi[-1:]=np.reshape(fi*self.Vt,(self.nX,self.nY))
                    dSet_Time[-1:]=self.time
                    
                    UVec=np.hstack((UVec,U))
                    fiVec=np.hstack((fiVec,fi))
                    tVec=np.hstack((tVec,np.array([[self.time]])))
                    tSave=ratio*tSave
                
                if dtcounter < 15:
                    dtcounter+=1
                    if self.time+dt > tSave:
                        dt=tSave-self.time
                else:
                    dt=dt*2
                    
                    if self.time+dt > self.timeEnd:
                        dt=self.timeEnd-self.time
                    elif self.time+dt > tSave:
                        dt=tSave-self.time
                        
#                    if self.time>1e-23:
#                        self.time=self.timeEnd
                    
                
            else:
                self.uInit=uSol_t
                self.uD_sol=uSol_t
                self.uR_sol=uSol_t
                self.fi_sol=fiSol_t
                dt=dt/2
                dtcounter=1
            
            if dt<1e-18:
                dt=1e-14
                
                
#        f.close()   
        warnings.filterwarnings("default")
        return tVec,UVec,fiVec
    
    def SolveTimeStep(self,dt):
#        print("Inside SolveTimeStep dt={0}".format(dt))
        U,fi,nIter,Error=self.algo.runAlgorithm(dt)
        return U,fi,nIter,Error
    
    def initialize(self):
        self.initializeSolvers()
    
    def initializeSolvers(self):
        self.algo=self.algo_list[self.typeAlgo](self)
        if self.typeAlgo==1:
            self.typeRS=2
            self.typeDS=5
#            print('Setting type for RS and DS FOP solvers\n')
        if not self.is0D:
            self.PS=self.PS_list[self.typePS](self)
            self.DS=self.DS_list[self.typeDS](self)
        self.RS=self.RS_list[self.typeRS](self)
        
        
    def reInitialize(self):
        self.RS.updateFields()
        if not self.is0D:
            self.PS.updateFields()
            self.DS.updateFields()
        
    
