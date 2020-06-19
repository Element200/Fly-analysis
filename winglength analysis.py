"""
    Winglength Analysis
                                                        By Siddharth S. Sane
                                                        
    This code calculates winglengths from an input csv file and plots it as 
    a function of frame number. It also calculates the average winglength,
    range, mean deviation, and standard deviation. Also, because I'm easily
    confused, I refer to standard deviation as 'standard variance' so that
    it's not confused with 'mean deviation'. Also, any variable prefixed 'r'
    refers to 'right'; any variable prefixed with 'l' refers to 'left'.
    
    Use the following convention of points:
        Point 1 = Left wing apex
        Point 2 = Right wing apex
        Point 3 = Left wing base
        Point 4 = Right wing base
        Point 5 = Head base (not used in this code)
    
    This is not an elegant code, but it does the job. 
 """



import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def length(x0,x1,y0,y1,z0,z1):
    l = np.sqrt((x1-x0)**2+(y1-y0)**2+(z1-z0)**2)
    return l
#Handy function that calculates lengths the Pythagorean way
    
lx = [0,0]
ly = [0,0]
lz = [0,0]
rx = [0,0]
ry = [0,0]
rz = [0,0]
# tmp arrays to hold current XYZ values: tmp[0] = wing apex(XYZ),
# tmp[1] = wing base (XYZ). 

ll = []
rl = []
#Arrays that store length values

#First test file: 
#fly1_asym_cutwing1_1_csv_xyzpts.csv
#test directory: C:/Users/Dinesh/Downloads

rdir = 'C:/Users/Dinesh/Downloads' #str(input('Directory containing files: '))

# Hard-coded present working directory. Uncomment the bit after the quotes 
# to make this process more varable-directory friendly, or change the directory
# to the location where your csv files are stored. This will be changed
# in the future to allow for measuring the error of multiple files.


try:
    if os.getcwd() != rdir:
        os.chdir(rdir)
        print('PWD is now ', os.getcwd())
        os.listdir(rdir)
        print()
        file = str(input('Csv file: ')) # Input the file name here.
    # Check if the current directory is the specified directory. If not, change it.
    


    df = pd.read_csv(file)
    print('csv file is: ', file)
    print()
    rows = len(df.axes[0])
    """THIS PART OF THE CODE PLOTS WING LENGTHS"""
    for i in range(rows):
        lx[0] = df.loc[i, 'pt1_X']
        lx[1] = df.loc[i, 'pt3_X']
        ly[0] = df.loc[i, 'pt1_Y']
        ly[1] = df.loc[i, 'pt3_Y']
        lz[0] = df.loc[i, 'pt1_Z']
        lz[1] = df.loc[i, 'pt3_Z']
        rx[0] = df.loc[i, 'pt2_X']
        rx[1] = df.loc[i, 'pt4_X']
        ry[0] = df.loc[i, 'pt2_Y']
        ry[1] = df.loc[i, 'pt4_Y']
        rz[0] = df.loc[i, 'pt2_Z']
        rz[1] = df.loc[i, 'pt4_Z']
        ll.append(length(lx[0],lx[1],ly[0],ly[1],lz[0],lz[1]))
        rl.append(length(rx[0],rx[1],ry[0],ry[1],rz[0],rz[1]))
        # This long for loop sets all the variables, calculates the length,
        # and inputs left and right lengths into the array.
        
    
    
    # Plot all values, then tell me it's done.
    
    """THIS PART OF THE CODE CALCULATES AVERAGE WING LENGTH AND RANGE AND M.D."""
    lav = 0
    rav = 0
    
    for i in range(rows):
        lav += ll[i]
        rav += rl[i]
    lav = lav/rows
    rav = rav/rows
    print('Average left wing length = ', lav)
    print('Average right wing length = ', rav)
    # Calculate & print left and right wing length average
    
    lrange = [min(ll), max(ll)]
    rrange = [min(rl), max(rl)]
    lr = lrange[1] - lrange[0]
    rr = rrange[1] - rrange[0]
    lbigger = max([np.abs(lav-lrange[0]), np.abs(lav-lrange[1])])
    rbigger = max([np.abs(rav-rrange[0]), np.abs(rav-rrange[1])])
    
    print('Left winglength range = ', lr)
    print('Right winglength range = ', rr)
    print('Maximum left wing deviation = ', lbigger, '(', 100*lbigger/lav, '% error)')
    print('Maximum right wing deviation = ', rbigger, '(', 100*rbigger/rav, '% error)')
    
    #Print left and right winglength ranges and maximum deviation
    
    lsd = 0
    rsd = 0
    lsv = 0
    rsv = 0
    rdev = []
    ldev = []
    rvar = []
    lvar = []
    for i in range(rows):
        lsd += np.sqrt((lav - ll[i])**2)
        ldev.append(np.sqrt((lav - ll[i])**2))
        rsd += np.sqrt((rav - rl[i])**2)
        rdev.append(np.sqrt((rav - rl[i])**2))
        lsv += (lav - ll[i])**2
        lvar.append((lav - ll[i])**2)
        rsv += (rav - rl[i])**2
        rvar.append((rav - rl[i])**2)

    lsd = (lsd/rows)
    rsd = (rsd/rows)
    lsv = (np.sqrt(lsv/rows))
    rsv = (np.sqrt(rsv/rows))
    
    # All of these variables have dimensions of length and shouldn't be measured
    # in percentages!
    
    lsderr = (lsd/lav) * 100
    rsderr = (rsd/rav) * 100
    lsverr = (lsv/lav) * 100
    rsverr = (rsv/rav) * 100
    
    # THESE variables are dimensionless fractions and can, in fact, be measured
    # in percentages!
    
    print('Left wing mean deviation = ', lsd, '(', lsderr, '% error)')
    print('Right wing mean deviation = ', rsd, '(', rsderr, '% error)')
    print('Left wing standard deviation = ', lsv, '(', lsverr, '% error)')
    print('Right wing standard deviation = ', rsv, '(',rlsverr, '% error)')
    

    
    """THIS PART OF THE CODE CREATES LINES AS VISUAL GUIDES"""
    
    laverage = []
    raverage = []
    lminimum = []
    lmaximum = []
    rminimum = []
    rmaximum = []
    lsdev = []
    rsdev = []
    lsvar = []
    rsvar = []
    
    for i in range(rows):
        laverage.append(lav)
        raverage.append(rav)
        lminimum.append(lrange[1])
        lmaximum.append(lrange[0])
        rminimum.append(rrange[1])
        rmaximum.append(rrange[0])
        lsdev.append(lsd/100)
        rsdev.append(rsd/100)
        lsvar.append(lsv/100)
        rsvar.append(rsv/100)
    
    #Create line arrays for visual guides
    
    """THIS PART OF THE CODE PLOTS STUFF"""
    
    plt.plot(range(rows), ll)
    plt.plot(range(rows), rl)
    plt.plot(range(rows), lmaximum)
    plt.plot(range(rows), rmaximum)
    plt.plot(range(rows), lminimum)
    plt.plot(range(rows), rminimum)
    plt.plot(range(rows), laverage)
    plt.plot(range(rows), raverage)
    plt.plot(range(rows), ldev, 'g', rdev, 'b')
    plt.plot(range(rows), lsdev, 'g', rsdev, 'b')



except FileNotFoundError:
    print('Not a file or directory!')
except KeyboardInterrupt:
    print('Manual shutdown!')
# First try-except prevents me from inputting random stuff into the file or directory
# input. Second allows me to manually shut down the code by using Ctrl-C
# (Which, in the LINUX lingo, shuts down a running code).