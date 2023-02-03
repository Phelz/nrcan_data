import pickle
from classes import DataFile

# Saving object
def write_object(file_name, obj):

    with open(file_name, 'wb') as o:
    
        pickle.dump(obj, o)

# Loading object
def load_object(file_name):

    with open(file_name, 'rb') as o:

        loaded_object = pickle.load(o)

    return loaded_object