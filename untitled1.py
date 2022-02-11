#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 21:57:45 2022

@author: kurtulus
"""

import pyqtgraph as pg 
import numpy as np 

from pyqtgraph.Qt import QtCore, QtGui

kazma = 10*np.random.rand(10)

pg.plot(kazma)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
