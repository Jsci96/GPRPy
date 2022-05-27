#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:49:43 2022
@author: jaahnavee

Reads .cor.txt files, collates them, and converts to a single .kml file that can be imported into Google Earth.
This code will collate all the GPS files in the selected directory to create a single .kml file. Be sure to separate your data into different folders if you want each track in a separate .kml file.
"""





"""
!!!!!!! IMPORTANT !!!!!!!

This code will ask the user for 3 prompts:
    1. The user will have to select the folder that contains all the MALA data files (.rad, .rd7, .cor.txt for each track)
    2. The user will have to select the folder they want to save the final .kml file in
    3. The user will have to input in the Spyder Console a label for the final .kml filename
    
!!!!!!!!!!!!!!!!!!!!!!!!!
"""

#########################
# Package imports
#########################

import numpy as np
import csv
import pandas as pd
import simplekml
from tkinter import filedialog
from tkinter import Tk
import os

#########################
# Directory prompts
#########################

root = Tk()
root.withdraw()
directory = filedialog.askdirectory()                                           # Asks the user to select the directory with MALA data
folder = os.listdir(directory)                                                  # Populates list of files within the selected directory

#########################
# Read in GPS files
#########################

finaltable = pd.DataFrame()
for topofile in folder:
    if '.cor' in topofile:
        with open (directory+'/'+topofile, 'r') as f: 
            reader = csv.reader(f, delimiter='\t')                              # Opens each GPS file
            topotable = pd.DataFrame(list(reader))                              # Puts each file into a data frame
            finaltable = finaltable.append(topotable)                           # Appends the data frame to the variable 'finaltable'
  
topotable = topotable.drop(columns=[0, 1, 2, 4, 6, 7, 8, 9]).astype(float)      # Drops all columns except Longitude, Latitude, and Altitude
topotable.iloc[:,1] = -topotable.iloc[:,1]                                      # Makes all the Longitude points negative (for accurate Google Earth positions)
P = np.asmatrix(topotable)                                                      # Puts final table into a matrix 'P'

#########################
# Convert to .kml
#########################

kml = simplekml.Kml()

edges = []
for i in range(len(P)-1):
    edges.append([(P[i, 1], P[i, 0]), (P[i+1, 1], P[i+1, 0])])                  # Reorganizes the matrix into a basic kml file structure

for i in range(len(edges)):
    line = kml.newlinestring(name='coord_'+str(i), coords=edges[i])             # Creates line segments from the GPS coordinates
    line.style.linestyle.width = 3                                              # Changes the width of the plotted line on Google Earth
    line.style.linestyle.color = simplekml.Color.red                            # Changes the color of the plotted line on Google Earth
    
#########################
# Save .kml file
#########################

directory2 = filedialog.askdirectory()                                          # Asks the user to select the directory where the final .kml file should be saved
track_label = input('Enter the file label: ')                                   # Asks the user to enter, in the Spyder Console, a label for the .kml file

kml.save(directory2+'/GPS_track_'+str(track_label)+'.kml')                      # Saves the .kml file