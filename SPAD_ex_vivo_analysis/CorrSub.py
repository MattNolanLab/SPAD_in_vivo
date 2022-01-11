# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 23:35:24 2021

@author: s2073467
This is
"""

import os
import scipy.io 
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import numpy as np
import crossCorr as Corr
import scipy.stats as stats

#%%
def get_detrend(sub):
     sub_detrend = signal.detrend(sub)
     return sub_detrend
 
def calculate_correlation (data1,data2):
    '''normalize'''
    s1 = (data1 - np.mean(data1)) / (np.std(data1))
    s2 = (data2 - np.mean(data2)) / (np.std(data2))
    lags=signal.correlation_lags(len(data1), len(data2), mode='full') 
    corr=signal.correlate(s1, s2, mode='full', method='auto')/len(data1)
    return lags,corr

def calculate_correlation_sub (sub1,sub2):
    trace1=get_detrend(sub1)
    trace2=get_detrend(sub2)
    lags,corr=calculate_correlation (trace1,trace2)
    return lags,corr
    
# def get_lags(sub1,sub2,lagtime=None):
#     sub1_detrend = signal.detrend(sub1)
#     sub2_detrend = signal.detrend(sub2)   
#     if lagtime==None:
#         maxlags=len(sub1)-1
#     else:
#         maxlags=lagtime
      
#     (lags,corr,_,_)=plt.xcorr(sub1_detrend,sub2_detrend,normed=True,usevlines=False,maxlags=maxlags) 
#     return lags

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a,axis=0), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


def get_mean_sub_corr_two_cells (cell1_sub, cell2_sub):
    column_num=len(cell1_sub.columns)
    for i in range(column_num):
        sub1_trace=cell1_sub.iloc[:,i]
        sub2_trace=cell2_sub.iloc[:,i]
        lags,corr =calculate_correlation_sub (sub1_trace,sub2_trace)
        if i==0:
            Corr_sum=corr
        else:
            Corr_sum=Corr_sum+corr
        Corr_mean=Corr_sum/column_num
    return lags,Corr_mean

def get_sub_corr_list_two_cells (cell1_sub, cell2_sub):
    column_num=len(cell1_sub.columns)
    for i in range(column_num):
        sub1_trace=cell1_sub.iloc[:,i]
        sub2_trace=cell2_sub.iloc[:,i]
        lags,corr =calculate_correlation_sub (sub1_trace,sub2_trace)       
        if i==0:
            Corr_list=np.zeros((column_num,len(lags)))
            Corr_list[i,:]=corr
        else:
            Corr_list[i,:]=corr        
    return lags,Corr_list

def get_shuffle_corr_list(cell1_sub, cell2_sub,cell3_sub, cell4_sub,cell5_sub, cell6_sub):
    lags,Corr_list1=get_sub_corr_list_two_cells (cell1_sub, cell2_sub)
    lags,Corr_list2=get_sub_corr_list_two_cells (cell1_sub, cell3_sub)
    lags,Corr_list3=get_sub_corr_list_two_cells (cell1_sub, cell4_sub)
    lags,Corr_list4=get_sub_corr_list_two_cells (cell1_sub, cell5_sub)
    lags,Corr_list5=get_sub_corr_list_two_cells (cell1_sub, cell6_sub)
    lags,Corr_list6=get_sub_corr_list_two_cells (cell2_sub, cell4_sub)
    lags,Corr_list7=get_sub_corr_list_two_cells (cell2_sub, cell5_sub)
    lags,Corr_list8=get_sub_corr_list_two_cells (cell2_sub, cell6_sub)
    lags,Corr_list9=get_sub_corr_list_two_cells (cell3_sub, cell4_sub)
    lags,Corr_list10=get_sub_corr_list_two_cells (cell3_sub, cell5_sub)
    Corr_list_shuffle=np.vstack((Corr_list1, Corr_list2, Corr_list3,
                                 Corr_list4, Corr_list5, Corr_list6, Corr_list7,
                                 Corr_list8, Corr_list9, Corr_list10))
    return lags,Corr_list_shuffle

    
def plot_corr_line (lags,corr,ax,frametime=0.1006198181):
    lags_ms=lags*frametime
    ax.plot(lags_ms,corr,label='mean_cross_correlation',zorder=2)

    ax.set_xlabel('lags(ms)',fontsize=10)
    ax.set_ylabel('Normalized Cross Correlation',fontsize=10)
    ax.legend(fontsize=8)
    ax.set_title('Cross Correlation',fontsize=10)
    return  ax

def plot_corr_CI (lags,mean_corr,CI_low,CI_high,ax,frametime=0.1006198181,title=None):
    lags_ms=lags*frametime
    ax.plot(lags_ms,mean_corr,label='mean_100_shuffled_pairs',color='tab:grey',zorder=1)
    ax.fill_between(lags_ms, CI_low, CI_high, color='tab:grey', alpha=.2)
    ax.set_xlabel('lags(ms)',fontsize=10)
    ax.set_ylabel('Normalized Cross Correlation',fontsize=10)
    ax.legend(fontsize=8)
    ax.set_title(title,fontsize=10)
    return  ax

def mean_percentile (data,lower_per=2.5,higher_per=97.5):
    a = 1.0 * np.array(data)
    #n = len(a)
    mean = np.mean(a,axis=0)
    lower_score=scipy.stats.scoreatpercentile(a, lower_per, axis=0)
    higher_score=scipy.stats.scoreatpercentile(a, higher_per, axis=0)
    return mean, lower_score,higher_score

def plot_shuffle_together (real_cell1,real_cell2,shuffle_mean,shuffle_lowerbound,shuffle_upperbound,title=None):
    lags,Corr_mean=get_mean_sub_corr_two_cells (real_cell1, real_cell2)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax=plot_corr_line (lags,Corr_mean,ax)
    ax=plot_corr_CI (lags,shuffle_mean,shuffle_lowerbound,shuffle_upperbound,ax,title=title)    
    return fig
#%%
dpath= "C:/SPAD/Tian/TianDataSorted"
spath= "C:/SPAD/Tian/Plots"
csv_cell1 =  os.path.join(dpath, "cell1.csv")
csv_cell2 =  os.path.join(dpath, "cell2.csv")
csv_cell3 =  os.path.join(dpath, "cell3.csv")
csv_cell4 =  os.path.join(dpath, "cell4.csv")
csv_cell5 =  os.path.join(dpath, "cell5.csv")
csv_cell6 =  os.path.join(dpath, "cell6.csv")


cell1_sub=pd.read_csv(csv_cell1).loc[:,'trace1_10Hz':'trace10_10Hz']
cell2_sub=pd.read_csv(csv_cell2).loc[:,'trace1_10Hz':'trace10_10Hz']
cell3_sub=pd.read_csv(csv_cell3).loc[:,'trace1_10Hz':'trace10_10Hz']
cell4_sub=pd.read_csv(csv_cell4).loc[:,'trace1_10Hz':'trace10_10Hz']
cell5_sub=pd.read_csv(csv_cell5).loc[:,'trace1_10Hz':'trace10_10Hz']
cell6_sub=pd.read_csv(csv_cell6).loc[:,'trace1_10Hz':'trace10_10Hz']


#%% get shuffled list 
lags,Corr_list_shuffle=get_shuffle_corr_list(cell1_sub, cell2_sub,cell3_sub, cell4_sub,cell5_sub, cell6_sub)

#%% confidence interval
m, CI_low, CI_high=mean_confidence_interval(Corr_list_shuffle, confidence=0.95)

fig = plt.figure()
ax = fig.add_subplot(111)
ax=plot_corr_CI (lags,m,CI_low,CI_high,ax)
#%%percentile
m, lower_score, higher_score=mean_percentile(Corr_list_shuffle, lower_per=5,higher_per=95)

fig = plt.figure()
ax = fig.add_subplot(111)
ax=plot_corr_CI (lags,m,lower_score,higher_score,ax)
#%%

fig=plot_shuffle_together (cell2_sub,cell3_sub,m,CI_low,CI_high,title='95% Confidence Interval')
fig=plot_shuffle_together (cell2_sub,cell3_sub,m,lower_score,higher_score,title='2.5 to 97.5 percentile')
#%%
fig=plot_shuffle_together (cell2_sub,cell3_sub,m,lower_score,higher_score,title='0 to 100 percentile')

#%%plot together
lags,Corr_mean=get_mean_sub_corr_two_cells (cell2_sub, cell3_sub)
fig = plt.figure()
ax = fig.add_subplot(111)
ax=plot_corr_line (lags,Corr_mean,ax)
ax=plot_corr_CI (lags,m,CI_low,CI_high,ax)

figpath1 = os.path.join(spath,'Only_shuffle_Cross_Correlation.svg')
fig.savefig(figpath1, format='svg')
#%%plot together subset
lags_zoom=lags[80000:120000]
Corr_mean_zoom=Corr_mean[80000:120000]
m_zoom,CI_low_zoom,CI_high_zoom=m[80000:120000],CI_low[80000:120000],CI_high[80000:120000]

fig = plt.figure()
ax = fig.add_subplot(111)
ax=plot_corr_line (lags_zoom,Corr_mean_zoom,ax)
ax=plot_corr_CI (lags_zoom,m_zoom,CI_low_zoom,CI_high_zoom,ax)

figpath1 = os.path.join(spath,'Cross_Correlation_with_shuffle_zoom2000ms.svg')
fig.savefig(figpath1, format='svg')

#%%Compare spike cross correlation
'''cell2'''
sub1=cell2_sub['trace1_10Hz']
sub2=cell2_sub['trace2_10Hz']

lags,corr =calculate_correlation_sub (sub1,sub2)
plt.plot(lags,corr)
a=np.max(corr)
