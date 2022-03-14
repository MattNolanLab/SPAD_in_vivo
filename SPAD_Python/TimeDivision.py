# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 18:46:12 2022

@author: Yifang
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy import signal
from sklearn.decomposition import FastICA, PCA


dpath="C:/SPAD/SPADData/20210312/2022_3_12_17_49_6_gr_30duty"
filename = os.path.join(dpath, "traceValue.csv")  #csv file is the file contain values for each frame
count_value = np.genfromtxt(filename, delimiter=',')

#%%
trace=count_value
mean1= np.mean(trace)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(count_value,linewidth=1)
ax.hlines(y=mean1, xmin=0, xmax=1000, linewidth=2, color='r')
ax.set_xlim(0,100)
#%%
dutyCycle=0.3
peaks1, _ = find_peaks(trace, height=mean1,width=2,distance=7)
#peaks1, _ = find_peaks(trace,width=2,distance=7)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(trace)
ax.plot(peaks1, trace[peaks1], "x")
ax.set_xlim(0,500)
#plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()
#%%
channel1=trace[peaks1]

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(channel1)
#%%
peaks2, _ = find_peaks(trace, height=(0, mean1),distance=7)
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(trace)
ax.plot(peaks2, trace[peaks2], "x")
ax.set_xlim(0,200)
#plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()
#%%
channel2=trace[peaks2]

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(channel2)
#%%
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(channel1, color='g')
ax.plot(channel2, color='r')
#%% fastICA
X = np.c_[channel1,channel2]
# Compute ICA
ica = FastICA(n_components=2)
S_ = ica.fit_transform(X)  # Reconstruct signals
A_ = ica.mixing_  # Get estimated mixing matrix

#%%
plt.figure()

models = [X, S_]
names = [
    "Observations (mixed signal)",
    "ICA recovered signals",
]
colors = ["green", "red"]

for ii, (model, name) in enumerate(zip(models, names), 1):
    plt.subplot(2, 1, ii)
    plt.title(name)
    for sig, color in zip(model.T, colors):
        plt.plot(sig, color=color,linewidth=1)
        plt.xlim(0,100)

plt.tight_layout()
plt.show()

