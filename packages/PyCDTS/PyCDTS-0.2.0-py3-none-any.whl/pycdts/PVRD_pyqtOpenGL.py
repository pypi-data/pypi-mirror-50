#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:19:03 2019

@author: abdul
"""

import pyqtgraph.opengl as gl
from pyqtgraph.opengl.GLGraphicsItem import GLGraphicsItem
from PyQt5 import QtCore, QtGui
from OpenGL.GL import *
import numpy as np

class GLTextItem(GLGraphicsItem):
    def __init__(self, X=None, Y=None, Z=None, text=None):
        GLGraphicsItem.__init__(self)
        self.setGLOptions('translucent')

        self.text = text
        self.X = X
        self.Y = Y
        self.Z = Z

    def setGLViewWidget(self, GLViewWidget):
        self.GLViewWidget = GLViewWidget

    def setText(self, text):
        self.text = text
        self.update()

    def setX(self, X):
        self.X = X
        self.update()

    def setY(self, Y):
        self.Y = Y
        self.update()

    def setZ(self, Z):
        self.Z = Z
        self.update()

    def paint(self):
        self.GLViewWidget.qglColor(QtCore.Qt.white)
        self.GLViewWidget.renderText(self.X, self.Y, self.Z, self.text)
        
class GLAxisItem(GLGraphicsItem):
    """
    **Bases:** :class:`GLGraphicsItem <pyqtgraph.opengl.GLGraphicsItem>`
    
    Displays three lines indicating origin and orientation of local coordinate system. 
    
    """
    def __init__(self, size=None, antialias=True, glOptions='translucent',xVec=None,yVec=None,zVec=None):
        GLGraphicsItem.__init__(self)
        if size is None:
            size = QtGui.QVector3D(10,10,10)
        self.antialias = antialias
        self.setSize(size=size)
        self.setGLOptions(glOptions)
        self.xVec=xVec
        self.yVec=yVec
        self.zVec=zVec

    
    def setSize(self, x=None, y=None, z=None, size=None):
        """
        Set the size of the axes (in its local coordinate system; this does not affect the transform)
        Arguments can be x,y,z or size=QVector3D().
        """
        if size is not None:
            x = size.x()
            y = size.y()
            z = size.z()
        self.__size = [x,y,z]
        self.update()

        
    def size(self):
        return self.__size[:]
    
    
    def paint(self):

        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glEnable( GL_BLEND )
        #glEnable( GL_ALPHA_TEST )
        self.setupGLState()
        
        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            
        glBegin( GL_LINES )
        
        x,y,z = self.size()
        xMin=0
        xMax=x
        yMin=0
        yMax=y
        zMin=0
        zMax=z
        if self.xVec is not None:
            xMin=min(self.xVec)
            xMax=max(self.xVec)
        if self.yVec is not None:
            yMin=min(self.yVec)
            yMax=max(self.yVec)
            
        if self.zVec is not None:
            zMin=min(self.zVec)
            zMax=max(self.zVec)
        
        glColor4f(1, 1, 1, .6)  # z is green
        glVertex3f(xMin, yMin, zMin)
        glVertex3f(xMin, yMin, zMax)

        glColor4f(1, 1, 1, .6)  # y is yellow
        glVertex3f(xMin, yMin, zMin)
        glVertex3f(xMin, yMax, zMin)

        glColor4f(1, 1, 1, .6)  # x is blue
        glVertex3f(xMin, yMin, zMin)
        glVertex3f(xMax, yMin, zMin)
        glEnd()
        
def main():
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.opts['distance'] = 40
    w.show()

    t = GLTextItem(X=0, Y=5, Z=10, text="Your text")
    t.setGLViewWidget(w)
    w.addItem(t)
    
    ax=GLAxisItem(xVec=np.array([-10,20]),yVec=np.array([-40,60]),zVec=np.array([-100,200]))

#    g = gl.GLGridItem()
#    w.addItem(g)
    
    w.addItem(ax)

    app.exec_()
    
if __name__ == '__main__':
    main()