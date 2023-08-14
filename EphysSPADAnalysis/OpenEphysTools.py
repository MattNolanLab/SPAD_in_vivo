# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 10:00:55 2023
@author:Yifang
PACKAGE THAT NEED FOR THIS ANALYSIS
https://github.com/open-ephys/open-ephys-python-tools
https://github.com/pynapple-org/pynapple
https://github.com/PeyracheLab/pynacollada#getting-started

These are functions that I will call in main analysis.
"""
import os
import numpy as np
import pandas as pd
from scipy import signal
from open_ephys.analysis import Session
import matplotlib.pylab as plt
import pynapple as nap
import pynacollada as pyna
from scipy.signal import filtfilt
import pickle
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable

def butter_filter(data, btype='low', cutoff=10, fs=9938.4, order=5): 
    # cutoff and fs in Hz
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype=btype, analog=False)
    y = signal.filtfilt(b, a, data, axis=0)
    return y

def band_pass_filter(data,low_freq,high_freq,Fs):
    data_high=butter_filter(data, btype='high', cutoff=low_freq,fs=Fs, order=1)
    data_low=butter_filter(data_high, btype='low', cutoff=high_freq, fs=Fs, order=5)
    return data_low

def notchfilter (data,f0=50,Q=20):
    f0 = 50 # Center frequency of the notch (Hz)
    Q = 20 # Quality factor
    b, a = signal.iirnotch(f0, Q, 30000)
    data=signal.filtfilt(b, a, data)
    return data

def getRippleEvents (lfp_raw,Fs=30000,windowlen=1200,Low_thres=1,High_thres=10):
	lfp_filtered = pyna.eeg_processing.bandpass_filter(lfp_raw, 100, 300, Fs)	
	squared_signal = np.square(lfp_filtered.values)
	window = np.ones(windowlen)/windowlen
	nSS = filtfilt(window, 1, squared_signal)
	nSS = (nSS - np.mean(nSS))/np.std(nSS)
	nSS = nap.Tsd(t=lfp_filtered.index.values, 
	              d=nSS, 
	              time_support=lfp_filtered.time_support)
	              
	nSS2 = nSS.threshold(Low_thres, method='above')
	nSS3 = nSS2.threshold(High_thres, method='below')
	return lfp_filtered,nSS,nSS3
	
def plotRippleSpectrogram (lfp_raw, lfp_filtered, restrict_interval,nSS,nSS3,Low_thres,y_lim=300,Fs=30000):	
	# Define the spectrogram parameters
	nperseg = 1024    # Number of samples per segment
	noverlap = nperseg // 2    # Overlap between adjacent segments
	# Compute the spectrogram using a Hann window
	f, t, Sxx = signal.spectrogram(lfp_raw.restrict(restrict_interval), fs=Fs, window='hann', nperseg=nperseg, noverlap=noverlap)
	
	plt.figure(figsize=(15,8))
	plt.subplot(411)
	plt.plot(lfp_raw.restrict(restrict_interval).as_units('s'))
	plt.margins(0,0)
	plt.subplot(412)
	plt.plot(lfp_filtered.restrict(restrict_interval).as_units('s'))
	plt.margins(0,0)
	plt.subplot(413)
	plt.plot(nSS.restrict(restrict_interval).as_units('s'))
	plt.plot(nSS3.restrict(restrict_interval).as_units('s'), '.')
	plt.margins(0,0)
	# Plot the spectrogram
	plt.axhline(Low_thres)
	plt.subplot(414)
	#plt.pcolormesh(t, f, 10 * np.log10(Sxx), cmap='nipy_spectral')
	plt.pcolormesh(t, f, Sxx, cmap='nipy_spectral',vmin = 0,vmax = 100)
	#plt.pcolormesh(t, f, Sxx, cmap='nipy_spectral')
	plt.xlabel('Time (s)')
	plt.ylabel('Frequency (Hz)')
	plt.ylim([0, y_lim])
	plt.xlabel("Time (s)")
	plt.tight_layout()
	#plt.colorbar()
	plt.show()
	return -1

def plotSpectrogramOld (lfp_raw,plot_unit='WHz',nperseg=2048,y_lim=300,v_max = 8,Fs=30000):
    #nperseg: Number of samples per segment
	noverlap = nperseg // 2    # Overlap between adjacent segments
	# Compute the spectrogram using a Hann window
	f, t, Sxx = signal.spectrogram(lfp_raw, Fs, window='hann', nperseg=nperseg, noverlap=noverlap)
	
	plt.figure(figsize=(16,8))
	plt.subplot(111)
	#plt.pcolormesh(t, f, 10 * np.log10(Sxx), cmap='nipy_spectral')
	if (plot_unit=='WHz'):
		plt.pcolormesh(t, f, Sxx, cmap='nipy_spectral',vmin = 0,vmax = v_max)
		plt.xlabel('Time (s)')
		plt.ylabel('Frequency (Hz)')
		plt.ylim([0, y_lim])
		plt.xlabel("Time (s)")
		plt.tight_layout()
		cbar=plt.colorbar()
		cbar.set_label('W/Hz')
		plt.show()
	else:
		plt.pcolormesh(t, f, 10 * np.log10(Sxx), cmap='nipy_spectral')
		plt.xlabel('Time (s)')
		plt.ylabel('Frequency (Hz)')
		plt.ylim([0, y_lim])
		plt.xlabel("Time (s)")
		plt.tight_layout()
		cbar=plt.colorbar()
		cbar.set_label('dB')
		plt.show()
	return -1

def plotSpectrogram(ax, lfp_raw, plot_unit='WHz', nperseg=2048, y_lim=300, v_max=8, Fs=30000,showCbar=True):
    noverlap = nperseg // 2    # Overlap between adjacent segments
    f, t, Sxx = signal.spectrogram(lfp_raw, Fs, window='hann', nperseg=nperseg, noverlap=noverlap)

    if (plot_unit == 'WHz'):
        pcm = ax.pcolormesh(t, f, Sxx, cmap='nipy_spectral', vmin=0, vmax=v_max)
        ax.set_ylabel('Frequency (Hz)')
        ax.set_ylim([0, y_lim])
    else:
        pcm = ax.pcolormesh(t, f, 10 * np.log10(Sxx), cmap='nipy_spectral')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_ylim([0, y_lim])

    ax.set_xlabel("")  # Hide x-label
    ax.set_xticks([])  # Hide x-axis tick marks
    ax.figure.tight_layout()
    if showCbar:        
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="2%", pad=0.2)  # Adjust 'pad' to control the distance between plot and colorbar
        cbar = plt.colorbar(pcm, cax=cax)
        if plot_unit == 'WHz':
            cbar.set_label('W/Hz')
        else:
            cbar.set_label('dB')
        cbar.ax.tick_params(labelsize=8)  # Adjust color bar tick label size
    return pcm

def plotRippleEvent (lfp_raw, lfp_filtered, restrict_interval,nSS,nSS3,Low_thres):
	
	plt.figure(figsize=(15,5))
	plt.subplot(311)
	plt.plot(lfp_raw.restrict(restrict_interval).as_units('s'))
	plt.subplot(312)
	plt.plot(lfp_filtered.restrict(restrict_interval).as_units('s'))
	plt.subplot(313)
	plt.plot(nSS.restrict(restrict_interval).as_units('s'))
	plt.plot(nSS3.restrict(restrict_interval).as_units('s'), '.')
	plt.axhline(Low_thres)
	plt.xlabel("Time (s)")
	plt.tight_layout()
	plt.show()
	return -1

def SPAD_sync_mask (SPAD_Sync, start_lim, end_lim):
    '''
       	SPAD_Sync : numpy array
       		This is SPAD X10 output to the Open Ephys acquisition board. Each recorded frame will output a pulse.
       	start_lim : frame number
       	end_lim : frame number
       	SPAD_Sync usually have output during live mode and when the GUI is stopped. 
       	start and end lim will roughly limit the time duration for the real acquistion time.
       	Returns: SPAD_mask : numpy list
       		0 and 1 mask, 1 means SPAD is recording during this time.
    '''
    SPAD_mask=np.zeros(len(SPAD_Sync),dtype=np.int)
    SPAD_mask[np.where(SPAD_Sync <5000)[0]]=1
    SPAD_mask[0:start_lim]=0
    SPAD_mask[end_lim:]=0
    for i in range(len(SPAD_Sync)-2):
        if ((SPAD_mask[i]==0)&(SPAD_mask[i+1]==0)&(SPAD_mask[i+2]==0))==False:
           	SPAD_mask[i]=1
    
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(SPAD_mask)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)	
    	
    mask_array_bool = np.array(SPAD_mask, dtype=bool)
    return mask_array_bool

def save_SPAD_mask (dpath,mask_data_array):
    savefilename=os.path.join(dpath, "SPAD_mask.pkl")
    with open(savefilename, 'wb') as pickle_file:
        pickle.dump(mask_data_array, pickle_file) 
        return -1
    
def readEphysChannel (Directory,recordingNum,Fs=30000):
    session = Session(Directory)
    recording= session.recordnodes[0].recordings[recordingNum]
    continuous=recording.continuous
    continuous0=continuous[0]
    samples=continuous0.samples
    timestamps=continuous0.timestamps
    events=recording.events
    
    '''Recording nodes that are effective'''
    LFP1=samples[:,8]
    LFP2=samples[:,9]
    LFP3=samples[:,10]
    LFP4=samples[:,11]
    LFP5=samples[:,13]
    '''ADC lines that recorded the analog input from SPAD PCB X10 pin'''
    Sync1=samples[:,16] #Full pulsed aligned with X10 input
    Sync2=samples[:,17]
    Sync3=samples[:,18]
    Sync4=samples[:,19]
    
    LFP_clean1= butter_filter(LFP1, btype='low', cutoff=1500, fs=Fs, order=5)
    LFP_clean2= butter_filter(LFP2, btype='low', cutoff=1500, fs=Fs, order=5)
    LFP_clean3= butter_filter(LFP3, btype='low', cutoff=1500, fs=Fs, order=5)
    LFP_clean4= butter_filter(LFP4, btype='low', cutoff=1500, fs=Fs, order=5)
    LFP_clean1= notchfilter (LFP_clean1,f0=50,Q=20)
    LFP_clean2= notchfilter (LFP_clean2,f0=50,Q=20)
    LFP_clean3= notchfilter (LFP_clean3,f0=50,Q=20)
    LFP_clean4= notchfilter (LFP_clean4,f0=50,Q=20)
    
    EphysData = pd.DataFrame({
        'timestamps': timestamps,
        'CamSync': Sync1,
        'SPADSync': Sync2,
        'LFP_1': LFP_clean1,
        'LFP_2': LFP_clean2,
        'LFP_3': LFP_clean3,
        'LFP_4': LFP_clean4,
    })
    
    return EphysData

def save_open_ephys_data (dpath, data):
    filepath=os.path.join(dpath, "open_ephys_read_pd.pkl")
    data.to_pickle(filepath)
    return -1

def plot_animal_tracking (trackingdata):
    # Calculate the ratio of units on X and Y axes
    x_range = trackingdata['X'].max() - trackingdata['X'].min()
    y_range = trackingdata['Y'].max() - trackingdata['Y'].min()
    aspect_ratio = y_range / x_range    
    # Set the figure size based on the aspect ratio
    fig, ax = plt.subplots(figsize=(16, 16 * aspect_ratio))  # Adjust the '5' based on your preference
    # Creating an x-y scatter plot
    trackingdata.plot.scatter(x='X', y='Y', color='blue', marker='o', s=2, ax=ax)    
    # Adding labels and title
    plt.xlabel('X')
    plt.yticks([])
    plt.title('Animal tracking Plot')
    plt.show()
    return -1

def plot_two_raw_traces (data1,data2, spad_label='spad',lfp_label='LFP'):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    sns.lineplot(x=data1.index, y=data1.values, ax=ax1, label=spad_label, linewidth=1, color=sns.color_palette("husl", 8)[3])
    #ax1.plot(spad_resampled, label='spad')
    #ax1.set_ylabel('PhotonCount')
    ax1.set_ylabel('z-score')
    ax1.legend()
    sns.lineplot(x=data2.index, y=data2.values, ax=ax2, label=lfp_label, linewidth=1, color=sns.color_palette("husl", 8)[5])
    ax2.set_ylabel('Amplitude')
    #ax2.set_title('LFP')
    ax2.set_xlabel('Time (s)')
    ax2.legend()
    plt.tight_layout()
    plt.show()
    return fig

def plot_trace_seconds (data,ax,label='data',color='b',ylabel='z-score',xlabel=True):
    sns.lineplot(x=data.index.total_seconds(), y=data.values, ax=ax, label=label, linewidth=1, color=color)
    ax.set_ylabel(ylabel)
    ax.spines['top'].set_visible(False)    # Hide the top spine
    ax.spines['right'].set_visible(False)  # Hide the right spine
    ax.spines['left'].set_visible(False)   # Hide the left spine
    #ax.spines['bottom'].set_visible(True)  # Show the bottom spine
    if xlabel==False:
        ax.set_xticks([])  # Hide x-axis tick marks
        ax.set_xlabel('')  # Hide x-axis label
        ax.spines['bottom'].set_visible(False)  # Show the bottom spine
    ax.set_xlim(data.index.total_seconds().min(), data.index.total_seconds().max())  # Set x-limits
    ax.legend(loc='upper right')
    return ax
    
def plot_speed_heatmap(ax, speed_series):
    speed_series = speed_series.to_frame()
    heatmap = sns.heatmap(speed_series.transpose(), annot=False, cmap='YlGnBu', vmax=50, ax=ax,cbar=False, yticklabels=[])
    ax.set_title("Heatmap of Animal speed over time")
    # Format x-axis labels to show seconds
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.Timedelta(x*100000).seconds))
    ax.set_xticks([])  # Hide x-axis tick marks
    ax.set_xlabel('')  # Hide x-axis label
    ax.set_ylabel('Speed')

    return -1