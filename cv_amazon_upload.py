# cv_amazon_upload.py
# (c) 2019 Stanford University

import par_amazon as config

import os
import boto3
import csv

def csv_to_dict(f):
    return [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

s3 = boto3.resource('s3')

imagelist_fname = os.path.join(
    os.getcwd(),
    config.downloaded_imagelist_fname + '.csv')

with open(imagelist_fname, 'r') as imagelist_file:
    imagelist = csv_to_dict(imagelist_file)
    for image in imagelist:
        if image['download'] is 'y':
            image_fn = os.path.join(
                os.getcwd(),
                config.downloaded_images_folder,
                image['panoid'] + '.jpg')

            s3.meta.client.upload_file(image_fn,
                config.aws_bucket_name,
                image['panoid'])
