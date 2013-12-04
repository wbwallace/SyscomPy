"""deprecated functions
"""
##This module is going to be for extracting info and data from
##Syscom .smr files - recordings made by MR200x recrders.

##Initial impetus is to get the data into a NumPy array for use
##with PyAudiere.  There was an unusual recording that looks like
##a sound in blah and when I saw it i wodered what it sounded like.

##Definitely other uses in the back of my mind - like previous VB
##projects that extracted data, calculate statistics,, dft ...

import numpy as np
import pprint
pp = pprint.pprint

##Start simple.
##pass a filepath of an smr file that has
##already been processed by to_ascii.

##open the file & read the lines:
##    get pertinent info from the header
##    get the x,y,z data and convert to a float -1 <= x >= 1
##    return the numpylists

# probably only use this once for a funny recording
# that looks like a sound on a graph

def dataforpyaudiere(filepath):
    """
    deprecated, use get_smr_data and get_smr_header instead.
    Assumes file has been processed with to_ascii raw counts
        offset subtracted
    Assumes the file is NOT a selftest file
    returns a numpy float32 array for each axis
    the arrays have had the mean subtracted
    the arrays have been scaled to the maximum (abs) value in
    the recording - because of this scaling relative amplitudes
    between the axes is lost

    """
    x = []
    y = []
    z = []
    f = open(filepath, 'r')
    # get number of samples, sample rate, bit resolution from header
    while 1:
        line = f.readline()
        # need to fix these so i just get the data i need
        if 'nb_samples' in line:
            nb_samples = line
        elif 'sampling' in line:
            samplerate = line
        elif 'adc_resol' in line:
            adc_resol = line
        elif 'elevation' in line:
            break
    # get the data
    # don't know enuff about numpy to know if it is better
    # to use np.append or just make regular python lists then convert
    while 1:
        line = f.readline()
        if line:
            line = line.strip()
            L = line.split('\t')
            x.append(float(L[0]))
            y.append(float(L[1]))
            z.append(float(L[2]))
        else:
            break
    # numpy arrays
    x_a = np.array(x, dtype='f4')
    y_a = np.array(y, dtype='f4')
    z_a = np.array(z, dtype='f4')

    # normalize the arrays
    x_a = x_a - x_a.mean()
    y_a = y_a - y_a.mean()
    z_a = z_a - z_a.mean()
    
    x_a = x_a / max(abs(x_a.min()) + 0.0001, abs(x_a.max()) + 0.0001)
    y_a = y_a / max(abs(y_a.min()) + 0.0001, abs(y_a.max()) + 0.0001)
    z_a = z_a / max(abs(z_a.min()) + 0.0001, abs(z_a.max()) + 0.0001)

##    print nb_samples, samplerate, adc_resol
##    print 'x.min:', x_a.min(), 'y.min:', y_a.min(), 'z.min:', z_a.min()
##    print 'x.mean:', x_a.mean(), 'y.mean:', y_a.mean(), 'z.mean:', z_a.mean()
##    print 'x.max:', x_a.max(), 'y.max:', y_a.max(), 'z.max:', z_a.max()

    return x_a, y_a, z_a                    

def get_smr_data1(filepath):
    """
    filepath -> string point to a .smr file
    returns a numpy array:
        array([[ x,  y,  z],
        [ x,  y,  z],
        [-3,  0, -5],
        [-2, -1, -8],
        [-2, -1, -2]], dtype=int16)

    x data is npData[:, 0]
    y data is npData[:, 1]
    z data is npData[:, 2]
    """
    
    with open(testfile, 'rb') as f:
        f.seek(256)
        data = f.read()
    npData = np.fromstring(data, dtype = np.int16)
 
    npData = npData.reshape((-1, 3))
        
def get_smr_data(filepath):
    """
    Read the data portion of an smr file that
    has been procesed by To_ASCII and return
    np arrays.

    filepath: string - full path
    """
    # not sure why I didn't just start with an np array
    x = []
    y = []
    z = []
    f = open(filepath, 'r')
    # get number of samples, sample rate, bit resolution from header
    while 1:
        line = f.readline()
        # need to fix these so i just get the data i need
        if 'nb_samples' in line:
            nb_samples = line
        elif 'sampling' in line:
            samplerate = line
        elif 'adc_resol' in line:
            adc_resol = line
        elif 'elevation' in line:
            break
    # elevation should have been the last line (85) of the header
    # next line should be the start of the data at line 86
    # get the data
    # don't know enuff about numpy to know if it is better
    # to use np.append or just make regular python lists then convert
    while 1:
        line = f.readline()
        # there might be a better way to do this
        # started this before i knew anything about Python
        if line:
            line = line.strip()
            L = line.split('\t')
            x.append(float(L[0]))
            y.append(float(L[1]))
            z.append(float(L[2]))
        else:
            break
    f.close()    
    # numpy arrays
    x_a = np.array(x, dtype='f4')
    y_a = np.array(y, dtype='f4')
    z_a = np.array(z, dtype='f4')

    return x_a, y_a, z_a

def get_smr_header(filepath):
    """
    Read the header portion of an smr file that
    has been procesed by To_ASCII and return
    a dictionary of parameter:value pairs.

    filepath: string - full path
    """
    f = open(filepath, 'r')
    header_dict = {}
    # each line of the header has the format:
    # parameter tab value (all strings)
    while 1:
        line = f.readline()
        L = line.strip().split("\t")
        header_dict[L[0]] = L[1]
        if 'elevation' in line:
            break
    f.close()
    # elevation should have been the last line (85) of the header
    # next line should be the start of the data at line 86
    return header_dict
    
