import io
import os
#import google.auth

credential_path = 'testing-urban-b5ca3188f903.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'img_samples/5HBZ76sDAYrF6ZtyPZ531Q.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description + " " + label.mid + " " + str(label.score) )
