# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 20:50:05 2022

@author: Yifang
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import traceAnalysis as Ananlysis
import SPADdemod

def getSignalTrace (filename, traceType='Constant',HighFreqRemoval=True,getBinTrace=False,bin_window=20):
    '''TraceType:Freq, Constant, TimeDiv'''
    trace=Ananlysis.Read_trace (filename,mode="SPAD")
    if HighFreqRemoval==True:
        trace=Ananlysis.butter_filter(trace, btype='low', cutoff=1000, fs=9938.4, order=10)       
    if traceType=='Constant':
        if getBinTrace==True:
            trace_binned=Ananlysis.get_bin_trace(trace,bin_window=bin_window,color='m')
            trace_binned=Ananlysis.get_bin_trace(trace,bin_window=bin_window)
            return trace_binned
        else:
            return trace
    if traceType=='Freq':
        #Red,Green= SPADdemod.DemodFreqShift (trace,fc_g=1000,fc_r=2000,fs=9938.4)
        Red,Green= SPADdemod.DemodFreqShift_bandpass (trace,fc_g=1009,fc_r=1609,fs=9938.4)
        #Red=Ananlysis.butter_filter(Red, btype='low', cutoff=200, fs=9938.4, order=10)
        #Green=Ananlysis.butter_filter(Green, btype='low', cutoff=200, fs=9938.4, order=10)
        Signal=Ananlysis.getSignal_subtract(Red,Green,fs=9938.4)
        return Red,Green,Signal
    if traceType=='TimeDiv': 
        #need to be modified for different time division traces
        lmin,lmax=SPADdemod.hl_envelopes_max(trace, dmin=2, dmax=2, split=True)
        fig, ax = plt.subplots(figsize=(12, 3))
        ax.plot(lmax,trace[lmax], color='r')
        ax.plot(lmin,trace[lmin], color='g')
        x_green, Green=SPADdemod.Interpolate_timeDiv (lmin,trace)
        x_red, Red=SPADdemod.Interpolate_timeDiv (lmax,trace)
        
        Signal=Ananlysis.getSignal_subtract(Red,Green,fs=9938.4)
        fig, ax = plt.subplots(figsize=(12, 3))
        ax=Ananlysis.plot_trace(Signal,ax, label="Signal")
        return Red,Green,Signal

#%%
# Sampling Frequency
fs   = 9938.4
#dpath= "C:/SPAD/SPADData/20220611/1516996_Freq_2022_6_11_16_8_21"
dpath="D:/SPAD/SPADData/20220913/1534725_HPC_50g_2022_9_13_16_3_57" 

#%%
filename=Ananlysis.Set_filename (dpath,"traceValue.csv")
#Red,Green,Signal=getSignalTrace (filename,traceType='TimeDiv',HighFreqRemoval=True,getBinTrace=False)
Signal_raw=getSignalTrace (filename,traceType='Constant',HighFreqRemoval=True,getBinTrace=False,bin_window=100)
#%%
import traceAnalysis as Ananlysis
bin_window=100

Signal_bin=Ananlysis.get_bin_trace(Signal_raw,bin_window=bin_window)
fig, ax = plt.subplots(figsize=(12, 2.5))
Ananlysis.plot_trace(Signal_bin,ax, fs=99.38, label="Binned to 100Hz",color="b")
#%%
import traceAnalysis as Ananlysis
bin_window=200
Red_bin=Ananlysis.get_bin_trace(Red,bin_window=bin_window)
Green_bin=Ananlysis.get_bin_trace(Green,bin_window=bin_window)
#%%
fig, ax = plt.subplots(figsize=(12, 2.5))
Ananlysis.plot_trace(Red_bin[0:500],ax, fs=49.7, label="Binned to 50Hz",color="r")

#ax.set_xlim([0, 0.1])
fig, ax = plt.subplots(figsize=(12, 2.5))
Ananlysis.plot_trace(Green_bin[0:500],ax, fs=49.7, label="Binned to 50Hz",color="g")
#ax.set_xlim([0, 0.1])
#%%
'''unmixing time division'''
lmin,lg=SPADdemod.hl_envelopes_max(Green, dmin=4, dmax=7, split=True)
lmin,lr=SPADdemod.hl_envelopes_max(Red, dmin=4, dmax=7, split=True)
fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(lg,Green[lg], color='g')
ax.plot(lr,Red[lr], color='r')
x_red, Red=SPADdemod.Interpolate_timeDiv (lr,Red)
x_green, Green=SPADdemod.Interpolate_timeDiv (lg,Green)

#%%
Signal=Ananlysis.getSignal_subtract(Red,Green,fs=49.7)
#%%
fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
ax0=Ananlysis.plot_trace(Green,ax0, fs=49.7, label="Green Signal 200Hz",color='g')
ax1=Ananlysis.plot_trace(Red,ax1, fs=49.7, label="Red Signal 200Hz", color='r')
ax2=Ananlysis.plot_trace(Signal,ax2, fs=49.7, label="Substract Signal 200Hz", color='b')
fig.tight_layout()
#%%
Signal=Ananlysis.butter_filter(Signal, btype='low', cutoff=100, fs=9938.4, order=5)

fig, ax = plt.subplots(figsize=(12, 2.5))
Ananlysis.plot_trace(Signal,ax, fs=9938.4, label="100Hz Low pass")
#%%
'''temporal bin dual channel'''
bin_window=200
Green_bin=Ananlysis.get_bin_trace(Green,bin_window=bin_window)
Red_bin=Ananlysis.get_bin_trace(Red,bin_window=bin_window)
Signal_binned=Ananlysis.get_bin_trace(Signal,bin_window=bin_window)

fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
ax0=Ananlysis.plot_trace(Green_bin,ax0, fs=99.384/2, label="Green Signal Binned 50Hz",color='g')
ax1=Ananlysis.plot_trace(Red_bin,ax1, fs=99.384/2, label="Red Signal Binned 50Hz", color='r')
ax2=Ananlysis.plot_trace(Signal_binned,ax2, fs=99.384/2, label="Substract Signal Binned 50Hz", color='b')
fig.tight_layout()

#%%
fs=200
fig, ax = plt.subplots(figsize=(8, 2))
powerSpectrum, freqenciesFound, time, imageAxis = ax.specgram(Signal,Fs=fs,NFFT=1024, detrend='linear',vmin=-130)
ax.set_xlabel('Time (Second)')
ax.set_ylabel('Frequency')
ax.set_ylim([0, 100])

#%%
signal1,signal2=Ananlysis.getICA (Red_bin,Green_bin)
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(signal1,ax, label="Signal1")
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(signal2,ax, label="Signal2")
#%%
fig, (ax0, ax1) = plt.subplots(nrows=2)
ax0=Ananlysis.plot_trace(signal1,ax0, fs=99.384/2, label="signal1 Signal Binned 50Hz",color='g')
ax1=Ananlysis.plot_trace(signal2,ax1, fs=99.384/2, label="signal2 Signal Binned 50Hz", color='r')
fig.tight_layout()
#%%
'''temporal bin'''
bin_window=200
signal1_bin=Ananlysis.get_bin_trace(signal1,bin_window=bin_window)
signal2_bin=Ananlysis.get_bin_trace(signal2,bin_window=bin_window)

fig, (ax0, ax1) = plt.subplots(nrows=2)
ax0=Ananlysis.plot_trace(signal1_bin,ax0, fs=99.384/2, label="signal1 Signal Binned 50Hz",color='r')
ax1=Ananlysis.plot_trace(signal2_bin,ax1, fs=99.384/2, label="signal2 Signal Binned 50Hz", color='g')
fig.tight_layout()

#%%
Red,Green,Signal = getSignalTrace (filename, traceType='TimeDiv',HighFreqRemoval=False,getBinTrace=False)

#%%
# Plot the spectrogram
fig, ax = plt.subplots(figsize=(8, 2))
powerSpectrum, freqenciesFound, time, imageAxis = ax.specgram(signal2_bin, Fs=fs/200,NFFT=1024, detrend='linear',vmin=-130)
ax.set_xlabel('Time (Second)')
ax.set_ylabel('Frequency')
ax.set_ylim([0, 250])
fig.colorbar(imageAxis,ax=ax)

#%%
Ananlysis.PSD_plot (Signal,fs=9938.4/200,method="welch",color='tab:blue',linewidth=1)
fig=Ananlysis.plot_PSD_bands (Signal,fs=9938.4)
#%%
fig=Ananlysis.plot_PSD_bands (trace_binned,fs=9938.4/20)
#%% Low pass filter
'''Get trend and detrend'''
# trace_trend=Ananlysis.butter_filter(trace_clean, btype='low', cutoff=10, fs=9938.4, order=5)
# trace_detrend = Ananlysis.get_detrend(trace_binned)
#%%
'''USE FASTICE method'''
#Red,Green,signal1, signal2 = FreqShift_getICA (trace_clean,fc_g=1000,fc_r=2000,fs=9938.4)

#%%
'''PHOTOMETRY DATA ANALYSIS'''

dpath= "C:/SPAD/SPADData/20220616"
filename=Ananlysis.Set_filename (dpath,csv_filename="1516995_cont-2022-06-16-145825.csv")
Green,Red=Ananlysis.Read_trace (filename,mode="photometry")

fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(Green,ax, fs=130, label="GCamp6 Raw")

Gcamp=Ananlysis.butter_filter(Green, btype='low', cutoff=10, fs=130, order=5)
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(Gcamp,ax, fs=130, label="GCamp6 10Hz lowpass")

fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(Red,ax, fs=130, label="Isospestic Raw", color='m')

Iso=Ananlysis.butter_filter(Red, btype='low', cutoff=10, fs=130, order=5)
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(Iso,ax, fs=130, label="Isospestic 10Hz lowpass", color='m')
#%%
sig=Ananlysis.getSignal_subtract(Red,Green,fs=130)
sig=Ananlysis.butter_filter(sig, btype='low', cutoff=20, fs=130, order=5)
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(sig,ax, fs=130, label="Isospestic")

#%%
Signal=Ananlysis.getSignal_subtract(Red,Green,fs=130)
#%%
signal1,signal2=Ananlysis.getICA (Red,Green)
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(signal1,ax, label="Signal1")
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(signal2,ax, label="Signal2")
#%%
Signal=Ananlysis.butter_filter(Signal, btype='low', cutoff=20, fs=130, order=10)     
fig, ax = plt.subplots(figsize=(12, 3))
ax=Ananlysis.plot_trace(Signal,ax, fs=130, label="trace")
