#!/usr/bin/python
import os.path
from downloadStreetview import *

##########
# CONFIG #
##########

# path to the base folder of the sample
sample = 'tainan/urbanextent14'

# name of the csv (without extension) file with the sample coordinates (three columns in this order: sample_id, X, Y)
csv_filename = 'tainan2015_10k_100m'

#########################################
# DON'T CHANGE ANYTHING BELOW THIS LINE #
#########################################

csv_path = os.path.join('E:/streetview', 'samples', sample)
# csv_path = os.path.join('..','samples',sample)

go = DownloadSamples(csv_filename, csv_path)
