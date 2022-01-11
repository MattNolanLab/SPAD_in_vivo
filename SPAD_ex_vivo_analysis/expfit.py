# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 15:05:13 2021

@author: s2073467
"""

from pylab import *
from math import log
import scipy as sp
import scipy.optimize

'''fitExponent and fit_exp_linear are linear models and not very good'''
# def fitExponent(tList,yList,ySS=0):
#    '''
#    This function finds a 
#        tList in sec
#        yList - measurements
#        ySS - the steady state value of y
#    returns
#        amplitude of exponent
#        tau - the time constant
#    '''
#    bList = [log(max(y-ySS,1e-6)) for y in yList]
#    b = matrix(bList).T
#    rows = [ [1,t] for t in tList]
#    A = matrix(rows)
#    #w = (pinv(A)*b)
#    (w,residuals,rank,sing_vals) = lstsq(A,b)
#    tau = -1.0/w[1,0]
#    amplitude = exp(w[0,0])
#    return (amplitude,tau)

# def fit_exp_linear(t, y, C=0):
#     y = y - C
#     y = np.log(y)
#     K, A_log = np.polyfit(t, y, 1)
#     A = np.exp(A_log)
#     return A, K

'''nonlinear model is better, tau=-1/K'''
def model_func(t, A, K, C):
    return A * np.exp(K*t) + C

def fit_exp_nonlinear(t, y):
    opt_parms, parm_cov = sp.optimize.curve_fit(model_func, t, y, maxfev=1000)
    A, K, C = opt_parms
    return A, K, C


#%%
'''
https://stackoverflow.com/questions/3938042/fitting-exponential-decay-with-no-initial-guessing
http://exnumerus.blogspot.com/2010/04/how-to-fit-exponential-decay-example-in.html

'''