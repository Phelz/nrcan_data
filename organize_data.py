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

nrcan_frequencies = [ 5.382, 6.9285, 8.0995, 10.422, 11.107, 14.3644 ]


if __name__ == "__main__":

    for year_indx, (year, file_list) in enumerate( zip([2013, 2014, 2016, 2017, 2019], separated_file_list) ):

        freq_files = []
        for freq in nrcan_frequencies:

            data_dir = "data\\%4d\\" % (year)
            if not os.path.isdir(data_dir): os.makedirs(data_dir)

            data_path_name = "%s\\%4d_%.4f" % (data_dir, year, freq)
            data_path_name = data_path_name.replace(".", "p") + ".dat"

            for file_path in file_list:
                
                data_file = DataFile(file_path)

                if data_file.frequency == freq:
                    freq_files.append(data_file)
                else: continue

            write_object( data_path_name, freq_files )
            freq_files = []
            







