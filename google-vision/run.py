#!/usr/bin/python
##########
# CONFIG #
##########

## Credetials for Google Computer Vision (.json)
## Should be inside folder 'safe'
credentials_file = 'testing-urban-b5ca3188f903.json'


# Name of the city and the sample
city = 'phoenix'
sample = 'urbanextent14'


## URL with the images
base_url = 'http://lbarleta.su.domains/discontents/samples/'

## Max number of labels expected
max_labels = 30

## Score Threshold
score_threshold = 0.5

#########################################
# DON'T CHANGE ANYTHING BELOW THIS LINE #
#########################################

from processGoogleVision import *
base_url = base_url + '/' + city + '/' + sample +'/low-res/'
#base_url = base_url + '/' + city + '/urbanextent14/low-res/'
go = processGoogleVision(city, sample, credentials_file, base_url, max_labels, score_threshold)
