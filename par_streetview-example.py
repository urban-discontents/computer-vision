#!/usr/bin/python

#################
# CONFIGURATION #
#################

# path to the base folder of the sample
csv_path = 'C:/Computer Vision/computer-vision/samples/phoenix/periphery75/'

# name of the csv (without extension) file with the sample coordinates (three columns in this order: sample_id, X, Y)
csv_filename = 'phoenix75_periphery_sample_1k_400m' # phoenix

# set the id number you want the script to start processing. it will download all ids that are equal or higher than that.
# set to -1 if you want to download the entire list
# not working
start_id = -1

# extension of the files
extension = ".jpg"

# adjust width and height for the low resolution images
width = 1000
height = 500

# DEPRECATED - we're not using API key for now
# create a python file in the same folder named safe.py with the following line:
# api_key = YOUR_API_KEY
api_key = ''
