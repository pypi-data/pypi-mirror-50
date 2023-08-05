#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:08:46 2018

@author: abdul
"""

from .diffusionSolver import DiffusionSolver
import numpy as np

class Newton_DS_ber(DiffusionSolver):
    Ap=np.array([])
    def Solve(self,dt):
        out=np.array([])
        return out
    def updateFields(self):
        numEng=self.numEng
