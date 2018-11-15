#!/usr/bin/python

#################
# CONFIGURATION #
#################

# path to the base folder of the sample
csv_path = 'D:/dev/vagrant/ubuntu14-04/computer-vision/samples/curitiba/periphery/'
#csv_path = '/afs/ir.stanford.edu/users/l/b/lbarleta/urban-discontents/streetview/phoenix/downtown/'

# name of the csv (without extension) file with the sample coordinates (three columns in this order: sample_id, X, Y)
csv_filename = 'sample_vila_pinto_50p_30m'

# DEPRECATED - we're not using API key for now
# create a python file in the same folder named safe.py with the following line:
# api_key = YOUR_API_KEY