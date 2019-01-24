#!/usr/bin/python

import csv, random, sys, os, shutil
# makes sure you have this library: https://github.com/robolyst/streetview
import streetview
from PIL import Image

try:
   from safe import *
except ImportError:
   pass

##########
# SCRIPT #
##########

# importing parameters
from par_streetview import *

# create image and tiles directories
<<<<<<< HEAD
img_dir = csv_path+"/images/"
if os.path.exists(img_dir) == False:
	os.mkdir(img_dir)

# creates a new CSV to save the panoids for each sample LatLong
with open(csv_path+csv_filename+"_panoids.csv", mode='a') as images:

=======
img_dir = csv_path+"images/"
imglow_dir = csv_path+"images-low/"
if os.path.exists(img_dir) == False:
	os.mkdir(img_dir)
	os.mkdir(imglow_dir)
	
# creates a new CSV to save the panoids for each sample LatLong
with open(csv_path+csv_filename+"_panoids.csv", mode='w') as images:
	
>>>>>>> ed92cbd30e33e7ab311c078388f4b19d7d833e5d
	# write header in case it is a new file
	if start_id == -1:
		fieldnames = ['sample_id','panoid','lat','lon','year','month','download']
		writer = csv.DictWriter(images, fieldnames=fieldnames)
		writer.writeheader()
<<<<<<< HEAD

=======
		
>>>>>>> ed92cbd30e33e7ab311c078388f4b19d7d833e5d
	# iterates through the csv with the sample LatLong
	with open(csv_path+csv_filename+".csv", 'r') as f:
		reader = csv.reader(f)

		#For each sample
		for row in reader:
			# uncomment for starting at a certain sample_id
			if row[0] == 'id' or int(row[0]) < start_id:
<<<<<<< HEAD
				print('jumping id: '+ row[0])
				continue

			#search for panoids
			panoids = streetview.panoids(lat=row[2], lon=row[1])

=======
				print('jumping id '+ row[0])
				continue
				
			#search for panoids
			panoids = streetview.panoids(lat=row[2], lon=row[1])
			
			print(panoids)
			
>>>>>>> ed92cbd30e33e7ab311c078388f4b19d7d833e5d
			# select a random panoid for download
			if panoids:
				selected = random.choice(panoids)

			# write the panoids in a file
			for panoid in panoids:
				truple = {'sample_id': row[0],'panoid': panoid['panoid'],'lat': panoid['lat'],'lon': panoid['lon']}
				if 'year' in panoid:
					truple['year'] = panoid['year']
				if 'month' in panoid:
					truple['month'] = panoid['month']

				# mark and download the randomly selected panoid
				if selected['panoid'] == panoid['panoid']:
					truple['download'] = "y"

					# create directories for downloading tiles
					pano_dir = img_dir+row[0] +"__"+ panoid['panoid']
					os.mkdir(pano_dir)
					tile_dir = pano_dir+'/tiles'
					os.mkdir(tile_dir)

					print("downlading "+ row[0] +" : "+ panoid['panoid'] +"...")

					# search for the 360 tiles
					tiles = streetview.tiles_info(panoid['panoid'])

					# download tiles
					streetview.download_tiles(tiles, tile_dir)

					# stiching tiles together
					streetview.stich_tiles(panoid['panoid'], tiles, tile_dir, img_dir)
<<<<<<< HEAD

=======
					
					# generating low resolutionTODO
					print("generating low resolution image for "+ row[0] +" : "+ panoid['panoid'] +"...")
					img_file = Image.open(img_dir+panoid['panoid']+extension)
					resized = img_file.resize((width, height), Image.ANTIALIAS)
					resized.save(imglow_dir+panoid['panoid']+extension)
					
>>>>>>> ed92cbd30e33e7ab311c078388f4b19d7d833e5d
					## uncomment this images for also downloading the 2d images
					#streetview.api_download(panoid['panoid'], 0, pano_dir)
					#streetview.api_download(panoid['panoid'], 90, pano_dir)
					#streetview.api_download(panoid['panoid'], 180, pano_dir)
					#streetview.api_download(panoid['panoid'], 270, pano_dir)

					# deleting tile files
					shutil.rmtree(tile_dir)

					print("sample "+ row[0] +" : "+ panoid['panoid'] +" downloaded")

				else:
					truple['download'] = "n"

				writer.writerow(truple)
print('end')
