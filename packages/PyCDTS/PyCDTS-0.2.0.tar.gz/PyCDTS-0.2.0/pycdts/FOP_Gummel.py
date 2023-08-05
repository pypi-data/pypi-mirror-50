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
Created on Wed Jun  5 23:20:50 2019

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from .algorithm import Algorithm
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.switch_backend('Qt5Agg')
from matplotlib.pyplot import pause
import time

class FOP_Gummel(Algorithm):
    def runAlgorithm(self,dt):
        U=np.array([])
        fi=np.array([])
        nIter=0
        Error=np.array([])
        
        self.numEng.uD_sol=self.numEng.uR_sol
        
        if not self.numEng.is0D:
            convergence=False
            self.numEng.uD_solInit=self.numEng.uD_sol
            Error_U=np.zeros((1,self.numEng.maxGummelIter))
            Error_Fi=np.zeros((1,self.numEng.maxGummelIter))
            
            while not convergence and nIter<self.numEng.maxGummelIter:
                nIter=nIter+1
                
                tS=time.time()
                
                if self.numEng.enableDS:
                    out=self.numEng.DS.Solve(dt)
                else:
                    out=self.numEng.uD_sol
                    
                if out.size==0:
#                    print("Could not solve diffusion for dt={0}".format(dt))
                    self.numEng.outLog.write("Could not solve diffusion for dt={0}\n".format(dt))
                    self.numEng.updateGUI()
                    raise ValueError('Could not solve diffusion for dt='+str(dt))
                    
                uD_old=self.numEng.uD_sol
                self.numEng.uD_sol=out
                
#                print('time for DS={0}'.format(time.time()-tS))
                
                tS=time.time()
                if self.numEng.enableRS:
                    out=self.numEng.RS.Solve(dt)
                else:
                    out=self.numEng.uR_sol
                    
                if out.size==0:
#                    print("Could not solve reactions for dt={0}".format(dt))
                    self.numEng.outLog.write("Could not solve reactions for dt={0}\n".format(dt))
                    self.numEng.updateGUI()
                    raise ValueError('Could not solve reactions for dt='+str(dt))
                    
                self.numEng.uR_sol=out
                self.numEng.uD_sol=self.numEng.uR_sol
                
                iCheck=np.where(uD_old !=0)
                if iCheck[0].size==0:
                    Error=np.float64('inf')
                else:
#                    Error=np.linalg.norm(out[iCheck]/uD_old[iCheck]-1)/np.sqrt(iCheck[0].size)
                    Error=np.linalg.norm(out[iCheck]/uD_old[iCheck]-1)/(iCheck[0].size)
                    
                conv_U=Error < self.numEng.gummelRelTolForConc
                Error_U[0,nIter-1]=Error
                
#                print('time for RS={0}'.format(time.time()-tS))
                
#                tS=time.time()
                if self.numEng.enablePS:
                    out=self.numEng.PS.Solve(dt)
                else:
                    out=self.numEng.fi_sol
                
                if out.size==0:
#                    print("Could not solve Poisson for dt={0}".format(dt))
                    self.numEng.outLog.write("Could not solve Poisson for dt={0}\n".format(dt))
                    self.numEng.updateGUI()
                    raise ValueError('Could not solve Poisson for dt'+str(dt))
                
                fi_old=self.numEng.fi_sol
                self.numEng.fi_sol=out
                
                Error=np.amax(abs(fi_old-out))
                Error_Fi[0,nIter-1]=Error
                conv_Fi=Error_Fi[0,nIter-1]<self.numEng.gummelRelTolForPotential
                
                convergence = conv_U and conv_Fi
#                print("GumIter={0:2d},\tError(Conc)={1:2.3e},\tError(Fi)={2:2.3e}".format(nIter,Error_U[0,nIter-1],Error_Fi[0,nIter-1]))
#                self.numEng.fIO.write("GumIter={0:2d},\tError(Conc)={1:2.3e},\tError(Fi)={2:2.3e}\n".format(nIter,Error_U[0,nIter-1],Error_Fi[0,nIter-1]))
                
                
#                if nIter>10:
#                    exit()
                
                if nIter % 100 == 1:
                    self.numEng.updateGUI()

        else:
            if self.numEng.enableRS:
                out=self.numEng.RS.Solve(dt)
            else:
                out=self.numEng.uR_sol
            
            if out.size==0:
#                print("Could not solve reactions for dt={0}".format(dt))
                self.numEng.outLog.write("Could not solve reactions for dt={0}\n".format(dt))
                self.numEng.updateGUI()
                
                raise ValueError('Could not solve reactions for dt='+str(dt))
                
            self.numEng.uR_sol=out
            self.numEng.uD_sol=self.numEng.uR_sol
            convergence=True
            
        if convergence:
            self.numEng.uInit=self.numEng.uD_sol
            self.numEng.uR_sol=self.numEng.uD_sol
            U=np.reshape(self.numEng.uD_sol,(self.numEng.nX*self.numEng.nY*self.numEng.M,1))
            fi=np.reshape(self.numEng.fi_sol,(self.numEng.nX*self.numEng.nY,1))
            
#            self.numEng.fIO.write('\nuD_sol\n')
#            np.savetxt(self.numEng.fIO,self.numEng.uD_sol,fmt='%2.5e')
#            
#            self.numEng.fIO.write('\nfi_sol\n')
#            np.savetxt(self.numEng.fIO,self.numEng.fi_sol.T,fmt='%2.5e')
            
#            self.numEng.fIO.close()
#            exit()
            
#            self.numEng.line1.set_ydata(self.numEng.uD_sol[:,0])
#            self.numEng.ax.set_yscale('log')
##            ax = plt.gca()
#            self.numEng.ax.relim()
#            self.numEng.ax.autoscale_view()
#            self.numEng.ax.set_title('Electron')
#            
#            self.numEng.line2.set_ydata(self.numEng.uD_sol[:,1])
#            self.numEng.ax1.set_yscale('log')
#            self.numEng.ax1.relim()
#            self.numEng.ax1.autoscale_view()
#            self.numEng.ax1.set_title('Hole')
#
#            self.numEng.line3.set_ydata(fi*self.numEng.Vt)
#            self.numEng.ax2.relim()
#            self.numEng.ax2.autoscale_view()
#            self.numEng.ax2.set_title('Potential')
#            
#            self.numEng.fig.canvas.draw()
#            self.numEng.fig.canvas.flush_events()
#            pause(0.5)
#            os.system('pause')
#            input()
        else:
            if nIter==self.numEng.maxGummelIter:
#                print("Could not Converge Gummel Loop for dt={0}".format(dt))
                self.numEng.outLog.write("Could not Converge Gummel Loop for dt={0}\n".format(dt))
                self.numEng.updateGUI()
                raise ValueError('Could not Converge Gummel Loop for dt='+str(dt)+', Error_Conc='+str(Error_U[0,-1])+', Error_Fi='+str(Error_Fi[0,-1]))
            else:
#                print("Divergence Detected. Stopped Gummel Loop for dt={0}".format(dt))
                self.numEng.outLog.write("Divergence Detected. Stopped Gummel Loop for dt={0}\n".format(dt))
                self.numEng.updateGUI()
                raise ValueError('Divergence Detected. Stopped Gummel Loop for dt='+str(dt))
        
        return U,fi,nIter,Error