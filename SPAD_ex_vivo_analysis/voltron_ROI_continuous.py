# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 23:18:03 2021

@author: s2073467
"""

# -*- coding: utf-8 -*-


from scipy.ndimage.morphology import binary_dilation, binary_fill_holes
import pandas as pd
import numpy as np
from scipy import stats
from scipy.interpolate import interp1d
import scipy.signal
import matplotlib.pyplot as plt
import sys
from scipy.sparse.linalg import lsqr
from scipy.stats import ttest_1samp



def butter_filter(data, btype='low', cutoff=0.1, fs=10000, order=5):
#def butter_filter(data, btype='high', cutoff=3, fs=130, order=5):
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    # cutoff and fs in Hz
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype=btype, analog=False)
    y = scipy.signal.filtfilt(b, a, data, axis=0)
    return y


def get_spiketimes(trace1, thresh1,trace2,thresh2,tlimit):
    
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    '''determine spike times based on threshold'''
    times = np.where((trace1[:tlimit] > thresh1[:tlimit]) & (trace2[:tlimit] > thresh2[:tlimit]))[0]
        
    # group neigbours together
    if (times.size>0):
        ls = [[times[0]]]
        for t in times[1:]:
            if t == ls[-1][-1] + 1:
                ls[-1].append(t)
            else:
                ls.append([t])
        # take local maximum if neighbors are above threshold
        times = np.array([l[np.argmax(trace1[l])] for l in ls])
    return times

def get_spiketimes_yy(trace1, backgroundf,dfonfthre,tlimit):
    
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    '''determine spike times based on threshold'''
    times = np.where(((trace1[:tlimit]-backgroundf[:tlimit])/backgroundf[:tlimit]) < dfonfthre)[0]
        
    # group neigbours together
    if (times.size>0):
        ls = [[times[0]]]
        for t in times[1:]:
            if t == ls[-1][-1] + 1:
                ls[-1].append(t)
            else:
                ls.append([t])
        # take local maximum if neighbors are above threshold
        times = np.array([l[np.argmax(trace1[l])] for l in ls])
    return times

def get_kernel(trace, spiketimes, spikesizes=None, tau=601, superfactor=1, b=False):
    '''tau was 31 and I dont know why'''
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    '''determine kernel via regression
    resolution of spike times must be some integer divided by superfactor
    '''
    th = tau // 2
    t = len(trace)
    s = np.zeros((superfactor, t + th))
    for k in range(superfactor):
        tmp = (spiketimes * superfactor + k) % superfactor == 0
        s[k, (spiketimes[tmp] + k / float(superfactor)).astype(int)
          ] = 1 if spikesizes is None else spikesizes[tmp]
    ss = np.zeros((tau * superfactor, t + th))
    for i in range(tau):
        ss[i * superfactor:(i + 1) * superfactor, i:] = s[:, :t + th - i]
    ssm = ss - ss.mean() if b else ss
    
    
    symm=ssm.dot(ssm.T)
    
    if np.linalg.cond(symm) < 1/sys.float_info.epsilon:
        invm=np.linalg.inv(symm)
    else:
        noise=np.random.rand(symm.shape[0],symm.shape[1])/10000
        symm+=noise
        invm=np.linalg.inv(symm)
    
    
    return invm.dot(ssm.dot(np.hstack([np.zeros(th), trace])))


def get_spikesizes(trace, spiketimes, kernel):
    
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    '''determine spike sizes via regression'''
    tau = len(kernel)
    th = tau // 2
        
    trace=trace.astype(np.float32)
        
    ans=np.zeros((len(spiketimes),)).astype(np.float32)
    
    spikebin=200
    binnum=int(len(spiketimes)/spikebin)+1
    
    for i in range(binnum):
        binsize=min(len(spiketimes)-(spikebin*i),spikebin)
        spike_range=np.arange((spikebin*i),(spikebin*i+binsize)).astype(int)
        if binsize>0:
        
            
            spike_min = spiketimes[spike_range[0]]
            spike_max = spiketimes[spike_range[-1]]
            if spike_min>th:
                trace_pre=trace[spike_min-th:spike_min]
            else:
                trace_pre=np.zeros(th)    
                
            if spike_max<(len(trace)-(tau - th)):
                trace_post=trace[spike_max:spike_max+tau - th]
            else:
                trace_post=np.zeros(tau-th)
            
            
            trace_tmp=trace[spike_min:spike_max]
            
            tmp = np.zeros((binsize, len(trace_tmp)+ tau) , dtype=np.float32)
            for j, t in enumerate(spiketimes[spike_range]-spike_min):
                tmp[j, t:t + tau] = kernel.astype(np.float32)
            
            
            ans[spike_range]=lsqr(tmp.T, np.hstack([trace_pre, trace_tmp, trace_post]))[0]
    
    
    return ans


def get_spiketrain(spiketimes, spikesizes, T):
    
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    s = np.zeros(T)
    s[spiketimes] = spikesizes
    return s


def upsample_kernel(kernel, superfactor=10, interpolation='linear'):
    
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    tau = len(kernel)
    k = interp1d(range(len(kernel)), kernel, kind=interpolation,
                 assume_sorted=True, fill_value='extrapolate')
    return k(np.arange(-1, tau + 1, 1. / superfactor))


# upsampled_k[grid-delta] is kernel for spike at time t+delta/superfactor instead t
def superresolve(high_freq, spiketimes, spikesizes, upsampled_k, superfactor=10):
    
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia
    
    tau = int(len(upsampled_k) / superfactor - 2)
    th = int(tau // 2)
    grid = superfactor * np.arange(1, tau + 1).astype(int)
    kk = [upsampled_k[grid - delta].dot(upsampled_k[grid - delta])
          for delta in range(1 - superfactor, superfactor)]  # precompute
    N = len(spiketimes)
    super_times = np.zeros(N)
    super_sizes = np.zeros(N)
    for i in range(N):
        t = spiketimes[i]
        int_t = int(t + .5)
        snippet = high_freq[max(0, int_t - th):int_t + tau - th].copy()
        if t < th:  # very early spike -> shortened snippet
            snippet = np.concatenate((np.zeros(th - int_t), snippet))
        elif t + tau - th > len(high_freq):  # very late spike -> shortened snippet
            zeropad = tau - len(snippet)
            snippet = np.concatenate((snippet, np.zeros(zeropad)))
        # remove contributions of other spikes to the snippet
        if i:
            tpre = spiketimes[i - 1]
            int_tpre = int(tpre + .5)
            if (tpre > t - tau) and ((int_t-int_tpre)>0):
                delta = int(superfactor * ((tpre - int_tpre) - (t - int_t)))
                snippet[:int_tpre - int_t] -= spikesizes[i - 1] * \
                    upsampled_k[grid - delta][int_t - int_tpre:]
        if i < N - 1:
            tpost = spiketimes[i + 1]
            int_tpost = int(tpost + .5)
            if (tpost < t + tau) and ((int_tpost-int_t)>0):
                delta = int(superfactor * ((tpost - int_tpost) - (t - int_t)))
                snippet[int_tpost - int_t:] -= spikesizes[i + 1] * \
                    upsampled_k[grid - delta][:int_t - int_tpost]
        # find best spike time and size
        ls = []
        for delta in range(1 - superfactor, superfactor):
            q = (snippet - upsampled_k[grid - delta] *
                 (upsampled_k[grid - delta].dot(snippet) / kk[delta + superfactor - 1]))
            if t < th:  # very early spike -> shortened snippet
                q = q[th - int_t:]
            elif t + tau - th > len(high_freq):  # very late spike -> shortened snippet
                q = q[:-zeropad]
            ls.append(q.dot(q))
        delta = np.argmin(ls) - superfactor + 1
        super_times[i] = t + delta / float(superfactor)
        super_sizes[i] = (upsampled_k[grid - delta].dot(snippet) / kk[delta + superfactor - 1])

    return super_times, super_sizes



def get_spikes_old (trace, superfactor=10, threshs=(.4, .6, .75),window=5000,threshold_sets=(2.5,3.,3.5),cutoff=10):
    
    # Originally written by Johannes Friedrich @ Flatiron Institute
    # Modified by Takashi Kawashima @ HHMI Janelia   
    # calculate beforehand the matrix for calculating pre-spike ramp gradients    
    regressor=np.hstack((np.array([[1],[1],[1]]),np.array([[-1],[-0],[1]])))
    inverse_matrix=np.dot(np.linalg.inv(np.dot(regressor.T,regressor)),regressor.T)       
    for iters in range(3):
        sub_thresh1 = trace if iters == 0 else (trace-np.convolve(spiketrain, kernel, 'same')) # subtract subthre
        sub_thresh2 = butter_filter(sub_thresh1, 'low', cutoff=cutoff )  # filter subthreshold part
        high_freq = trace - sub_thresh2  # high frequency part: spikes and noise
        
        high_freq_med = np.array(pd.Series(high_freq).rolling(window=window,min_periods=window,center=True).median())
        high_freq_std = np.array(pd.Series(high_freq).rolling(window=window,min_periods=window,center=True).std())       
        trace_med = np.array(pd.Series(sub_thresh1).rolling(window=window,min_periods=window,center=True).median())
        trace_std = np.array(pd.Series(sub_thresh1).rolling(window=window,min_periods=window,center=True).std())
        
        if iters == 0:            
            ## adapt threshold for each neurons based on spike shape integrity   
            threshold_sets=threshold_sets;
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
                                    
                spiketimes = get_spiketimes(high_freq, high_freq_med + thre * high_freq_std,trace, trace_med+thre*trace_std,tlimit)                
                spikebins=50 #Detected APs were binned into contiguous blocks of 50 APs.
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
            best_inds=np.where(th_scores<0.05)[0]

            if best_inds.size>0:
                best_thre=threshold_sets[best_inds[0]]
                best_tlimit=int(th_tlimits[best_inds[0]])
            else:
                best_thre=threshold_sets[0]
                best_tlimit=0
                            
            if best_tlimit==0:
                spiketimes = np.zeros((0,))
                break;            
            spiketimes = get_spiketimes(high_freq, high_freq_med + best_thre * high_freq_std,trace, trace_med+best_thre*trace_std,best_tlimit)                                       
        if spiketimes.size==0:
            break;
            
        kernel = get_kernel(high_freq, spiketimes)
        
        # lower threshold, now picking up spikes not merely based on threshold but spike shape        
        spiketimes = get_spiketimes(high_freq, high_freq_med + (best_thre-0.2) * high_freq_std,trace, trace_med+(best_thre-0.5)*trace_std,best_tlimit)
        spikesizes = get_spikesizes(high_freq, spiketimes, kernel)
        spiketrain = get_spiketrain(spiketimes, spikesizes, len(trace))        
        # iteratively remove too small spikes 'slowly' increasing threshold
        for thresh in threshs:
            while np.sum(spikesizes < thresh):
                spiketimes = np.where(spiketrain > thresh)[0]
                spikesizes = get_spikesizes(high_freq, spiketimes, kernel)
                spiketrain = get_spiketrain(spiketimes, spikesizes, len(trace))
    ##End of for loop
    
    if spiketimes.size>0:
          # refine frame_rate result to obtain super-resolution
        upsampled_kernel = upsample_kernel(kernel, superfactor=superfactor, interpolation='linear')
        super_times, super_sizes = superresolve(
            high_freq, spiketimes, spikesizes, upsampled_kernel, superfactor)
        # (maybe) TODO: refine spike sizes by linear regression
        super_kernel = get_kernel(high_freq, super_times, spikesizes=super_sizes,
                                  tau=len(kernel) + 2, superfactor=superfactor)
        super_times2, super_sizes2 = superresolve(
            high_freq, super_times, super_sizes, super_kernel, superfactor)
        
        
        return (sub_thresh2, high_freq, spiketimes, spiketrain, spikesizes, super_times, super_sizes,
                super_times2, super_sizes2, kernel, upsampled_kernel, super_kernel,best_tlimit,best_thre)
    else:
        return (sub_thresh2, high_freq, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0)
            
