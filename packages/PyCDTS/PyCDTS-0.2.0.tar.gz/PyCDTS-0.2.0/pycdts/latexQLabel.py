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
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 18:09:41 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

from PyQt5.QtWidgets import (
        QWidget,QVBoxLayout,
        QApplication,qApp
        )

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class latexQLabel(QWidget):

    def __init__(self, mathText, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        l=QVBoxLayout(self)
        l.setContentsMargins(0,0,0,0)

        r,g,b,a=self.palette().base().color().getRgbF()
        self._figure=Figure(edgecolor=(r,g,b), facecolor=('none'))
        self._canvas=FigureCanvas(self._figure)
        l.addWidget(self._canvas)
        
        self._figure.clear()
        text=self._figure.suptitle(
                mathText,
                x=0.0,
                y=1.0,
                horizontalalignment='left',
                verticalalignment='top',
                size=qApp.font().pointSize()*2)
        self._canvas.draw()
        
        (x0,y0),(x1,y1)=text.get_window_extent().get_points()
        w=x1-x0; h=y1-y0
        
        self._figure.set_size_inches(w/80, h/80)
        self.setFixedSize(w,h)
    def updateText(self,mathText):
        self._figure.clear()
        text=self._figure.suptitle(
                mathText,
                x=0.0,
                y=1.0,
                horizontalalignment='left',
                verticalalignment='top',
                size=qApp.font().pointSize()*1)
        self._canvas.draw()
        
        (x0,y0),(x1,y1)=text.get_window_extent().get_points()
        w=x1-x0; h=y1-y0
        
        self._figure.set_size_inches(w/80, h/80)
        self.setFixedSize(w,h)
        
        
if __name__=='__main__':
    from sys import argv, exit
    a=QApplication(argv)
    mathText1='$D_{C}^{0} \\rightleftharpoons D_{C}^{+} + e_{c}^{-}$\n$D_{C}^{0} \\rightleftharpoons D_{C}^{+} + e_{c}^{-}$'
    w=latexQLabel(mathText1)
    mathText2='Hey'
    w.updateText(mathText2)
    w.show()
    w.raise_()
    exit(a.exec_())