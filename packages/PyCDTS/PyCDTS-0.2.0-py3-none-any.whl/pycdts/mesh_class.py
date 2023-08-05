#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:21:14 2018

@author: abdul
"""
import numpy as np

class Mesh_class:
    """
    Place Holder for mesh variables used in discretized equations
    """
    def __init__(self):
        self.nX=0
        self.nY=0
        self.X=np.empty([1,1])
        self.Y=np.empty([1,1])
        self.dY=np.empty([1,1])
        self.dX=np.empty([1,1])
        self.Hx=0
        self.hx=0
        self.Hy=0
        self.hy=0