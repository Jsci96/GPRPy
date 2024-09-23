#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:49:43 2022
@author: jaahnavee

Reads the all the .cor files in selected directory and converts each track to a separate .kml file

!!!!!!! IMPORTANT !!!!!!!

This code will ask the user for 2 prompts:
    1. The user will have to select the folder that contains the .cor files of interest
    2. The user will have to select the folder they want to save the final .kml file in

!!!!!!!!!!!!!!!!!!!!!!!!!
"""

#%%

#########################
# Package imports
#########################

import numpy as np
import pandas as pd
import simplekml
from tkinter import filedialog
from tkinter import Tk
import os
import datetime
import re

#########################
# Directory prompts
#########################

# select folder with .cor files
root = Tk()
root.withdraw()
directory = filedialog.askdirectory()                                                               # Asks the user to select the directory with MALA data
folder = os.listdir(directory)                                                                      # Populates list of files within the selected directory

directory2 = filedialog.askdirectory()                                                              # Asks the user to select the directory where the final .kml file should be saved

#########################
# Read in GPS files
#########################

columns_to_remove = [0, 1, 2, 4, 6, 7, 8, 9]

c = 0
for topofile in folder:

    kml = simplekml.Kml()
    if '.cor' in topofile:

        c+=1

        with open (directory+'/'+topofile, 'r') as f: 
            topotable = pd.read_csv(f, delimiter='\t', header=None)                                             # Puts each file into a data frame
            topotable.drop(columns_to_remove, axis=1, inplace=True)
            topotable.iloc[:,1] = -topotable.iloc[:,1]                                                          # Makes all the Longitude points negative (for accurate Google Earth positions)
            P = np.asmatrix(topotable)                                                                          # Puts final table into a matrix 'P'
            
            for i in range(len(P)):

                point = kml.newpoint(name='coord_'+str(i), coords=[(P[i, 1], P[i, 0])])                         # Creates line segments from the GPS coordinates
                point.style.labelstyle.scale = 0
                point.style.iconstyle.icon.href = 'https://img.icons8.com/?size=100&id=85913&format=png&color=FA5252'
                point.style.iconstyle.scale = 0.25

            time_label = datetime.datetime.now().strftime('%d-%m-%Y-%H%M%S')
            track_label = re.findall(r'\d+', topofile)[0]
            kml.save(directory2+'/'+track_label+'_'+time_label+'.kml')                                          # Saves the .kml file

        print('Saved '+str(c)+' of '+str(sum('.cor' in t for t in folder)))

# %%
