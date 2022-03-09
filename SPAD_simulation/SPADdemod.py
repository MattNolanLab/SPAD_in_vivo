# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:36:16 2022

@author: Yifang
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import irfft, rfft, rfftfreq
from scipy.signal import hilbert
import scipy


#%%
def ShowRFFT(count_value,fs=9938.4):
    sample_number=len(count_value)
    print ('sample_number is', sample_number)
    
    yf = rfft(count_value)
    xf = rfftfreq(sample_number, 1 / fs)
    #plt.plot(xf, yf)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xf, np.abs(yf))
    return fig, ax

def plotDemodFreq (mixedTrace,envelope,xf,yfMixed,yfEnvelope,color):
    '''
    Plot 
    1.Separated single channel mixed signal.
    2.Single channel spectrum.
    3.Zoomed window of modulated signal and envelope
    4.Spectrum of recovered signal
    '''
    sample_points=np.arange(len(mixedTrace)) #timeline in sample points    
    
    fig, ((ax0, ax2), (ax1,ax3)) = plt.subplots(2,2)
    ax0.plot(sample_points, mixedTrace, label='Modulated',linewidth=1)
    ax0.plot(sample_points, envelope, color=color,label='Envelope',linewidth=1)
    ax0.legend(loc='best')
    
    ax1.plot(sample_points, mixedTrace, label='Modulated',linewidth=1)
    ax1.plot(sample_points, envelope,color=color,label='Envelope',linewidth=1)
    ax1.set_xlim(2000,2200)
    ax1.set_xlabel("Time in frames")
    ax1.legend(loc='best')
    
    ax2.plot(xf, np.abs(yfMixed), label='Modulated spectrum',linewidth=1)
    ax2.legend(loc='best')
    
    ax3.plot(xf, np.abs(yfEnvelope), label='Envelope spectrum',color=color,linewidth=1)
    ax3.set_xlabel("Frequency")
    ax3.legend(loc='best')
    ax3.set_xlim(-10,100)    
    fig.tight_layout()
    return fig

def plotTwoChannel (mixed_red,envelope_red,mixed_green,envelope_green,zoomWindw=[2000,2200]):
    '''
    Plot Two Color
    '''
    sample_points=np.arange(len(mixed_red)) #timeline in sample points    
    
    fig, (ax0,ax1,ax2,ax3) = plt.subplots(nrows=4)
    #ax0.plot(sample_points, mixed_red, label='Red Mixed',linewidth=1)
    ax0.plot(sample_points, envelope_red, color='r',label='Red Envelope',linewidth=1)
    #ax0.legend(loc='best')
    
    #ax1.plot(sample_points, mixed_red, label='Red Mixed',linewidth=1)
    ax1.plot(sample_points, envelope_red,color='r',label='Envelope',linewidth=1)
    ax1.set_xlim(zoomWindw)
    ax1.legend(loc='upper right')
    
    #ax2.plot(sample_points, mixed_green, label='Green Mixed',linewidth=1)
    ax2.plot(sample_points, envelope_green,color='g',label='Envelope',linewidth=1)    
    
    #ax3.plot(sample_points, mixed_green, label='Green Mixed',linewidth=1)
    ax3.plot(sample_points, envelope_green,color='g',label='Envelope',linewidth=1)
    ax3.legend(loc='upper right')
    ax3.set_xlim(zoomWindw)   
    ax3.set_xlabel("Time in frames")
    fig.tight_layout()
    return fig


def butter_filter(data, btype='low', cutoff=10, fs=9938.4, order=10):   
    # cutoff and fs in Hz
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype=btype, analog=False)
    y = scipy.signal.filtfilt(b, a, data, axis=0)
    return y

def DemodFreqShift_Bandpass (count_value,fc_g,fc_r,fs=10000):
    sample_number=len(count_value)
    sample_points=np.arange(sample_number) #timeline in sample points
    print ('sample_number is', sample_number)
    print ('sampling rage is', fs)
    
    trace1=butter_filter(count_value, btype='low', cutoff=3000, fs=10000, order=10)
    print ('High frequency noise above 3kHz removed')
    # trace2=butter_filter(trace1, btype='high', cutoff=10, fs=10000, order=10)
    # print ('Low frequency noise below 10Hz removed')
    
    yf = rfft(trace1)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax1,ax2) = plt.subplots(nrows=2)
    ax1.plot(sample_points, trace1,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Freq Peaks (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    #ax2.set_ylim(-10,1e6)
    fig.tight_layout() 

    
    '''The maximum frequency is half the sample rate'''
    points_per_freq = len(xf) / (fs/2)
    fc_g_idx = int(points_per_freq * fc_g)
    sideBand=int(points_per_freq * 300) 
    fc_r_idx = int(points_per_freq * fc_r) 
    print ('fc_green is',fc_g)
    print ('fc_red is',fc_r)
    print ('fc_g_idx is',fc_g_idx)
    print ('sideBand_idx is',sideBand)
    print ('fc_r_idx is',fc_r_idx)
  
    '''For red---bandpass filter'''
    signal_r = butter_filter(trace1, btype='high', cutoff=1700, fs=10000, order=10) 
    yf_r = rfft(signal_r)
    print ('For red channal, keep 1kHz band')    
    
    '''Hilbert transform--red'''
    analytic_signal = hilbert(signal_r)
    red_recovered = np.abs(analytic_signal)
    yf_rre = rfft(red_recovered)
    
    '''For green---bandpass filter'''
    signal_g = butter_filter(trace1, btype='low', cutoff=1300, fs=10000, order=10) 
    yf_g = rfft(signal_g)
    print ('For green channal, keep 2kHz band')   
    
    '''Hilbert transform--green'''
    analytic_signal = hilbert(signal_g)
    green_recovered = np.abs(analytic_signal)
    yf_gre = rfft(green_recovered)          
    
    '''PLOT TO COMPARE'''
    fig=plotDemodFreq (mixedTrace=signal_r,envelope=red_recovered,
                    xf=xf,yfMixed=yf_r,yfEnvelope=yf_rre,color='r') 
    
    fig=plotDemodFreq (mixedTrace=signal_g,envelope=green_recovered,
                    xf=xf,yfMixed=yf_g,yfEnvelope=yf_gre,color='g')  
    
    fig=plotTwoChannel (mixed_red=signal_r,envelope_red=red_recovered,
                        mixed_green=signal_g,envelope_green=green_recovered,
                        zoomWindw=[4000,5000]) 
    
    return red_recovered,green_recovered

def DemodFreqShift (count_value,fc_g,fc_r,fs=9938.4):
    sample_number=len(count_value)
    sample_points=np.arange(sample_number) #timeline in sample points
    print ('sample_number is', sample_number)
    print ('sampling rage is', fs)
    
    yf = rfft(count_value)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax1,ax2) = plt.subplots(nrows=2)
    ax1.plot(sample_points, count_value,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Freq Peaks (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    ax2.set_xlim(0,200)
    #ax2.set_ylim(0,1e5)
    fig.tight_layout() 
    
    '''Remove unwanted low/high frequencies and demodulation'''
    yf[0:100] = 0 
    yf[3060:]=0
    
    mix = irfft(yf)
    
    fig, (ax1,ax2) = plt.subplots(nrows=2)
    ax1.plot(sample_points, mix,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Freq Peaks (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    ax2.set_xlim(-10,2200)
    fig.tight_layout() 
    
    print ('High frequency noise around 4kHz removed')
    print ('Low frequency noise removed (Hz):','[0:20]')
    yf_g = np.copy(yf)
    yf_r=np.copy(yf)
    
    '''The maximum frequency is half the sample rate'''
    points_per_freq = len(xf) / (fs/2)
    fc_g_idx = int(points_per_freq * fc_g)
    sideBand=int(points_per_freq * 250) 
    fc_r_idx = int(points_per_freq * fc_r) 
    print ('fc_green is',fc_g)
    print ('fc_red is',fc_r)
    print ('fc_g_idx is',fc_g_idx)
    print ('sideBand_idx is',sideBand)
    print ('fc_r_idx is',fc_r_idx)
    
    '''For red---remove unwanted band'''
    # yf_r[fc_g_idx - sideBand : fc_g_idx + sideBand] = 0 
    # signal_r = irfft(yf_r)
    # print ('For red channal, remove band:',fc_g_idx - sideBand,'to',fc_g_idx + sideBand)
    '''For red---preserve wanted band'''
    yf_r[0: fc_r_idx - sideBand] = 0 
    yf_r[fc_r_idx + sideBand : ] = 0 
    signal_r = irfft(yf_r)    
    print ('For red channal, keep band:',fc_r_idx - sideBand,'to',fc_r_idx + sideBand)    
    '''Hilbert transform--red'''
    analytic_signal = hilbert(signal_r)
    red_recovered = np.abs(analytic_signal)
    yf_rre = rfft(red_recovered)
        
    '''For green'''
    # yf_g[fc_r_idx - sideBand : fc_r_idx + sideBand] = 0 
    # signal_g = irfft(yf_g)
    # print ('For green channal, remove band:',fc_r_idx - sideBand,'to',fc_r_idx + sideBand)   
    '''For green'''
    yf_g[0: fc_g_idx - sideBand] = 0 
    yf_g[fc_g_idx + sideBand : ] = 0 
    signal_g = irfft(yf_g)
    print ('For green channal, keep band:',fc_g_idx - sideBand,'to',fc_g_idx + sideBand)   
    '''Hilbert transform--green'''
    analytic_signal = hilbert(signal_g)
    green_recovered = np.abs(analytic_signal)
    yf_gre = rfft(green_recovered)          
    
    '''PLOT TO COMPARE'''
    fig=plotDemodFreq (mixedTrace=signal_r,envelope=red_recovered,
                    xf=xf,yfMixed=yf_r,yfEnvelope=yf_rre,color='r') 
    
    fig=plotDemodFreq (mixedTrace=signal_g,envelope=green_recovered,
                    xf=xf,yfMixed=yf_g,yfEnvelope=yf_gre,color='g')  
    
    fig=plotTwoChannel (mixed_red=signal_r,envelope_red=red_recovered,
                        mixed_green=signal_g,envelope_green=green_recovered,
                        zoomWindw=[4000,6000])
    return red_recovered,green_recovered

def DemodPhaseShift (count_value,fc,ini_phase=0,fs=9938.4):
    sample_number=len(count_value)
    sample_points=np.arange(sample_number) #timeline in sample points
    print ('sample_number is', sample_number)
    print ('sampling rage is', fs)
    
    yf = rfft(count_value)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax1,ax2) = plt.subplots(nrows=2)
    ax1.plot(sample_points, count_value,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Freq Peaks (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    #ax2.set_ylim(-10,1e8)
    fig.tight_layout() 
    
    
    '''Remove unwanted low/high frequencies and demodulation'''
    yf[0:100] = 0 
    print ('Low frequency noise removed (Hz):','[0:100]')
    
    mix = irfft(yf)
    
    fig, (ax1,ax2) = plt.subplots(nrows=2)
    ax1.plot(sample_points, mix,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Freq Peaks (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    ax2.set_xlim(995,1005)
    fig.tight_layout()
    
    '''Simulate the carrier signals'''
    t = np.arange(sample_number)/fs #timeline in seconds
    pi=np.pi 
    
    green_c=np.sin(2*pi*(fc)*t+ini_phase) #Amplitude of green is lower
    red_c=np.sin(2*pi*fc*t+pi/2+ini_phase) #red carrier is pi/2 phase shifted
    
    print ('Demodulate signals')
    green_d=mix*green_c
    red_d=mix*red_c    
    
    '''Remove unwanted frequencies and demodulation'''
    '''For red'''
    yf = rfft(red_d)
    xf = rfftfreq(sample_number, 1 / fs)
    
    yf_r=np.copy(yf)
    # #remove high frequecy sprectrum
    yf_r[250:] = 0
    #Inverse rfft
    red_recovered = irfft(yf_r)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, red_recovered,color='r',label='red_recovered')
    ax0.set_xlabel("time in frames")
    ax0.legend(loc='upper right')
    ax1.plot(xf, np.abs(yf), label='red mixed spectrum')
    ax1.legend(loc='upper right')
    ax1.set_ylim(-10,1e7)

    ax2.plot(xf, np.abs(yf_r), label='red recovered spectrum')
    ax2.set_xlabel("Frequency")
    #ax2.set_xlim(-10,50)
    ax2.legend(loc='upper right')
    fig.tight_layout()
        
    '''For green'''
    yf = rfft(green_d)
    xf = rfftfreq(sample_number, 1 / fs)
     
    yf_g=np.copy(yf)
    yf_g[250:] = 0

    #Inverse rfft
    green_recovered = irfft(yf_g)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, green_recovered,color='g',label='green_recovered')
    ax0.set_xlabel("time in frames")
    ax0.legend(loc='upper right')
    ax1.plot(xf, np.abs(yf), label='green mixed spectrum')
    ax1.legend(loc='upper right')
    ax1.set_ylim(-10,1e7)
    ax2.plot(xf, np.abs(yf_g), label='green recovered spectrum')
    ax2.set_xlabel("Frequency")
    #ax2.set_xlim(-2,20)
    ax2.legend(loc='upper right')
    fig.tight_layout()
    
    '''PLOT TO COMPARE'''
    # fig=plotDemodFreq (mixedTrace=signal_r,envelope=red_recovered,
    #                 xf=xf,yfMixed=yf_r,yfEnvelope=yf_rre,color='r') 
    
    # fig=plotDemodFreq (mixedTrace=signal_g,envelope=green_recovered,
    #                 xf=xf,yfMixed=yf_g,yfEnvelope=yf_gre,color='g')  
    
    # fig=plotTwoChannel (mixed_red=signal_r,envelope_red=red_recovered,
    #                     mixed_green=signal_g,envelope_green=green_recovered,
    #                     zoomWindw=[4000,6000])
    return red_recovered,green_recovered
#%%
def main():
    dpath="C:/SPAD/SPADData/20220303/2022_3_3_17_21_7_r2_DiI"
    filename = os.path.join(dpath, "traceValue.csv")  #csv file is the file contain values for each frame
    count_value = np.genfromtxt(filename, delimiter=',')
    '''PLOT the trace'''
    plt.figure(figsize=(10, 6))
    plt.plot(count_value,linewidth=1)
    plt.title("trace")
    '''PLOT the details of the trace'''
    plt.figure()
    plt.plot(count_value,linewidth=1)
    plt.xlim(2000,2200)
    
    '''Using freq shift modulation'''
    red_recovered,green_recovered=DemodFreqShift (count_value,fc_g=1000,fc_r=2000,fs=9938.4)
    '''Using phase shift modulation'''
    #red_recovered,green_recovered=DemodPhaseShift (count_value,fc=1000,ini_phase=(-0.848* np.pi))
    
    return -1

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
        
        