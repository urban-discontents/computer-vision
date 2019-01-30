import io, os, csv
import pandas as pd

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# importing parameters
from par_google_integration import *

# loading credentials
print('Loading Google Vision credentials...')
credential_path = credentials_file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Instantiates a Vision client
client = vision.ImageAnnotatorClient()

# Loading CSV with pandas
images = pd.read_csv(base_folder+csv_images+'.csv');
print('Initiating Processing of '+ csv_images +' through Google Vision...')

# CLeaning up the dataset
filter = images["download"] == "y"
images = images[filter]

# add new columns to pandas DataFrame
for i in range(res_num):
    images['obj'+str(i+1)] = ''
    images['obj'+str(i+1)+'_score'] = 0.0

for index, row in images.iterrows():

    # check

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        base_folder+fld_images+row['panoid']+'.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    count = 1
    for label in labels:
        images.at[index,'obj'+str(count)] = label.description
        images.at[index,'obj'+str(count)+'_score'] = label.score
        count += 1

    print('Image '+ str(row['sample_id']) +' - '+ row['panoid'] +'.jpg analyzed.')

output_file = base_folder+csv_images+'_googlevision.csv'
print('Saving results to a '+ output_file + '...')
images.to_csv(output_file)

print("Showing sample results...")
print(images.sample(10))

print("Execution ended.")
