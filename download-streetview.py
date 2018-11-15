#!/usr/bin/python

import csv, random, sys, os, shutil
# makes sure you have this library: https://github.com/robolyst/streetview
import streetview

# importing parameters
from par_streetview import *

# create image and tiles directories
img_dir = csv_path+"images/"
if os.path.exists(img_dir) == False:
	os.mkdir(img_dir)
	
# creates a new CSV to save the panoids for each sample LatLong
with open(csv_path+csv_filename+"_panoids.csv", mode='w') as images:
	fieldnames = ['sample_id','panoid','lat','lon','year','month','download']
	writer = csv.DictWriter(images, fieldnames=fieldnames)
	writer.writeheader()
	
	# iterates through the csv with the sample LatLong
	with open(csv_path+csv_filename+".csv", 'r') as f:
		reader = csv.reader(f)
			
		#For each sample
		for row in reader:
			#search for panoids
			panoids = streetview.panoids(lat=row[2], lon=row[1])
			
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
					
					## uncomment this images for also downloading the 2d images
					streetview.api_download(panoid['panoid'], 0, pano_dir)
					streetview.api_download(panoid['panoid'], 90, pano_dir)
					streetview.api_download(panoid['panoid'], 180, pano_dir)
					streetview.api_download(panoid['panoid'], 270, pano_dir)

					# deleting tile files
					shutil.rmtree(tile_dir)
					
					print("sample "+ row[0] +" : "+ panoid['panoid'] +" downloaded")
					
				else:
					truple['download'] = "n"
					
				writer.writerow(truple)
print('end')