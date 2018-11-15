import PIL
from PIL import Image
import os

# folder with the images
img_dir = "imgs/"

# output dir
output_dir = "lowres2/"

# extension of the files
ext = ".jpg"

# adjust width and height
width = 1000
height = 500

# creating output directory
if os.path.exists(output_dir) == False:
	os.mkdir(output_dir)

# iterating through files
for root, dirs, files in os.walk(img_dir):  
	for filename in files:
		# open image file
		img_file = Image.open(img_dir+filename)
		# resize using ANTIALIAS (other options are NEAREST, BILINEAR, and BICUBIC)
		resized = img_file.resize((width, height), Image.ANTIALIAS)
		# saving 
		resized.save(output_dir+filename)
		
		print(filename +" resized!")