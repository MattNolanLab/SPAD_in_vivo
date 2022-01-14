#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 21:21:05 2021

@author: kurtulus
"""

"""
In this exapmple we cover the button application. 
"""


import wx

class Button_Example(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(Button_Example, self).__init__(*args, **kw)
        
        self.InitUI()
        
    def InitUI(self):
            
        pnl = wx.Panel(self)
        InfoButton = wx.Button(pnl, label = 'Change Text', pos = (100,20))
            
        self.str1 = wx.StaticText(pnl, label = '', pos = (100,80) )
            
        InfoButton.Bind(wx.EVT_BUTTON, self.OnClick)
            
        self.SetSize((350,250))
        self.SetTitle('Button Application')
        self.Centre()
            
    def OnClick(self, event):
        
        print('button clicked')
        
        for i in range(200000):
        
            kazma = i
            self.str1.SetLabel(str(kazma))
            
            
            
def main():
    
    app = wx.App()
    ex = Button_Example(None)
    ex.Show()
    app.MainLoop()
    
    
if __name__ == '__main__':
    main()