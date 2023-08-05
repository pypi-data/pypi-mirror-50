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
Created on Mon Nov  5 08:24:44 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

import math

from PyQt5.QtWidgets import (
        QGraphicsItem, QMessageBox, QGraphicsRectItem, QGraphicsLineItem
        )
from PyQt5.QtGui import (
        QPen, QBrush, QPainter, QPainterPath, QPolygonF, QKeyEvent
        )
from PyQt5.QtCore import (
        Qt, QLineF, QPointF,QDataStream, QIODevice, QRectF
        )
from .generalFunctions import (
        fac
        )

from .PVRD_DialogBox import (
        PVRD_RectangleDlg_Mode2,
        PVRD_LineDlg_Mode2,
        PVRD_PointDlg_Mode2,
        PVRD_RectangleDlg_Mode3,
        PVRD_LineDlg_Mode3,
        PVRD_PointDlg_Mode3,
        PVRD_Dlg_Mode4,
        PVRD_Dlg_Mode5,
        PVRD_Mode4_TemperatureDlg_Point,
        PVRD_Mode4_TemperatureDlg_NCooling,
        PVRD_Mode4_LightDlg_Point,
        PVRD_Mode4_BiasDlg_Point
        )

from pyqtgraph import (
        PlotDataItem, mkPen
        )

import numpy as np

class PVRD_Rectangle_Mode1_Boundary(QGraphicsRectItem):
    def __init__(self,r1=0,r2=0,rW=100,rH=100,pen=None,Brush=None,parent=None):
        super(PVRD_Rectangle_Mode1_Boundary,self).__init__(r1,r2,rW,rH,parent)
        self.pen=QPen(Qt.green)
        if pen is not None:
            self.pen=pen
        self.pen.setCosmetic(True)
        self.pen.setWidth(2)
        self.setPen(self.pen)
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.dlgBox=None
    def updateRect(self):
        """
        This function is only applicable for displaying graphics in 0D.
        """
        if self.dlgBox.nDims==0:
            self.setRect(0,0,2,2)
            self.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            
class PVRD_Rectangle_Mode1_Material(QGraphicsRectItem):
    def __init__(self,r1=0,r2=0,rW=100,rH=100,Brush=None,nDims=0,parent=None):
        super(PVRD_Rectangle_Mode1_Material,self).__init__(r1,r2,rW,rH,parent)
        self.parent=parent
        self.nDims=nDims
        if Brush is None:
            Brush=QBrush(QBrush(Qt.white,Qt.SolidPattern))
        self.Brush=Brush
        self.setBrush(Brush)
        self.setFlags(
                QGraphicsItem.ItemIsSelectable
#                |QGraphicsItem.ItemStacksBehindParent
#                |QGraphicsItem.ItemIsMovable
#                |QGraphicsItem.ItemClipsChildrenToShape
#                |QGraphicsItem.ItemIgnoresTransformations
                )
        if nDims >=2:
            self.setFlags(
                    QGraphicsItem.ItemStacksBehindParent
                    )
        if nDims==1:
            self.setPen(QPen(Brush.color()))
            
    def updateRect(self):
        """
        This function is only applicable for displaying graphics in 0D.
        """
        if self.nDims==0:
            self.setRect(0,0,2,2)
            self.setBrush(self.Brush)
            pen=QPen(self.Brush.color())
            pen.setCosmetic(True)
            pen.setWidth(1)
            self.setPen(pen)
        
        
#    def mouseDoubleClickEvent(self,event):
#        if self.parent.pWidget.isMaterialDone==0:
#            self.parent.pWidget.updateLogic()
#        self.updateLogic()
#        QMessageBox.about(self.parent.pWidget,"Warning","Still Developing")
            
class PVRD_Rectangle_Mode1_GrainBoundary(QGraphicsRectItem):
    def __init__(self,r1=0,r2=0,rW=100,rH=100,Brush=None,pen=None,nDims=0,parent=None):
        super(PVRD_Rectangle_Mode1_GrainBoundary,self).__init__(r1,r2,rW,rH,parent)
        self.parent=parent
        self.nDims=nDims
        if Brush is None:
            Brush=QBrush(QBrush(Qt.white,Qt.SolidPattern))
        if pen is not None:
            self.setPen(pen)
        self.Brush=Brush
        
        if self.nDims >=2:
            self.setFlags(
                    QGraphicsItem.ItemStacksBehindParent
                    )
        if self.nDims==1:
            pen=QPen(Brush.color())
#            pen.setWidth(1)
            pen.setCosmetic(False)
            self.setPen(pen)
#            self.setBrush(Brush)
            
        if self.nDims==2:
            self.setBrush(Brush)
            
    def updateRect(self):
        """
        This function is only applicable for displaying graphics in 0D.
        """
        if self.nDims==0:
            self.setRect(0,0,2,2)
            self.setBrush(self.Brush)
            pen=QPen(self.Brush.color())
            pen.setCosmetic(True)
            pen.setWidth(1)
            self.setPen(pen)
        
    def paint(self,painter,option,index):
        painter.setCompositionMode(QPainter.CompositionMode_Difference)
        return QGraphicsRectItem.paint(self,painter,option,index)
    
class PVRD_Line_Mode1_GrainBoundary_NoSelect(QGraphicsLineItem):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,nDims=0,parent=None):
        super(PVRD_Line_Mode1_GrainBoundary_NoSelect,self).__init__(x1,y1,x2,y2,parent)
        
        self.nDims=nDims
        pen=QPen(Qt.white)
        pen.setCosmetic(True)
        pen.setWidth(1)
        pen.setStyle(Qt.DashLine)
        self.setPen(pen)
        
        if self.nDims==1:
            self.setLine(x1-1,y1,x1+1,y1)
            pen.setCosmetic(False)
            pen.setStyle(Qt.SolidLine)
            pen.setWidth(2)

#        self.setFlags(
#                QGraphicsItem.ItemIsSelectable
#                )
        
class PVRD_Line_Mode1_GrainBoundary(QGraphicsLineItem):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,nDims=0,parent=None):
        super(PVRD_Line_Mode1_GrainBoundary,self).__init__(x1,y1,x2,y2,parent)
        self.line=QLineF(x1,y1,x2,y2)
        self.nDims=nDims
        pen=QPen(Qt.white)
        pen.setCosmetic(True)
        pen.setWidth(2)
        pen.setStyle(Qt.DotLine)
        self.pen=pen
        self.setPen(pen)
        if self.nDims==1:
#            self.setLine(x1-1,y1,x1+1,y1)
            self.line=QLineF(x1-1,y1,x1+1,y1)
            pen.setStyle(Qt.SolidLine)
        self.setAcceptHoverEvents(True)
        self.selectionOffset=2
        self.setFlags(
                QGraphicsItem.ItemIsSelectable
                )
        self.createSelectionPolygon()
        
    def createSelectionPolygon(self):
#            QMessageBox.about(self,"Warning","in CreateSelectionPolygon")
        nPolygon=QPolygonF()
        radAngle=self.line.angle()*math.pi/180
        dx=self.selectionOffset*math.sin(radAngle)
        dy=self.selectionOffset*math.cos(radAngle)
        offset1=QPointF(dx,dy)
        offset2=QPointF(-dx,-dy)
        nPolygon.append(self.line.p1()+offset1)
        nPolygon.append(self.line.p1()+offset2)
        nPolygon.append(self.line.p2()+offset2)
        nPolygon.append(self.line.p2()+offset1)
        self.selectionPolygon=nPolygon
        self.update()
            
            
    def boundingRect(self):
        return self.selectionPolygon.boundingRect()
        
    def shape(self):
        ret=QPainterPath()
        ret.addPolygon(self.selectionPolygon)
        return ret;
        
    def paint(self,painter,options,index):
        painter.setPen(self.pen)
        painter.drawLine(self.line)
        if self.isSelected():
            pen=QPen(Qt.white, 1, Qt.DashDotLine)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawPolygon(self.selectionPolygon)
            
class PVRD_Rectangle_Mode2(QGraphicsRectItem):
    def __init__(self,bx=0,by=0,width=0,height=0,Name="",matName="",pen=None,brush=None,projWindow=None,parent=None,pCindx=None,nDims=0,gType=0):
        super(PVRD_Rectangle_Mode2,self).__init__(bx*fac,by*fac,width*fac,height*fac)
#        QMessageBox.about(parent,"Warning","main Line {0}".format(matName))
        self.projWindow=projWindow
        self.bx=bx*fac
        self.by=by*fac
        self.w=width*fac
        self.h=height*fac
        self.isDropped=False
        self.nDims=nDims
        if pen is None:
            pen=QPen(Qt.black)
            pen.setCosmetic(True)
            pen.setWidth(1)
            pen.setStyle(Qt.SolidLine)
        if brush is None:
            brush=QBrush(Qt.white)
        self.pen=pen
        self.brush=brush
        self.setPen(pen)
        self.setBrush(brush)
        
        self.selectionOffset=2
        self.pCindx=pCindx
            
        self.setFlags(
                QGraphicsItem.ItemIsSelectable
                |QGraphicsItem.ItemIsFocusable
                )
        if gType==0:
            self.dlgBox=PVRD_RectangleDlg_Mode2(bx,by,width,height,Name,matName,parent=self)
            self.setAcceptDrops(True)
            self.setAcceptHoverEvents(True)
            
        if gType==1:
            self.dlgBox=PVRD_RectangleDlg_Mode3(bx,by,width,height,Name,matName,parent=self)
            
        if gType==2:
            self.dlgBox=PVRD_Dlg_Mode4(typeVal=2,parent=self)
            
        if gType==3:
            self.dlgBox=PVRD_Dlg_Mode5(parent=self,typeVal=2)
        
        if nDims==1:
            pen=QPen(brush.color())
            pen.setCosmetic(True)
            pen.setWidth(4)
            pen.setStyle(Qt.SolidLine)
            self.setPen(pen)
            
        if nDims==0:
            self.setRect(0,0,2,2)
            self.setBrush(self.brush)
            pen=QPen(self.brush.color())
            pen.setCosmetic(True)
            pen.setWidth(1)
            self.setPen(pen)
            
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Q and self.isSelected:
                self.dlgBox.exec_()
            
#            if event.key() == Qt.Key_F:
#                self.projWindow.fit()
                
    def mouseDoubleClickEvent(self,event):
        self.dlgBox.exec_()
        
    def dragEnterEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        self.isDropped=True
        if self.isSelected and event.mimeData().hasFormat(model_mime_type):
            event.accept()
        else:
            event.reject()
            
    def dragLeaveEvent(self,event):
        self.isDropped=False
    
    def dragMoveEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        if self.isSelected and event.mimeData().hasFormat(model_mime_type):
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        if self.isUnderMouse and event.mimeData().hasFormat(model_mime_type):
            encoded = event.mimeData().data(model_mime_type)
            stream = QDataStream(encoded, QIODevice.ReadOnly)
            while not stream.atEnd():
                row = stream.readInt()
                column = stream.readInt()
                mapp = stream.readQVariantMap()
                itemName = mapp['']
                if itemName in self.projWindow.pC.db.mechanisms:
                    self.dlgBox.addMechanisms((itemName))
                
                if itemName in self.projWindow.pC.db.reactions:
                    self.dlgBox.addReactions((itemName))
                    
                if itemName in self.projWindow.pC.db.species:
                    self.dlgBox.addSpecies((itemName))
                    
                    
class PVRD_Line_Mode2(QGraphicsLineItem):
    def __init__(self,x1=0,y1=0,x2=0,y2=0,Name="",matName="",pen=None,projWindow=None,parent=None,pCindx=None,nDims=0,gType=0):
        super(PVRD_Line_Mode2,self).__init__(x1,y1,x2,y2)
        self.projWindow=projWindow
#        QMessageBox.about(parent,"Warning","main Line {0}".format(matName))
        self.line=QLineF(x1*fac,y1*fac,x2*fac,y2*fac)
        self.nDims=nDims
        self.isDropped=False
        if pen is None:
            pen=QPen(Qt.white)
            pen.setCosmetic(True)
            pen.setWidth(2)
            pen.setStyle(Qt.DotLine)
        self.pen=pen
        self.setPen(pen)
        self.selectionOffset=2
        self.pCindx=pCindx
        
        if nDims==1:
            self.line=QLineF(x1*fac-2,y1*fac,x1*fac+2,y1*fac)
            pen.setStyle(Qt.SolidLine)
            pen.setCosmetic(True)
            pen.setWidth(2)
            self.setPen(pen)
        
        self.setFlags(
                QGraphicsItem.ItemIsSelectable
                |QGraphicsItem.ItemIsFocusable
                )
        self.createSelectionPolygon()
        
        if gType==0:
            self.dlgBox=PVRD_LineDlg_Mode2(x1,y1,x2,y2,Name,matName,parent=self)
            self.setAcceptHoverEvents(True)        
            self.setAcceptDrops(True)
        
        if gType==1:
            self.dlgBox=PVRD_LineDlg_Mode3(x1,y1,x2,y2,Name,matName,parent=self)
            
        if gType==2:
            self.dlgBox=PVRD_Dlg_Mode4(typeVal=1,parent=self)
            
        if gType==3:
            self.dlgBox=PVRD_Dlg_Mode5(parent=self,typeVal=1)
        
    def createSelectionPolygon(self):
#            QMessageBox.about(self,"Warning","in CreateSelectionPolygon")
        nPolygon=QPolygonF()
        radAngle=self.line.angle()*math.pi/180
        dx=self.selectionOffset*math.sin(radAngle)
        dy=self.selectionOffset*math.cos(radAngle)
        offset1=QPointF(dx,dy)
        offset2=QPointF(-dx,-dy)
        nPolygon.append(self.line.p1()+offset1)
        nPolygon.append(self.line.p1()+offset2)
        nPolygon.append(self.line.p2()+offset2)
        nPolygon.append(self.line.p2()+offset1)
        self.selectionPolygon=nPolygon
        self.update()
            
            
    def boundingRect(self):
        return self.selectionPolygon.boundingRect()
        
    def shape(self):
        ret=QPainterPath()
        ret.addPolygon(self.selectionPolygon)
        return ret;
        
    def paint(self,painter,options,index):
        painter.setPen(self.pen)
        painter.drawLine(self.line)
        if self.isSelected():
            pen=QPen(Qt.white, 1, Qt.DashDotLine)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawPolygon(self.selectionPolygon)
            
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Q and self.isSelected:
                self.dlgBox.exec_()
#            if event.key() == Qt.Key_F:
#                self.projWindow.fit()
                
    def mouseDoubleClickEvent(self,event):
        self.dlgBox.exec_()
        
        
    def dragEnterEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        self.isDropped=True
        if self.isSelected and event.mimeData().hasFormat(model_mime_type):
            event.accept()
        else:
            event.reject()
            
    def dragLeaveEvent(self,event):
        self.isDropped=False
    
    def dragMoveEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        if self.isSelected and event.mimeData().hasFormat(model_mime_type):
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        if self.isUnderMouse and event.mimeData().hasFormat(model_mime_type):
            encoded = event.mimeData().data(model_mime_type)
            stream = QDataStream(encoded, QIODevice.ReadOnly)
            while not stream.atEnd():
                row = stream.readInt()
                column = stream.readInt()
                mapp = stream.readQVariantMap()
                itemName = mapp['']
                if itemName in self.projWindow.pC.db.mechanisms:
                    self.dlgBox.addMechanisms((itemName))
                
                if itemName in self.projWindow.pC.db.reactions:
                    self.dlgBox.addReactions((itemName))
                    
                if itemName in self.projWindow.pC.db.species:
                    self.dlgBox.addSpecies((itemName))
                    
class PVRD_Point_Mode2(QGraphicsLineItem):
    def __init__(self,x1=0,y1=0,Name="",matName="",pen=None,projWindow=None,parent=None,pCindx=None,nDims=0,gType=0):
        super(PVRD_Point_Mode2,self).__init__(x1,y1,x1,y1)
        self.projWindow=projWindow
#        QMessageBox.about(parent,"Warning","main Line {0}".format(matName))
        self.line=QLineF(x1*fac,y1*fac,x1*fac,y1*fac)
        self.nDims=nDims
        self.isDropped=False
        if pen is None:
            pen=QPen(Qt.white)
            pen.setCosmetic(True)
            pen.setWidth(2)
            pen.setStyle(Qt.DotLine)
        self.pen=pen
        self.setPen(pen)
        
        self.selectionOffset=2
        self.pCindx=pCindx
        
        if self.nDims==2:
            self.line=QRectF(x1*fac-1,y1*fac-1,2,2)
            pen.setStyle(Qt.SolidLine)
            pen.setCosmetic(True)
            pen.setWidth(2)
            self.setPen(pen)
            
        
        self.setFlags(
                QGraphicsItem.ItemIsSelectable
                |QGraphicsItem.ItemIsFocusable
                )
        self.createSelectionPolygon()
        
        if gType==0:
            self.dlgBox=PVRD_PointDlg_Mode2(x1,y1,Name,matName,parent=self)
            self.setAcceptHoverEvents(True)
            self.setAcceptDrops(True)
            
        if gType==1:
            self.dlgBox=PVRD_PointDlg_Mode3(x1,y1,Name,matName,parent=self)
            
        if gType==2:
            self.dlgBox=PVRD_Dlg_Mode4(typeVal=0,parent=self)
            
        if gType==3:
            self.dlgBox=PVRD_Dlg_Mode5(parent=self,typeVal=0)
        
    def createSelectionPolygon(self):
#            QMessageBox.about(self,"Warning","in CreateSelectionPolygon")
        nPolygon=QPolygonF()
        if self.nDims==2:
            radAngle=0*math.pi/180
        else:
            radAngle=self.line.angle()*math.pi/180
        dx=self.selectionOffset*math.sin(radAngle)
        dy=self.selectionOffset*math.cos(radAngle)
        offset1=QPointF(dx,dy)
        offset2=QPointF(-dx,-dy)
        if self.nDims==2:
            dx=dx+self.selectionOffset
            dy=dy+self.selectionOffset
            offset1=QPointF(dx,dy)
            offset2=QPointF(-dx,-dy)
            offset3=QPointF(-dx,dy)
            offset4=QPointF(dx,-dy)
            nPolygon.append(self.line.topRight()+offset1)
            nPolygon.append(self.line.topLeft()+offset3)
            nPolygon.append(self.line.bottomLeft()+offset2)
            nPolygon.append(self.line.bottomRight()+offset4)
#            nPolygon.append(self.line.p2()+offset2)
#            nPolygon.append(self.line.p2()+offset1)
        else:
            nPolygon.append(self.line.p1()+offset1)
            nPolygon.append(self.line.p1()+offset2)
            nPolygon.append(self.line.p2()+offset2)
            nPolygon.append(self.line.p2()+offset1)
        self.selectionPolygon=nPolygon
        self.update()
            
            
    def boundingRect(self):
        return self.selectionPolygon.boundingRect()
        
    def shape(self):
        ret=QPainterPath()
        ret.addPolygon(self.selectionPolygon)
        return ret;
        
    def paint(self,painter,options,index):
        painter.setPen(self.pen)
        if self.nDims==2:
            painter.drawRect(self.line)
            painter.fillRect(self.line,QBrush(Qt.white,Qt.SolidPattern))
        else:
            painter.drawLine(self.line)
        if self.isSelected():
            pen=QPen(Qt.white, 1, Qt.DashDotLine)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawPolygon(self.selectionPolygon)
            
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Q and self.isSelected:
                self.dlgBox.exec_()
#            if event.key() == Qt.Key_F:
#                self.projWindow.fit()
                
    def mouseDoubleClickEvent(self,event):
        self.dlgBox.exec_()
        
        
    def dragEnterEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        self.isDropped=True
        if self.isSelected and event.mimeData().hasFormat(model_mime_type):
            event.accept()
        else:
            event.reject()
            
    def dragLeaveEvent(self,event):
        self.isDropped=False
    
    def dragMoveEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        if self.isSelected and event.mimeData().hasFormat(model_mime_type):
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self,event):
        model_mime_type='application/x-qabstractitemmodeldatalist'
        if self.isUnderMouse and event.mimeData().hasFormat(model_mime_type):
            encoded = event.mimeData().data(model_mime_type)
            stream = QDataStream(encoded, QIODevice.ReadOnly)
            while not stream.atEnd():
                row = stream.readInt()
                column = stream.readInt()
                mapp = stream.readQVariantMap()
                itemName = mapp['']
                if itemName in self.projWindow.pC.db.mechanisms:
                    self.dlgBox.addMechanisms((itemName))
                
                if itemName in self.projWindow.pC.db.reactions:
                    self.dlgBox.addReactions((itemName))
                    
                if itemName in self.projWindow.pC.db.species:
                    self.dlgBox.addSpecies((itemName))

class PVRD_pgLine_Mode4(PlotDataItem):
    def __init__(self,projWindow,indx,dlg,*args, **kargs):
        super(PVRD_pgLine_Mode4,self).__init__(*args, **kargs)
        self.projWindow=projWindow
        self.indx=indx
        self.dlg=dlg
        self.curve.setClickable(True)
        self.curve.mouseClickEvent=self.mouseClickEventPlot
        self.scatter.mouseClickEvent=self.mouseClickEventScatter
        
#        self.curve.setFlags(QGraphicsItem.ItemIsSelectable
##                |QGraphicsItem.ItemIsFocusable
#                )
#        
#        self.scatter.setFlags(QGraphicsItem.ItemIsSelectable
#                |QGraphicsItem.ItemIsFocusable
#                )
        
        self.setPen(mkPen('r', width=2))
        
        x,y = self.updateData()
        self.setData(x=x,y=y)
        self.setSymbol('o')
        
    def updateData(self):
        if isinstance(self.dlg,PVRD_Mode4_TemperatureDlg_Point) or isinstance(self.dlg,PVRD_Mode4_TemperatureDlg_NCooling):
            tempData=self.projWindow.pC.tempParList[self.indx]
        
        if isinstance(self.dlg,PVRD_Mode4_LightDlg_Point):
            tempData=self.projWindow.pC.lightParList[self.indx]
            
        if isinstance(self.dlg,PVRD_Mode4_BiasDlg_Point):
            tempData=self.projWindow.pC.biasParList[self.indx]
        
        start=tempData.startTimeVal # should get the units
        stop=tempData.endTimeVal # should get the units
        
        self.dlg.curTimeTB.setText("{0}".format(start))
        self.dlg.nextTimeTB.setText("{0}".format(stop-start))
        self.dlg.curTimeCB.setCurrentIndex(0)
        self.dlg.nextTimeCB.setCurrentIndex(0)
        
        x=np.linspace(start,stop,tempData.nParVal+2)
        
        start=tempData.startParVal # should get the units
        stop=tempData.endParVal # should get the units
        
        if isinstance(self.dlg,PVRD_Mode4_TemperatureDlg_Point) or isinstance(self.dlg,PVRD_Mode4_TemperatureDlg_NCooling):
            self.dlg.curTempTB.setText("{0}".format(start))
            self.dlg.nextTempTB.setText("{0}".format(stop))
            self.dlg.curTempCB.setCurrentIndex(0)
            self.dlg.nextTempCB.setCurrentIndex(0)
               
        if isinstance(self.dlg,PVRD_Mode4_LightDlg_Point):
            self.dlg.curLightTB.setText("{0}".format(start))
            self.dlg.nextLightTB.setText("{0}".format(stop))
#            self.dlg.curLightCB.setCurrentIndex(0)
#            self.dlg.nextLightCB.setCurrentIndex(0)
        if isinstance(self.dlg,PVRD_Mode4_BiasDlg_Point):
            self.dlg.curBiasTB.setText("{0}".format(start))
            self.dlg.nextBiasTB.setText("{0}".format(stop))
        
        y=np.linspace(start,stop,tempData.nParVal+2)
        
        if isinstance(self.dlg,PVRD_Mode4_TemperatureDlg_NCooling):
            rate=self.dlg.getRate()
            for ii in range(0,len(y)):
                y[ii]=stop+(start-stop)*np.exp(-rate*(x[ii]-x[0]))
            y[-1]=stop
        
        if isinstance(self.dlg,PVRD_Mode4_TemperatureDlg_Point) or isinstance(self.dlg,PVRD_Mode4_TemperatureDlg_NCooling):
            self.projWindow.pC.tempParList[self.indx].xPointList=x
            self.projWindow.pC.tempParList[self.indx].yPointList=y
        
        if isinstance(self.dlg,PVRD_Mode4_LightDlg_Point):
            self.projWindow.pC.lightParList[self.indx].xPointList=x
            self.projWindow.pC.lightParList[self.indx].yPointList=y
            
        if isinstance(self.dlg,PVRD_Mode4_BiasDlg_Point):
            self.projWindow.pC.biasParList[self.indx].xPointList=x
            self.projWindow.pC.biasParList[self.indx].yPointList=y
        
        return x,y
    
    def updateAndSetData(self):
        x,y=self.updateData()
        print('x={0},y={1}'.format(x,y))
        self.setData(x=x,y=y)
        
    def mouseClickEventPlot(self,ev):
        if not self.curve.clickable or ev.button() != Qt.LeftButton:
            return
        if self.curve.mouseShape().contains(ev.pos()):
#            QMessageBox(self.projWindow,"Warning","isSelected={0}".format(self.isSelected()))
            if ev.double():
                ev.accept()
                self.sigClicked.emit(self)
            
                
    def mouseClickEventScatter(self,ev):
        if ev.button() == Qt.LeftButton:
            pts = self.scatter.pointsAt(ev.pos())
            if len(pts) > 0:
                if ev.double():
                    self.scatter.ptsClicked = pts
                    self.scatter.sigClicked.emit(self, self.scatter.ptsClicked)
                    ev.accept()
            else:
                ev.ignore()
        else:
            ev.ignore()
        
      
#    def isSelected(self):
#        return self.curve.isSelected() or self.scatter.isSelected()

class PVRD_Rectangle_Mode5(QGraphicsRectItem):
    def __init__(self,bx=0,by=0,width=0,height=0,Name="",matName="",pen=None,brush=None,projWindow=None,parent=None,pCindx=None,nDims=0):
        super(PVRD_Rectangle_Mode5,self).__init__(bx*fac,by*fac,width*fac,height*fac)
        self.projWindow=projWindow
        self.bx=bx*fac
        self.by=by*fac
        self.w=width*fac
        self.h=height*fac
        self.nDims=nDims
        self.parent=parent
        if pen is None:
            pen=QPen(Qt.black)
            pen.setCosmetic(True)
            pen.setWidth(1)
            pen.setStyle(Qt.SolidLine)
        if brush is None:
            brush=QBrush(Qt.white)
            
        pen=QPen(brush.color())
        pen.setCosmetic(True)
        pen.setWidth(1)
        self.pen=pen
        self.brush=brush

        self.setPen(pen)
#        self.setBrush(brush)
        
        self.selectionOffset=2
        self.pCindx=pCindx
            
        self.setFlags(
                QGraphicsItem.ItemIsSelectable
                |QGraphicsItem.ItemIsFocusable
                )

        self.dlgBox=PVRD_Dlg_Mode5(parent=self,typeVal=2)
        
        if nDims==1:
            pen=QPen(brush.color())
            pen.setCosmetic(True)
            pen.setWidth(4)
            pen.setStyle(Qt.SolidLine)
            self.setPen(pen)
            
        if nDims==0:
            self.setRect(0,0,2,2)
            self.setBrush(self.brush)
            pen=QPen(self.brush.color())
            pen.setCosmetic(True)
            pen.setWidth(1)
            self.setPen(pen)
            
    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Q and self.isSelected:
                if self.dlgBox.exec_():
                    self.parent.gView.viewport().repaint()
            
#            if event.key() == Qt.Key_F:
#                self.projWindow.fit()
                
    def mouseDoubleClickEvent(self,event):
        if self.dlgBox.exec_():
            self.parent.gView.viewport().repaint()
        
    def paint(self,painter,options=None,index=None):
        painter.setPen(self.pen)
        if self.nDims==2:
            painter.drawRect(QRectF(self.bx,self.by,self.w,self.h))
            xMeshList=self.projWindow.pC.allRectList[self.pCindx].xMeshPointList
            yMeshList=self.projWindow.pC.allRectList[self.pCindx].yMeshPointList
            for ii in range(1,len(xMeshList)-1):
                painter.drawLine(QLineF(xMeshList[ii]*fac,self.by,xMeshList[ii]*fac,self.by+self.h))
            for ii in range(1,len(yMeshList)-1):
                painter.drawLine(QLineF(self.bx,yMeshList[ii]*fac,self.bx+self.w,yMeshList[ii]*fac))
                
        if self.nDims==1:
            painter.drawRect(QRectF(self.bx,self.by,self.w,self.h))
            yMeshList=self.projWindow.pC.allRectList[self.pCindx].yMeshPointList
            for ii in range(1,len(yMeshList)-1):
                painter.drawLine(QLineF(self.bx-0.5,yMeshList[ii]*fac,self.bx+0.5,yMeshList[ii]*fac))
                
        if self.nDims==0:
            rect=QRectF(self.bx-1,self.by-1,2,2)
            painter.drawRect(rect)
            painter.fillRect(rect,self.brush)
