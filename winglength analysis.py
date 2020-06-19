"""
Winglength Analysis #2
                                                    By Siddharth S. Sane
                                                    
This code calculates winglengths from an input csv file and plots it as 
a function of frame number. It also calculates the average winglength,
range, mean deviation, and standard deviation. Also, because I'm easily
confused, I refer to standard deviation as 'standard variance' so that
it's not confused with 'mean deviation'. I also managed to halve the 
number of variables with one caveat of convention: in a duplet, [0] means
'left' and [1] means 'right'. Comments have also been cleaned substantially.

Use the following convention of points:
    Point 1 = Left wing apex
    Point 2 = Right wing apex
    Point 3 = Left wing base
    Point 4 = Right wing base
    Point 5 = Head base (not used in this code)

Hopefully this code is slightly more elegant. 
Note: Keyboard interrupts don't work in the command line input!
If you accidentally press Ctrl-C, you'll have to restart your kernel by pressing Ctrl-.
 """

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def length(x,y,z):
    l = np.sqrt((x[1]-x[0])**2+(y[1]-y[0])**2+(z[1]-z[0])**2)
    return l

# Handy function that calculates lengths the Pythagorean way, 
# and takes list inputs - each list[i] = [wing coord, base coord]
    
l = [[0,0] , [0,0] , [0,0]] # Left wing XYZ list
r = [[0,0] , [0,0] , [0,0]] # Right wing XYZ list

# tmp arrays to hold current XYZ values: l/r[i][j] = x_i for l/r wing/base(0/1)

lengths = [[],[]]

#Arrays that store length values

rdir = str(input('Directory containing files: ')) # input directory name here.

# Right directory - the one that contains the csv files. This can later be
# changed to accomodate multiple csv files


try:
    os.chdir(rdir)
    file = str(input('Csv file: ')) # Input the file name here.
    print()
    # Check if the current directory is the specified directory. If not, change
    # it. Then, input the file name.

    df = pd.read_csv(file)
    rows = len(df.axes[0])
    
    # Read the inputed csv file and count the number of rows in it.
    
    """THIS PART OF THE CODE PLOTS WING LENGTHS"""

    for j in range(rows):
        for i in range(3):
            l[i][0] = df.loc[j, df.columns[i]] #XYZ for point 1
            r[i][0] = df.loc[j, df.columns[i+3]] #XYZ for point 2
            l[i][1] = df.loc[j, df.columns[i+6]] #XYZ for point 3
            r[i][1] = df.loc[j, df.columns[i+9]] #XYZ for point 4
        lengths[0].append(length(l[0], l[1], l[2]))
        lengths[1].append(length(r[0], r[1], r[2]))
        # This for loop sets all the variables, calculates the length,
        # and inputs left and right lengths into the array.
    
    
    """THIS PART OF THE CODE CALCULATES AVERAGE WING LENGTH AND RANGE AND M.D."""
    av = [0,0]
    
    for i in range(rows):
        av[0] += lengths[0][i]
        av[1] += lengths[1][i]
    av[0] = av[0]/rows
    av[1] = av[1]/rows
    print('Average left wing length = ', av[0])
    print('Average right wing length = ', av[1])
    # Calculate & print left and right wing length average
    
    ranges = [[min(lengths[0]), max(lengths[0])],[min(lengths[1]), max(lengths[1])]]
    lr = ranges[0][1] - ranges[0][0]
    rr = ranges[1][1] - ranges[1][0]
    lbigger = max([np.abs(av[0]-ranges[0][0]), np.abs(av[0]-ranges[0][1])])
    rbigger = max([np.abs(av[1]-ranges[1][0]), np.abs(av[1]-ranges[1][1])])
    
    print('Left winglength range = ', lr)
    print('Right winglength range = ', rr)
    print('Maximum left wing deviation = ', lbigger, '('+ str(100*lbigger/av[0])+ '% error)')
    print('Maximum right wing deviation = ', rbigger, '('+ str(100*rbigger/av[1])+ '% error)')
    
    #Print left and right winglength ranges and maximum deviation
    
    sd = [0,0]
    sv = [0,0]
    dev = [[],[]]
    var = [[],[]]
    
    # Deviation, variance lists to store deviation and variance values.
    
    for j in range(2):
        for i in range(rows):
            sd[j] += np.abs(av[j] - lengths[j][i])
            dev[j].append(np.abs(av[j]-lengths[j][i]))
            sv[j] += (av[j] - lengths[j][i])**2
            var[j].append((av[j] - lengths[j][i])**2)        
        sd[j] = sd[j]/rows
        sv[j] = np.sqrt(sv[j]/rows)

    # All of these variables have dimensions of length and shouldn't be measured in percentages!
    
    sderr = [(sd[0]/av[0]) * 100 , (sd[1]/av[1]) * 100]
    sverr = [(sv[0]/av[0]) * 100 , (sv[1]/av[1]) * 100]
    
    # THESE variables are dimensionless fractions and can be measured in percentages!
    
    print()
    print('Left wing mean deviation = ', sd[0], '('+ str(sderr[0])+ '% error)')
    print('Right wing mean deviation = ', sd[1], '('+ str(sderr[1])+ '% error)')
    print('Left wing standard deviation = ', sv[0], '('+ str(sverr[0])+ '% error)')
    print('Right wing standard deviation = ', sv[1], '('+ str(sverr[1])+ '% error)')
    
    """THIS PART OF THE CODE CREATES LINES AS VISUAL GUIDES"""
    
    average = [[],[]]
    minimum = [[],[]]
    maximum = [[],[]]
    sdev = [[],[]]
    svar = [[],[]]
    
    for i in range(rows):
        for j in range(2):
            average[j].append(av[j])
            minimum[j].append(ranges[j][0])
            maximum[j].append(ranges[j][1])
            sdev[j].append(sd[j])
            svar[j].append(sv[j])
    
    """THIS PART OF THE CODE PLOTS STUFF"""
    fig1 = plt.figure(1)
    plt.plot(range(rows), lengths[0], 'b', lengths[1], 'y')
    plt.plot(range(rows), average[0], 'b', average[1], 'y')
    plt.plot(range(rows), maximum[0], 'g', maximum[1], 'g')
    plt.plot(range(rows), minimum[0], 'r', minimum[1], 'r')
    plt.ylabel('Length(mm)')
    fig1.show()

    # This plot contains left and right wing lengths plus visual guides.
    
    fig2 = plt.figure(2)
    plt.plot(range(rows), dev[0], 'g', dev[1], 'b')
    plt.plot(range(rows), sdev[0], 'g', sdev[1], 'b')
    plt.ylabel('Absolute deviation in length(mm)')
    fig2.show()
    
    fig3 = plt.figure(3)
    plt.plot(range(rows), var[0], 'g', var[1], 'b')
    plt.plot(range(rows), (svar[0])**2, 'g', svar[1], 'b')
    plt.ylabel('Root-square deviation in length(mm)')
    fig3.show
    
    # This plot contains left and right mean and standard deviations, plus visual guides.

except FileNotFoundError:
    print('Not a file or directory!')
    
# First try-except prevents me from inputting random stuff into the file or directory input
