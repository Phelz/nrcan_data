import os, sys, glob, gc

from datetime import datetime, timedelta
import numpy as np

from read_matlab_data import DataFile
import pickle

# Saving object
def write_object(file_name, obj):

    with open(file_name, 'wb') as o:
    
        pickle.dump(obj, o)

# Loading object
def load_object(file_name):

    with open(file_name, 'rb') as o:

        loaded_object = pickle.load(o)

    return loaded_object

CURR_DIR = os.getcwd()
DATA_FOLDER = "%s\\matlab_files\\" % (CURR_DIR)


folder_list = glob.glob("%s\\*" % (DATA_FOLDER))
separated_file_list = [ glob.glob("%s\\*" % (folder)) for folder in folder_list  ] 

files = []
for file_path in separated_file_list[-1]:

    data_file = DataFile(file_path)
    files.append( data_file )


print(files[0:2])
    

