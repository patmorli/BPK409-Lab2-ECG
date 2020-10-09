#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:13:32 2020

@author: patrickmayerhofer

This code was created for the use in the open source Wearables Course BPK409, Lab2 - ECG
For more information: 
    https://docs.google.com/document/d/e/2PACX-1vTr1zOyrUedA1yx76olfDe5jn88miCNb3EJcC3INmy8nDmbJ8N5Y0B30EBoOunsWbA2DGOVWpgJzIs9/pub
"""

"""This code creates a serial communication with the microcontroller that is connected
via USB. The code needs to output 2 values. In the ECG that is the activation and the time.
The Arduino serial monitor needs to be closed for this code to run.

The code also saves the file of the collected data with the specified savename in
the current working directory, as a .txt file.

To do: change the savename and change the serial port that you are using.
You can find the serial port number in your Arduino Software at Tools-->Port

Just disconnect the microcontroller from the computer to stop the data collection."""

#change the name of the .csv file that will be saved in this working directory. keep .csv
savename = 'mydata1.txt'

# import libraries
import serial 
import time
import csv
import re
import numpy as np

# prepare serial communication
ser = serial.Serial('/dev/cu.wchusbserial14140') # change this to name of your port
ser.flushInput()
ser.baudrate = 500000 # change this for baud rate in arduino code

t0 = time.time() #default time for zeroing 
l = []
print("Data is collecting.")

while True:
    try: # it will try to get data from serial communication
        l.append(ser.readline().decode().strip('\r\n'))
        
        #t = np.append(t, time.time()-t0) # get time from python
        #value = np.append(value, float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))) #decode value from serial communication
        #print(decoded_bytes)
    except: # if error in before (when disconnecting the microcontroller)
        print("Data collection ended. Have a great day.")
        break
 
# get list data into a numpy array    
data = np.empty([len(l)-1,2]) # create an empty matrix with 11 variables, - 2 because first and last line might not have full information
for i in range(len(data)):  
    data[i,0:2] = re.findall('\-?\d*\.?\-?\d+',l[i+1]) #i+1 to not use first line 


"""save data in csv file"""
np.savetxt(savename, data, delimiter='\t')


