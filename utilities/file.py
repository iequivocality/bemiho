import os
from os.path import join, exists, isdir

def create_directory(directory_path):
    print(directory_path)
    try:
        if (not exists(directory_path)):
            os.mkdir(directory_path)
            print ("Successfully created the directory %s" % directory_path)
        else:
            print("Output folder creation not necessary")
    except OSError:  
        print ("Creation of the directory %s failed" % directory_path)