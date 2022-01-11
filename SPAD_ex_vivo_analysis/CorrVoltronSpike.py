# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 18:07:40 2021

This is using Voltron pipeline to test Tian's data 
and calculate cross correlation'

@author: s2073467
"""
import os
import scipy.io 
import matplotlib.pyplot as plt
import scipy.signal
import voltron_ROI_continuous as ROI
import pandas as pd
import numpy as np
import crossCorr as Corr
import getSpikes
#%%
'''Original Voltron Pipeline with spike shape template to get spkie'''
#superfactor=10,threshs=(.75,.85,.94),window=2000,threshold_sets=(2.53,3.,3.5))
def get_spiketimes_voltron (spike,title='spikeOnTrace',superfactor=10,threshs=(.75,.85,.96),
                                   window=10000,threshold_sets=(2.55,3.,3.5)):
    spike=getSpikes.get_inverse_trace(spike)    
    spike_data=ROI.get_spikes_old(spike, superfactor=superfactor, threshs=threshs,
                                   window=window,threshold_sets=threshold_sets)
    #spike_data1=ROI.get_spikes(spike1, superfactor=10, threshs=(.4, .6))
    #sub_thresh2=spike_data[0]
    #high_freq=spike_data[1]
    spiketimes=spike_data[2]
    #spiketrain=spike_data[3]
    #spikesizes=spike_data[4]
    fig=getSpikes.plotSpikeOnTrace(spike, spiketimes,name=title)
    return fig,spiketimes

def get_spike_corr_list_two_cells (cell1_sub, cell2_sub):
    column_num=len(cell1_sub.columns)
    for i in range(column_num):
        trace1=cell1_sub.iloc[:,i]
        trace2=cell2_sub.iloc[:,i]
        _,spiketime1=get_spiketimes_voltron(trace1)
        _,spiketime2=get_spiketimes_voltron(trace2)
        Totalcounts1,Edges1 = Corr.get_PSTH_value_spiketrain(spiketime1,spiketime2,
                                                             binsize=2,HalfWindowSize=50,
                                                             frametime=0.1006198181)
        Totalcounts2,Edges2 = Corr.get_PSTH_value_spiketrain(spiketime1,spiketime2,
                                                             binsize=100,HalfWindowSize=1000,
                                                             frametime=0.1006198181)
        if i==0:
            Corr_list1=np.zeros((column_num,len(Totalcounts1)))
            Corr_list1[i,:]=Totalcounts1
            
            Corr_list2=np.zeros((column_num,len(Totalcounts2)))
            Corr_list2[i,:]=Totalcounts2
        else:
            Corr_list1[i,:]=Totalcounts1
            Corr_list2[i,:]=Totalcounts2   
            
    return Edges1,Corr_list1,Edges2,Corr_list2

def get_shuffle_corr_list(cell1_sub, cell2_sub,cell3_sub, cell4_sub,cell5_sub, cell6_sub):
    Edges1,Corr_list11,Edges2,Corr_list21=get_spike_corr_list_two_cells (cell1_sub, cell2_sub)
    Edges1,Corr_list12,Edges2,Corr_list22=get_spike_corr_list_two_cells (cell1_sub, cell3_sub)
    Edges1,Corr_list13,Edges2,Corr_list23=get_spike_corr_list_two_cells (cell1_sub, cell4_sub)
    Edges1,Corr_list14,Edges2,Corr_list24=get_spike_corr_list_two_cells (cell1_sub, cell5_sub)
    Edges1,Corr_list15,Edges2,Corr_list25=get_spike_corr_list_two_cells (cell1_sub, cell6_sub)
    Edges1,Corr_list16,Edges2,Corr_list26=get_spike_corr_list_two_cells (cell2_sub, cell4_sub)
    Edges1,Corr_list17,Edges2,Corr_list27=get_spike_corr_list_two_cells (cell2_sub, cell5_sub)
    Edges1,Corr_list18,Edges2,Corr_list28=get_spike_corr_list_two_cells (cell2_sub, cell6_sub)
    Edges1,Corr_list19,Edges2,Corr_list29=get_spike_corr_list_two_cells (cell3_sub, cell4_sub)
    Edges1,Corr_list110,Edges2,Corr_list210=get_spike_corr_list_two_cells (cell3_sub, cell5_sub)
    Corr_list_shuffle1=np.vstack((Corr_list11, Corr_list12, Corr_list13,
                                 Corr_list14, Corr_list15, Corr_list16, Corr_list17,
                                 Corr_list18, Corr_list19, Corr_list110))
    Corr_list_shuffle2=np.vstack((Corr_list21, Corr_list22, Corr_list23,
                                 Corr_list24, Corr_list25, Corr_list26, Corr_list27,
                                 Corr_list28, Corr_list29, Corr_list210))
    return Edges1,Corr_list_shuffle1,Edges2,Corr_list_shuffle2



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
#%% For 100 shufle pairs PSTH
dpath= "C:/SPAD/Tian/TianDataSorted"
spath= "C:/SPAD/Tian/Plots"
#%%
csv_cell1 =  os.path.join(dpath, "cell1.csv")
csv_cell2 =  os.path.join(dpath, "cell2.csv")
csv_cell3 =  os.path.join(dpath, "cell3.csv")
csv_cell4 =  os.path.join(dpath, "cell4.csv")
csv_cell5 =  os.path.join(dpath, "cell5.csv")
csv_cell6 =  os.path.join(dpath, "cell6.csv")

cell1_trace=pd.read_csv(csv_cell1).loc[:,'trace1_500Hz':'trace10_500Hz']
cell2_trace=pd.read_csv(csv_cell2).loc[:,'trace1_500Hz':'trace10_500Hz']
cell3_trace=pd.read_csv(csv_cell3).loc[:,'trace1_500Hz':'trace10_500Hz']
cell4_trace=pd.read_csv(csv_cell4).loc[:,'trace1_500Hz':'trace10_500Hz']
cell5_trace=pd.read_csv(csv_cell5).loc[:,'trace1_500Hz':'trace10_500Hz']
cell6_trace=pd.read_csv(csv_cell6).loc[:,'trace1_500Hz':'trace10_500Hz']

#%% test spike corr list
#Edges1,Corr_list1,Edges2,Corr_list2=get_spike_corr_list_two_cells(cell1_trace,cell2_trace)
Edges1,Corr_list_shuffle1,Edges2,Corr_list_shuffle2 = get_shuffle_corr_list(cell1_trace, 
                                                                            cell2_trace,
                                                                            cell3_trace, 
                                                                            cell4_trace,
                                                                            cell5_trace, 
                                                                            cell6_trace)
#%%
np.savetxt(os.path.join(spath, "Edges1.csv"), Edges1, delimiter=",")
np.savetxt(os.path.join(spath, "Edges2.csv"), Edges2, delimiter=",")
#%%
np.savetxt(os.path.join(spath, "Corr_list_shuffle1.csv"), Corr_list_shuffle1, delimiter=",")
np.savetxt(os.path.join(spath, "Corr_list_shuffle2.csv"), Corr_list_shuffle2, delimiter=",")

#%%
Corr_list_shuffle1 = np.genfromtxt(os.path.join(spath, "Corr_list_shuffle1.csv"), delimiter=',')
Corr_list_shuffle2 = np.genfromtxt(os.path.join(spath, "Corr_list_shuffle2.csv"), delimiter=',')
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
_,spiketimes1=get_spiketimes_voltron (spike2,title='spikeOnTrace',superfactor=10,threshs=(.75,.85,.94),
                                   window=10000,threshold_sets=(2.53,3.,3.5))
#%%
_,spiketimes2=get_spiketimes_voltron (spike1,title='spikeOnTrace',superfactor=10,threshs=(.75,.85,.91),
                                   window=10000,threshold_sets=(2.53,3.,3.5))
#%%
fig=getSpikes.get_correlogram_voltron_spiketime (spiketimes1,spiketimes2)
fig.suptitle('NeighbourCells', fontsize=16)
#%%
m1, CI_low1, CI_high1=mean_confidence_interval(Corr_list_shuffle1, confidence=0.95)
m2, CI_low2, CI_high2=mean_confidence_interval(Corr_list_shuffle2, confidence=0.95)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,m1, CI_low1, CI_high1,m2, CI_low2, CI_high2)  
fig.suptitle('Confidence Interval', fontsize=16)
fig.tight_layout()    
fig.savefig(os.path.join(spath,'PSTH_with_shuffled_CI.svg'), format='svg')
#%%
mean1, lower_score1,higher_score1 = mean_percentile (Corr_list_shuffle1,lower_per=0,higher_per=100)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list_shuffle2,lower_per=0,higher_per=100)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('min to max_percentile', fontsize=16)
fig.tight_layout()  
fig.savefig(os.path.join(spath,'PSTH_with_shuffled_min_max_percentile.svg'), format='svg')
#%%
mean1, lower_score1,higher_score1 = mean_percentile (Corr_list_shuffle1,lower_per=2.5,higher_per=97.5)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list_shuffle2,lower_per=2.5,higher_per=97.5)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('2.5 to 97.5 percentile', fontsize=16)
fig.tight_layout()  
fig.savefig(os.path.join(spath,'PSTH_with_shuffled_2.5_97.5_percentile.svg'), format='svg')
#%%
mean1, lower_score1,higher_score1 = mean_percentile (Corr_list_shuffle1,lower_per=5,higher_per=95)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list_shuffle2,lower_per=5,higher_per=95)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('5 to 95 percentile', fontsize=16)
fig.tight_layout()  
fig.savefig(os.path.join(spath,'PSTH_with_shuffled_5_95_percentile.svg'), format='svg')
#%%
mean1, lower_score1,higher_score1 = mean_percentile (Corr_list_shuffle1,lower_per=25,higher_per=75)
mean2, lower_score2,higher_score2 = mean_percentile (Corr_list_shuffle2,lower_per=25,higher_per=75)

fig=plot_PSTH_shuffle (spiketimes1,spiketimes2,mean1, lower_score1,higher_score1,mean2, lower_score2,higher_score2)  
fig.suptitle('25 to 75 percentile', fontsize=16)
fig.tight_layout()  
fig.savefig(os.path.join(spath,'PSTH_with_shuffled_25_75_percentile.svg'), format='svg')
#%%

#%% For cell pair PSTH
dpath= "C:/SPAD/Tian/"
spath= "C:/SPAD/Tian/Plots"
csv_1 =  os.path.join(dpath, "ROI1_500Hz.csv")
csv_2 =  os.path.join(dpath, "ROI2_500Hz.csv")
csv_3 =  os.path.join(dpath, "negtive_ctrl_500Hz.csv")
csv_4 =  os.path.join(dpath, "negtive_ctrl_10Hz.csv")

roi1_data=pd.read_csv(csv_1)  
roi2_data=pd.read_csv(csv_2) 

neg_crtl_spike=pd.read_csv(csv_3)
neg_crtl_sub=pd.read_csv(csv_4)


'''trace3 ROI1 and ROI2'''
spike1=roi1_data['trace3']
spike2=roi2_data['trace3']

'''negtive control ROI1 trace3_14/15'''
spike3=neg_crtl_spike['trace3_14']
spike4=neg_crtl_spike['trace3_15']

'''negtive control ROI1 trace3_15/trace1_15'''
spike5=neg_crtl_spike['trace3_15']
spike6=neg_crtl_spike['trace1_15']


#%%
#%%
fig=getSpikes.get_correlogram_voltron_spiketime (spiketimes1,spiketimes2)
fig.suptitle('NeighbourCells', fontsize=16)
#%%Plot mean,CI shaded area and PSTH together
fig, ax = plt.subplots(1,2)
_,Edges_1=Corr.plot_PSTH_correlogram_spiketrain(spiketimes1,spiketimes2,ax=ax[0],binsize=2,
                                      HalfWindowSize=50,frametime=0.1006198181,title='')
Edges_1=Edges_1+0.5
plot_corr_CI (Edges_1,m1,CI_low1,CI_high1,ax=ax[0])


_,Edges_2=Corr.plot_PSTH_correlogram_spiketrain(spiketimes1,spiketimes2,ax=ax[1],binsize=100,
                                      HalfWindowSize=1000,frametime=0.1006198181,title='')    
Edges_2=Edges_2+0.5
plot_corr_CI (Edges_2,m2,CI_low2,CI_high2,ax=ax[1])

fig.tight_layout()
fig.savefig(os.path.join(spath,'PSTH_with_shuffled.svg'), format='svg')

#%% Best for now

#%%test
spiketimes1,spiketimes2= getSpikes.get_two_spiketimes_voltron (spike2,spike1,title1='Cell3',title2='Cell2')
Totalcounts,Edges = Corr.get_PSTH_value_spiketrain(spiketimes1,spiketimes2,binsize=2,HalfWindowSize=50,
                                     frametime=0.1006198181)    

#%% For cell pair PSTH
#%%
'''neighbour cell'''
spiketimes1,spiketimes2= getSpikes.get_two_spiketimes_voltron (spike2,spike1,title1='Cell3',title2='Cell2')
fig=getSpikes.get_correlogram_voltron_spiketime (spiketimes1,spiketimes2)
fig.suptitle('NeighbourCells', fontsize=16)
# figpath1 = os.path.join(spath,'Spikecorrelogram_NeighbourCells_cell2cell3.svg')
# fig.savefig(figpath1, format='svg')
#%%
'''ctrl_diff_Cell'''
spiketimes1,spiketimes2= getSpikes.get_two_spiketimes_voltron (spike3,spike1,title1='Cell_Diff_Slice',title2='Cell2')
fig=getSpikes.get_correlogram_voltron_spiketime (spiketimes1,spiketimes2)
fig.suptitle('Ctrl_Diff_Two_Cells', fontsize=16)
#figpath1 = os.path.join(spath,'Spikecorrelogram_Ctrl_Diff_Two_Cells.svg')
#fig.savefig(figpath1, format='svg')
#%%
'''ctrl_diffTrace'''
spiketimes1,spiketimes2= getSpikes.get_two_spiketimes_voltron (spike6,spike1,title1='Cell2_Diff_Traces',title2='cell2')
fig=getSpikes.get_correlogram_voltron_spiketime (spiketimes1,spiketimes2)
fig.suptitle('Ctrl_Diff_Traces', fontsize=16)
#figpath1 = os.path.join(spath,'Spikecorrelogram_Ctrl_Diff_Traces.svg')
#fig.savefig(figpath1, format='svg')
#%%
