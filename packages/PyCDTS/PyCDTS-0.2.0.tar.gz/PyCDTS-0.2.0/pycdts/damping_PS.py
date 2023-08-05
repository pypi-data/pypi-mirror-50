#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:00:31 2018

@author: abdul
"""

from .poissonSolver import PoissonSolver
import numpy as np

class damping_PS(PoissonSolver):
    Ap=np.array([])
    def Solve(self,dt):
        out=np.array([])
        return out
    def updateFields(self):
        numEng=self.numEng
    def formAp(self):
        mG=self.numEng.mGrid
        dX=np.tile(np.transpose(mG.dX),[1,2])
