# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 11:12:47 2021

@author: Yifang
"""
import os
import scipy.io 
import matplotlib.pyplot as plt
import scipy.signal
import voltron_ROI as ROI
import pandas as pd
import numpy as np
from scipy import stats
import getSpikes
#%%
def plot_trace(trace, name='signal',ax=None,color='m',zorder=1,linewidth=1): 
    if ax is None:
        fig = plt.figure(figsize=[25,8])
        ax = fig.add_subplot(111)
    ax.plot(trace,color,linewidth=linewidth,zorder=zorder)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return ax

def get_bin_trace (trace_raw,bin_window=20):
    '''Basic filter and smooth'''
    trace_raw=trace_raw.astype(np.float64)
    plot_trace(trace_raw, name='raw_trace')  
    '''reverse the trace (voltron is reversed)''' 
    # trace_reverse=np.negative(trace_raw)
    # plot_trace(trace_reverse, name='raw_trace_reverse') 
    
    '''5 frames as a rolling window to bin the data'''
    trace_rolling = pd.Series(trace_raw).rolling(window=bin_window,min_periods=bin_window,center=True).mean()
    trace_rolling.fillna(method="bfill",inplace=True)
    trace_rolling.fillna(method="ffill",inplace=True)
    trace_roll = np.array(trace_rolling)
    
    trace_binned=np.array(trace_raw).reshape(-1, bin_window).mean(axis=1)
    
    return trace_binned,trace_roll


#%%
dpath= "C:/SPAD/Tian/"
spath= "C:/SPAD/Tian/Plots"
# csv_1 =  os.path.join(dpath, "ROI1_500Hz.csv")
# csv_2 =  os.path.join(dpath, "ROI2_500Hz.csv")
# roi1_data=pd.read_csv(csv_1)  
# roi2_data=pd.read_csv(csv_2) 
original_trace3=pd.read_csv(os.path.join(dpath, "cell1_trace3_original.csv")) ['trace']

#%%
bin_window=20
trace_raw=original_trace3
trace_binned,trace_roll=get_bin_trace(original_trace3,bin_window=bin_window)

#%% Test threshold for binned data, 10kHZ
#spiketimes_1=getSpikes.get_spiketimes_voltron (trace_raw,title='spikeDetection_raw_trace',
#                                        threshs=(.4,.6,.7),
#                                        window=1000,threshold_sets=(2.5,3.,3.5))

spiketimes_2=getSpikes.get_spiketimes_voltron (trace_roll,title='spikeDetection_rollmean_trace',
                                        threshs=(.5,.7,.9),
                                        window=2000,threshold_sets=(2.51,3.1,3.5))

#%%
spiketimes_bin, spiketrain,trace_inverse=getSpikes.get_spiketimes_voltron (trace_binned,title='spikeDetection_binmeam_trace',
                                        threshs=(.4,.6,.75),
                                        window=1000,threshold_sets=(2.5,3.,3.2))
#%%
'''Shuffle analysis'''
import ShuffleSpikeTimes as Shuffle
spiketrain_shuffle,spiketimes_shuffle=Shuffle.shuffle_spiketimes(spiketrain, trace_inverse)
#%%
fig = plt.figure(figsize=[25,8])
ax = fig.add_subplot(111)
ax.plot(trace_roll,color='m',linewidth=1,zorder=2,label='rolling')
x=range(0,100000,20)
ax.plot(x,trace_binned,color='c',zorder=3,linewidth=1,label="binned")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title("20 frame binned", fontsize=20)
plt.legend(loc="upper right",fontsize=20)
fig.savefig( os.path.join(spath,'Overlay_rolling_binned_20frame.svg'), format='svg')


fig = plt.figure(figsize=[25,8])
ax = fig.add_subplot(111)
ax.plot(trace_roll[70000:80000],color='m',linewidth=1,zorder=2,label='rolling')
x=range(0,10000,20)
ax.plot(x,trace_binned[3500:4000],color='c',zorder=3,linewidth=1,label="binned")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title("20 frame binned_zoom7to8s", fontsize=20)
plt.legend(loc="upper right",fontsize=20)
fig.savefig( os.path.join(spath,'Overlay_rolling_binned_20frame_zoom1s.svg'), format='svg')

fig = plt.figure(figsize=[25,8])
ax = fig.add_subplot(111)
ax.plot(trace_roll[60000:80000],color='m',linewidth=1,zorder=2,label='rolling')
x=range(0,20000,20)
ax.plot(x,trace_binned[3000:4000],color='c',zorder=3,linewidth=1,label="binned")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title("20 frame binned_zoom6to8s", fontsize=20)
plt.legend(loc="upper right",fontsize=20)
fig.savefig( os.path.join(spath,'Overlay_rolling_binned_20frame_zoom2s.svg'), format='svg')
np.savetxt(os.path.join(spath, "trace3_5_binned.csv"), trace_binned, delimiter=",")