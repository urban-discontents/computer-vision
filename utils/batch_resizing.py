import PIL
from PIL import Image
import os

# folder with the images
input_dir = "E:\\streetview\\samples\\tainan\\urbanextent14\\high-res\\"

# output dir
output_dir = "E:\\streetview\\samples\\tainan\\urbanextent14\\low-res\\"

# extension of the files
ext = ".jpg"

# adjust width and height
width = 1200
height = 600

# creating output directory
if os.path.exists(output_dir) == False:
	os.mkdir(output_dir)

# iterating through files
for root, dirs, files in os.walk(input_dir):
	for dir in dirs:
		# creates the folder
		if os.path.exists(output_dir + dir) == True:
			print(dir +" jumped!")
		else:
			os.mkdir(output_dir + dir)
			for root, dirs, files in os.walk(os.path.join(input_dir,dir)):
				for filename in files:
					# open image file
					img_file = Image.open(os.path.join(input_dir, dir, filename))
					# resize using ANTIALIAS (other options are NEAREST, BILINEAR, and BICUBIC)
					resized = img_file.resize((width, height), Image.ANTIALIAS)
					# saving
					resized.save(os.path.join(output_dir, dir, filename))

			print(dir +" resized!")
