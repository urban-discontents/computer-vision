# cv_amazon_integration.py
# (c) 2019 Stanford University

from par_amazon import *

import boto3

s3 = boto3.resource('s3')
client = boto3.client('rekognition')

bucket = s3.Bucket(amazon_bucket_name)

for obj in bucket.objects.all():
    response = client.detect_labels(Image={
        'S3Object': {
            'Bucket': amazon_bucket_name,
            'Name': obj.key
        }
    })

    print(response['Labels'])
