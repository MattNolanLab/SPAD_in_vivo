# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:03:35 2023

@author: Yifang
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import FastICA
from scipy import signal
from scipy.fft import fft
import seaborn as sns
import OpenEphysTools as OE
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pynapple as nap
import pynacollada as pyna

class OESPADsingleTrace:
    def __init__(self, dpath):
        '''
        Parameters
        ----------
        dpath : TYPE
            DESCRIPTION.
        EphysData : TYPE:pandas, readout from open-ephys recording, with SPAD mask

        '''
        self.Spad_fs = 9938.4
        self.ephys_fs = 30000
        self.tracking_fs = 30
        self.fs = 10000.0
        self.dpath=dpath                

        self.Ephys_data=self.read_open_ephys_data() #read ephys data that we pre-processed from dpath          
        self.read_tracking_data() #read tracking raw data   
        self.trackingdata_extent,frame_count, frame_indices= self.extent_tracking_to_ephys_pd ()    
        
        # #self.Format_tracking_data_index () ## this is to change the index to timedelta index, for resampling
        self.Sync_ephys_with_spad() #output self.spad_align, self.ephys_align
               		
    def Sync_ephys_with_spad(self, containTracking=True):
        if containTracking:
           self.Ephys_data = pd.concat([self.Ephys_data, self.trackingdata_extent], axis=1)
           
        self.form_ephys_spad_sync_data() # find the spad sync part
        self.Format_ephys_data_index () # this is to change the index to timedelta index, for resampling
        self.SPADdata=self.Read_SPAD_data() #read spad data
        self.resample_spad()
        self.resample_ephys()
        self.slice_ephys_to_align_with_spad()
        self.Ephys_tracking_spad_aligned=pd.concat([self.ephys_align, self.spad_align], axis=1)  
        self.save_data(self.Ephys_tracking_spad_aligned, 'Ephys_tracking_spad_aligned.pkl')
        return self.Ephys_tracking_spad_aligned
        
    def Read_SPAD_data (self):
        '''
        SPAD has sampling rate of 9938.4 Hz.
        But if we use 500Hz time division photometry recording, the effective sampling rate for sig_raw and ref_raw is 500Hz.
        In the pre-processing for SPAD data, I usually smooth it to 200Hz to obtain the z-score.
        '''
        self.sig_csv_filename=os.path.join(self.dpath, "Green_traceAll.csv")
        self.ref_csv_filename=os.path.join(self.dpath, "Red_traceAll.csv")
        self.zscore_csv_filename=os.path.join(self.dpath, "Zscore_traceAll.csv")
        sig_data = np.genfromtxt(self.sig_csv_filename, delimiter=',')
        ref_data = np.genfromtxt(self.ref_csv_filename, delimiter=',')
        zscore_data = np.genfromtxt(self.zscore_csv_filename, delimiter=',')
        time_interval = 1.0 / self.Spad_fs
        total_duration = len(sig_data) * time_interval
        timestamps = np.arange(0, total_duration, time_interval)
        timestamps_time = pd.to_timedelta(timestamps, unit='s')
        sig_raw = pd.Series(sig_data, index=timestamps_time)
        ref_raw = pd.Series(ref_data, index=timestamps_time)
        zscore_raw = pd.Series(zscore_data, index=timestamps_time)
        'Zscore data is obtained by Kate Martian method, smoothed to 250Hz effective sampling rate'
        self.SPADdata = pd.DataFrame({
            'sig_raw': sig_raw,
            'ref_raw': ref_raw,
            'zscore_raw': zscore_raw,
        })
        return self.SPADdata
    
    def read_open_ephys_data (self):
        filepath=os.path.join(self.dpath, "open_ephys_read_pd.pkl")
        self.Ephys_data = pd.read_pickle(filepath)  
        return self.Ephys_data
    
    def form_ephys_spad_sync_data (self):
        mask = self.Ephys_data['SPAD_mask'] 
        self.Ehpys_sync_data=self.Ephys_data[mask]
        OE.plot_two_raw_traces (mask,self.Ehpys_sync_data['LFP_2'], spad_label='spad_mask',lfp_label='LFP_2_raw') 
        return self.Ehpys_sync_data   
       

    def Format_ephys_data_index (self):
        time_interval = 1.0 / self.ephys_fs
        total_duration = len(self.Ehpys_sync_data) * time_interval
        timestamps = np.arange(0, total_duration, time_interval)
        timedeltas_index = pd.to_timedelta(timestamps, unit='s')            
        self.Ehpys_sync_data.index = timedeltas_index
        return self.Ehpys_sync_data
    
    def resample_spad (self):
        time_interval_common = 1.0 / self.fs
        self.spad_resampled = self.SPADdata.resample(f'{time_interval_common:.9f}S').mean()
        self.spad_resampled = self.spad_resampled.fillna(method='ffill')
        return self.spad_resampled
    
    def resample_ephys (self):
        time_interval_common = 1.0 / self.fs
        self.ephys_resampled = self.Ehpys_sync_data.resample(f'{time_interval_common:.9f}S').mean()
        self.ephys_resampled = self.ephys_resampled.fillna(method='ffill')
        return self.ephys_resampled                     
    
    def slice_ephys_to_align_with_spad (self):
        '''
        This is important because sometimes the effective SPAD recording is shorter than the real recording time due to deadtime. 
        E.g, I recorded 10 blocks 10s data, should be about 100s recording, but in most cases, there's no data in the last block.
        '''
        self.ephys_align = self.ephys_resampled[:len(self.spad_resampled)]
        self.spad_align=self.spad_resampled
        #lfp_path=os.path.join(self.dpath, "LFP_align_10kHz.pkl")
        #lfp_new.to_pickle(lfp_path) 
        #spad_path=os.path.join(self.dpath, "SPAD_align_10kHz.pkl")
        #spad_resampled.to_pickle(spad_path) 
        # Create the plot 
        return self.spad_align, self.ephys_align
    
    def read_tracking_data (self):
        keyword='Tracking'
        files_in_directory = os.listdir(self.dpath)
        matching_files = [filename for filename in files_in_directory if keyword in filename]
        if matching_files:
            csv_file_path = os.path.join(self.dpath, matching_files[0])
            self.trackingdata = pd.read_csv(csv_file_path)
            self.trackingdata=self.trackingdata.fillna(method='ffill')
            self.trackingdata=self.trackingdata/20
            self.trackingdata['speed']=self.trackingdata.X.diff() #This is to calculate the speed per frame
            self.trackingdata['speed']=self.trackingdata['speed']*30 # cm per second
            self.trackingdata['speed'] = self.trackingdata['speed'].fillna(method='bfill')
            self.trackingdata['speed_abs']=self.trackingdata.speed.abs()
            OE.plot_animal_tracking (self.trackingdata)
        else:
            print ('No available Tracking data in the folder!')
        return self.trackingdata
    
    def Format_tracking_data_index (self):
        time_interval = 1.0 / self.tracking_fs
        total_duration = len(self.trackingdata) * time_interval
        timestamps = np.arange(0, total_duration, time_interval)
        timedeltas_index = pd.to_timedelta(timestamps, unit='s')            
        self.trackingdata.index = timedeltas_index
        return self.trackingdata
    
    def resample_tracking_to_ephys (self):
        time_interval_common = 1.0 / self.ephys_fs
        tracking_resampled_to_ephys = self.trackingdata.resample(f'{time_interval_common:.9f}S').mean()
        tracking_resampled_to_ephys = tracking_resampled_to_ephys.fillna(method='ffill')
        return tracking_resampled_to_ephys    
    
    def count_frames_and_indices(self, threshold=29000):
        frame_count = 0
        frame_indices = []
        prev_value = self.Ephys_data['CamSync'][0] > threshold
        
        for i, value in enumerate(self.Ephys_data['CamSync']):
            current_value = value > threshold
            if current_value != prev_value:
                frame_count += 1
                frame_indices.append(i)
            prev_value = current_value        
        return frame_count, frame_indices
    
    def extent_tracking_to_ephys_pd (self):
        frame_count, frame_indices=self.count_frames_and_indices()
        if len(self.trackingdata)>frame_count:            
            self.trackingdata=self.trackingdata[1:frame_count+1]
        if len(self.trackingdata)<frame_count:
            frame_indices=frame_indices[0:len(self.trackingdata)]
        trackingdata_extent = pd.DataFrame(index=range(len(self.Ephys_data)), columns=self.trackingdata.columns)
        trackingdata_extent.loc[frame_indices,:] = self.trackingdata.values
        trackingdata_extent=trackingdata_extent.fillna(method='bfill')
        trackingdata_extent=trackingdata_extent.fillna(method='ffill')  
        return trackingdata_extent,frame_count, frame_indices
    
    def save_data (self, data,filename):
        filepath=os.path.join(self.dpath, filename)
        data.to_pickle(filepath)
        return -1
        
    
    def low_pass_two_traces (self, spad_data,lfp_data, lowpassFreq):
        spad_lowpass= OE.butter_filter(spad_data, btype='low', cutoff=lowpassFreq, fs=self.fs, order=5)
        lfp_lowpass = OE.butter_filter(lfp_data, btype='low', cutoff=lowpassFreq, fs=self.fs, order=5)
        spad_low = pd.Series(spad_lowpass, index=spad_data.index)
        lfp_low = pd.Series(lfp_lowpass, index=lfp_data.index)
        return spad_low,lfp_low
    
    def slicing_pd_data (self, data,start_time, end_time):
        # Start time in seconds
        # End time in seconds
        time_interval = 1 / self.fs # Time interval in seconds      
        slicing_index = pd.timedelta_range(start=f'{start_time}S', end=f'{end_time}S', freq=f'{time_interval}S')   
        silced_data=data.loc[slicing_index]
        return silced_data
    
    def slicing_np_data (self, data,start_time, end_time):
        # Start time in seconds
        # End time in seconds
        start_idx =int( start_time * self.fs)# Time interval in seconds   
        end_idx = int(end_time * self.fs)# Time interval in seconds
        silced_data=data[start_idx:end_idx]
        return silced_data
    
        
    def plot_two_traces (self, spad_data,lfp_data, speed_series, spad_label='spad',lfp_label='LFP'):
        fig, (ax1, ax2, ax3,ax4) = plt.subplots(4, 1, figsize=(16, 12))
        OE.plot_trace_seconds (spad_data,ax1,label=spad_label,color=sns.color_palette("husl", 8)[3],
                               ylabel='z-score',xlabel=False)
        OE.plot_trace_seconds (lfp_data,ax2,label=lfp_label,color=sns.color_palette("husl", 8)[5],ylabel='mV')
        pcm=OE.plotSpectrogram (ax3,lfp_data,plot_unit='WHz',nperseg=4096,y_lim=250,v_max = 8,Fs=self.fs,showCbar=False)
        # # Create a new axis for the color bar
        # divider = make_axes_locatable(ax3)
        # cax = divider.append_axes("right", size="2%", pad=0.2)  # Adjust 'pad' to control the distance between plot and colorbar
        # cbar = plt.colorbar(pcm,cax=cax)
        # cbar.set_label('W/Hz')  # Set color bar label
        OE.plot_speed_heatmap(ax4, speed_series)
        plt.subplots_adjust(hspace=0.2)
        #plt.tight_layout()
        plt.show()
        return fig
             
    def get_detrend(self, data):
         data_detrend = signal.detrend(data)
         return data_detrend
        
    def calculate_correlation (self, data1,data2):
        '''normalize'''
        s1 = (data1 - np.mean(data1)) / (np.std(data1))
        s2 = (data2 - np.mean(data2)) / (np.std(data2))
        lags=signal.correlation_lags(len(data1), len(data2), mode='full') 
        corr=signal.correlate(s1, s2, mode='full', method='auto')/len(data1)
        return lags,corr
    
    def calculate_correlation_with_detrend (self, spad_data,lfp_data):
        if isinstance(spad_data, (pd.DataFrame, pd.Series)):
            spad_np=spad_data.values
        else:
            spad_np=spad_data
        if isinstance(lfp_data, (pd.DataFrame, pd.Series)):
            lfp_np=lfp_data.values
        else:
            lfp_np=spad_data
            
        spad_1=self.get_detrend(spad_np)
        lags,corr=self.calculate_correlation (spad_1,lfp_np)
        return lags,corr
    
    def plot_corr_line (self, lags,corr,ax,frametime=0.1, title='Cross Correlation'):
        lags_ms=lags*frametime
        ax.plot(lags_ms,corr,label='mean_cross_correlation',zorder=2)

        ax.set_xlabel('lags(ms)',fontsize=10)
        ax.set_ylabel('Normalized Cross Correlation',fontsize=10)
        ax.legend(fontsize=8)
        ax.set_title(title,fontsize=10)
        return  ax
    
    def get_mean_corr_two_traces (self, spad_data,lfp_data,corr_window):
        # corr_window as second
        total_second=len(spad_data)/self.fs 
        print('total_second:',total_second)
        total_num=int(total_second-corr_window)
        print('total_num:',total_num)
        Corr_sum=0
        for i in range(total_num):
            spad_1=self.slicing_pd_data (spad_data,start_time=i, end_time=i+corr_window)
            lfp_1=self.slicing_pd_data (lfp_data,start_time=i, end_time=i+corr_window)
            lags,corr =self.calculate_correlation_with_detrend (spad_1,lfp_1)
            Corr_sum=Corr_sum+corr
            print('Corr_sum 1:',Corr_sum[0])
        Corr_mean=Corr_sum/total_num
        return lags,Corr_mean,Corr_sum    
    
    def pynappleAnalysis (self,lfp_channel='LFP_2'):
        'This is the LFP data that need to be saved for the sync ananlysis'
        #LFP_data=EphysData['LFP_2']
        timestamps=self.Ephys_data['timestamps'].copy()
        timestamps=timestamps.to_numpy()
        timestamps=timestamps-timestamps[0]
        lfp_data=self.Ephys_data[lfp_channel]
        'To plot the LFP data using the pynapple method'
        LFP=nap.Tsd(t = timestamps, d = lfp_data.to_numpy(), time_units = 's')
        fig, ax = plt.subplots(figsize=(18,5))
        ax.plot(LFP.as_units('s'))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel("Time (s)")
        ax.set_title('LFP raw data')
        return -1

    