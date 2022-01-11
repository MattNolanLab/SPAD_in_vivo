# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 22:44:24 2021

@author: s2073467
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
#%%
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
dpath= "G:/SPAD/SPADData"

mat_2 =  scipy.io.loadmat(os.path.join(dpath, "trace_ref1.mat"))
mat_3 =  scipy.io.loadmat(os.path.join(dpath, "trace_ref2.mat"))

con_1 = mat_2['trace_ref'][:,0]
con_2 = mat_3['trace_ref'][:,0]

#%%
trace_raw=con_1
trace_smooth=get_smoothed_trace (trace_raw, lowpass_cutoff=2000,bin_window=5)
#%%
'''Original Pipeline  with spike shape template to get spkie'''
spike_data=ROI.get_spikes(trace_smooth, superfactor=10, threshs=(.80,0.95,1.0))
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
plot_trace(spikesizes, name='spikesizes')
plot_trace(spiketrain, name='spiketrain')
plot_trace(upsampled_kernel, name='upsampled_kernel')
plot_trace(super_kernel, name='super_kernel')
#%% plot spike shapes on kernel
ax=plot_trace(kernel, name='spikes',color='k',zorder=2,linewidth=3)
pdTrace=get_pdTrace(trace_smooth,high_freq,spiketrain)
ax=plot_spike_trace(pdTrace,spiketimes,ax,window_frame=len(kernel)-1)
#%%
trace_sub,spiketime_sub=get_subset(pdTrace,60000,80000)
plotSpikeOnTrace(trace_sub.high_freq,spiketime_sub)
plotSpikeOnTrace(trace_sub.trace,spiketime_sub)

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
'''Use airPLS baseline correction'''
# baseline=airPLS(trace_reverse)
# trace_removebs=trace_reverse-baseline

# plot_trace(baseline)
# plot_trace(trace_removebs)

# sub_thresh1=baseline
# high_freq=trace_removebs
#%% Get subthreshold part and high freq part
'''USE Voltron paper, lowpass filter as subthreshold'''
sub_thresh1=trace_smooth
sub_thresh2=ROI.butter_filter(sub_thresh1,'low',cutoff=10)
high_freq = sub_thresh1 - sub_thresh2  # high frequency part: spikes and noise
plot_trace(high_freq)
plot_trace(sub_thresh2)


#%%
high_freq_med = np.array(pd.Series(high_freq).rolling(window=200,min_periods=200,center=True).mean())
high_freq_std = np.array(pd.Series(high_freq).rolling(window=200,min_periods=200,center=True).std())
trace_med = np.array(pd.Series(sub_thresh1).rolling(window=200,min_periods=200,center=True).mean())
trace_std = np.array(pd.Series(sub_thresh1).rolling(window=200,min_periods=200,center=True).std())

plot_trace(high_freq_med)
plot_trace(trace_med)

#%%
'''try df/f,not as good as 3std'''
#dfonf_thre=-5
#spiketimes = ROI.get_spiketimes_yy(high_freq_filt, high_freq_med,dfonf_thre,tlimit) 
thre=3
tlimit=len(sub_thresh1)
spiketimes = ROI.get_spiketimes(high_freq, high_freq_med + thre * high_freq_std,sub_thresh1, trace_med+thre*trace_std,tlimit)


#%%
