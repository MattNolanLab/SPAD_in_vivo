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

def FindHotPixel(dpath,BinData,thres=0.1):
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
    HotPixelIdx_read=np.genfromtxt(IdxFilename, delimiter=',')
    HotPixelIdx_read=HotPixelIdx_read.astype(int)
    BinData=RemoveHotPixel(BinData,HotPixelIdx_read)
    return BinData


def ShowImage(BinData,dpath):
    '''Show the accumulated image'''
    from PIL import Image
    PixelArrary=np.sum(BinData, axis=0)
    # Pixel = (((PixelArrary - PixelArrary.min()) / (PixelArrary.max() - 
    #                                                 PixelArrary.min())) * 255.9).astype(np.uint8)
    Pixel = (((PixelArrary - PixelArrary.min()) / (PixelArrary.max() - 
                                                    PixelArrary.min())) * 256).astype(np.uint8)
    img = Image.fromarray(Pixel)
    img.show()
    filename = os.path.join(dpath, "FOV_image.png")
    img.save(filename)
    
    # im = plt.imshow(Pixel, cmap='gray', interpolation='none')
    # cbar = plt.colorbar(im)
    # plt.show()   

    return img


#%%
def main():
    #Set path
    #dpath="C:/SPAD/SPADData/20220413/1432002_Green100mA_2022_4_13_16_48_35"# Sim1 Cre
    dpath="C:/SPAD/SPADData/20220423/1454214_Red50mA_2022_4_23_13_32_0"# PV cre
    filename = os.path.join(dpath, "spc_data1.bin")
    Bindata=SPADreadBin(filename,pyGUI=False)
    ShowImage(Bindata,dpath)
    count_value,HotPixelNum=countTraceValue(dpath,Bindata,xxrange=[80,180],yyrange=[30,150]) ##For animals
    #count_value,HotPixelNum=countTraceValue(dpath,Bindata,xxrange=[10,310],yyrange=[10,230])
    ShowImage(Bindata,dpath)
    print(HotPixelNum)

    plt.figure(figsize=(20, 6))
    plt.plot(count_value,linewidth=1)
    plt.title("trace")
    
    return -1

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()