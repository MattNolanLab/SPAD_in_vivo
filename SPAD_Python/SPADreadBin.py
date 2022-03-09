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
import scipy
import SPADdemod

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
    dtype = np.uint8
    bytedata = np.fromfile(binfile,dtype)
    '''Change bytedata to bits'''
    bytedatasize=len(bytedata) #bytesize=9600*bit plane blocks/frames
    print('bytedatasize is',bytedatasize)
    blocksize=int(bytedatasize/(9600*yrange/240))
    print('blocksize is', blocksize)
    ByteData_bi = np.unpackbits(bytedata)
    '''Reshape the data to block number*frame number*framesize'''
    datashape=(blocksize,)+spadRange
    BinData=np.reshape(ByteData_bi, datashape)        
    return BinData

def countTraceValue (dpath,BinData,xxrange=[10,310],yyrange=[10,230]):
    '''set ROI'''
    '''for bulk activity---fibre'''
    # xxrange=[10,310]
    # yyrange=[10,230]
    '''make a mask of ROI, 0---unmask'''
    ROImask=np.ones((240,320))
    ROImask[yyrange[0]:yyrange[1],xxrange[0]:xxrange[1]]=0
    '''photon count sum in each frame, within ROI'''
    blocksize=np.shape(BinData)[0]
    print ('blocksize is', blocksize)
    print ('---Calculate trace values----')
    count_value=np.zeros(blocksize)
    for i in range(blocksize):
        frame=BinData[i,:,:]
        frame_mask=np.ma.masked_array(frame, mask=ROImask)
        count_value[i]=frame_mask.sum()
    filename = os.path.join(dpath, "traceValue.csv")
    np.savetxt(filename, count_value, delimiter=",")
    return count_value

def ShowImage(BinData,dpath):
    '''Show the accumulated image'''
    from PIL import Image
    PixelArrary=np.sum(BinData, axis=0)
    Pixel = (((PixelArrary - PixelArrary.min()) / (PixelArrary.max() - 
                                                   PixelArrary.min())) * 255.9).astype(np.uint8)
    img = Image.fromarray(Pixel)
    img.show()
    filename = os.path.join(dpath, "FOV_image.png")
    img.save(filename)
    return img
#%%
def main():
    '''Set path'''
    dpath="C:/SPAD/SPADData/20220302/2022_3_2_16_8_52_g1r2"
    filename = os.path.join(dpath, "spc_data1.bin")
    Bindata=SPADreadBin(filename,pyGUI=False)
    count_value=countTraceValue(dpath,Bindata)

    plt.figure(figsize=(10, 6))
    plt.plot(count_value,linewidth=1)
    plt.title("trace")
    
    ShowImage(Bindata,dpath)
    
    # SPADdemod.ShowRFFT(count_value,fs=10000)
    # red_recovered,green_recovered=SPADdemod.DemodFreqShift (count_value,fc_g=1000,fc_r=2000,fs=10000)
    
    # SPADdemod.ShowRFFT(count_value,fs=10000)
    # red_recovered,green_recovered=SPADdemod.DemodFreqShift (count_value,fc_g=1000,fc_r=2000,fs=10000)
    
    return -1

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()


