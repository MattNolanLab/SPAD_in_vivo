# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:52:17 2021
This is for testing Jinghua's GCamp data
@author: s2073467
"""

import os
import scipy.io 
import matplotlib.pyplot as plt
import scipy.signal
import voltron_ROI as ROI
from scipy.ndimage.morphology import binary_dilation, binary_fill_holes
import pandas as pd
import numpy as np
from scipy import stats
from scipy.interpolate import interp1d
import sys
from scipy.sparse.linalg import lsqr
from scipy.stats import ttest_1samp
from  airPLS import airPLS

def plot_trace(trace, name='signal'):    
    fig = plt.figure(figsize=[20,4])
    plt.plot(trace,'r-',linewidth=1)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return fig

dpath= "G:/JY"

df =  pd.read_csv(os.path.join(dpath, "longtime.csv"))

transient=df.Signal-df.Control
plot_trace(transient)
#%%
#trace=transient[350000:351000]
trace=transient[400300:401500]
plot_trace(trace)
trace_np=np.array(trace)

trace_high=ROI.butter_filter(trace, btype='high', cutoff=2, fs=130, order=5)
plot_trace(trace_high)


#%%
spike_data=ROI.get_spikes(trace_np, superfactor=10)
sub_thresh2=spike_data[0]
high_freq=spike_data[1]
spiketimes=spike_data[2]
spiketrain=spike_data[3]
spikesizes=spike_data[4]
super_times, super_sizes, super_times2, super_sizes2 =spike_data[5:9]
kernel, upsampled_kernel, super_kernel,best_tlimit,best_thre=spike_data[9:14]

plot_trace(kernel, name='kernel')
plot_trace(spikesizes, name='spikesizes')
plot_trace(spiketrain, name='spiketrain')
plot_trace(upsampled_kernel, name='upsampled_kernel')
plot_trace(super_kernel, name='super_kernel')
#%%
#plot_trace(trace_high)

trace_theta=ROI.butter_filter(trace_high, btype='low', cutoff=7, fs=130, order=5)

plot_trace(trace_theta,'theta')

trace_gamma=ROI.butter_filter(trace_high, btype='low', cutoff=60, fs=130, order=5)
trace_gamma=ROI.butter_filter(trace_high, btype='high', cutoff=30, fs=130, order=5)
plot_trace(trace_gamma,'gamma')