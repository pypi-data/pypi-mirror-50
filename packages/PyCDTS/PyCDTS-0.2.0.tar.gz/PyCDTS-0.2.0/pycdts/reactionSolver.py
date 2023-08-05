#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:36:04 2018

@author: abdul
"""

from abc import ABC, abstractmethod
import numpy as np

class ReactionSolver(ABC):
    def __init__(self,numEng):
        self.numEng=numEng
    
    @abstractmethod
    def Solve(self,dt):
        out=np.array([])
        return out
    @abstractmethod
    def updateFields(self):
        pass