# cv_amazon_upload.py
# (c) 2019 Stanford University

from par_amazon import *
from par_streetview import *
img_dir = csv_path+"/images/"

import os
import boto3

s3 = boto3.resource('s3')

for filename in os.listdir(img_dir):
    if filename.endswith('.jpg'):
        s3.meta.client.upload_file(img_dir + filename, amazon_bucket_name, filename)
