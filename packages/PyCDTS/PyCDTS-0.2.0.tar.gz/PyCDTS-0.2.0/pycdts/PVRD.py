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
Created on Sun Nov  4 13:29:33 2018

@author: Abdul Rawoof Shaik
@email: arshaik@asu.edu
"""

import sys
from . import resources
import platform
import os

from PyQt5.QtWidgets import (
        QMainWindow, QApplication, QMdiArea, QMessageBox, QAction, QFrame, QLabel,
        QWidget, QFileDialog
        )
from PyQt5.QtGui import (
        QIcon, QPixmap, QPainter, QKeySequence
        )
from PyQt5.QtCore import (
        QT_VERSION_STR,PYQT_VERSION_STR
        )

from .PVRD_ProjectWidget import (PVRD_ProjectWidget,
                                __version__,
                                __MAGIC_NUMBER__,
                                __FILE_VERSION__
                                )

from .PVRD_DialogBox import(
        NewProjectDlg
        )
 
class PVRD:
    """
    This Class is the Root class for the PVRD code.
    It has mainWindow QApplication object with QStackedWidget as central widget.
    It contains 2 widget objects namely welcomeWidget and projectWidget.
    welcomeWidget class is a QWidget subclass to show the welcome image.
    projectWidget class is a QWidget subclass customized for the PVRD_projects.
    """
    def __init__(self):
        
        # mainWindow
        self.app = QApplication(sys.argv)
        self.app.setOrganizationName("ASU")
        self.app.setOrganizationDomain("asu.edu")
        self.app.setApplicationName("PVRD")
        self.app.setWindowIcon(QIcon(":/icon.png"))
        self.mainWindow=PVRD_mainWindow()
        
    def startApplication(self):
#        ex = PVRD()
        self.mainWindow.show()
        sys.exit(self.app.exec_())
        

    
class PVRD_mainWindow(QMainWindow):
    
    def __init__(self,parent=None):
        super(PVRD_mainWindow,self).__init__(parent)
        
        self.mdi = MdiArea()
        self.setCentralWidget(self.mdi)
        
        sizeLabel = QLabel()
        sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(sizeLabel)
        status.showMessage("Ready", 5000)
        
        # About the tool Message.
        self.aboutMsg=\
        "Python porting done by Abdul Rawoof Shaik (arshaik@asu.edu)<br>"\
        "Solver algorithms, Defect Chemistry Models and Infrastructure developed by<br>"\
        "Abdul R. Shaik(ASU), <br>Daniel Brinkman(SJSU), <br>Igor Sankin(FSLR),"\
        "<br>Dmitry Krasikov(FSLR), <br>Christian Ringhofer(ASU), <br>Hao Kang(Prudue),"\
        "<br>Benes Bedrich(Prudue) and <br>Dragica Vasileska (ASU)"\
        "<p>Acknowledgement:<br>This material is based upon work supported by the U.S. Department of"\
        " Energy’s Office of Energy Efficiency and Renewable Energy (EERE) "\
        "under Solar Energy Technologies Office (SETO) Agreement Number DE-EE0007536"
        
        self.dirty=False
        self.filename=None
    
        self.setWindowTitle('PVRD')
        self.setWindowIcon(QIcon(':/images/PVRD_icon.JPG'))
        self.setGeometry(10,40,1280,800)
        
        self.create_actions()
        
    def create_actions(self):
        """
        All the menu items as well as their actions are connected in this method.
        """
        fileNewAction = self.createAction("&New...", self.fileNew,
                QKeySequence.New, "filenew", "Create a project file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen", "Open a project file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the project")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, "Ctrl+Shift+S","filesaveas",
                tip="Save the project using a new name")
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction,fileOpenAction,fileSaveAction,\
                                fileSaveAsAction)
        self.addActions(self.fileMenu,self.fileMenuActions)
        
        helpAboutAction = self.createAction("&About PVRD",
                self.helpAbout,"","",tip="Information about tool authors and funding agency")
        
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction,None))
        
    def fileNew(self):
        """
        Creates New PVRD Project. 
        """
        projDialog = NewProjectDlg()
        projDialog.exec_()
        if not projDialog.nDims<0:
            proj=PVRD_ProjectWidget(nDims=projDialog.nDims,mainWindow=self)
            self.mdi.addSubWindow(proj)
            proj.show()
#        QMessageBox.about(self,"Under Development","Under Development")
        
    def fileOpen(self):
        """
        Opens previous PVRD Projects
        """
#        QMessageBox.about(self,"Under Development","Under Development")
        filename,_ = QFileDialog.getOpenFileName(self,"PVRD Project -- Open File",'',"PVRD Project Data files (*.ppd)")
        if filename:
            for proj in self.mdi.subWindowList():
                if proj.widget().fileName==filename:
                    self.mdi.setActiveSubWindow(proj)
                    break
            else:
                self.loadFile(filename)
                
    def loadFile(self,filename):
        proj=PVRD_ProjectWidget(mainWindow=self)
        try:
            proj.load(filename)
        except (IOError, OSError) as err:
            QMessageBox.warning(self,"PVRD Project -- Load Error",
                                "Failed to load {0}: {1}".format(filename,err))
            del proj
        else:
            self.mdi.addSubWindow(proj)
            proj.show()
#            self.mdi.setActiveSubWindow(proj)
        
    def fileSave(self):
        """
        Saves the PVRD Project
        """
        proj=self.mdi.activeSubWindow()
        if proj is None or not isinstance(proj,QWidget):
            return True
        try:
            proj.widget().save()
            return True
        except (IOError, OSError) as err:
            QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save {0}: {1}".format(proj.widget().filename, err))
            return False
        
#        QMessageBox.about(self,"Under Development","Under Development")
        
    def fileSaveAs(self):
        """
        Saves the PVRD Project with different name.
        """
        proj=self.mdi.activeSubWindow()
        if proj is None or not isinstance(proj,QWidget):
            return True
        fname = proj.widget().fileName if proj.widget().fileName is not None else "."
        fname,_ = QFileDialog.getSaveFileName(self,
                "Project -- Save As", fname,
                "PVRD Project Data files (*.ppd)")
        if fname:
            if "." not in fname:
                fname += ".ppd"
            
            proj.widget().fileName=fname
            self.statusBar().showMessage("Saved the file as {0}".format(os.path.basename(fname)), 5000)
            return self.fileSave()
        return True
        
        
    def helpAbout(self):
        """
        Displays the information about PVRD Tool, Authors and Versions.
        """
        QMessageBox.about(self, "About PVRD",
                """<b>PVRD</b> v {0}
                <p>Copyright &copy; 2017-19 ASU,FSLR,SJSU,Purdue. 
                All rights reserved.
                <p>A Unified Solver for Studying Point Defect Dynamics
                <p>Python {1} - Qt {2} - PyQt {3} on {4}<br><br>
                {5}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system(),self.aboutMsg))
        
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False):
        """
        This method is used for creating QActions for each of the file menu
        operations.
        """
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def addActions(self, target, actions):
        """
        Method to create Actions in a loop.
        """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

class MdiArea(QMdiArea):
    """
    Class created for displaying welcome image by modifying QMdiArea paintEvent()
    Inherits QMdiArea (Multiple Document Interface)
    """
    def __init__(self,parent=None):
        QMdiArea.__init__(self,parent=parent)
        
    def paintEvent(self,event):
        QMdiArea.paintEvent(self,event)
        painter=QPainter(self.viewport())
        painter.drawPixmap(self.rect(),QPixmap(":/images/welcome1.JPG"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("ASU")
    app.setOrganizationDomain("asu.edu")
    app.setApplicationName("PVRD")
    app.setWindowIcon(QIcon(":/icon.png"))
    ex = PVRD()
    ex.startApplication()
    sys.exit(app.exec_())        
