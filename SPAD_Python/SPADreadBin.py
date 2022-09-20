# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 23:00:45 2022

.bin file analysis for pySPAD and MATLAB GUI
pySPAD DO NOT have ExpIndex,yrange,globalshutter at the first three bytes

@author: Yifang
"""
## .bin file analysis for pySPAD,
import os
import numpy as np
import matplotlib.pyplot as plt
import traceAnalysis as Analysis
from PIL import Image

def SPADreadBin(filename,pyGUI=True):
    binfile = open(filename, "rb") #open binfile
    yrange=240
    
    if pyGUI==False:
        '''read first three information and convert to decimal'''
        byte_first3 =binfile.read(3)

        ExpIndex=byte_first3[0] #int type
        yrange=byte_first3[1]
        globalshutter=byte_first3[2]
        print('This Experiment used MATLAB GUI')
        print('ExpIndex is', ExpIndex)
        print('yrange is', yrange)
        print('globalshutter is',globalshutter)
        '''if it is not global shutter fisrt 19200 byte does not count. So read them but not save or convert'''
        rolling_shutter_num= yrange*10*8*(1-globalshutter)*(ExpIndex==1)
        binfile.read(rolling_shutter_num)
    
    
    print ('---Reading SPAD Binary data---')
    spadRange=(yrange,320)#define SPAD sensor size, x=320,y=240
    #spadRange=(320,yrange)#define SPAD sensor size, x=320,y=240
    dtype = np.uint8
    bytedata = np.fromfile(binfile,dtype)
    '''Change bytedata to bits'''
    bytedatasize=len(bytedata) #bytesize=9600*bit plane blocks/frames
    print('bytedatasize is',bytedatasize)
    blocksize=int(bytedatasize/(9600*yrange/240))
    print('blocksize is', blocksize)
    ByteData_bi = np.unpackbits(bytedata,bitorder='little')
    #ByteData_bi = np.unpackbits(bytedata)
    '''Reshape the data to block number*frame number*framesize'''
    datashape=(blocksize,)+spadRange
    BinData=np.reshape(ByteData_bi, datashape)        
    return BinData

''' Bin data shape: [bitplane numbers (block size), 240,320]'''

def countTraceValue (dpath,BinData,xxrange=[10,310],yyrange=[10,230],filename="traceValue.csv"):
    '''set ROI'''
    '''for bulk activity---fibre'''
    # xxrange=[10,310]
    # yyrange=[10,230]
    '''make a mask of ROI, 0---unmask'''
    ROImask=np.ones((240,320))
    ROImask[yyrange[0]:yyrange[1],xxrange[0]:xxrange[1]]=0
    '''photon count sum in each frame, within ROI'''
    blocksize=np.shape(BinData)[0]
    # HotPixelIdx,HotPixelNum=FindHotPixel(BinData,blocksize,thres=0.5)
    BinData=RemoveHotPixelFromTemp(BinData)
    print ('blocksize is', blocksize)
    print ('---Calculate trace values----')
    count_value=np.zeros(blocksize)
    for i in range(blocksize):
        frame=BinData[i,:,:]
        frame_mask=np.ma.masked_array(frame, mask=ROImask)
        count_value[i]=frame_mask.sum()
    filename = os.path.join(dpath, filename)
    np.savetxt(filename, count_value, delimiter=",")
    return count_value

def FindHotPixel(dpath,BinData,thres=0.07):
    '''Show the accumulated image'''
    blocksize=np.shape(BinData)[0]
    PixelArrary=np.sum(BinData, axis=0)
    HotPixelIdx=np.argwhere(PixelArrary > thres*blocksize)
    HotPixelNum=len(HotPixelIdx)
    filename = os.path.join(dpath, "HotPixelIdx_TianPCB.csv")
    np.savetxt(filename, HotPixelIdx, delimiter=",")
    #np.save(filename, HotPixelIdx)
    return HotPixelIdx,HotPixelNum

def RemoveHotPixel(BinData,HotPixelIdx):
    rows, cols = zip(*HotPixelIdx)
    BinData[:, rows, cols] = 0
    return BinData

def RemoveHotPixelFromTemp(BinData):
    IdxFilename="C:/SPAD/SPADData/HotPixelIdx_TianPCB.csv"
    #IdxFilename="D:/20220623/HotPixelIdx_MyPCB.csv"
    
    HotPixelIdx_read=np.genfromtxt(IdxFilename, delimiter=',')
    HotPixelIdx_read=HotPixelIdx_read.astype(int)
    BinData=RemoveHotPixel(BinData,HotPixelIdx_read)
    return BinData


def readMultipleBinfiles(dpath,fileNum):
    for i in range(fileNum):
        Savefilename = "traceValue"+str(i+1)+".csv"
        Binfilename = os.path.join(dpath, "spc_data"+str(i+1)+".bin")
        Bindata=SPADreadBin(Binfilename,pyGUI=False)
        countTraceValue(dpath,Bindata,xxrange=[0,160],yyrange=[60,220],filename=Savefilename) #top green
        #countTraceValue(dpath,Bindata,xxrange=[136,167],yyrange=[151,181],filename=Savefilename) #bottom red
    trace_raw=combineTraces (dpath,fileNum)
        #ShowImage(Bindata,dpath)
    return trace_raw

def combineTraces (dpath,fileNum):
    for i in range(fileNum):
        filename = os.path.join(dpath, "traceValue"+str(i+1)+".csv")  #csv file is the file contain values for each frame
        print(filename)
        if i==0:
            trace_raw = np.genfromtxt(filename, delimiter=',')
        else:
            trace_add = np.genfromtxt(filename, delimiter=',')
            trace_raw=np.hstack((trace_raw,trace_add))
    filename = os.path.join(dpath, "traceValueAll.csv")
    np.savetxt(filename, trace_raw, delimiter=",")
    return trace_raw
def plot_trace(trace,ax, fs=9938.4, label="trace"):
    t=(len(trace)) / fs
    taxis = np.arange(len(trace)) / fs
    ax.plot(taxis,trace,linewidth=1,label=label)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim(0,t)
    ax.legend(loc="upper right", frameon=False)
    ax.set_xlabel('Time(second)')
    ax.set_ylabel('Photon Count')
    return ax


def ShowImage(BinData,dpath):
    '''Show the accumulated image'''
    BinData=RemoveHotPixelFromTemp(BinData)
    PixelArrary=np.sum(BinData, axis=0)
    magify=2
    Pixel = (((PixelArrary) / (PixelArrary.max()))*255*magify)
    Pixel = (np.where(Pixel > 255, 255, Pixel)).astype(np.uint8)
    from scipy.ndimage import gaussian_filter
    Pixel_f = gaussian_filter(Pixel, sigma=1)
    img = Image.fromarray(Pixel_f)
    img.show()
    filename = os.path.join(dpath, "FOV_image.png")
    img.save(filename) 
    return img

def ShowImage_backgroundRemoved(BinData,BinData_b,dpath):
    '''Show the accumulated image'''
    #BinData=RemoveHotPixelFromTemp(BinData)
    PixelArrary=np.sum(BinData, axis=0)-np.sum(BinData_b, axis=0)
    magify=2.5
    Pixel = (((PixelArrary) / (PixelArrary.max()))*255*magify)
    Pixel = (np.where(Pixel > 255, 255, Pixel)).astype(np.uint8)
    from scipy.ndimage import gaussian_filter
    Pixel_f = gaussian_filter(Pixel, sigma=1.2)
    img = Image.fromarray(Pixel_f)
    img.show()
    filename = os.path.join(dpath, "FOV_image.png")
    img.save(filename) 
    return img
#%%
#dpath="D:/SPAD/SPADData/20220818JuliaFish/2022_8_18_14_25_15_Voltron1_axon" 
dpath="D:/SPAD/SPADData/TianDataSample/continuous_SPAD/real_data"
#count_value=readMultipleBinfiles(dpath,4)
filename = os.path.join(dpath, "spc_data3.bin")
Bindata=SPADreadBin(filename,pyGUI=False)
#%%
'''Show image with background removed'''
dpath_b="D:/SPAD/SPADData/20220423/Baseline_Dark_2022_4_23_12_37_45" #Dark condition, Tian board
Bindata_b=SPADreadBin(os.path.join(dpath_b, "spc_data1.bin"),pyGUI=False)
#%%
ShowImage_backgroundRemoved(Bindata[0:100000,:,:],Bindata_b[0:500,:,:],dpath)
#%%
ShowImage(Bindata,dpath)
#%%
count_value=countTraceValue(dpath,Bindata,xxrange=[40,110],yyrange=[10,90]) 

#count_value=countTraceValue(dpath,Bindata,xxrange=[112,151],yyrange=[119,151]) #top green dot
#%%
fig, ax = plt.subplots(figsize=(12, 2.5))
plot_trace(count_value,ax, fs=9938.4, label="Raw data trace")
#%%
import traceAnalysis as Ananlysis
bin_window=10
Tracebinned=Ananlysis.get_bin_trace(count_value,bin_window=bin_window)
