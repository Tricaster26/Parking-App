import os
import glob
import shutil
from jimutmap import api, sanity_check, stitch_whole_tile


download_obj = api(min_lat_deg = 24.4539,
                      max_lat_deg = 24.466,
                      min_lon_deg = 54.366,
                      max_lon_deg = 54.377,
                      zoom = 19,
                      verbose = False,
                      threads_ = 50,
                      container_dir = "myOutputFolder")

# getMasks = False if you just need the tiles
download_obj.download(getMasks = True)

# create the object of class jimutmap's api
sanity_obj = api(min_lat_deg = 24.4539,
                      max_lat_deg = 24.466,
                      min_lon_deg = 54.366,
                      max_lon_deg = 54.377,
                      zoom = 19,
                      verbose = False,
                      threads_ = 50,
                      container_dir = "myOutputFolder")

sanity_check(min_lat_deg = 24.4539,
                      max_lat_deg = 24.466,
                      min_lon_deg = 54.366,
                      max_lon_deg = 54.377,
                      zoom = 19,
                      verbose = False,
                      threads_ = 50,
                      container_dir = "myOutputFolder")

print("Cleaning up... hold on")

sqlite_temp_files = glob.glob('*.sqlite*')



# update_stitcher_db("myOutputFolder")
#Class needs to be looked into, can be better
stitch_whole_tile(save_name="Abu Dhabi", folder_name="0 Training Set")


print("Temporary sqlite files to be deleted = {} ? ".format(sqlite_temp_files))
inp = input("(y/N) : ")
if inp == 'y' or inp == 'yes' or inp == 'Y':
    for item in sqlite_temp_files:
        os.remove(item)



## Try to remove tree; if failed show an error using try...except on screen
try:
    chromdriver_folders = glob.glob('[0-9]*')
    print("Temporary chromedriver folders to be deleted = {} ? ".format(chromdriver_folders))
    inp = input("(y/N) : ")
    if inp == 'y' or inp == 'yes' or inp == 'Y':
        for item in chromdriver_folders:
            shutil.rmtree(item)
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))
