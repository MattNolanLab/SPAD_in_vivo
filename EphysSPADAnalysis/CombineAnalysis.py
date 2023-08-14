# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 22:30:19 2023

@author: Yifang
"""
import os
import numpy as np
import pandas as pd
from scipy import signal
#from open_ephys.analysis import Session
import matplotlib.pylab as plt
import pynapple as nap
import pynacollada as pyna
from scipy.signal import filtfilt
from OESPADsingleTraceClass import OESPADsingleTrace
import OpenEphysTools as OE
#%%
dpath="G:/SPAD/SPADData/20230722_SPADOE/SyncRecording1/"
Recording1=OESPADsingleTrace(dpath) 
#%%lfp_low
silced_recording=Recording1.slicing_pd_data (Recording1.Ephys_tracking_spad_aligned,start_time=0, end_time=84)
Recording1.plot_two_traces (silced_recording['zscore_raw'],silced_recording['LFP_2'],silced_recording['speed_abs'])
#%%
# spad_lowpass= OE.butter_filter(silced_recording['zscore_raw'], btype='low', cutoff=100, fs=Recording1.fs, order=5)
# lfp_lowpass = OE.butter_filter(silced_recording['LFP_2'], btype='low', cutoff=1000, fs=Recording1.fs, order=5)
# spad_low = pd.Series(spad_lowpass, index=silced_recording['zscore_raw'].index)
# lfp_low = pd.Series(lfp_lowpass, index=silced_recording['LFP_2'].index)
#%%
for i in range(7):
    silced_recording=Recording1.slicing_pd_data (Recording1.Ephys_tracking_spad_aligned,start_time=10*i, end_time=10*(i+1))
    Recording1.plot_two_traces (silced_recording['zscore_raw'],silced_recording['LFP_2'],silced_recording['speed_abs'])
#%%
for i in range(7):
    silced_recording=Recording1.slicing_pd_data (Recording1.Ephys_tracking_spad_aligned,start_time=10*i, end_time=10*(i+1))
    spad_lowpass= OE.butter_filter(silced_recording['zscore_raw'], btype='low', cutoff=50, fs=Recording1.fs, order=5)
    lfp_lowpass = OE.butter_filter(silced_recording['LFP_2'], btype='low', cutoff=500, fs=Recording1.fs, order=5)
    spad_low = pd.Series(spad_lowpass, index=silced_recording['zscore_raw'].index)
    lfp_low = pd.Series(lfp_lowpass, index=silced_recording['LFP_2'].index)
    Recording1.plot_two_traces (spad_low,lfp_low,silced_recording['speed_abs'])
#%%
lags,corr=Recording1.calculate_correlation_with_detrend (silced_recording['zscore_raw'],silced_recording['LFP_2'])
fig, ax = plt.subplots(figsize=(15,5))
Recording1.plot_corr_line (lags,corr,ax,frametime=0.1)
#%%
lags,Corr_mean,Corr_sum=Recording1.get_mean_corr_two_traces (silced_recording['zscore_raw'],silced_recording['LFP_2'],corr_window=5)
fig, ax = plt.subplots(figsize=(15,5))
Recording1.plot_corr_line (lags,Corr_mean,ax,frametime=0.1,title='Mean Cross Correlation')

#%%
