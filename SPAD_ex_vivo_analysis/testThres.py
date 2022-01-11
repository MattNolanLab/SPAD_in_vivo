# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 00:09:14 2021

@author: s2073467
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 18:07:40 2021

This is using Voltron pipeline to test Tian's data 
and calculate cross correlation'

@author: s2073467
"""

import os
import scipy.io 
import matplotlib.pyplot as plt
import scipy.signal as signal
import voltron_ROI_continuous as ROI
import pandas as pd
import numpy as np
from scipy import stats
import crossCorr as Corr
import getSpikes
#%%

#%%test threshold
dpath= "G:/Tian/TianDataSorted"
csv_cell2 =  os.path.join(dpath, "cell2.csv")
csv_cell2_ephys =  os.path.join(dpath, "cell2_ephys.csv")

cell2_data=pd.read_csv(csv_cell2)  
cell2_ephys_data=pd.read_csv(csv_cell2_ephys) 

'''cell2'''
trace2=cell2_data['trace2_500Hz']
trace3=cell2_data['trace3_500Hz']
trace4=cell2_data['trace4_500Hz']
trace5=cell2_data['trace5_500Hz']
trace6=cell2_data['trace6_500Hz']
trace7=cell2_data['trace7_500Hz']
trace8=cell2_data['trace8_500Hz']
trace10=cell2_data['trace10_500Hz']

'''ephys signal'''
trace2_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace2'])
trace3_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace3']) 
trace4_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace4'])
trace5_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace5']) 
trace6_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace6'])
trace7_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace7']) 
trace8_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace8'])
trace10_ephys=getSpikes.get_inverse_trace(cell2_ephys_data['trace10'])
#%%
get_spike_plot(trace2)
get_spike_plot(trace2_ephys,thre=50)
get_spike_plot(trace3)
get_spike_plot(trace3_ephys,thre=50)
get_spike_plot(trace4)
get_spike_plot(trace4_ephys,thre=50)
get_spike_plot(trace5)
get_spike_plot(trace5_ephys,thre=50)
get_spike_plot(trace6)
get_spike_plot(trace6_ephys,thre=50)
get_spike_plot(trace7)
get_spike_plot(trace7_ephys,thre=100)

#%%generate  threshold
dpath= "G:/Tian/TianDataSorted"
spath= "G:/Tian/Plots"
csv_cell1 =  os.path.join(dpath, "cell1.csv")
csv_cell2 =  os.path.join(dpath, "cell2.csv")
csv_cell3 =  os.path.join(dpath, "cell3.csv")
csv_cell4 =  os.path.join(dpath, "cell4.csv")
csv_cell5 =  os.path.join(dpath, "cell5.csv")
csv_cell6 =  os.path.join(dpath, "cell6.csv")

cell1_data=pd.read_csv(csv_cell1) 
cell2_data=pd.read_csv(csv_cell2)  
cell3_data=pd.read_csv(csv_cell3)  
cell4_data=pd.read_csv(csv_cell4)  
cell5_data=pd.read_csv(csv_cell5)    

spike_cell1_trace3=cell1_data['trace3_500Hz']
spike_cell2_trace3=cell2_data['trace3_500Hz']
spike_cell3_trace3=cell3_data['trace3_500Hz']
spike_cell5_trace3=cell5_data['trace3_500Hz']

#%% Use local minimum 
get_spike_plot(spike_cell1_trace3,thre=3.5,name='spike_cell1_trace3')
get_spike_plot(spike_cell2_trace3,thre=3.5,name='spike_cell2_trace3')
get_spike_plot(spike_cell3_trace3,thre=3.5,name='spike_cell3_trace3')
get_spike_plot(spike_cell5_trace3,thre=3.5,name='spike_cell5_trace3')

#%%  Use signal peak
get_spike_plot_peak(spike_cell1_trace3,thre=3.5,name='spike_cell1_trace3')
get_spike_plot_peak(spike_cell2_trace3,thre=3.5,name='spike_cell2_trace3')
get_spike_plot_peak(spike_cell3_trace3,thre=3.5,name='spike_cell3_trace3')
get_spike_plot_peak(spike_cell5_trace3,thre=3.5,name='spike_cell5_trace3')
#%% Best for now: window=4000, (0.75,0.85,0.92),(2.5,3.2,3.7)
#Best for now: window=2000, (0.75,0.85,0.95),(2.53,3.,3.5) #Manuscript
'''Voltron method'''

spiketimes_c1s3=get_spiketimes_voltron (spike_cell1_trace3,title='spike_cell1_trace3',
                                        threshs=(.75,.85,.94),
                                        window=2000,threshold_sets=(2.53,3.2,3.7))

spiketimes_c2s3=get_spiketimes_voltron (spike_cell2_trace3,title='spike_cell2_trace3',
                                        threshs=(.75,.85,.94),
                                        window=2000,threshold_sets=(2.53,3.2,3.7))

spiketimes_c3s3=get_spiketimes_voltron (spike_cell3_trace3,title='spike_cell3_trace3',
                                        threshs=(.75,.85,.94),
                                        window=2000,threshold_sets=(2.53,3.2,3.7))

spiketimes_c5s3=get_spiketimes_voltron (spike_cell5_trace3,title='spike_cell5_trace3',
                                        threshs=(.75,.85,.94),
                                        window=2000,threshold_sets=(2.53,3.2,3.7))

#%%
#%% Test threshold
dpath= "G:/Tian/TianDataSorted"
csv_cell2 =  os.path.join(dpath, "cell2.csv")
csv_cell2_ephys =  os.path.join(dpath, "cell2_ephys.csv")

cell2_data=pd.read_csv(csv_cell2)  
cell2_ephys_data=pd.read_csv(csv_cell2_ephys) 

'''cell2'''
trace2=cell2_data['trace2_500Hz']
trace3=cell2_data['trace3_500Hz']
trace4=cell2_data['trace4_500Hz']
trace5=cell2_data['trace5_500Hz']
trace6=cell2_data['trace6_500Hz']
trace7=cell2_data['trace7_500Hz']
trace8=cell2_data['trace8_500Hz']
trace10=cell2_data['trace10_500Hz']

'''ephys signal'''
trace2_ephys=get_inverse_trace(cell2_ephys_data['trace2'])
trace3_ephys=get_inverse_trace(cell2_ephys_data['trace3']) 
trace4_ephys=get_inverse_trace(cell2_ephys_data['trace4'])
trace5_ephys=get_inverse_trace(cell2_ephys_data['trace5']) 
trace6_ephys=get_inverse_trace(cell2_ephys_data['trace6'])
trace7_ephys=get_inverse_trace(cell2_ephys_data['trace7']) 
trace8_ephys=get_inverse_trace(cell2_ephys_data['trace8'])
trace10_ephys=get_inverse_trace(cell2_ephys_data['trace10'])

#%%
'''SPAD and ephys'''
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace2,trace2_ephys,title1='SPAD2',title2='ephys2')
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace3,trace3_ephys,title1='SPAD3',title2='ephys3')
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace4,trace4_ephys,title1='SPAD4',title2='ephys4')
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace5,trace5_ephys,title1='SPAD5',title2='ephys5')
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace6,trace6_ephys,title1='SPAD6',title2='ephys6')
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace7,trace7_ephys,title1='SPAD7',title2='ephys7')
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace8,trace8_ephys,title1='SPAD8',title2='ephys8')
spiketimes1,spiketimes2= get_two_spiketimes_voltron (trace10,trace10_ephys,title1='SPAD10',title2='ephys10')


