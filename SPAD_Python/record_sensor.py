#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:12:20 2022

@author: kurtulus
"""

"""
Script for test the sensor. 

"""



from SPCIMAGERAA import SPCIMAGER
from SPADAnalysis import SPADAnalysis
import numpy as np
import pyqtgraph as pg

#instantiate the sensor class
s = SPCIMAGER('SPCIMAGER_TOP.bit')

#connect to the sensor 
s.SensorConnect(s.bank)

#Start the sensor
s.SensorStart()

#recording_time = int(input("Please enter the duration of the recording: "))

#Show the total photon counts from the sensor
#s.RecordData(recording_time)


while 1:
    
    data = s.GetLiveData()
    
    data_new=np.unpackbits(data)
    
    print(data_new.sum())
    #image = data_new.reshape(240,320)
    
    #pg.image(image)
    


#p = SPADAnalysis("sample.bin", recording_time)

s.SensorDisconnect()




