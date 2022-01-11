# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:13:04 2021

@author: s2073467
Calculate and plot cross-correlation 
(1) Typical correlogram
(2) for spike trains, use PSTH method to compare spike times
(3) for subthreshold potential...
"""
import os
import scipy.io 
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator

def get_threshold (trace, window1=99400, window2=99900, std_thre=3.5):
    '''To get threshold from a continuous recording'''
    trace_reference=trace[window1:window2]
    mean=np.mean(trace_reference)
    std=np.std(trace_reference)
    thres=mean-std_thre*std
    return thres

def get_spiketrain(trace,thres):
    spiketrain=np.zeros(len(trace))
    for i in range(len(trace)):
        if trace[i]<thres:
            spiketrain[i]=1
    return spiketrain

def get_lowerdatapoint(trace,window=10):
    '''bin the time frames to get new spike train
    This should not be used'''
    spiketrain=np.zeros(int(len(trace)/window))
    for i in range (len(spiketrain)):
        sum=np.sum(trace[i*window:i*window+window-1])
        if sum>0:
            spiketrain[i]=1
    return spiketrain

def get_spiketrain_all(roi_spike, tracenum):
    '''get a concatenated spiketrain from all traces'''
    for i in range(tracenum):
        spike_i=np.array(roi_spike.iloc[:,i])
        thres_i=get_threshold(spike_i)
        spiketrain_i=get_spiketrain(spike_i,thres_i)
        if i==0:
            spiketrain=spiketrain_i
        else:
            spiketrain=np.concatenate((spiketrain, spiketrain_i), axis=0)
    return spiketrain
        
def plot_cross_correlation(spiketrain1,spiketrain2,maxlags=99999,title='ROI1-ROI2',linewidth=8,frametime=0.1006198181):
    '''This is to plot the typical correlogram'''
    fig = plt.figure(figsize=[20,15])
    (lags,corr,_,_) = plt.xcorr(spiketrain1, spiketrain2, normed=False,maxlags=maxlags,linewidth=linewidth)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('lags(ms)',fontsize=20)
    #plt.ylabel('cross correlation',fontsize=20)
    plt.ylabel('Overlap event count',fontsize=20)
    x = [-maxlags,-3/4*maxlags,-1/2*maxlags,-1/4*maxlags,0,1/4*maxlags,1/2*maxlags,3/4*maxlags,
        maxlags]
    frame=frametime*maxlags
    labels = [int(-frame),int(-3/4*frame),int(-1/2*frame),int(-1/4*frame),
              0, int(1/4*frame),int(1/2*frame),int(3/4*frame),int(frame)]
    plt.xticks(x, labels)
    plt.yticks(fontsize=20)
    plt.title(title, fontsize=20)
    return fig,lags,corr

def get_cross_correlation_all(roi_data1,roi_data2,tracenum):
    '''sum cross correlation from all trains'''
    corr_sum=np.zeros(199999)
    for i in range(tracenum):
        spike_i1=np.array(roi_data1.iloc[:,i])
        thres_i1=get_threshold(spike_i1)
        spiketrain_i1=get_spiketrain(spike_i1,thres_i1)
        spike_i2=np.array(roi_data2.iloc[:,i])
        thres_i2=get_threshold(spike_i2)
        spiketrain_i2=get_spiketrain(spike_i2,thres_i2)
        fig,lags_i,corr_i=plot_cross_correlation(spiketrain_i1,spiketrain_i2,maxlags=99999,title='ROI1-ROI2-trace'+str(i+1),linewidth=8)
        corr_sum=corr_sum+corr_i
        lag=lags_i
    return corr_sum,lag

def plot_bin_corr(corr,window=10,frametime=0.1006198181,linewith=12):
    '''get mean cross-corr with window size, maxlags unit is frame
    frametime is original frametime in ms. 
    This is to smooth the typical correlogram
    '''
    maxlags=(len(corr)+1)/2-1
    bin_corr_len=int((len(corr)+1)/window-1)
    corr_bin=np.zeros(bin_corr_len)
    for i in range (len(corr_bin)):
        mean=np.mean(corr[i*window:i*window+window-1])
        corr_bin[i]=mean
    lagframe=(bin_corr_len+1)/2-1
    lag_bin=np.arange(-lagframe,lagframe+1,1)
    fig = plt.figure(figsize=[20,15])
    plt.plot(lag_bin,corr_bin,linewidth=linewith)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('lags(ms)',fontsize=20)
    plt.ylabel('Overlap event count_sum',fontsize=20)
   # plt.ylabel('cross correlation',fontsize=20)
    plt.yticks(fontsize=20)
    #bin_frametime=frametime*window
    x = [-lagframe,-3/4*lagframe,-1/2*lagframe,-1/4*lagframe,0,
         1/4*lagframe,1/2*lagframe,3/4*lagframe,lagframe]
    time_ms=frametime*maxlags
    labels = [int(-time_ms),int(-3/4*time_ms),int(-1/2*time_ms),int(-1/4*time_ms),
              0, int(1/4*time_ms),int(1/2*time_ms),int(3/4*time_ms),int(time_ms)]    
    plt.xticks(x, labels)
    plt.axvline(x=0, color='k', linestyle='--')
    binsize=int(window*0.1) #binsize in ms
    lagsize=int(time_ms)  #lagsize in ms
    plt.title('corr_mean_bin'+str(binsize)+'ms_lag'+str(lagsize)+'ms', fontsize=20)  
    return fig,corr_bin,lag_bin

def plot_bin_corr_hist(corr,window=10,frametime=0.1006198181,linewith=1):
    '''get mean cross-corr with window size
    maxlags unit is frame
    frametime is original frametime in ms'''
    maxlags=(len(corr)+1)/2-1
    bin_corr_len=int((len(corr)+1)/window-1)
    corr_bin=np.zeros(bin_corr_len)
    for i in range (len(corr_bin)):
        sum=np.sum(corr[i*window:i*window+window-1])
        corr_bin[i]=sum
    lagframe=(bin_corr_len+1)/2-1
    lag_bin=np.arange(-lagframe,lagframe+1,1)
    fig = plt.figure(figsize=[20,15])
    '''This is using bar plot not hist, should use hist by changing the weight'''
    plt.bar(lag_bin,corr_bin,width=1,linewidth=linewith) 
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('lags(ms)',fontsize=20)
    plt.ylabel('Overlap event count_sum',fontsize=20)
    plt.yticks(fontsize=20)
    #bin_frametime=frametime*window
    x = [-lagframe,-3/4*lagframe,-1/2*lagframe,-1/4*lagframe,0,
         1/4*lagframe,1/2*lagframe,3/4*lagframe,lagframe]
    time_ms=frametime*maxlags
    labels = [int(-time_ms),int(-3/4*time_ms),int(-1/2*time_ms),int(-1/4*time_ms),
              0, int(1/4*time_ms),int(1/2*time_ms),int(3/4*time_ms),int(time_ms)]    
    plt.xticks(x, labels)
    plt.axvline(x=0, color='k', linestyle='--')
    binsize=int(window*0.1) #binsize in ms
    lagsize=int(time_ms)  #lagsize in ms
    plt.title('corr_mean_bin'+str(binsize)+'ms_lag'+str(lagsize)+'ms', fontsize=20)  
    return fig,corr_bin,lag_bin

def get_lagframe(lagtime,frametime=0.1006198181):
    'lag time in ms'
    maxlag_frame=int(lagtime/frametime)
    return maxlag_frame

def plot_correlogram (spike1,spike2,spath,lagtime=None,title='ROI1_2'):
    '''This is to plot the correlogram with different format in a single function'''
    thres1=get_threshold(spike1)
    thres2=get_threshold(spike2)
    spiketrain1=get_spiketrain(spike1,thres1)
    spiketrain2=get_spiketrain(spike2,thres2)    
    maxlags_default=len(spike1)-1
            
    if lagtime is None:
        maxlags=maxlags_default
    else:
        maxlags=get_lagframe(lagtime)

    fig0,lags0,corr0=plot_cross_correlation(spiketrain1,spiketrain2,maxlags=maxlags,linewidth=1,title='trace3_no_bin')
    figpath0 = os.path.join(spath,title+'_trace3_nobin_lag'+str(lagtime)+'.svg')
    fig0.savefig(figpath0, format='svg')
    
    fig1,corr_bin,maxlag_bin=plot_bin_corr_hist(corr0,window=100,linewith=1)
    figpath1 = os.path.join(spath,title+'_trace3_1msbin_lag'+str(lagtime)+'.svg')
    fig1.savefig(figpath1, format='svg')
    
    return

def get_spiketime(spiketrain):
    return np.where(spiketrain == 1)[0]

def plotSpikeOnTrace(trace, spiketimes,name='signal'):
    fig = plt.figure(figsize=[20,8])
    plt.plot(trace,'c-',linewidth=1,zorder=1)
    plt.scatter(spiketimes,trace[spiketimes],
                                 s=30,c='k',marker='o',zorder=2)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title(name, fontsize=20)
    return fig

def plot_PSTH_correlogram(spike1,spike2,binsize=2,HalfWindowSize=50,frametime=0.1006198181,title=''):
    '''
    binsize and window size in ms
    1. Take spiketrain1 as reference (or “a trigger”), for each spike in spiketrain1:
    2. make a time window [-1000ms,1000ms],
    3. count spike numbers in spiketrain2 within this window by 10ms bins,
    ----1 and 2 makes a histogram for each single spike in spiketrain1.
    4. Sum the “counts” for all spikes in spiketrain1
    '''    
    thres1=get_threshold(spike1)
    thres2=get_threshold(spike2)
    spiketrain1=get_spiketrain(spike1,thres1)
    spiketrain2=get_spiketrain(spike2,thres2)  
    # fig1 = plt.figure()
    # plt.plot(spiketrain1)
    # fig2 = plt.figure()
    # plt.plot(spiketrain2)
    
    spiketime1 = get_spiketime(spiketrain1)
    '''spike2 as reference'''
    spiketime2 = get_spiketime(spiketrain2) 
    
    plotSpikeOnTrace(spike1, spiketime1)
    plotSpikeOnTrace(spike2, spiketime2)
    
    bin_number=int(2*HalfWindowSize/(binsize))
    Totalcounts=[0] * bin_number
    half_windowSize_framenum=int(HalfWindowSize/frametime)
    for i in range(spiketime2.size - 1):
        tmpCounts, tmpEdges = np.histogram(spiketime1,
                                           bins = bin_number, 
                                           range = (spiketime2[i]-half_windowSize_framenum, 
                                                    spiketime2[i]+half_windowSize_framenum))
        Totalcounts = Totalcounts + tmpCounts
        
    Edges=np.arange(-bin_number/2,bin_number/2)
    fig = plt.figure()
    (n,bins,_)=plt.hist(Edges, bins=bin_number, weights=Totalcounts)
    
    x = [-bin_number/2,-3/8*bin_number,-1/4*bin_number,-1/8*bin_number,0,
         1/8*bin_number,1/4*bin_number,3/8*bin_number,bin_number/2]
    
    labels = [-HalfWindowSize,-3/4*HalfWindowSize,int(-1/2*HalfWindowSize),-1/4*HalfWindowSize,
              0, 1/4*HalfWindowSize,int(1/2*HalfWindowSize),3/4*HalfWindowSize,HalfWindowSize]    
    plt.xticks(x, labels)
    plt.axvline(x=0, color='k', linestyle='--')
    plt.xlabel('lags(unit:ms)',fontsize=10)
    plt.ylabel('spike count',fontsize=10)
    plt.title('correlogram '+title+str(binsize)+'ms bin',fontsize=10)
       
    return fig

def plot_PSTH_correlogram_spiketrain(spiketime1,spiketime2,ax,binsize=2,HalfWindowSize=50,
                                     frametime=0.1006198181,title='',):
    '''
    binsize and window size in ms
    1. Take spiketrain1 as reference (or “a trigger”), for each spike in spiketrain1:
    2. make a time window [-1000ms,1000ms],
    3. count spike numbers in spiketrain2 within this window by 10ms bins,
    ----1 and 2 makes a histogram for each single spike in spiketrain1.
    4. Sum the “counts” for all spikes in spiketrain1
    '''    
    # fig1 = plt.figure()
    # plt.plot(spiketrain1)
    # fig2 = plt.figure()
    # plt.plot(spiketrain2)
    # spiketime1 = get_spiketime(spiketrain1)
    # '''spike2 as reference'''
    # spiketime2 = get_spiketime(spiketrain2) 
    
    bin_number=int(2*HalfWindowSize/(binsize))
    Totalcounts=[0] * bin_number
    half_windowSize_framenum=int(HalfWindowSize/frametime)
    for i in range(spiketime2.size - 1):
        tmpCounts, tmpEdges = np.histogram(spiketime1,
                                           bins = bin_number, 
                                           range = (spiketime2[i]-half_windowSize_framenum, 
                                                    spiketime2[i]+half_windowSize_framenum))
        Totalcounts = Totalcounts + tmpCounts
        
    Edges=np.arange(-bin_number/2,bin_number/2)
    (n,bins,_)=ax.hist(Edges, bins=bin_number, weights=Totalcounts)
    
    x = [-bin_number/2,-3/8*bin_number,-1/4*bin_number,-1/8*bin_number,0,
         1/8*bin_number,1/4*bin_number,3/8*bin_number,bin_number/2]
    
    labels = [str(-HalfWindowSize),'',str(int(-1/2*HalfWindowSize)),'', str(0),'',
              str(int(1/2*HalfWindowSize)),'',str(HalfWindowSize)]
    # labels = [-HalfWindowSize,-3/4*HalfWindowSize,int(-1/2*HalfWindowSize),-1/4*HalfWindowSize,
    #           0, 1/4*HalfWindowSize,int(1/2*HalfWindowSize),3/4*HalfWindowSize,HalfWindowSize]
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xticks(x)
    ax.set_xticklabels(labels,fontsize=10)
    ax.axvline(x=0, color='k', linestyle='--')
    ax.set_xlabel('Window(ms)',fontsize=10)
    ax.set_ylabel('Spike Count',fontsize=10)
    ax.set_title(title+str(binsize)+' ms bin',fontsize=10)
       
    return ax,Edges

def get_PSTH_value_spiketrain(spiketime1,spiketime2,binsize=2,HalfWindowSize=50,
                                     frametime=0.1006198181):
    '''
    binsize and window size in ms
    1. Take spiketrain1 as reference (or “a trigger”), for each spike in spiketrain1:
    2. make a time window [-1000ms,1000ms],
    3. count spike numbers in spiketrain2 within this window by 10ms bins,
    ----1 and 2 makes a histogram for each single spike in spiketrain1.
    4. Sum the “counts” for all spikes in spiketrain1
    '''        
    bin_number=int(2*HalfWindowSize/(binsize))
    Totalcounts=[0] * bin_number
    half_windowSize_framenum=int(HalfWindowSize/frametime)
    for i in range(spiketime2.size - 1):
        tmpCounts, tmpEdges = np.histogram(spiketime1,
                                           bins = bin_number, 
                                           range = (spiketime2[i]-half_windowSize_framenum, 
                                                    spiketime2[i]+half_windowSize_framenum))
        Totalcounts = Totalcounts + tmpCounts
        
    Edges=np.arange(-bin_number/2,bin_number/2)   
       
    return Totalcounts,Edges

def plot_correlogram_sub_save (sub1,sub2,spath,lagtime=None,title='ROI1_2'):
    sub1_detrend = signal.detrend(sub1)
    sub2_detrend = signal.detrend(sub2)
    maxlags_default=len(sub1)-1
    fig,lags0,corr0=plt.xcorr(sub1_detrend,sub2_detrend,normed=True,maxlags=maxlags_default)##
    plt.ylim(-0.4,0.9)
    figpath1 = os.path.join(spath,title+'_sub_correlogram.svg')
    fig.savefig(figpath1, format='svg')
    return

def plot_correlogram_sub (sub1,sub2,lagtime=None,title='ROI1_2'):
    sub1_detrend = signal.detrend(sub1)
    sub2_detrend = signal.detrend(sub2)   
    if lagtime==None:
        maxlags=len(sub1)-1
    else:
        maxlags=lagtime
    
    fig=plt.figure()
    (lags,corr,_,_)=plt.xcorr(sub1_detrend,sub2_detrend,normed=True,maxlags=maxlags)
    plt.ylim(-0.4,0.9)
    fig.suptitle(title, fontsize=16)
    x = [-maxlags,-3/4*maxlags,-1/2*maxlags,-1/4*maxlags,0,
         1/4*maxlags,1/2*maxlags,3/4*maxlags,maxlags]
    labels = [int(-maxlags/10),'',int(-maxlags/20),'',
              0, '',int(maxlags/20),'',int(maxlags/10)] 
    plt.xticks(x, labels)
    plt.axvline(x=0, color='k', linestyle='--')
    plt.xlabel('lags(unit:ms)',fontsize=10)
    plt.ylabel('spike count',fontsize=10)
    
    return fig

def plot_correlation_sub_line (sub1,sub2,ax,lagtime=None,title='ROI1_2',color='b'):
    sub1_detrend = signal.detrend(sub1)
    sub2_detrend = signal.detrend(sub2)   
    if lagtime==None:
        maxlags=len(sub1)-1
    else:
        maxlags=lagtime
    
    (lags,corr,_,_)=ax.xcorr(sub1_detrend,sub2_detrend,normed=True,maxlags=maxlags,
                              usevlines=False,color=color,label=title)
    ax.set_ylim(-0.4,0.9)
    ax.set(alpha=0.1)
    #fig.suptitle(title, fontsize=16)
    x = [-maxlags,-3/4*maxlags,-1/2*maxlags,-1/4*maxlags,0,
         1/4*maxlags,1/2*maxlags,3/4*maxlags,maxlags]
    labels = [int(-maxlags/10),'',int(-maxlags/20),'',
              0, '',int(maxlags/20),'',int(maxlags/10)] 
    # plt.xticks(x, labels)
    # plt.axvline(x=0, color='k', linestyle='--')
    # plt.xlabel('lags(unit:ms)',fontsize=10)
    # plt.ylabel('spike count',fontsize=10)
    ax.legend(title,fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels,fontsize=10)
    #ax.axvline(x=0, color='k', linestyle='--')
    ax.set_xlabel('lags(unit:ms)',fontsize=10)
    ax.set_ylabel('Normalized correlation',fontsize=10)
    ax.set_title('correlogram',fontsize=10)
    return ax
#%%
'''Using'''
# dpath= "G:/Tian/"
# spath= "G:/Tian/Plots"
# csv_1 =  os.path.join(dpath, "ROI1_500Hz.csv")
# csv_2 =  os.path.join(dpath, "ROI2_500Hz.csv")
# csv_3 =  os.path.join(dpath, "negtive_ctrl_500Hz.csv")
# csv_4 =  os.path.join(dpath, "negtive_ctrl_10Hz.csv")
# csv_5 =  os.path.join(dpath, "trace3_10Hz.csv")
# roi1_data=pd.read_csv(csv_1)  
# roi2_data=pd.read_csv(csv_2) 
# trace3_sub=pd.read_csv(csv_5)
# neg_crtl_spike=pd.read_csv(csv_3)
# neg_crtl_sub=pd.read_csv(csv_4)
#%%Compare spike cross correlation
# # '''trace3 ROI1 and ROI2'''
# # spike1=roi1_data['trace3']
# # spike2=roi2_data['trace3']

# # plot_correlogram (spike1,spike2,spath,lagtime=None,title='ROI1_2')
# # plot_correlogram (spike1,spike2,spath,lagtime=1000,title='ROI1_2')

# # '''negtive control ROI1 trace3_14/15'''
# # spike1=neg_crtl_spike['trace3_14']
# # spike2=neg_crtl_spike['trace3_15']

# # '''negtive control ROI1 trace3_15/trace1_15'''
# # spike1=neg_crtl_spike['trace3_15']
# # spike2=neg_crtl_spike['trace1_15']

# '''trace3 ROI1 and ROI2'''
# spike1=roi1_data['trace3']
# spike2=roi2_data['trace3']


# '''negtive control ROI1 trace3_14/15'''
# spike3=neg_crtl_spike['trace3_14']
# spike4=neg_crtl_spike['trace3_15']

# '''negtive control ROI1 trace3_15/trace1_15'''
# spike5=neg_crtl_spike['trace3_15']
# spike6=neg_crtl_spike['trace1_15']

#%%
# #fig = plt.figure()
# plot_PSTH_correlogram(spike1,spike2,binsize=2,HalfWindowSize=50,title='neighbour 2 cell ')
# #fig = plt.figure()
# plot_PSTH_correlogram(spike3,spike4,binsize=2,HalfWindowSize=50,title=' diffslice ctrl ')
# #fig = plt.figure()
# plot_PSTH_correlogram(spike5,spike6,binsize=2,HalfWindowSize=50,title='same cell diff trace ctrl ')
# #import seaborn as sns

# #sns.distplot(list(Edges),bins=200,kde=False,hist_kws={"weights": list(counts)},color='k',linewidth=10)

'''Using'''
#%%
# fig,lags,corr=plot_cross_correlation(spiketrain1,spiketrain2,maxlags=999,title='ROI1-ROI2',linewidth=1)
# fig,corr_bin,lag_bin=plot_bin_corr_hist(corr,window=200,frametime=0.1006198181,linewith=1)




#%%
# (lags,corr,_,_) = plt.xcorr(sub1_detrend,sub2_detrend,normed=True,maxlags=99999)
# plt.ylim(-0.4,0.8)

#%%sum cross correlation
'''Sum correlation'''
# corr_sum,lag=get_cross_correlation_all(roi1_data,roi2_data,6)
# #%%
# fig = plt.figure(figsize=[20,10])
# plt.plot(lag,corr_sum,linewidth=2)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.xlabel('lags(time frame)',fontsize=20)
# plt.ylabel('cross correlation',fontsize=20)
# plt.yticks(fontsize=20)
# plt.title('Sum_corr', fontsize=20)
# #%%
# spiketrain_all_1=get_spiketrain_all(roi1_data, 6)
# spiketrain_all_2=get_spiketrain_all(roi2_data, 6)
# #%%
# plt.plot(spiketrain_all_1)
# plt.plot(spiketrain_all_2)
# #%%
# plot_cross_correlation(spiketrain_all_1,spiketrain_all_2,maxlags=599999,title='trace_60s_nobin',linewidth=3)
# #%%
# plot_cross_correlation(spiketrain_all_1,spiketrain_all_2,maxlags=59999,title='trace_60s_nobin_6slag',linewidth=3)
# #%%
# spiketrain_ms_1=get_lowerdatapoint(spiketrain_all_1,window=10)
# spiketrain_ms_2=get_lowerdatapoint(spiketrain_all_2,window=10)
# plot_cross_correlation(spiketrain_ms_1,spiketrain_ms_2,maxlags=59999,title='trace_60s_1ms_bin',linewidth=5)
# #%%
# spiketrain_ms_1=get_lowerdatapoint(spiketrain_all_1,window=20)
# spiketrain_ms_2=get_lowerdatapoint(spiketrain_all_2,window=20)
# plot_cross_correlation(spiketrain_ms_1,spiketrain_ms_2,maxlags=29999,title='trace_60s_2ms_bin',linewidth=5)
