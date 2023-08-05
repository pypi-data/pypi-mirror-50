from .NumericalEngine import NumericalEngine
import numpy as np
import scipy.io
import scipy.constants
from .solutionBrowser import SolutionBrowser
class Project:
    """
    Project class
    """
    def __init__(self):
        self.inputDataFile = ""
        self.numEng = NumericalEngine()
        self.info = np.empty([1,1])
        self.snapShot = np.empty([1,1])
        self.isInCms = 0
        self.topReference=0
        self.tOut=0
        self.uOut=0
        self.fiOut=0
        self.SB=SolutionBrowser(self)

    def setDataToNumEngine(self):
        # first read the mat file for recovering the data
        inputData=scipy.io.loadmat(self.inputDataFile,squeeze_me=True)
        self.info=inputData['Info']
        self.snapShot=inputData['SnapShot']
        self.numEng.is0D = (self.info['nDims'][()]==0)
        self.numEng.nDims= self.info['nDims'][()]
        self.numEng.nX = self.info['nX'][()]
        self.numEng.nY = self.info['nY'][()]
        self.numEng.M = self.info['nSpecies'][()]
        self.numEng.K = self.info['nReactions'][()]
        self.numEng.iter_tol = 1e-3
        
        X = np.reshape(self.info['XVector'][()],(self.numEng.nX,1))
        Y = np.reshape(self.info['YVector'][()],(self.numEng.nY,1))
        if not self.isInCms :
            X=X*1e-4
            Y=Y*1e-4

        if not X.size==1:
            X.sort()
        Y.sort()
        if not X.size==1:
            dX_diff=np.diff(X,n=1,axis=0)
        else:
            dX_diff=np.array([])
            dX_diff=np.reshape(dX_diff,(0,1))
        dY_diff=np.diff(Y,n=1,axis=0)
        
#        if self.info['nDims'][()]==2:
#            DMatx=np.diag(np.ones(self.info['nX'][()]))+np.diag(np.ones(self.info['nX'][()]-1),k=1)
#            DMatx[-1,-1]=0
#            minIndx=np.argmin(dX_diff)
#            if minIndx==self.info['nX'][()]:
#                minIndx=minIndx-1
#            DMatx[-1,minIndx]=1
#            DMatx[-1,minIndx+1]=-1
#            dX=np.linalg.solve(DMatx,np.vstack((2*dX_diff,[0])))
#            
#            DMaty=np.diag(np.ones(self.info['nY'][()]))+np.diag(np.ones(self.info['nY'][()]-1),k=1)
#            DMaty[-1,-1]=0
#            minIndx=np.argmin(dY_diff)
#            if minIndx==self.info['nY'][()]:
#                minIndx=minIndx-1
#            DMaty[-1,minIndx]=1
#            DMaty[-1,minIndx+1]=-1
#            dY=np.linalg.solve(DMaty,np.vstack((2*dY_diff,[0])))
##            print(dY)
#        elif self.info['nDims'][()]==1:
#            dX = 1e-4;
#            
#            DMaty=np.diag(np.ones(self.info['nY'][()]))+np.diag(np.ones(self.info['nY'][()]-1),k=1)
#            DMaty[-1,-1]=0
#            minIndx=np.argmin(dY_diff)
#            if minIndx==self.info['nY'][()]:
#                minIndx=minIndx-1
#            DMaty[-1,minIndx]=1
#            DMaty[-1,minIndx+1]=-1
#            dY=np.linalg.solve(DMaty,np.vstack((2*dY_diff,[0])))
#        else:
#            dX=1e-4
#            dY=1e-4
        if self.info['nDims'][()]==2:
            dX1=np.vstack((dX_diff[0],dX_diff))
            dX2=np.vstack((dX_diff,dX_diff[-1]))
            
            dY1=np.stack((dY_diff[0],dY_diff))
            dY2=np.stack((dY_diff,dY_diff[-1]))
        elif self.info['nDims'][()]==1:
            if not self.isInCms:
                dX1=0.5e-4
                dX2=0.5e-4
            else:
                dX1=0.5
                dX2=0.5
            dY1=np.vstack((dY_diff[0],dY_diff))
            dY2=np.vstack((dY_diff,dY_diff[-1]))
        
        if self.info['nDims'][()]:
            dX=(dX1+dX2)/2
            dY=(dY1+dY2)/2
        
        
        self.numEng.mGrid.nX=self.info['nX'][()]
        self.numEng.mGrid.nY=self.info['nY'][()]
        self.numEng.mGrid.X=X
        self.numEng.mGrid.Y=Y
        if self.info['nDims'][()]:
            self.numEng.mGrid.dX=np.transpose(dX)
            self.numEng.mGrid.dY=np.transpose(dY)
            self.numEng.mGrid.Hx=np.tile(dX,[1,self.numEng.mGrid.nY])
            self.numEng.mGrid.Hy=np.tile(self.numEng.mGrid.dY,[self.numEng.mGrid.nX,1])
            self.numEng.mGrid.hx=np.tile(dX_diff,[1,self.numEng.mGrid.nY])
            self.numEng.mGrid.hy=np.tile(np.transpose(dY_diff),[self.numEng.mGrid.nX,1])
        
        self.numEng.qVec=np.reshape(self.info['Charge'][()],(self.info['nSpecies'][()],1))
        self.numEng.U0=self.info['Concentration'][()]
        self.numEng.fi0=np.zeros((self.info['nMesh'][()],1))
        self.numEng.Dop=np.zeros((self.info['nMesh'][()],1))
        self.numEng.LHS=np.int32(self.info['iLHS'][()])
        self.numEng.RHS=np.int32(self.info['iRHS'][()])
        self.numEng.Species=self.info['Species'][()]
        
        if 'ConservationMatrix' in self.info.dtype.names:
            self.numEng.cMat=np.transpose(self.info['ConservationMatrix'][()])
        
        
        self.setSnapShotData(self.snapShot[1])
        self.numEng.initialize()

    def setSnapShotData(self,SnapShot):
        self.numEng.Vt=SnapShot['Et']
        self.numEng.Ns=SnapShot['Ns'][()]
        self.numEng.G=SnapShot['G0'][()]
        self.numEng.D=SnapShot['Diffusivity'][()]
        self.numEng.Eps=SnapShot['Eps']*scipy.constants.epsilon_0
        self.numEng.Kf=np.reshape(SnapShot['KF'],(self.numEng.nX*self.numEng.nY,self.numEng.K))
        self.numEng.Kb=np.reshape(SnapShot['KB'],(self.numEng.nX*self.numEng.nY,self.numEng.K))
        
        if self.info['nDims'][()]:
            TopA=np.reshape(SnapShot['TopRobinA'][()],(self.info['nX'][()],self.info['nSpecies'][()]))
            TopB=np.reshape(SnapShot['TopRobinB'][()],(self.info['nX'][()],self.info['nSpecies'][()]))
            TopC=np.reshape(SnapShot['TopRobinC'][()],(self.info['nX'][()],self.info['nSpecies'][()]))
            BottomA=np.reshape(SnapShot['BottomRobinA'][()],(self.info['nX'][()],self.info['nSpecies'][()]))
            BottomB=np.reshape(SnapShot['BottomRobinB'][()],(self.info['nX'][()],self.info['nSpecies'][()]))
            BottomC=np.reshape(SnapShot['BottomRobinC'][()],(self.info['nX'][()],self.info['nSpecies'][()]))
            
            
#            TopA=np.concatenate((TopA,),axis=1)
            TopA=np.hstack((TopA,np.zeros((self.info['nX'][()],1))))
            TopB=np.hstack((TopB,np.zeros((self.info['nX'][()],1))))
            TopC=np.hstack((TopC,np.zeros((self.info['nX'][()],1))))
            
            
            BottomA=np.hstack((BottomA,np.zeros((self.info['nX'][()],1))))
            BottomB=np.hstack((BottomB,np.zeros((self.info['nX'][()],1))))
            BottomC=np.hstack((BottomC,np.zeros((self.info['nX'][()],1))))
            
            if SnapShot['IsFloating']:
                if not self.topReference:
#                    Top Contact with zero field
                    TopB[:,-1]=1
#                    Bottom Contact with zero potential
                    BottomA[:,-1]=1
                else:
#                    Bottom Contact with zero field
                    BottomB[:,-1]=1
#                    Top Contact with zero potential
                    TopA[:,-1]=1
            else:
#                Setting the applied bias conditions
                if not self.topReference:
                    TopA[:,-1]=1
#                   Voltage is assumed to be scaled by Vt in Numerical Engine
                    TopC[:,-1]=SnapShot['Bias']/SnapShot['Et']
                    BottomA[:,-1]=1
                else:
                    BottomA[:,-1]=1
                    BottomC[:,-1]=SnapShot['Bias']/SnapShot['Et']
                    TopA[:,-1]=1
                
            TopB[np.where(TopB==0)]=1e-6
            BottomB[np.where(BottomB==0)]=1e-6
            
            self.numEng.FC_BC=np.vstack((TopA,TopB,TopC))
            self.numEng.BC_BC=np.vstack((BottomA,BottomB,BottomC))
            
    def runRecipe(self):
        dtStart=1e-14
        tOut=np.array([[]])
        uOut=np.array([[]])
        uOut.shape=(self.numEng.nX*self.numEng.nY*self.numEng.M,0)
        fiOut=np.array([[]])
        fiOut.shape=(self.numEng.nX*self.numEng.nY,0)
        for i in range(1,self.snapShot.size):
            timeStart=self.snapShot[i-1]['time']
            timeEnd=self.snapShot[i]['time']
            tVec,UVec,fiVec=self.numEng.Run(timeStart,timeEnd,dtStart)
            tOut=np.hstack((tOut,tVec))
            uOut=np.hstack((uOut,UVec))
            fiOut=np.hstack((fiOut,fiVec*self.snapShot[i-1]['Et']))
            nextInitConc=np.reshape(UVec[:,-1],(self.numEng.nX*self.numEng.nY,self.numEng.M),order='F')
            nextInitFi=fiVec[:,-1]
            nextInitFi.shape=(self.numEng.nX*self.numEng.nY,1)
            self.setSnapShotData(self.snapShot[i])
            self.numEng.reInitialize()
            self.numEng.U0=nextInitConc
            self.numEng.fi0=nextInitFi
            dtStart=tVec[0,-1]-tVec[0,-2]
        self.tOut=tOut
        self.fiOut=fiOut
        self.uOut=uOut
        # Should start solution browser.
        
        self.SB.startInteractive()
