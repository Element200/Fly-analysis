"""                         flypy
    This code is an object-oriented version of the previous code. 
    It's meant to make life easier by adding a fly as an object. 
    This makes life much easier when you want to iterate over a large
    number of files.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CWD = os.getcwd() # As long as you start in your default directory, this code will work fine.

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
    a list of all 3D coordinate files (with extension 'xyzpts')

    """
    assert (type(mode), type(directory)) == (str,str), "Invalid file type"
    assert mode == 'asym' or 'sc' or 'epi' or 'halt' # Assert statements ensure code is less breakable.
    
    csvholder = [] # This list will contain any csv files that satisfy certain conditions
    for root, dirs, files in os.walk(directory): # This can be changed later to some kind of glob.glob statement.
        for file in files:
            if file.endswith('csv') and not(file.startswith('0')):
                if mode == 'asym':
                    if (mode in file) and not('sc' in file): #This bit is necessary because slit sc files have the extension "_asym_sc_"
                        csvholder.append(file)
                elif mode == 'halt':
                    if mode in file or 'load' in file:
                        csvholder.append(file)
                else:
                    if mode in file:
                        csvholder.append(file)
    output = []
    for file in csvholder:
        if ('fly' in file) and ('xyzpts' in file):
            output.append(file)
            # This part of the code just makes sure that the files collected are in fact fly files and are the 'xyzpts' files, which contain the 3D data
    return output

def get_instructions(file_name):
    """
    Reads a .txt file and uses the information there to figure out the point naming convention.
    INSTRUCTIONS FOR WRITING AN INSTRUCTION .txt FILE:
        1) Try to minimize whitespace, I've dealt with some of it but there are always exceptions
        2) The format for a command is thus:
            a) mode=<either 'asym' or 'sc' or 'epi' or 'halt', any other command will raise an error>
            b) pointname=pointnumber
            pointname can be any of the following: 
            'lwapex' (Left Wing apex), 'rwapex' (Right Wing apex),
            'lwbase' (Left Wing base), 'rwbase' (Right Wing base),
            'fixed' (fixed point), 'lhapex' (Left Haltere apex)
            'rhapex' (Right Haltere apex), 'lhbase' (Left Haltere base), 
            or 'rhbase' (Right Haltere base)
            pointnumber must be an integer.
        3) To write a comment, make sure the text is preceded by a '#'

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
            
    # raise FileNotFoundError

class statistic(object):
    """This class just contains a bunch of statistical operations that are useful
        for statistical analysis of anything. It takes an array as an input and spits 
        out averages, means, standard deviation, and so on.
    """
    def __init__(self, array):
        self.array = array
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
        
        #Plots all winglengths. Doesn't plot errors, though
    
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
        """
        assert (type(file_name), type(flynumber), type(trial)) == (str, int, str), "Erroneous input!"
        try: 
            file = find_file(file_name)
            instructions = get_instructions(file)
            mode = instructions['mode']
            self.mode = mode
            self.flynumber = flynumber
            self.trial = trial        
            print('You are viewing fly'+ str(flynumber)+'_'+str(trial), 'in', str(mode), 'mode.')
            assert mode in ['asym', 'sc', 'epi', 'halt'], "Unknown mode"
            pointnames = ['lwapex','rwapex','lwbase','rwbase','fixed','lhapex','rhapex','lhbase','rhbase']
            if mode in ['asym', 'sc']:
                self.points = {pointnames[i]:int(instructions[pointnames[i]]) for i in range(5)}
            else:
                self.points = {pointnames[i]:int(instructions[pointnames[i]]) for i in range(9)}
        
        except FileNotFoundError: 
            print("Couldn't find", file_name)
    
    def __str__(self):
        """Makes representing classes easy"""
        string = "fly"+ str(self.flynumber)+ "_"+ str(self.trial) + " in mode: "+ str(self.mode) + "."
        return string
    
    def open_csv(self):
        """
        Opens the csv file corresponding to the appropriate fly number and trial
        
        Returns
        -------
        The Pandas dataframe from the csv file.

        """
        try:
            flynumber = self.flynumber
            trial = self.trial
            files = get_3d_coord_files(self.mode, CWD)
            csv = None # csv is NoneType by default, finding 
            for file in files:
                index = file.index('fly') + 3 # +3 because 'fly' has 3 letters, and at this position, the fly number will be declared.
                if file[index] == str(flynumber):
                    if trial in file:
                        csv = file # Set the csv file equal to the file we found. 
            if type(csv) != None:
                print("A file was found!")
                print(csv)
                
                self.file_name = find_file(csv) # New global variable, initiated only if open_csv() is called
                df = pd.read_csv(self.file_name)
                return df
            else:
                print("No file found!")
    
        except FileNotFoundError:
            print("No file found in module open_csv")
            
            print("The file name is:", self.file_name)
            raise FileNotFoundError
            
        
    def get_points(self):
        """
        Generates a points list out of all the csv data

        Returns
        -------
        A list with sublists corresponding to all the point data in coordinate format

        """
        try:
            df = self.open_csv() # Get the Pandas dataframe
            rows = len(df.axes[0])
            self.rows = rows # New global variable
            points = []
            for i in range(5+(self.mode == 'epi' or self.mode == 'halt')*4): # The thing within the range(parentheses) just means "5 if the mode is not 'epi' or 'halt', 9 otherwise"
                points.append([])
            print("Rows:", rows); print()
            numpoints = 5 + (self.mode == 'epi' or self.mode == 'halt')*4
            for j in range(numpoints):
                for i in range(rows):
                    x = df.loc[i, df.columns[3*j]]
                    y = df.loc[i, df.columns[3*j+1]]
                    z = df.loc[i, df.columns[3*j+2]]
                    points[j].append((x,y,z)) # XYZ data is stored in tuples, not lists. Makes things easier to read, plus it's faster.
            points_dictionary = {key : points[self.points[key]-1] for key in self.points} # self.points[key] - 1 because counting from 0 and all that mess.
            # Points dictionary maps the name of a point to the list of points corresponding to the name. For instance, 'lwapax' in 'epi' will be mapped to points[0], the first in the points list
            return points_dictionary
        except FileNotFoundError:
            print("No file found in module get_points")
            raise FileNotFoundError
    
    def find_winglengths(self):
        """
        Calculate the winglengths out of the previously generated point data

        Returns
        -------
        tuple
            first part = left winglengths
            second part = right winglengths
        """
        def length(v1, v2):
            """Handy function to calculate lengths given two tuples."""
            return ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2)**0.5
        try:
            points_dictionary = self.get_points()
            left_lengths = []
            right_lengths = [] # Create two variables to store length data
            for i in range(self.rows):
                left_lengths.append(length(points_dictionary['lwapex'][i], points_dictionary['lwbase'][i])) # Calculate and append
                right_lengths.append(length(points_dictionary['rwapex'][i], points_dictionary['rwbase'][i])) # lengths to both lists
            return left_lengths, right_lengths # return the two lists as a tuple. Remember to assign two variables while calling this function
        except FileNotFoundError:
            print("File not found in module find_winglengths")
    def print_statistics(self):
        """
        This function just prints out the statistical data
        Returns nothing, its only job is to print
        """
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
    def get_errors(self):
        left_lengths, right_lengths = self.find_winglengths()
        left = statistic(left_lengths); right = statistic(right_lengths)
        self.left_averr, self.right_averr, self.left_maxerr, self.right_maxerr = left.get_stderr(), right.get_stderr(), left.get_maxerr(), right.get_maxerr()
        return self.left_averr, self.right_averr, self.left_maxerr, self.right_maxerr
    
    def plot_statistics(self):
        """
        Plots the aforementioned statistical data.
        Returns: nothing, its only purpose is to plot stuff.
        """
        left_lengths, right_lengths = self.find_winglengths()
        left = statistic(left_lengths); right = statistic(right_lengths)
        left.plot_vals()
        right.plot_vals()
