#!/usr/bin/python
import os.path
from downloadStreetview import *

##########
# CONFIG #
##########

# path to the base folder of the sample
sample = 'testing/sample1'

# name of the csv (without extension) file with the sample coordinates (three columns in this order: sample_id, X, Y)
csv_filename = 'samplecsv'


#########################################
# DON'T CHANGE ANYTHING BELOW THIS LINE #
#########################################

csv_path = os.path.join('..','samples',sample)

go = DownloadSamples(csv_filename, csv_path)
