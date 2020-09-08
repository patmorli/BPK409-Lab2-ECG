#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 09:25:17 2020

@author: patrickmayerhofer

This library was created for the use in the open source Wearables Course BPK409, Lab2 - ECG
For more information: 
    https://docs.google.com/document/d/e/2PACX-1vTr1zOyrUedA1yx76olfDe5jn88miCNb3EJcC3INmy8nDmbJ8N5Y0B30EBoOunsWbA2DGOVWpgJzIs9/pub
"""


import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps

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
    
"""Step 2: This function filters out all peaks that are under the height threshold
    and not over a minimum distance from each other. \
     Input: d_ecg signal, position of peaks from decg_peaks(), time, 
         height threshold percentage in decimal, distance threshold in decimal
     Output: Rwave peaks of d_ecg"""    
def d_ecg_peaks(d_ecg, peaks_d_ecg, time, heightper, distanceper):
    meanpeaks_d_ecg = np.mean(d_ecg[peaks_d_ecg]) # find the mean of the peaks
    max_d_ecg = np.max(d_ecg) #find max of the ecg signal
    threshold = np.mean([meanpeaks_d_ecg,max_d_ecg])*heightper # find mean of meanpeakecg and maxecg - this will be a good threshold for finding peaks. it filters out all the peaks from the bottom
    newpeaks_d_ecg,_ = sps.find_peaks(d_ecg, height = threshold) # find the new peaks
    newpeaks_d_ecg_t = time[newpeaks_d_ecg]
    newpeaks_d_ecg_t = newpeaks_d_ecg_t.reset_index(drop = True)
    meandistance = np.mean(np.diff(newpeaks_d_ecg))
    Rwave_peaks_d_ecg,_ = sps.find_peaks(d_ecg,height = threshold, distance = meandistance*distanceper) # 
    
      #plot step 2
    plt.figure()  
    plt.plot(time[0:len(time)-1], d_ecg, color = 'red') 
    plt.plot(time[Rwave_peaks_d_ecg], d_ecg[Rwave_peaks_d_ecg], "x", color = 'g')
    #plt.axhline(meanpeaks_d_ecg, color = 'b')
    #plt.axhline(max_d_ecg, color = 'b')
    thres = plt.axhline(threshold, color = 'black', label = 'threshold')
    plt.title('R-wave peaks step 2: d_ECG peaks')
    plt.ylabel('Derivative of activation []')
    plt.xlabel('Time [s]')
    plt.legend()
    return Rwave_peaks_d_ecg
    

    
    """Step 3: this function finds the Rwave peaks at the original ecg signal
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
    
    # plot step 3
    fig, ax1 = plt.subplots()
    ax1.plot(time[0:len(time)-1], d_ecg, color = 'r', label = 'Derivative of ECG')
    ax1.set_ylabel('Activation Derivative []')
    plt.xlabel('Time [s]') 
    plt.title('R-wave peaks step 3: R-wave peaks')
    ax2 = ax1.twinx()
    ax2.plot(time, ecg, color = 'b', label = 'ECG')
    ax2.plot(time[Rwave], ecg[Rwave], "x", color = 'g')
    ax2.set_ylabel('Activation []')
    ax1.legend()
    ax2.legend()
    return Rwave_t