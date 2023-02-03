import os, glob, shutil
from time import sleep

from concurrent.futures import ProcessPoolExecutor as ppe

CURR_DIR = os.getcwd()
DATA_FOLDER = "%s\\matlab_files\\" % (CURR_DIR)

separated_list = [ glob.glob("%s\\*_%4d*" % (DATA_FOLDER, year) ) for year in range(2013, 2019 + 1) ]


def move_file(file):

    year_str = file.split("\\")[-1].split("_")[-2][:4]

    new_path = file.replace(DATA_FOLDER, "%s\\%s\\" % (DATA_FOLDER, year_str))
    if not os.path.isfile( new_path ):
        shutil.move(file, new_path)

    sleep(0.1)

def main():
    with ppe(max_workers=4) as executor:

        for list_indx, file_list in enumerate(separated_list):
            executor.map( move_file, file_list )


if __name__ == "__main__":
    main()



