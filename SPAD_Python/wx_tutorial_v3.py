#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 21:54:09 2021

@author: kurtulus
"""

import wx 

class Show_Info(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(Show_Info, self).__init__(*args, **kw)
        
        self.InitUI()
        
        
    def InitUI(self):
        
        Panel = wx.Panel(self)
        
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        text_1= wx.StaticText(Panel, label='Welcome to SPAD-based Photometry Project', pos=(10,10))
        h_sizer.Add(text_1, 0, wx.CENTER)
        
        btn = wx.Button(Panel, label='Button', pos = (10,40), size=(100,100))
        h_sizer.Add(btn, 0, wx.CENTER)
        
        main_sizer.Add((0,0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0,0), 1, wx.EXPAND)
        
        
        self.SetSize((350,250))
        self.SetTitle('SPAD-based Photometry')
        self.Centre()
        
        Panel.SetSizer(main_sizer)
        
        self.Show()
        

def main():
    
    app = wx.App()
    ex = Show_Info(None)
    ex.Show()
    app.MainLoop()
    
if __name__=='__main__':
    main()