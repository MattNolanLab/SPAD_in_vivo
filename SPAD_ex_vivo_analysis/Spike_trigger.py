# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 17:56:41 2021

@author: s2073467
"""
import os
import scipy.io 
import matplotlib.pyplot as plt
import scipy.signal
import voltron_ROI as ROI
import pandas as pd
import numpy as np

from  airPLS import airPLS
#%% Load triggered mode data
'''triggered: lowpass cutoff:2000Hz, fOR 4KHznoise
rolling window 250, bigger rolling window, more false positive, smaller window will loss spikes
thre: 3std'''

dpath= "G:/SPAD/SPADData"
mat_1 =  scipy.io.loadmat(os.path.join(dpath, "trace_ref.mat"))
trace_raw = mat_1['trace_ref'][:,0]

#%% Defined functions

def get_smoothed_trace (trace_raw, lowpass_cutoff=2000,bin_window=5):
    '''Basic filter and smooth'''
    trace_raw=trace_raw.astype(np.float64)
    plot_trace(trace_raw, name='raw_trace')  
    '''reverse the trace (voltron is reversed)''' 
    trace_reverse=np.negative(trace_raw)
    plot_trace(trace_reverse, name='raw_trace_reverse') 
    '''2000Hz low pass filter'''
    trace_filtered=ROI.butter_filter(trace_reverse,'low',cutoff=lowpass_cutoff)
    plot_trace(trace_filtered, name='trace_2kHz filtered')
    '''5 frames as a rolling window to bin the data'''
    trace_binned = pd.Series(trace_filtered).rolling(window=bin_window,min_periods=bin_window,center=True).mean()
    trace_binned.fillna(method="bfill",inplace=True)
    trace_binned.fillna(method="ffill",inplace=True)
    trace_smooth = np.array(trace_binned)
    plot_trace(trace_smooth, name='trace_smooth')
    return trace_smooth

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
    fig = plt.figure(figsize=[20,8])
    plt.plot(trace,'c-',linewidth=1,zorder=1)
    plt.scatter(spiketimes,trace[spiketimes],
                                 s=30,c='k',marker='o',zorder=2)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return fig

def get_pdTrace(trace_smooth,high_freq,spiketrain):
    data=np.array([trace_smooth,high_freq,spiketrain]).T
    traceSpike_pd = pd.DataFrame(data,columns=['trace', 'high_freq', 'spiketrain'])
    return traceSpike_pd

def get_subset(traceSpike_pd,low_idx,high_idx):
    traceSpike_sub=traceSpike_pd[low_idx:high_idx]
    spiketime_sub=traceSpike_sub.index[traceSpike_sub['spiketrain']!=0]
    return traceSpike_sub,spiketime_sub
    
def plot_spike_trace(pdTrace,spiketimes,ax,window_frame=600):
    for i in range(len(spiketimes)):
        trace_sub,_=get_subset(pdTrace,int(spiketimes[i]-window_frame/2),
                                            int(spiketimes[i]+window_frame/2))
        ax=plot_trace(np.array(trace_sub.high_freq),name='spikes',ax=ax,color='c')
    return ax

def get_spike_mean(pdTrace,spiketimes,ax,window_frame=600):
    spike_mean=np.zeros(window_frame)
    spike_sum=np.zeros(window_frame)
    for i in range(len(spiketimes)):
        trace_sub,_=get_subset(pdTrace,int(spiketimes[i]-window_frame/2),
                                            int(spiketimes[i]+window_frame/2))
        spike_i=np.array(trace_sub.high_freq)
        spike_sum=spike_i+spike_sum
    spike_mean=spike_sum/len(spiketimes)    
    return spike_mean
#%%
'''Use original function with spike shape template
unpack the result'''
trace_smooth=get_smoothed_trace (trace_raw)
spike_data=ROI.get_spikes(trace_smooth, superfactor=10, threshs=(.4, .6, .75))

sub_thresh2=spike_data[0]
high_freq=spike_data[1]
spiketimes=spike_data[2]
spiketrain=spike_data[3]
spikesizes=spike_data[4]
super_times, super_sizes, super_times2, super_sizes2 =spike_data[5:9]
kernel, upsampled_kernel, super_kernel,best_tlimit,best_thre=spike_data[9:14]
#%%
plotSpikeOnTrace(trace_smooth,spiketimes)
plotSpikeOnTrace(high_freq,spiketimes)
plot_trace(kernel, name='kernel')
#plot_trace(spikesizes, name='spikesizes')
plot_trace(spiketrain, name='spiketrain')
#%% plot traces on kernel

ax=plot_trace(kernel, name='kernel',color='k',zorder=2,linewidth=3)
pdTrace=get_pdTrace(trace_smooth,high_freq,spiketrain)
ax=plot_spike_trace(pdTrace,spiketimes,ax,window_frame=len(kernel)-1)


#%%
spike_mean=get_spike_mean(pdTrace,spiketimes,ax,window_frame=600)
ax1=plot_trace(spike_mean, name='spike_mean',color='k',zorder=2,linewidth=3)
pdTrace=get_pdTrace(trace_smooth,high_freq,spiketrain)
ax1=plot_spike_trace(pdTrace,spiketimes,ax1,window_frame=len(kernel)-1)

#%% exponential fit
from pylab import *
from math import log
import expfit

tList = arange(0.0,0.03,0.0001) # pick 10 ms after the spike
'''use Kernel to fit, can also use spike_mean data'''
#yList = kernel[301:] 
yList = spike_mean[300:] 
#yList=ROI.butter_filter(yTrace,'low',cutoff=500)  #cutoff=308 works for fitExponent
#trace_binned = pd.Series(trace_filtered).rolling(window=bin_window,min_periods=bin_window,center=True).mean()
'''linear fit'''
#(amplitudeEst,tauEst) = expfit.fitExponent(tList,yList,ySS=0)
#amplitudeEst,tauEst= expfit.fit_exp_linear(tList,yList,0)
'''nonlinear fit'''
amplitudeEst,K,yBaseline= expfit.fit_exp_nonlinear(tList,yList)
tauEst=-1/K

print ('Amplitude estimate = %f, tau estimate = %f'
    % (amplitudeEst,tauEst))
yEst = amplitudeEst*(exp(-tList/tauEst))+yBaseline
figure(1)
plot(tList,yList,'b')
#plot(tSamples,yMeasured,'+r',markersize=12,markeredgewidth=2)
plot(tList,yEst,'--g')
xlabel('seconds')
legend(['True value','Estimated value'])
grid(True)
show()
#%%

#%%
'''Df/F, need a for loop'''
F_base=np.mean(trace_smooth[100:1100])
dfonF_array=np.zeros(len(spiketimes))
for i in range(len(spiketimes)):
    spike_i=trace_smooth[spiketimes[i]]
    df_i=spike_i-F_base
    dfonF_i=-(df_i)/F_base   
    dfonF_array[i]=dfonF_i
plot_trace(dfonF_array, name='df/f')
average_dff=np.mean(dfonF_array)
'''
df/f values in percentage
6.95896
6.76306
7.6022
8.47525
7.71551
7.36897
7.37012
7.51645
7.84111
8.51643

'''
#%%
'''SNR'''
F_base_std=np.std(trace_smooth[100:1100])
SNR_array=np.zeros(len(spiketimes))
for i in range(len(spiketimes)):
    spike_i=trace_smooth[spiketimes[i]]
    df_i=spike_i-F_base
    snr_i=df_i/F_base_std
    SNR_array[i]=snr_i
plot_trace(SNR_array, name='SNR')
average_snr=np.mean(SNR_array)

''' SNR values
7.13128
6.93052
7.79044
8.68511
7.90656
7.55144
7.55262
7.70257
8.03527
8.72732

'''

#%%
'''spike time compare with ephys
SPAD frequency 9938.4'''


