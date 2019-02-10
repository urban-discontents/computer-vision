# cv_amazon_integration.py
# (c) 2019 Stanford University

import par_amazon as config
import boto3, os, csv

def csv_to_dict(f):
    return [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]

s3 = boto3.resource('s3')
client = boto3.client('rekognition')

imagelist_fname = os.path.join(
    os.getcwd(),
    config.downloaded_imagelist_fname + '.csv')

with open(imagelist_fname, 'r') as imagelist_file:
    imagelist = csv_to_dict(imagelist_file)
    for image in imagelist:
        if image['download'] is 'y':
            response = client.detect_labels(Image={
                'S3Object': {
                    'Bucket': config.aws_bucket_name,
                    'Name': image['panoid']
                }
            })
            
            counter = 1
            for label in response['Labels']:
                # Rekognitions tells us *where* an object is, but
                # we're ignoring that for now.
                key_prefix = 'obj' + str(counter)
                image[key_prefix] = label['Name']
                image[key_prefix + '_score'] = label['Confidence']

                counter += 1
    
    output_fname = os.path.join(
        os.getcwd(),
        config.downloaded_imagelist_fname + '_rekognition.csv')
    
    with open(output_fname, 'w') as outputf:
        dictwriter = csv.DictWriter(outputf, imagelist[0].keys())
        dictwriter.writeheader()
        dictwriter.writerows(imagelist)
