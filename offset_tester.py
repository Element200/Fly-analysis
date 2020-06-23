import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

os.chdir('C:/Users/Dinesh/Downloads')

#Hard coded, change to your default directory

file = 'fly2_asym_cutwing1_1_originalflippedxypts.csv'
test = 'fly2_asym_cutwing1_1_offsettestxypts.csv'

#Both of these files are in the Dropbox folder . The first file has the 
# vertical flipped.

df0 = pd.read_csv(file)
df1 = pd.read_csv(test)

#Read the files

r1_0 = [df0.loc[0:81, 'pt4_cam2_X'], df0.loc[0:81, 'pt4_cam2_Y']]
r1_1 = [df1.loc[0:81, 'pt5_cam2_X'], df1.loc[0:81, 'pt5_cam2_Y']]

# Quick note: I accidentally marked point 5 as the point that was normally
# marked point 4 and vice-versa. 

r3_0 = [df0.loc[0:81, 'pt4_cam3_X'], df0.loc[0:81, 'pt4_cam3_Y']]
r3_1 = [df1.loc[0:81, 'pt5_cam3_X'], df1.loc[0:81, 'pt5_cam3_Y']]

l2_0 = [df0.loc[0:81, 'pt5_cam1_X'], df0.loc[0:81, 'pt5_cam1_Y']]
l2_1 = [df1.loc[0:81, 'pt4_cam1_X'], df1.loc[0:81, 'pt4_cam1_Y']]

l3_0 = [df0.loc[0:81, 'pt5_cam3_X'], df0.loc[0:81, 'pt5_cam3_Y']]
l3_1 = [df1.loc[0:81, 'pt4_cam3_X'], df1.loc[0:81, 'pt4_cam3_Y']]

# Not a particularly elegant way of readin things, but it works.

arr0 = []
arr1 = []
arr2 = []
arr3 = []

for i in range(81):
    arr0.append(np.sqrt((r1_0[0][i]-r1_1[0][i])**2 + (r1_0[1][i]-r1_1[1][i])**2))
    arr1.append(np.sqrt((r3_0[0][i]-r3_1[0][i])**2 + (r3_0[1][i]-r3_1[1][i])**2))
    arr2.append(np.sqrt((l2_0[0][i]-l2_1[0][i])**2 + (l2_0[1][i]-l2_1[1][i])**2))
    arr3.append(np.sqrt((l3_0[0][i]-l3_1[0][i])**2 + (l3_0[1][i]-l3_1[1][i])**2))
    
    # Calculate difference in lengths and append them to arrays.
    
plt.plot(range(81), arr0, 'r', arr1, 'g', arr2, 'b', arr3, 'y')
plt.plot(range(81), arr0, 'r', arr1, 'g', arr2, 'b', arr3, 'y')
