#!/usr/bin/python

#################
# CONFIGURATION #
#################

# path to the base folder of the sample
csv_path = 'C:/Computer Vision/computer-vision/samples/curitiba/periphery75/'
#csv_path = '/afs/ir.stanford.edu/users/l/b/lbarleta/urban-discontents/streetview/phoenix/downtown/'

# name of the csv (without extension) file with the sample coordinates (three columns in this order: sample_id, X, Y)
csv_filename = 'sample_ctba75_periphery_1k_400m'

# set the id number you want the script to start processing. it will download all ids that are equal or higher than that.
# set to -1 if you want to download the entire list
start_id = -1

# DEPRECATED - we're not using API key for now
# create a python file in the same folder named safe.py with the following line:
# api_key = YOUR_API_KEY
