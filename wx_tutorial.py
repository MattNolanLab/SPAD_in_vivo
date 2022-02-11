#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 21:31:15 2021

@author: kurtulus
"""

import wx 

class GUI_SPAD(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'SPAD-based Photometry', size=(600,200)) 
        
        panel=wx.Panel(self)
        button=wx.Button(panel,label="Connect to System", pos=(200,10),size=(200,50))
        
        self.StaticText(panel, label = '', pos = ())
        
        self.Bind(wx.EVT_BUTTON, self.closebutton,button)
        
    def closebutton(self, event):
        box=wx.MessageDialog(None, 'Welcome, Yifang! Are you ready for the project? :)')
        box.ShowModal()
        
    def open_system(self, event):
        
        
        
    def close_system(self,event):
        
        

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=GUI_SPAD(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
    

    
    