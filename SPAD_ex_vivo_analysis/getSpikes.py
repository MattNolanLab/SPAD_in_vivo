# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 16:04:19 2021

@author: Yifang
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
#%%
def get_inverse_trace (trace_raw):
    '''Basic filter and smooth'''
    trace_raw=trace_raw.astype(np.float64)
    '''reverse the trace (voltron is reversed)''' 
    trace_reverse=np.negative(trace_raw)
    return trace_reverse

def plot_trace(trace, name='signal',ax=None,color='r',zorder=1,linewidth=1): 
    if ax is None:
        fig = plt.figure(figsize=[16,8])
        ax = fig.add_subplot(111)
    ax.plot(trace,color,linewidth=linewidth,zorder=zorder)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return ax

def plotSpikeOnTrace(trace, spiketimes,name='signal'):
    fig = plt.figure(figsize=[25,8])
    plt.plot(trace,color='tab:blue',linewidth=1,zorder=1)
    plt.scatter(spiketimes,trace[spiketimes],
                                 s=30,c='k',marker='o',zorder=2)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return fig

'''Original Voltron Pipeline with spike shape template to get spkie'''
def get_spiketimes_voltron (trace,title='spikeOnTrace',superfactor=10,threshs=(.75,.85,.94),
                                   window=2000,threshold_sets=(2.53,3.1,3.5),cutoff=10):
    trace=get_inverse_trace(trace)    
    spike_data=ROI.get_spikes_old(trace, superfactor=superfactor, threshs=threshs,
                                   window=window,threshold_sets=threshold_sets,cutoff=cutoff)
    
    sub_thresh2=spike_data[0]
    fig = plt.figure(figsize=[20,8])
    plt.plot(sub_thresh2)    
    high_freq=spike_data[1]
    fig = plt.figure(figsize=[20,8])
    plt.plot(high_freq)
    
    spiketimes=spike_data[2]
    spiketrain=spike_data[3]
    # spikesizes=spike_data[4]
    plotSpikeOnTrace(trace, spiketimes,name=title)
    return spiketimes,spiketrain,trace

def get_two_spiketimes_voltron (spike1,spike2,title1='SPAD',title2='ephys'):
    _,spiketimes1 = get_spiketimes_voltron (spike1,title=title1)    
    _,spiketimes2 = get_spiketimes_voltron (spike2,title=title2)  
    return spiketimes1,spiketimes2


def get_correlogram_voltron_spiketime (spiketimes1,spiketimes2, title=''):
    fig, ax = plt.subplots(1,2)
    Corr.plot_PSTH_correlogram_spiketrain(spiketimes1,spiketimes2,ax=ax[0],binsize=2,
                                          HalfWindowSize=50,frametime=0.1006198181,title=title)
    
    Corr.plot_PSTH_correlogram_spiketrain(spiketimes1,spiketimes2,ax=ax[1],binsize=100,
                                          HalfWindowSize=1000,frametime=0.1006198181,title=title)    
    fig.suptitle('SPAD-Ephys', fontsize=16)
    fig.tight_layout()
    return fig

def get_threshold (trace, window1=99400, window2=99900, std_thre=3.5,tracetype='Voltron'):
    '''To get threshold from a continuous recording'''
    trace_reference=trace[window1:window2]
    mean=np.mean(trace_reference)
    std=np.std(trace_reference)
    if tracetype=='Voltron':
        thres=mean-std_thre*std
    elif tracetype=='Normal':
        thres=mean+std_thre*std            
    return thres

def get_spiketrain(trace,thres):
    '''find peak above threshold'''
    spiketrain=np.zeros(len(trace))    
    min = (np.diff(np.sign(np.diff(trace))) > 0).nonzero()[0] + 1         # local min
    #min = (np.diff(np.sign(np.diff(trace))) < 0).nonzero()[0] + 1         # actally local max
    for i in range(len(min)):
        spiketrain[min[i]]=1 if trace[min[i]]<thres else 0
        
    spiketimes=np.where(spiketrain == 1)[0]
    
    for i in range(len(spiketimes)):
        if spiketimes[i]+3 <len(trace):
            if trace[spiketimes[i]+3]>thres or trace[spiketimes[i]-2]>thres :
                spiketrain[spiketimes[i]]=0            
    spiketimes=np.where(spiketrain == 1)[0]
    
    for i in range(len(spiketimes)-1):
        if spiketimes[i+1]-spiketimes[i]<6:
            if trace[spiketimes[i+1]]>trace[spiketimes[i]]:
                spiketrain[spiketimes[i+1]]=0   
            else:
                spiketrain[spiketimes[i]]=0 
    spiketimes=np.where(spiketrain == 1)[0]     
    return spiketrain,spiketimes


def get_spiketime(spiketrain):
    return np.where(spiketrain != 0)[0]

def get_spike_plot(trace,thre=3.5,name='signal'):
    spike_thres=get_threshold (trace,std_thre=thre)
    #spike_thres=get_threshold (trace,std_thre=thre,tracetype='Normal')
    spiketrain,spiketimes=get_spiketrain(trace,spike_thres)
    plotSpikeOnTrace(trace, spiketimes,name=name)
    return spiketrain,spiketimes

def get_spiketrain_peak(trace,thres,distance=4):    
    '''find peak above threshold'''
    peaks, _ = signal.find_peaks(trace, height=thres, threshold=None,
                                 width=20, distance=distance)
    spiketrain=np.zeros(len(trace))    
    spiketrain[peaks]=1        
    spiketimes=peaks
        
    return spiketrain,spiketimes

def get_spike_plot_peak(trace,thre=3.5,name='signal'):
    trace=get_inverse_trace (trace)
    spike_thres=get_threshold (trace,std_thre=thre,tracetype='Normal')
    spiketrain,spiketimes=get_spiketrain_peak(trace,spike_thres)
    plotSpikeOnTrace(trace, spiketimes,name=name)
    return spiketrain,spiketimes

