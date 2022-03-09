# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 08:32:38 2022

@author: Yifang
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq,irfft,ifft, rfft, rfftfreq
from scipy.signal import hilbert
from scipy import signal

sample_number=int(2000)
fc_g=2000 #carrier frequency
fc_r=1000 #also used for phase shift carriers

fm_g=10
fm_r=15  #modulating signal frequency
fs=10000  #sampling rate

duration=sample_number/fs #second
sample_points=np.arange(sample_number) #timeline in sample points
t = np.arange(sample_number)/fs #timeline in seconds
pi=np.pi

def SimulateRawSignal (sample_number,fm_g,fm_r,fs):
    sample_points=np.arange(sample_number) #timeline in sample points
    t = np.arange(sample_number)/fs #timeline in seconds
    pi=np.pi 
    print ('Simulating modulating signals.')
    green_sig=np.sin(2*pi*fm_g*t)
    red_sig=np.sin(2*pi*fm_r*t)
    mix_sig=green_sig+red_sig
    yf = rfft(mix_sig)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, green_sig, color='g',label='green_'+str(fm_g)+'Hz')
    ax0.plot(sample_points, red_sig, color='r',label='red_'+str(fm_r)+'Hz')
    ax0.set_title('Modulating Sinals')
    ax0.legend(loc='upper right')
    ax1.plot(sample_points, mix_sig,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_ylim(0.0, 120.0)
    ax2.plot(xf, np.abs(yf),color='b',label='Specrum (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    ax2.set_xlim(0, 100)
    fig.tight_layout()    
    return green_sig,red_sig

def SimulateRawSignal_square (sample_number,fm_g,fm_r,fs):
    sample_points=np.arange(sample_number) #timeline in sample points
    t = np.arange(sample_number)/fs #timeline in seconds
    pi=np.pi 
    print ('Simulating modulating signals.')
    green_sig=signal.square(2 * pi * fm_g * t)
    red_sig=signal.square(2 * pi * fm_r * t)
    mix_sig=green_sig+red_sig
    yf = rfft(mix_sig)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, green_sig, color='g',label='green_'+str(fm_g)+'Hz')
    ax0.plot(sample_points, red_sig, color='r',label='red_'+str(fm_r)+'Hz')
    ax0.set_title('Modulating Sinals')
    ax0.legend(loc='upper right')
    ax1.plot(sample_points, mix_sig,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_ylim(0.0, 120.0)
    ax2.plot(xf, np.abs(yf),color='b',label='Specrum (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    ax2.set_xlim(0, 100)
    fig.tight_layout()    
    return green_sig,red_sig

def SimulateFreqShiftCarriers (sample_number,fc_g,fc_r,fs):
    sample_points=np.arange(sample_number) #timeline in sample points
    t = np.arange(sample_number)/fs #timeline in seconds
    pi=np.pi 
    print ('Simulating carrier signals.')
    
    green_c=10*np.sin(2*pi*fc_g*t)
    red_c=50*np.sin(2*pi*fc_r*t)
    mix_carrier=green_c+red_c
    yf = rfft(mix_carrier)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, green_c, color='g',label='green_'+str(fc_g)+'Hz')
    ax0.plot(sample_points, red_c, color='r',label='red_'+str(fc_r)+'Hz')
    ax0.set_title('Freq Shifted Carrier Sine waves')
    ax0.legend(loc='upper right')
    ax0.set_xlim(0,100)
    ax1.plot(sample_points, mix_carrier,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Specrum (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    fig.tight_layout() 
    return green_c,red_c

def SimulateDemodFreq (sample_number,green_sig,red_sig,green_c,red_c,fc_g,fc_r,fs):
    green_total=(1+1/10*green_sig)*green_c
    red_total=(1+1/50*red_sig)*red_c
    mix_total=green_total+red_total
    
    yf = rfft(mix_total)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    
    ax0.plot(sample_points, red_total, color='r',label='red_'+str(fc_r)+'Hz')
    ax0.plot(sample_points, green_total, color='g',label='green_'+str(fc_g)+'Hz')
    ax0.set_title('Modulated signals')
    ax0.legend(loc='upper right')
    #ax0.set_xlim(0,100)
    ax1.plot(sample_points, mix_total,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Specrum (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    fig.tight_layout() 
    
    print ('Demodulate signals')
    yf_g = np.copy(yf)
    yf_r=np.copy(yf)
    '''Remove unwanted frequencies and demodulation'''
    '''The maximum frequency is half the sample rate'''
    points_per_freq = len(xf) / (fs/2)
    fc_g_idx = int(points_per_freq * fc_g)
    sideBand=int(points_per_freq * 250)
    fc_r_idx = int(points_per_freq * fc_r) 
    '''For red'''
    yf_r[fc_g_idx - sideBand : fc_g_idx + sideBand] = 0 
    signal_r = irfft(yf_r)
    
    '''Hilbert transform--red'''
    analytic_signal = hilbert(signal_r)
    red_recovered = np.abs(analytic_signal)
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, signal_r, label='mixed_red')
    ax0.plot(sample_points, red_recovered, label='envelope_red')
    ax0.legend(loc='upper right')
    ax1.plot(sample_points, red_recovered,color='r',label='envelope_red')
    ax1.set_xlabel("time in seconds")
    ax1.legend(loc='upper right')
    ax2.plot(xf, np.abs(yf_r), label='red spectrum')
    ax2.set_xlabel("Frequency")
    ax2.legend(loc='upper right')
    fig.tight_layout()
    
    '''For green'''
    yf_g[fc_r_idx - sideBand : fc_r_idx + sideBand] = 0 
    signal_g = irfft(yf_g)

    '''Hilbert transform--green'''
    analytic_signal = hilbert(signal_g)
    green_recovered = np.abs(analytic_signal)
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, signal_g, label='mixed_green')
    ax0.plot(sample_points, green_recovered, label='envelope_green')
    ax0.legend(loc='upper right')
    ax1.plot(sample_points, green_recovered,color='g',label='envelope_green')
    ax1.set_xlabel("time in seconds")
    ax1.legend(loc='upper right')
    ax2.plot(xf, np.abs(yf_g), label='green spectrum')
    ax2.set_xlabel("Frequency")
    ax2.legend(loc='upper right')
    
    fig.tight_layout()
    return red_recovered,green_recovered

def SimulatePhaseShiftCarriers (sample_number,fc,fs):
    sample_points=np.arange(sample_number) #timeline in sample points
    t = np.arange(sample_number)/fs #timeline in seconds
    pi=np.pi 
    print ('Simulating carrier signals.')
    
    green_c=10*np.sin(2*pi*fc*t) #Amplitude of green is lower
    red_c=50*np.sin(2*pi*fc*t+pi/2) #red carrier is pi/2 phase shifted
    mix_carrier=green_c+red_c
    yf = fft(mix_carrier)
    xf = fftfreq(sample_number, 1 / fs)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, green_c, color='g',label='green_'+str(fc)+'Hz')
    ax0.plot(sample_points, red_c, color='r',label='red_'+str(fc)+'Hz')
    ax0.set_title('Phase shifted Carrier Sine waves')
    ax0.legend(loc='upper right')
    ax0.set_xlim(0,100)
    ax1.plot(sample_points, mix_carrier,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Spectrum (fft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    fig.tight_layout() 
    return green_c,red_c

def SimulateDemodPhase (sample_number,green_sig,red_sig,green_c,red_c,fc,fs):
    '''Mixing signals'''  
    green_total=(1+1/10*green_sig)*green_c
    red_total=(1+1/50*red_sig)*red_c
    mix_total=green_total+red_total
    
    yf = rfft(mix_total)
    xf = rfftfreq(sample_number, 1 / fs)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    
    ax0.plot(sample_points, red_total, color='r',label='red_'+str(fc)+'Hz')
    ax0.plot(sample_points, green_total, color='g',label='green_'+str(fc)+'Hz')
    ax0.set_title('Modulated signals')
    ax0.legend(loc='upper right')
    #ax0.set_xlim(0,100)
    ax1.plot(sample_points, mix_total,color='b',label='Mixed')
    ax1.set_xlabel("time in frames")
    ax1.legend(loc='upper right')
    #ax1.set_xlim(0,100)
    ax2.plot(xf, np.abs(yf),color='b',label='Specrum (rfft)')
    ax2.set_xlabel("frequency in Hz")
    ax2.legend(loc='upper right')
    fig.tight_layout() 
    
    print ('Demodulate signals')
    green_d=mix_total*green_c
    red_d=mix_total*red_c
    
    '''Remove unwanted frequencies and demodulation'''
    '''For red'''
    yf = rfft(red_d)
    xf = rfftfreq(sample_number, 1 / fs)
    #remove 0
    yf_r=np.copy(yf)
    yf_r[0] = 0
    #remove high frequecy sprectrum
    points_per_freq = len(xf) / (fs/2)
    fc_idx = int(points_per_freq * 2*fc_r) 
    yf_r[fc_idx-300:fc_idx+300] = 0
    #Inverse rfft
    red_recovered = irfft(yf_r)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, red_recovered,color='r',label='red_recovered')
    ax0.set_xlabel("time in frames")
    ax0.legend(loc='upper right')
    ax1.plot(xf, np.abs(yf), label='red mixed spectrum')
    ax1.legend(loc='upper right')
    ax2.plot(xf, np.abs(yf_r), label='red recovered spectrum')
    ax2.set_xlabel("Frequency")
    ax2.set_xlim(-10,50)
    ax2.legend(loc='upper right')
    fig.tight_layout()
    
    '''For green'''
    yf = rfft(green_d)
    xf = rfftfreq(sample_number, 1 / fs)
    #remove 0
    yf_g=np.copy(yf)
    yf_g[0] = 0
    #remove high frequecy sprectrum
    points_per_freq = len(xf) / (fs/2)
    fc_idx = int(points_per_freq * 2*fc_r) 
    yf_g[fc_idx-300:fc_idx+300] = 0
    #Inverse rfft
    green_recovered = irfft(yf_g)
    
    fig, (ax0, ax1,ax2) = plt.subplots(nrows=3)
    ax0.plot(sample_points, green_recovered,color='g',label='green_recovered')
    ax0.set_xlabel("time in frames")
    ax0.legend(loc='upper right')
    ax1.plot(xf, np.abs(yf), label='green mixed spectrum')
    ax1.legend(loc='upper right')
    ax2.plot(xf, np.abs(yf_g), label='green recovered spectrum')
    ax2.set_xlabel("Frequency")
    ax2.set_xlim(-10,50)
    ax2.legend(loc='upper right')
    fig.tight_layout()
    return red_recovered,green_recovered


def main():
    '''Main excutive command for Simulating frequency shift modulation'''
    print ('Simulating frequency shift modulation for sine wave')
    green_sig,red_sig=SimulateRawSignal (sample_number,fm_g,fm_r,fs)
    green_c,red_c=SimulateFreqShiftCarriers (sample_number,fc_g,fc_r,fs)
    red_recovered,green_recovered=SimulateDemodFreq (sample_number,green_sig,red_sig,green_c,red_c,fc_g,fc_r,fs)

    '''Main excutive command for Simulating frequency shift modulation---square wave'''
    print ('Simulating frequency shift modulation for square wave')
    green_sig,red_sig=SimulateRawSignal_square (sample_number,fm_g,fm_r,fs)
    green_c,red_c=SimulateFreqShiftCarriers (sample_number,fc_g,fc_r,fs)
    red_recovered,green_recovered=SimulateDemodFreq (sample_number,green_sig,red_sig,green_c,red_c,fc_g,fc_r,fs)

    '''Main excutive command for Simulating Phase shift modulation'''
    print ('Simulating phase shift modulation for sine wave')
    fc=1000
    green_sig,red_sig=SimulateRawSignal (sample_number,fm_g,fm_r,fs)
    green_c,red_c=SimulatePhaseShiftCarriers (sample_number,fc_r,fs)
    red_recovered,green_recovered=SimulateDemodPhase (sample_number,green_sig,red_sig,green_c,red_c,fc,fs)

    #%%
    '''Main excutive command for Simulating Phase shift modulation------square wave'''
    print ('Simulating phase shift modulation for square wave')
    green_sig,red_sig=SimulateRawSignal_square (sample_number,fm_g,fm_r,fs)
    green_c,red_c=SimulatePhaseShiftCarriers (sample_number,fc_r,fs)
    red_recovered,green_recovered=SimulateDemodPhase (sample_number,green_sig,red_sig,green_c,red_c,fc,fs)
    
    return -1

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
