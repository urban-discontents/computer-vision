#!/usr/bin/python

#################
# CONFIGURATION #
#################

# path to the base folder of the sample
<<<<<<< HEAD
#csv_path = 'E:/computer-vision/samples/curitiba/periphery/' # curitiba
csv_path = 'C:/Computer Vision/computer-vision/samples/phoenix/periphery14/' # phoenix
#csv_path = '/afs/ir.stanford.edu/users/l/b/lbarleta/urban-discontents/streetview/phoenix/downtown/'

# name of the csv (without extension) file with the sample coordinates (three columns in this order: sample_id, X, Y)
#csv_filename = 'sample_points_1k' # curitiba
csv_filename = 'phoenix14_periphery_sample_1k_400m' # phoenix
=======
csv_path = 'D:/dev/vagrant/ubuntu14-04/computer-vision/samples/pune/' # pune

# name of the csv (without extension) file with the sample coordinates (three columns in this order: sample_id, X, Y)
csv_filename = 'pune_sample_1k_400m'
>>>>>>> ed92cbd30e33e7ab311c078388f4b19d7d833e5d

# set the id number you want the script to start processing. it will download all ids that are equal or higher than that.
# set to -1 if you want to download the entire list
start_id = -1
<<<<<<< HEAD
=======

# extension of the files
ext = ".jpg"

# adjust width and height for the low resolution images
width = 1000
height = 500
>>>>>>> ed92cbd30e33e7ab311c078388f4b19d7d833e5d

# DEPRECATED - we're not using API key for now
# create a python file in the same folder named safe.py with the following line:
# api_key = YOUR_API_KEY
api_key = ''
