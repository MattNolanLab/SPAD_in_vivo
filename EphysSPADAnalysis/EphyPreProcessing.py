# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:11:42 2023

@author: Yifang
"""
import os
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pylab as plt
import pynapple as nap
import pynacollada as pyna
from scipy.signal import filtfilt
import OpenEphysTools as OE
from OESPADsingleTraceClass import OESPADsingleTrace
import seaborn as sns
'''
For animal 1673372_OEC, only LFP2 (channel 9 is working)
'''

#directory = "G:/SPAD/SPADData/20230424_Ephys_sleep_ASAPpyPhoto/2023-04-24_18-04-55_9819_sleep2"
directory = "G:/SPAD/SPADData/20230722_SPADOE/OE/2023-07-22_17-12-06" #Indeed noisy
dpath="G:/SPAD/SPADData/20230722_SPADOE/SyncRecording1/"
#directory = "E:/SPAD/SPADData/20230409_OEC_Ephys/2023-04-05_15-25-32_9819"
frequency=30000
#%%
'''
This part is for finding the SPAD recording mask, camera recording masks, and to read animal tracking data (.csv).
The final output should be a pandas format EphysData with data recorded by open ephys, a SPAD_mask,and a synchronised behavior state data. 
'''
EphysData=OE.readEphysChannel (directory, recordingNum=2)
#%%
fig, ax = plt.subplots(figsize=(15,5))
ax.plot(EphysData['SPADSync'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#%%
SPAD_mask = OE.SPAD_sync_mask (EphysData['SPADSync'], start_lim=3000000, end_lim=6500000)
#%%
EphysData['SPAD_mask'] = SPAD_mask
#%%
OE.save_open_ephys_data (dpath,EphysData)
#%%
fig, ax = plt.subplots(figsize=(15,5))
ax.plot(EphysData['CamSync'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#%%
'This is the LFP data that need to be saved for the sync ananlysis'
LFP_data=EphysData['LFP_2']
timestamps=EphysData['timestamps'].copy()
timestamps=timestamps.to_numpy()
timestamps=timestamps-timestamps[0]

'To plot the LFP data using the pynapple method'
LFP=nap.Tsd(t = timestamps, d = LFP_data.to_numpy(), time_units = 's')
fig, ax = plt.subplots(figsize=(15,5))
ax.plot(LFP.as_units('s'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel("Time (s)")

#%%
LFP_lowpass= OE.butter_filter(LFP, btype='low', cutoff=300, fs=frequency, order=5)
LFP_lowpass=nap.Tsd(t = timestamps, d = LFP_lowpass, time_units = 's')
#%%
'''This is to set the short interval you want to look at '''
ex_ep = nap.IntervalSet(start = 17, end = 18, time_units = 's') 

fig, ax = plt.subplots(figsize=(15,5))
ax.plot(LFP.restrict(ex_ep).as_units('s'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel("Time (s)")
plt.show()
#%%
lfp_filtered,nSS,nSS3 = OE.getRippleEvents (LFP,frequency,windowlen=1000,Low_thres=1,High_thres=5)
#%% detect theta wave
lfp_theta = OE.band_pass_filter(LFP,4,15,frequency)
lfp_theta=nap.Tsd(t = timestamps, d = lfp_theta, time_units = 's')

plt.figure(figsize=(15,5))
plt.plot(lfp_theta.restrict(ex_ep).as_units('s'))
plt.xlabel("Time (s)")
plt.show()
#%%
OE.plotRippleSpectrogram (LFP, lfp_filtered,ex_ep,nSS,nSS3,Low_thres=1,y_lim=300,Fs=30000)

#%%
windowLength = 1000
squared_signal = np.square(signal.values)
window = np.ones(windowLength)/windowLength
nSS = filtfilt(window, 1, squared_signal)
nSS = (nSS - np.mean(nSS))/np.std(nSS)
nSS = nap.Tsd(t = signal.index.values, d = nSS, time_support = signal.time_support)
# Round1 : Detecting Ripple Periods by thresholding normalized signal
low_thres = 1
high_thres = 10

nSS2 = nSS.threshold(low_thres, method='above')
nSS3 = nSS2.threshold(high_thres, method='below')

# Round 2 : Excluding ripples whose length < minRipLen and greater than Maximum Ripple Length
minRipLen = 20 # ms
maxRipLen = 200 # ms

rip_ep = nSS3.time_support
rip_ep = rip_ep.drop_short_intervals(minRipLen, time_units = 'ms')
rip_ep = rip_ep.drop_long_intervals(maxRipLen, time_units = 'ms')

# Round 3 : Merging ripples if inter-ripple period is too short
minInterRippleInterval = 20 # ms


rip_ep = rip_ep.merge_close_intervals(minInterRippleInterval, time_units = 'ms')
rip_ep = rip_ep.reset_index(drop=True)

# Extracting Ripple peak
rip_max = []
rip_tsd = []
for s, e in rip_ep.values:
    tmp = nSS.loc[s:e]
    rip_tsd.append(tmp.idxmax())
    rip_max.append(tmp.max())

rip_max = np.array(rip_max)
rip_tsd = np.array(rip_tsd)

rip_tsd = nap.Tsd(t = rip_tsd, d = rip_max)
#%%