"""         Get files
    Finds all relevent files in the folder and picks a method
    of classifying points based on a .txt file
    """
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CWD = os.getcwd()

class statistic(object):
        def __init__(self, array):
            self.array = array
            self.reallen = array.count(np.nan)
        def get_range(self):
            return max(self.array)-min(self.array)
        def get_mean(self):
            return np.nanmean(self.array)
        def get_dev(self):
            return [np.abs(element-self.get_mean()) for element in self.array]
        def get_stdev(self):
            return np.nanmean(self.get_dev())
        def get_stderr(self):
            return self.get_stdev()/self.get_mean()
        def get_maxerr(self):
            mean = self.get_mean()
            return max(np.abs(max(self.array)-mean), np.abs(min(self.array)-mean))/mean
        def plot_vals(self):
            array = self.array
            plt.plot(array, 'b')
            plt.plot([max(array)]*len(array), 'g')
            plt.plot([min(array)]*len(array), 'r')
            plt.plot([self.get_mean()]*len(array), 'y')
            plt.show()
        
            
        

def get_3d_coord_files(mode, directory):
    """
    Parameters
    ----------
    trial : string
        Use 'asym' for asymmetric wings, 'sc' for slit sc,
        'epi' for epi ridge cut, and 'halt' for haltere loading.
    directory : string
        This folder contains all csv files.

    Returns
    -------
    a list of all 3D coordinate files (with extension '_xyzpts')

    """
    assert (type(mode), type(directory)) == (str,str), "Invalid file type"
    assert mode == 'asym' or 'sc' or 'epi' or 'halt'
    
    csvholder = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('csv') and not(file.startswith('0')):
                if mode == 'asym':
                    if ('asym' in file) and not('sc' in file):
                        csvholder.append(file)
                elif mode == 'sc':
                    if ('asym' in file) and ('sc' in file):
                        csvholder.append(file)
                elif mode == 'epi':
                    if 'epi' in file:
                        csvholder.append(file)
                elif mode == 'halt':
                    if not(('epi' in file) or ('asym' in file)):
                        csvholder.append(file)
    output = []
    for file in csvholder:
        if ('fly' in file) and ('xyzpts' in file):
            output.append(file)
    return output

def get_instructions(file_name):
    """
    

    Parameters
    ----------
    file_name : string
        A .txt file containiing instructions for what point corresponds
        to what part of the fly.

    Returns
    -------
    output : dictionary
        A dictionary containing the name of the point as the key and the 
        number as the value

    """
    output = {}
    with open(file_name, 'r') as file:
        for line in file:
            if not(line.startswith('#')):
                words = line.split('=')
                output[words[0].strip()] = words[1].strip()
    return output

def find_file(file_name):
    """
    Parameters
    ----------
    file_name : string
        The name of the file to be found
    Raises
    ------
    FileNotFoundError if the file doesn't exist
    Returns
    -------
    Name and directory of file if found.
    """
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == file_name:
                return os.path.join(root,file)
    raise FileNotFoundError
    

    
class fly(object):
    """
    Contains a fly in one of four modes(asym, epi, sc, or halt). The mode, along with how to read the points, 
    is determined by a text file of name type 'data_organization_<mode>.txt'.
    After this, the functions 'open_csv' and 'get_points' - which take in the fly number and
    experiment trial as arguments - then look up the relevant .csv file and open it, arranging
    data appropriately into tuples. 
    """
    def __init__(self, file_name, flynumber, trial):
        """
        Parameters
        ----------
        flynumber : int
            Number of fly being used (fly1, fly2, etc.)
        trial: string
            Experimental trial (cutwing1, cutwing2, intactwings, etc.). The number of times the trial has been done is irrelevant;
            don't type in "cutwing1_1", for instance.
        file_name : string
            A .txt file containing the instructions for how to read the points
        Returns
        -------
        None.

        """
        try: file = find_file(file_name)
        except FileNotFoundError: print("Couldn't find", file_name)
        instructions = get_instructions(file)
        mode = instructions['mode']
        self.mode = mode
        self.flynumber = flynumber
        self.trial = trial        
        print('You are viewing fly'+ str(flynumber)+'_'+trial, 'in', mode, 'mode.')
        assert mode == 'asym' or mode == 'sc' or mode == 'epi' or mode == 'halt', "Unknown mode"
        pointnames = ['lwapex','rwapex','lwbase','rwbase','fixed','lhapex','rhapex','lhbase','rhbase']
        if mode == 'asym' or mode == 'sc':
            self.points = {pointnames[i]:int(instructions[pointnames[i]]) for i in range(5)}
        else:
            self.points = {pointnames[i]:int(instructions[pointnames[i]]) for i in range(9)}
    
    def __str__(self):
        return "Fly"+ self.flynumber, "in", self.trial, "in mode:", self.mode + "."
    
    def open_csv(self):
        """
        Opens the csv file corresponding to the appropriate fly number and trial

        Parameters
        ----------
        flynumber : int
            The number of the fly - for instance fly1, fly2, and so on.
        trial : string
            cutwing1, cutwing2, etc. Ignore the number of times the experiment has been done;
            don't type in "intactwings_1" or something like that, just type "intactwings.
        You only need specify these if you don't want the program evaluating the default fly for whatever reason.
        Returns
        -------
        The dataframe from the csv file.

        """
        flynumber = self.flynumber
        trial = self.trial
        files = get_3d_coord_files(self.mode, CWD)
        csv = None
        for file in files:
            index = file.index('fly') + 3
            if file[index] == str(flynumber):
                if trial in file:
                    csv = file
        if type(csv) != None:
            df = pd.read_csv(find_file(csv))
            
            return df
        else:
            print("No file found")
            return
        
    def get_points(self):
        """
        Generates a points list out of all the csv data

        Returns
        -------
        A list with sublists corresponding to all the point data in coordinate format

        """
        df = self.open_csv()
        rows = len(df.axes[0])
        self.rows = rows
        points = []
        for i in range(5+(self.mode == 'epi' or self.mode == 'halt')*4):
            points.append([])
        print("Rows:", rows)
        numpoints = 5 + (self.mode == 'epi' or self.mode == 'halt')*4
        for j in range(numpoints):
            for i in range(rows):
                x = df.loc[i, df.columns[3*j]]
                y = df.loc[i, df.columns[3*j+1]]
                z = df.loc[i, df.columns[3*j+2]]
                points[j].append((x,y,z)) 
        points_dictionary = {key : points[self.points[key]-1] for key in self.points}
        return points_dictionary
    
    def find_winglengths(self):
        def length(v1, v2):
            return ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2)**0.5
        points_dictionary = self.get_points()
        left_lengths = []
        right_lengths = []
        for i in range(self.rows):
            left_lengths.append(length(points_dictionary['lwapex'][i], points_dictionary['lwbase'][i]))
            right_lengths.append(length(points_dictionary['rwapex'][i], points_dictionary['rwbase'][i]))
        return left_lengths, right_lengths
    def print_statistics(self):
        left_lengths, right_lengths = self.find_winglengths()
        left = statistic(left_lengths); right = statistic(right_lengths)
        print("Left range:", left.get_range())
        print("Right range:", right.get_range())
        print("Left average:", left.get_mean())
        print("Right average:", right.get_mean())
        print("Left mean deviation:", left.get_stdev())
        print("Right mean deviation:", right.get_stdev())
        print("Left standard error:", left.get_stderr())
        print("Right standard error:", right.get_stderr())
        print("Left maximum error:", left.get_maxerr())
        print("Right maximum error:", right.get_maxerr())
    def plot_statistics(self):
        left_lengths, right_lengths = self.find_winglengths()
        left = statistic(left_lengths); right = statistic(right_lengths)
        left.plot_vals()
        right.plot_vals()
    
        













