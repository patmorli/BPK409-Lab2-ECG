#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 09:25:17 2020

@author: patrickmayerhofer
"""


import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps
from scipy.stats import iqr
import statistics as s
import math as m
from hrvanalysis import get_time_domain_features
from hrvanalysis import get_frequency_domain_features
from hrvanalysis import plot_psd
from hrvanalysis import plot_poincare
import scipy.signal

"""Step 1: This function finds the peaks of the derivative of the ECG signal
Input: ecg signal, time
Output: ecg derivative, position of peaks of d_ecg"""
def decg_peaks(ecg, time):
    """Step 1: Find the peaks of the derivative of the ECG signal"""
    d_ecg = np.diff(ecg) #find derivative of ecg signal
    peaks_d_ecg,_ = sps.find_peaks(d_ecg) #peaks of d_ecg
     
    # plot step 1
    plt.figure()
    plt.plot(time[0:len(time)-1], d_ecg, color = 'red')
    plt.plot(time[peaks_d_ecg], d_ecg[peaks_d_ecg], "x", color = 'g')
    plt.xlabel('Time [s]')
    plt.ylabel('Derivative of activation []')
    plt.title('R-wave peaks step 1: peaks of derivative of ECG')
    plt.show()
    return d_ecg, peaks_d_ecg
    
"""Step 2: This function filters out all peaks that are lower than 40% of the mean of the following: 
     the mean of all peaks and the max ecg value
     Input: d_ecg signal, position of peaks from decg_peaks(), time
     Output: Position of the peaks that are over a certain threshold, calculated threshold"""    
def height_threshold_peaks(d_ecg, peaks_d_ecg, time, p):
    meanpeaks_d_ecg = np.mean(d_ecg[peaks_d_ecg]) # find the mean of the peaks
    max_d_ecg = np.max(d_ecg) #find max of the ecg signal
    threshold = np.mean([meanpeaks_d_ecg,max_d_ecg])*0.4 # find mean of meanpeakecg and maxecg - this will be a good threshold for finding peaks. it filters out all the peaks from the bottom
    newpeaks_d_ecg,_ = sps.find_peaks(d_ecg, height = threshold) # find the new peaks
    newpeaks_d_ecg_t = time[newpeaks_d_ecg]
    newpeaks_d_ecg_t = newpeaks_d_ecg_t.reset_index(drop = True)
    
     #plot step 2
    plt.figure()  
    plt.plot(time[0:len(time)-1], d_ecg, color = 'red') 
    plt.plot(time[newpeaks_d_ecg], d_ecg[newpeaks_d_ecg], "x", color = 'g')
    mean_d = plt.axhline(meanpeaks_d_ecg, color = 'b', label = 'mean of peaks')
    max_d = plt.axhline(max_d_ecg, color = 'b', label = 'max of peaks')
    meanmaxmean = plt.axhline(threshold, color = 'black', label = 'mean of max and mean')
    thres = plt.axhline(threshold, color = 'g', label = 'threshold')
    plt.title('R-wave peaks step 2: All peaks over threshold')
    plt.ylabel('Derivative of activation []')
    plt.xlabel('Time [s]')
    plt.legend()
    return newpeaks_d_ecg, threshold
    
    """Step 3: This function finds the mean distance of the peaks from 
    height_threshold_peaks and finds all peaks that are again
    # over the same threshold as before and that have at least 0.4 times 
    the mean distance of the peaks before
    Input: d_ecg signal, position of peaks from height_threshold_peaks(), 
       threshold from height_threshold_peaks(), time
    Output: Rwave peaks of d_ecg"""
def height_distance_threshold_peaks(d_ecg, newpeaks_d_ecg, threshold, time, p):
    meandistance = np.mean(np.diff(newpeaks_d_ecg))
    Rwave_peaks_d_ecg,_ = sps.find_peaks(d_ecg,height = threshold, distance = meandistance*p) # 
    
    #plot step 3
    plt.figure()  
    plt.plot(time[0:len(time)-1], d_ecg, color = 'red') 
    plt.plot(time[Rwave_peaks_d_ecg], d_ecg[Rwave_peaks_d_ecg], "x", color = 'g')
    #plt.axhline(meanpeaks_d_ecg, color = 'b')
    #plt.axhline(max_d_ecg, color = 'b')
    thres = plt.axhline(threshold*0.4, color = 'g', label = 'threshold')
    plt.title('R-wave peaks step 3: All peaks over threshold and with minimum distance')
    plt.ylabel('Derivative of activation []')
    plt.xlabel('Time [s]')
    plt.legend()
    return Rwave_peaks_d_ecg
    
    """Step 4: this function finds the Rwave peaks at the original ecg signal
    with the before defined peaks of the d_ecg signal
    Input: ecg signal,derivative of ecg signal,
        Rwave peaks of d_ecg from height_distance_threshold_peaks
    Output: Rwave peaks"""
def Rwave_peaks(ecg, d_ecg, Rwave_peaks_d_ecg, time):   
    Rwave = np.empty([len(Rwave_peaks_d_ecg)-1]) 
    for i in range(0, len(Rwave)): # for all peaks
        ecgrange = ecg[Rwave_peaks_d_ecg[i]:Rwave_peaks_d_ecg[i+1]] # create array that contains of the ecg within the d_ecg_peaks
        percentage = np.round(len(ecgrange)*0.2)
        maxvalue = np.array(list(np.where(ecgrange == np.max(ecgrange[0:int(percentage)])))) # find the index of the max value of ecg
        Rwave[i] = Rwave_peaks_d_ecg[i] + maxvalue[0,0]  # save this index         
    
    Rwave = Rwave.astype(np.int64)
    Rwave_t = time[Rwave]
    Rwave_t = Rwave_t.reset_index(drop = True)
    Rwave_t = Rwave_t.drop(columns = ['index'])
    
    # plot step 4
    fig, ax1 = plt.subplots()
    ax1.plot(time[0:len(time)-1], d_ecg, color = 'r')
    ax1.set_ylabel('Activation Derivative []')
    plt.xlabel('Time [s]') 
    plt.title('R-wave peaks step 4: R-wave peaks')
    ax2 = ax1.twinx()
    ax2.plot(time, ecg, color = 'b')
    ax2.plot(time[Rwave], ecg[Rwave], "x", color = 'g')
    ax2.set_ylabel('Activation []')
    return Rwave_t