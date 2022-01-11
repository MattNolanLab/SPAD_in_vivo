# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 10:02:19 2022

@author: Yifang
"""
import numpy as np
import pandas as pd
import getSpikes
import crossCorr as Corr
import os
import scipy.signal
import matplotlib.pyplot as plt
#%%
def shuffle_spiketimes(spiketrain, trace):  
    '''Shift a randon distance'''
    # shift_dist=np.random.randint(100,len(trace)-100, size=1)
    # spiketrain_shuffle=np.roll(spiketrain, shift_dist)   
    '''Random shuffle'''
    spiketrain_shuffle=np.copy(spiketrain) #don't use assign because it is the same array
    np.random.shuffle(spiketrain_shuffle)
    
    spiketimes_shuffle=getSpikes.get_spiketime(spiketrain_shuffle)
    #fig=getSpikes.plotSpikeOnTrace(trace, spiketimes_shuffle)    
    return spiketrain_shuffle,spiketimes_shuffle

'''Use manually shuffled data'''
'''shuffle one trace and compare with the other'''
def get_spike_corr_shuffle_pairs (spiketrain1, trace1, spiketimes2,trace2):
    spiketrain_shuffle,spiketimes_shuffle=shuffle_spiketimes(spiketrain1, trace1)
    Totalcounts1,Edges1 = Corr.get_PSTH_value_spiketrain(spiketimes_shuffle,spiketimes2,
                                                         binsize=2,HalfWindowSize=50,
                                                         frametime=0.1006198181)
    Totalcounts2,Edges2 = Corr.get_PSTH_value_spiketrain(spiketimes_shuffle,spiketimes2,
                                                         binsize=100,HalfWindowSize=1000,
                                                         frametime=0.1006198181)            
    return Edges1,Totalcounts1,Edges2,Totalcounts2

'''shuffle two traces'''
def get_spike_corr_shuffle_pairs_two (spiketrain1, trace1, spiketrain2,trace2):
    spiketrain_shuffle,spiketimes_shuffle=shuffle_spiketimes(spiketrain1, trace1)
    spiketrain_shuffle2,spiketimes_shuffle2=shuffle_spiketimes(spiketrain2, trace2)
    
    Totalcounts1,Edges1 = Corr.get_PSTH_value_spiketrain(spiketimes_shuffle,spiketimes_shuffle2,
                                                         binsize=2,HalfWindowSize=50,
                                                         frametime=0.1006198181)
    Totalcounts2,Edges2 = Corr.get_PSTH_value_spiketrain(spiketimes_shuffle,spiketimes_shuffle2,
                                                         binsize=100,HalfWindowSize=1000,
                                                         frametime=0.1006198181)            
    return Edges1,Totalcounts1,Edges2,Totalcounts2

def get_manual_shuffle_corr_list(spiketrain1, trace1, spiketimes2, trace2,shuffle_num=100):
    for i in range(shuffle_num):
        '''shuffle one trace and compare with the other'''
        Edges1,Totalcounts1,Edges2,Totalcounts2=get_spike_corr_shuffle_pairs (spiketrain1, 
                                                                              trace1, spiketimes2, trace2)
        '''shuffle two traces'''
        # Edges1,Totalcounts1,Edges2,Totalcounts2=get_spike_corr_shuffle_pairs_two (spiketrain1, 
        #                                                                       trace1, spiketrain2, trace2)
                
        if i==0:
            Corr_list1=np.zeros((shuffle_num,len(Totalcounts1)))
            Corr_list1[i,:]=Totalcounts1
            
            Corr_list2=np.zeros((shuffle_num,len(Totalcounts2)))
            Corr_list2[i,:]=Totalcounts2
        else:
            Corr_list1[i,:]=Totalcounts1
            Corr_list2[i,:]=Totalcounts2       
    return Edges1,Corr_list1,Edges2,Corr_list2

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a,axis=0), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def plot_corr_CI (lags,mean_corr,CI_low,CI_high,ax):
    lags_ms=lags
    ax.plot(lags_ms,mean_corr,color='tab:grey',zorder=1)
    ax.fill_between(lags_ms, CI_low, CI_high, color='tab:grey', alpha=.2)
    #ax.set_xlabel('lags(ms)',fontsize=10)
    #ax.set_ylabel('Normalized Cross Correlation',fontsize=10)
    #ax.legend(fontsize=8)
    #ax.set_title('Cross Correlation',fontsize=10)
    return  ax

def mean_percentile (data,lower_per=2.5,higher_per=97.5):
    a = 1.0 * np.array(data)
    #n = len(a)
    mean = np.mean(a,axis=0)
    lower_score=scipy.stats.scoreatpercentile(a, lower_per, axis=0)
    higher_score=scipy.stats.scoreatpercentile(a, higher_per, axis=0)
    return mean, lower_score,higher_score

def plot_PSTH_shuffle (spiketimes1,spiketimes2,shuffle_mean1,shuffle_lower1, shuffle_upper1,shuffle_mean2,shuffle_lower2, shuffle_upper2):  
    fig, ax = plt.subplots(1,2)
    _,Edges_1=Corr.plot_PSTH_correlogram_spiketrain(spiketimes1,spiketimes2,ax=ax[0],binsize=2,
                                          HalfWindowSize=50,frametime=0.1006198181,title='')
    Edges_1=Edges_1+0.5
    plot_corr_CI (Edges_1,shuffle_mean1,shuffle_lower1,shuffle_upper1,ax=ax[0])
    
    
    _,Edges_2=Corr.plot_PSTH_correlogram_spiketrain(spiketimes1,spiketimes2,ax=ax[1],binsize=100,
                                          HalfWindowSize=1000,frametime=0.1006198181,title='')    
    Edges_2=Edges_2+0.5
    plot_corr_CI (Edges_2,shuffle_mean2,shuffle_lower2,shuffle_upper2,ax=ax[1])
    
    return fig
#%%
#%% Plot mean,CI shaded area and PSTH together
dpath= "C:/SPAD/Tian/"
csv_1 =  os.path.join(dpath, "ROI1_500Hz.csv")
csv_2 =  os.path.join(dpath, "ROI2_500Hz.csv")
roi1_data=pd.read_csv(csv_1)  
roi2_data=pd.read_csv(csv_2) 
'''trace3 ROI1 and ROI2'''
spike1=roi1_data['trace3']
spike2=roi2_data['trace3']

'''neighbour cell with shuffled data overlay'''
#spiketimes1,spiketimes2= get_two_spiketimes_voltron (spike2,spike1,title1='Cell3',title2='Cell2')
#%%
spiketimes2,spiketrain2,trace2=getSpikes.get_spiketimes_voltron (spike2,title='spikeOnTrace',superfactor=10,threshs=(.75,.85,.93),
                                   window=10000,threshold_sets=(2.53,3.,3.5),cutoff=10)
#%%
spiketimes1,spiketrain1,trace1=getSpikes.get_spiketimes_voltron (spike1,title='spikeOnTrace1',superfactor=10,threshs=(.75,.85,.90),
                                   window=10000,threshold_sets=(2.53,3.,3.5),cutoff=10)
#%%
fig=getSpikes.get_correlogram_voltron_spiketime (spiketimes1,spiketimes2)
fig.suptitle('NeighbourCells', fontsize=16)
#%%
'''shuffle one trace and compare with the other'''
Edges1,Corr_list1,Edges2,Corr_list2=get_manual_shuffle_corr_list(spiketrain1, trace1, spiketimes2, trace2)
'''shuffle two traces'''
#Edges1,Corr_list1,Edges2,Corr_list2=get_manual_shuffle_corr_list(spiketrain1, trace1, spiketrain2, trace2)
#%%
mean1, lower_score1,higher_score1 = mean_percentile (Corr_list1,lower_per=5,higher_per=95)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list2,lower_per=5,higher_per=95)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('5 to 95 percentile', fontsize=16)
fig.tight_layout()  
#fig.savefig(os.path.join(spath,'PSTH_with_shuffled_5_95_percentile.svg'), format='svg')

#%%
m1, CI_low1, CI_high1=mean_confidence_interval(Corr_list1, confidence=0.95)
m2, CI_low2, CI_high2=mean_confidence_interval(Corr_list2, confidence=0.95)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,m1, CI_low1, CI_high1,m2, CI_low2, CI_high2)  
fig.suptitle('Confidence Interval', fontsize=16)
fig.tight_layout()    
#fig.savefig(os.path.join(spath,'PSTH_with_shuffled_CI.svg'), format='svg')

#%%

mean1, lower_score1,higher_score1 = mean_percentile (Corr_list1,lower_per=0,higher_per=100)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list2,lower_per=0,higher_per=100)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('min to max_percentile', fontsize=16)
fig.tight_layout()  
#fig.savefig(os.path.join(spath,'PSTH_with_shuffled_min_max_percentile.svg'), format='svg')

#%%
'''
mean1, lower_score1,higher_score1 = mean_percentile (Corr_list1,lower_per=2.5,higher_per=97.5)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list2,lower_per=2.5,higher_per=97.5)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('2.5 to 97.5 percentile', fontsize=16)
fig.tight_layout()  
#fig.savefig(os.path.join(spath,'PSTH_with_shuffled_2.5_97.5_percentile.svg'), format='svg')

mean1, lower_score1,higher_score1 = mean_percentile (Corr_list1,lower_per=25,higher_per=75)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list2,lower_per=25,higher_per=75)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('25 to 75 percentile', fontsize=16)
fig.tight_layout()  
#fig.savefig(os.path.join(spath,'PSTH_with_shuffled_25_75_percentile.svg'), format='svg')
'''