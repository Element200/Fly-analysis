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
Hopefully this code is slightly more elegant. Also got rid of the point 
numbering convention, now it's user-input.
Note: Keyboard interrupts don't work in the Spyder command line input!
If you accidentally press Ctrl+C, you'll have to restart your kernel by pressing Ctrl+.
If you want to interrupt the code, use Ctrl+D instead.
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

while True:
    try:
        rdir = str(input('Directory containing files: ')) # input directory name here.
        os.chdir(rdir)
        file = str(input('Csv file: ')) # Input the file name here.
        print()
        df = pd.read_csv(file)
        rows = len(df.axes[0])
        # Read the inputed csv file and count the number of rows in it.
        
        """THIS PART OF THE CODE PLOTS WING LENGTHS"""
        
        rwapex = int(input("Which point corresponds to right wing apex? "))
        lwapex = int(input("Which point corresponds to left wing apex? "))
        rwbase = int(input("Which point corresponds to right wing base? "))
        lwbase = int(input("Which point corresponds to left wing base? "))
        print()
        for j in range(rows):
            for i in range(3):
                l[i][0] = df.loc[j, df.columns[i+3*(lwapex-1)]]
                r[i][0] = df.loc[j, df.columns[i+3*(rwapex-1)]]
                l[i][1] = df.loc[j, df.columns[i+3*(lwbase-1)]]
                r[i][1] = df.loc[j, df.columns[i+3*(rwbase-1)]]
            lengths[0].append(length(l[0], l[1], l[2]))
            lengths[1].append(length(r[0], r[1], r[2]))
            # This for loop sets all the variables, calculates the length,
            # and inputs left and right lengths into the array.
        
        
        """THIS PART OF THE CODE CALCULATES AVERAGE WING LENGTH AND RANGE AND M.D."""
        av = [0,0]
        
        numcounter = 0
        for i in range(rows):
            if not(np.isnan(lengths[0][i])):
                av[0] += lengths[0][i]
                av[1] += lengths[1][i]
                numcounter += 1
        av[0] = av[0]/numcounter
        av[1] = av[1]/numcounter
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
                if not(np.isnan(lengths[j][i])):
                    sd[j] += np.abs(av[j] - lengths[j][i])
                    sv[j] += (av[j] - lengths[j][i])**2
                dev[j].append(np.abs(av[j]-lengths[j][i]))
                var[j].append((av[j] - lengths[j][i])**2)        
            sd[j] = sd[j]/numcounter
            sv[j] = np.sqrt(sv[j]/numcounter)
        
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
        
        lines = []
        for i in range(5):
            lines.append([[],[]])
        
        for i in range(rows):
            for j in range(2):
                lines[0][j].append(av[j]) # Lines representing averages
                lines[1][j].append(ranges[j][0]) # Maxima
                lines[2][j].append(ranges[j][1]) # Minima
                lines[3][j].append(sd[j]) # Mean deviation
                lines[4][j].append(sv[j]) # Standard deviation
        
        """THIS PART OF THE CODE PLOTS STUFF"""
        fig1 = plt.figure(1)
        plt.plot(range(rows), lengths[0], 'b', lengths[1], 'y')
        for i in range(3):
            plt.plot(range(rows), lines[i][0], lines[i][1])
        plt.ylabel('Length(mm)')
        fig1.show()
        
        # This plot contains left and right wing lengths plus visual guides.
        
        fig2 = plt.figure(2)
        plt.plot(range(rows), dev[0], 'g', dev[1], 'b')
        plt.plot(range(rows), lines[3][0], 'g', lines[3][1], 'b')
        plt.ylabel('Absolute deviation in length(mm)')
        fig2.show()
        
        fig3 = plt.figure(3)
        plt.plot(range(rows), var[0], 'g', var[1], 'b')
        plt.plot(range(rows), lines[4][0], 'g', lines[4][1], 'b')
        plt.ylabel('Root-square deviation in length(mm)')
        fig3.show()
        
        # This plot contains left and right mean and standard deviations, plus visual guides.
        break
    except FileNotFoundError:
        print("Not a file or directory!")
    # Prevents user from inputting random characters into the command line.
    except EOFError:
        print("Keyboard interrupt!")
        break
# Raising an EOF Error with Ctrl+D substitutes the usual Ctrl+C Keyboard Interrupt, which doesn't work.
