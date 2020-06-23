import os
#import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def length(w,x,y,z):
    l = np.sqrt((w[1]-w[0])**2+(x[1]-x[0])**2+(y[1]-y[0])**2+(z[1]-z[0])**2)
    return l

os.chdir('C:/Users/Dinesh/Downloads')
file = 'fly2_asym_cutwing1_1_originalflippedxypts.csv'
test = 'fly2_asym_cutwing1_1_offsettestxypts.csv'

df0 = pd.read_csv(file)
df1 = pd.read_csv(test)

r1_0 = [df0.loc[0:81, 'pt4_cam2_X'], df0.loc[0:81, 'pt4_cam2_Y']]
r1_1 = [df1.loc[0:81, 'pt5_cam2_X'], df1.loc[0:81, 'pt5_cam2_Y']]

r3_0 = [df0.loc[0:81, 'pt4_cam3_X'], df0.loc[0:81, 'pt4_cam3_Y']]
r3_1 = [df1.loc[0:81, 'pt5_cam3_X'], df1.loc[0:81, 'pt5_cam3_Y']]

l2_0 = [df0.loc[0:81, 'pt5_cam1_X'], df0.loc[0:81, 'pt5_cam1_Y']]
l2_1 = [df1.loc[0:81, 'pt4_cam1_X'], df1.loc[0:81, 'pt4_cam1_Y']]

l3_0 = [df0.loc[0:81, 'pt5_cam3_X'], df0.loc[0:81, 'pt5_cam3_Y']]
l3_1 = [df1.loc[0:81, 'pt4_cam3_X'], df1.loc[0:81, 'pt4_cam3_Y']]

arr0 = []
arr1 = []
arr2 = []
arr3 = []

for i in range(81):
    arr0.append(np.sqrt((r1_0[0][i]-r1_1[0][i])**2 + (r1_0[1][i]-r1_1[1][i])**2))
    arr1.append(np.sqrt((r3_0[0][i]-r3_1[0][i])**2 + (r3_0[1][i]-r3_1[1][i])**2))
    arr2.append(np.sqrt((l2_0[0][i]-l2_1[0][i])**2 + (l2_0[1][i]-l2_1[1][i])**2))
    arr3.append(np.sqrt((l3_0[0][i]-l3_1[0][i])**2 + (l3_0[1][i]-l3_1[1][i])**2))
    
plt.plot(range(81), arr0, 'r', arr1, 'g', arr2, 'b', arr3, 'y')