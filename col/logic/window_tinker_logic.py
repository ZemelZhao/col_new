#!/usr/bin/env python3

import sys
import os
import configparser
try:
    myFolder = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(os.path.join(myFolder, os.path.pardir))
    from windows.window_tinker import *
    from base.log import Log
except ImportError:
    pass
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import pyqtgraph as pg
import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowAboutLogic(WindowAbout):
    def __init__(self, log, parent=None):
        self.log = log
        super(WindowAboutLogic, self).__init__()
        self.parent = parent

    def initUI(self):
        super(WindowAboutLogic, self).initUI()
        self.log.debug(self, 'Open Window')

    def keyReleaseEvent(self, event):
        """DocString for keyReleaseEvent"""
        #@todo: to be defined.
        if event.key() == Qt.Key_Q:
            self.close()

class WindowHelpLogic(WindowHelp):
    def __init__(self, log, parent=None):
        self.log = log
        super(WindowHelpLogic, self).__init__()
        self.parent = parent

    def keyReleaseEvent(self, event):
        """DocString for keyReleaseEvent"""
        #@todo: to be defined.
        if event.key() == Qt.Key_Q:
            self.close()


    def initUI(self):
        super(WindowHelpLogic, self).initUI()
        self.log.debug(self, 'Open Window')

    def action_pushbutton_ok(self):
        self.log.debug(self, 'Close Window')
        self.close()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    log = Log(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir, 'log', 'log.out'))
    win = WindowHelpLogic(log)
    win.show()
    sys.exit(app.exec_())


