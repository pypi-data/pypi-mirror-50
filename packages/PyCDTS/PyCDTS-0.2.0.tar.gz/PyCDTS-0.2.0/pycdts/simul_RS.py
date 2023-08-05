#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:09:42 2018

@author: abdul
"""

from .reactionSolver import ReactionSolver
import numpy as np

class simul_RS(ReactionSolver):
    Ap=np.array([])
    def Solve(self,dt):
        out=np.array([])
        return out
    def updateFields(self):
        numEng=self.numEng
