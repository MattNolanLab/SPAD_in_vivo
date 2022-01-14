#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 16:54:48 2021

@author: kurtulus
"""
import ok

device = ok.FrontPanelDevices()
xem = device.Open()

if not xem:
    print("A device could not be opened. Is one connected?")


devInfo = ok.okTDeviceInfo()

if (xem.NoError != xem.GetDeviceInfo(devInfo)):
    print("Unable to retrieve device information")
    
print("         Product: " + devInfo.productName)
print("Firmware version: %d.%d" % (devInfo.deviceMajorVersion,devInfo.deviceMinorVersion))
print("   Serial Number: %s "  % devInfo.serialNumber)
print("       Device ID: %s" % devInfo.deviceID)
print(devInfo.usbSpeed)



