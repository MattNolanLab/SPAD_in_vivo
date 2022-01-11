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
def plot_trace(trace, name='signal'):    
    fig = plt.figure(figsize=[20,8])
    plt.plot(trace,'r-',linewidth=1)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return fig

def plotSpikeOnTrace(trace, spiketimes,name='signal'):
    fig = plt.figure(figsize=[20,8])
    plt.plot(trace,'c-',linewidth=1,zorder=1)
    plt.scatter(spiketimes,trace[spiketimes],
                                 s=30,c='k',marker='o',zorder=2)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return fig

def get_subset(traceSpike,low_idx,high_idx):
    traceSpike_sub=traceSpike[low_idx:high_idx]
    spiketime_sub=traceSpike_sub.index[traceSpike_sub['spiketrain'] == 1]
    return traceSpike_sub,spiketime_sub
#%%
dpath= "G:/SPAD/SPADData"

mat_2 =  scipy.io.loadmat(os.path.join(dpath, "trace_ref1.mat"))
mat_3 =  scipy.io.loadmat(os.path.join(dpath, "trace_ref2.mat"))

con_1 = mat_2['trace_ref'][:,0]
con_2 = mat_3['trace_ref'][:,0]

#%%
plot_trace(con_1)
con_1=con_1.astype(np.float64)          
trace_reverse=-con_1
trace1=ROI.butter_filter(trace_reverse,'low',cutoff=4000) #filter the 4KHz noise
trace = np.array(pd.Series(trace1).rolling(window=5,min_periods=5,center=True).mean())
#trace=ROI.butter_filter(trace,'low',cutoff=800)
plot_trace(trace_reverse)
plot_trace(trace1)
plot_trace(trace)
#%%
'''Original Pipeline  with spike shape template to get spkie'''
# spike_data=ROI.get_spikes(trace, superfactor=10, threshs=(.4, .6, .75))
# spiketimes=spike_data[2]
# spiketrain=spike_data[3]
# high_freq=spike_data[1]
# sub_thresh2=spike_data[0]

# plotSpikeOnTrace(trace,spiketimes)
# plotSpikeOnTrace(high_freq,spiketimes)
# plot_trace(high_freq)
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
sub_thresh1=trace[2:99997]
sub_thresh2=ROI.butter_filter(sub_thresh1,'low',cutoff=10)
high_freq = sub_thresh1 - sub_thresh2  # high frequency part: spikes and noise
plot_trace(high_freq)
plot_trace(sub_thresh2)
#%%
'''Original Pipeline  with spike shape template to get spkie'''
spike_data=ROI.get_spikes(sub_thresh1, superfactor=10, threshs=(.4, .6, .75))
spiketimes=spike_data[2]
spiketrain=spike_data[3]
high_freq=spike_data[1]
sub_thresh2=spike_data[0]

plotSpikeOnTrace(sub_thresh1,spiketimes)
plotSpikeOnTrace(high_freq,spiketimes)
plot_trace(high_freq)

#%%
high_freq_med = np.array(pd.Series(high_freq).rolling(window=200,min_periods=100,center=True).median())
high_freq_std = np.array(pd.Series(high_freq).rolling(window=200,min_periods=100,center=True).std())
trace_med = np.array(pd.Series(sub_thresh1).rolling(window=200,min_periods=100,center=True).median())
trace_std = np.array(pd.Series(sub_thresh1).rolling(window=200,min_periods=100,center=True).std())

plot_trace(high_freq_med)
plot_trace(trace_med)

#%%
'''try df/f,not as good as 3std'''
#dfonf_thre=-5
#spiketimes = ROI.get_spiketimes_yy(high_freq_filt, high_freq_med,dfonf_thre,tlimit) 
thre=3.2
tlimit=len(sub_thresh1)
spiketimes = ROI.get_spiketimes(high_freq, high_freq_med + thre * high_freq_std,sub_thresh1, trace_med+thre*trace_std,tlimit)

#%%
plotSpikeOnTrace(sub_thresh1,spiketimes)
plotSpikeOnTrace(high_freq,spiketimes)
#%% To pd.DataFrame
spiketrain=np.zeros (99995)
spiketrain[spiketimes]=1
data=np.array([sub_thresh1,high_freq,spiketrain]).T
traceSpike = pd.DataFrame(data,columns=['trace', 'high_freq', 'spiketrain'])
#%%
trace_sub,spiketime_sub=get_subset(traceSpike,70000,80000)
plotSpikeOnTrace(trace_sub.high_freq,spiketime_sub)
plotSpikeOnTrace(trace_sub.trace,spiketime_sub)


#%%
'''Can be used'''
#spiketimes = ROI.get_spiketimes(high_freq_filt, high_freq_med + thre * high_freq_std,trace_filt, trace_med+thre*trace_std,tlimit)

regressor=np.hstack((np.array([[1],[1],[1]]),np.array([[-1],[-0],[1]])))
inverse_matrix=np.dot(np.linalg.inv(np.dot(regressor.T,regressor)),regressor.T)
## adapt threshold for each neurons based on spike shape integrity

threshold_sets=(2,2.5,3);
th_scores=np.ones((len(threshold_sets),))
th_tlimits=np.zeros((len(threshold_sets),))

for th in range(len(threshold_sets)):
    
    tlimit=len(trace)

    thre=threshold_sets[th]
    
    ## check validity of spike kernel by detecting pre-spike ramp 
    ## if the shape of first 50 spikes are suspicious, it will return an empty array 
    ## this will stop erroneous detection of noise after there is no spike anymore
    
    def test_spikeshape(time,tcourse,tcourse_med,tcourse_std,regress_matrix):
        
        
        time=time[(time-4)>=0]
        
        spike_matrix=np.zeros((len(time),3))
        for t in range(3):
            spike_matrix[:,t]=tcourse[time-3+t]
        
        spike_matrix -= spike_matrix.mean(axis=1)[:,None]
        
        gradient=np.dot(regress_matrix,spike_matrix.T)[1,:]
        
        s,p = ttest_1samp(gradient,0)
        
        return (s,p)
        
    
    spiketimes = ROI.get_spiketimes(high_freq, high_freq_med + thre * high_freq_std,trace, trace_med+thre*trace_std,tlimit)
    
    spikebins=50
    spikenrep=(len(spiketimes)//spikebins)+int((len(spiketimes)%spikebins)>0)
    
    tlimit=0
    for n in range(spikenrep):
        spike_inds=np.arange(spikebins*n,min(spikebins*(n+1),len(spiketimes)))
        slen=len(spike_inds)
        spike_t=spiketimes[spike_inds]
    
        (s,p) = test_spikeshape(spike_t,trace,trace_med,trace_std, inverse_matrix)
        if n==0:
            th_scores[th]=p
        
        if (p<0.05) and (s>0):
                
            tlimit=min(spike_t[-1]+15,len(trace))
                
        elif n>0:
            for j in range(slen):
                endt=min(spikebins*(n+1),len(spiketimes))-j
                spike_inds=np.arange((endt-50),endt)
                spike_t=spiketimes[spike_inds]
    
                (s,p) = test_spikeshape(spike_t,trace,trace_med,trace_std , inverse_matrix)
        
                if (p<0.05) and (s>0):
                    tlimit=min(spike_t[-1]+15,len(trace))
                    break
            
            break
        
        else:
            th_scores[th]=1
            break
    
    th_tlimits[th]=tlimit


#%%    
best_inds=np.where(th_scores<0.05)[0]
if best_inds.size>0:
    best_thre=threshold_sets[best_inds[0]]
    best_tlimit=int(th_tlimits[best_inds[0]])
else:
    best_thre=threshold_sets[0]
    best_tlimit=0
    
    

if best_tlimit==0:
    spiketimes = np.zeros((0,))


spiketimes = ROI.get_spiketimes(high_freq, high_freq_med + best_thre * high_freq_std,trace, trace_med+best_thre*trace_std,best_tlimit)

    
kernel = ROI.get_kernel(high_freq, spiketimes)

# lower threshold, now picking up spikes not merely based on threshold but spike shape


