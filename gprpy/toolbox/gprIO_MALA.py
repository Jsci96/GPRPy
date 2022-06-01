import numpy as np


def readMALA(file_name):
    '''
    Reads the MALA .rd3 data file and the .rad header. Can also be used
    to read .rd7 files but I'm not sure if they are really organized
    the same way.

    INPUT: 
    file_name     data file name without the extension!

    OUTPUT:
    data          data matrix whose columns contain the traces
    info          dict with information from the header
    '''
    # First read header
    info = readGPRhdr(file_name+'.rad')
    try:
        filename = file_name + '.rd3'
        data = np.fromfile(filename, dtype=np.int16)        
    except:
        filename = file_name + '.rd7'
        data = np.fromfile(filename, dtype=np.int32)
    
    nrows=int(len(data)/int(info['SAMPLES']))
    
    data = (np.asmatrix(data.reshape(nrows,int(info['SAMPLES'])))).transpose()
        
    return data, info
    


def readGPRhdr(filename):
    '''
    Reads the MALA header

    INPUT: 
    filename      file name for header with .rad extension
    
    OUTPUT:
    info          dict with information from the header
    '''
    # Read in text file
    info = {}
    with open(filename) as f:
        for line in f:
            strsp = line.split(':')
            info[strsp[0]] = strsp[1].rstrip()
    return info

# test

# file = 112
# data = readMALA('/Users/jaahnavee/Desktop/MALA Test/'+str(file)+'/DAT_0'+str(file))[0]
# info = readGPRhdr('/Users/jaahnavee/Desktop/MALA Test/'+str(file)+'/DAT_0'+str(file)+'.rad')