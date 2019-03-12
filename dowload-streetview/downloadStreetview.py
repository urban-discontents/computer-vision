import streetview, os.path, random, time, shutil, cv2, glob, sys, json
import numpy as np
import pandas as pd
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

class DownloadSamples:
    ext = '.jpg'
    width = 1000
    height = 500

    def __init__(self, csv_file, sample_name):
        print('Initialization the download of sample: '+ sample_name)
        self._input = os.path.join(sample_name, csv_file + '.csv')
        self._output = os.path.join(sample_name, csv_file + '_panoids.csv')

        # create directory stucture
        print('Creating folder structure')
        self._tiles_dir = os.path.join(sample_name, 'tiles')
        self._lowres_dir = os.path.join(sample_name, 'low-res')
        self._highres_dir = os.path.join(sample_name, 'high-res')

        if os.path.isdir(self._tiles_dir) == True:
            shutil.rmtree(self._tiles_dir)

        os.mkdir(self._tiles_dir)

        if os.path.isdir(self._lowres_dir) == False:
            os.mkdir(self._lowres_dir)
            os.mkdir(self._highres_dir)

        # open csv file and prepare dataset
        self._list = pd.read_csv(self._input);
        self._list['panoid'] = ''
        self._list['year'] = 0
        self._list['month']= 0
        self._list['download'] = 'n'

        # don't generate panoid list if already exists
        if os.path.isfile(self._output) == False:
            self._list.to_csv(self._output, index=False)
        else:
            self._list = pd.read_csv(self._output)

        self.GetRandomPanoIds()
        self.DownloadPanos()

    def GetRandomPanoIds(self):
        print('Fetching panos info (this step may take several minutes)')
        counter = 0
        start_time = time.time()
        filter = self._list["download"] == "n"

        for index, row in self._list[filter].iterrows():
            # get all pano ids for each image
            panoids = streetview.panoids(lat=row[2], lon=row[1])

            if panoids:
                # choose a random pano id to download
                panoid = random.choice(panoids)

                self._list.at[index, 'panoid'] = panoid['panoid']
                self._list.at[index, 'download'] = 'r'

                if 'year' in panoid:
                    self._list.at[index, 'year'] = panoid['year']
                if 'month' in panoid:
                    self._list.at[index, 'month'] = panoid['month']
            else:
                self._list.at[index, 'download'] = 'x'

            counter = counter + 1
            if counter % 50 == 0:
                print("Fetched "+ str(counter) + " panoids in "+ str(time.time() - start_time) + " seconds")
                start_time = time.time()

                # saving the list with selected panoids every 100 rows
                self._list.to_csv(self._output, index=False)

    def DownloadPanos(self):
        # load dataframe with panoids
        filter = self._list["download"] == "r"

        for index, row in self._list[filter].iterrows():
            start_time = time.time()
            print("Downloading panorama id "+ str(row['id']))
            # search, download, stich tiles and save panorama
            tiles = streetview.tiles_info(row['panoid'])
            streetview.download_tiles(tiles, self._tiles_dir)

            pano_dir = os.path.join(self._highres_dir,str(row['id']).rjust(6,'0') +'_'+ row['panoid'])
            if os.path.isdir(pano_dir) == False:
                os.mkdir(pano_dir)

            streetview.stich_tiles(row['panoid'], tiles, self._tiles_dir, pano_dir)
            self._list.at[index, 'download'] = 'y' # download successfull

            # generating low resolution
            print("Generating low-res image "+ str(row['id']))
            img_file = Image.open(os.path.join(pano_dir, row['panoid']+self.ext))
            resized = img_file.resize((self.width, self.height), Image.ANTIALIAS)
            resized.save(os.path.join(self._lowres_dir,str(row['id']).rjust(6,'0') +'_'+ row['panoid']+self.ext))

            # generating 4 perspectives
            equ = Equirectangular(os.path.join(pano_dir, row['panoid']+self.ext))
            for j in range(4):
                img = equ.GetPerspective(90, j*90, 0, 2400, 2400)
                oupname = os.path.join(pano_dir, "view_"+ str(j) + self.ext)
                cv2.imwrite(oupname, img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                print('Saved perspective ' + str(j*90))

#            except:
#                self._list.at[index, 'download'] = 'n' # n again, to search for a new panoid in the next run
#                print("Image "+ str(row['id']) +" couldn't be downloaded.")

            self._list.to_csv(self._output, index=False)

            # remove tiles
            for filename in glob.glob(os.path.join(self._tiles_dir, row['panoid'] +"*")):
                os.remove(filename)

            print("Download completed in "+ str(time.time() - start_time) + " seconds")

        shutil.rmtree(self._tiles_dir)
        print("Download completed!")

class Equirectangular:
    def __init__(self, img_name):
        self._img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        #print(self._img)
        [self._height, self._width, _] = self._img.shape
        #cp = self._img.copy()
        #w = self._width
        #self._img[:, :w/8, :] = cp[:, 7*w/8:, :]
        #self._img[:, w/8:, :] = cp[:, :7*w/8, :]

    def GetPerspective(self, FOV, THETA, PHI, height, width, RADIUS = 128):
        #
        # THETA is left/right angle, PHI is up/down angle, both in degree
        #

        equ_h = self._height
        equ_w = self._width
        equ_cx = (equ_w - 1) / 2.0
        equ_cy = (equ_h - 1) / 2.0

        wFOV = FOV
        hFOV = float(height) / width * wFOV

        c_x = (width - 1) / 2.0
        c_y = (height - 1) / 2.0

        wangle = (180 - wFOV) / 2.0
        w_len = 2 * RADIUS * np.sin(np.radians(wFOV / 2.0)) / np.sin(np.radians(wangle))
        w_interval = w_len / (width - 1)

        hangle = (180 - hFOV) / 2.0
        h_len = 2 * RADIUS * np.sin(np.radians(hFOV / 2.0)) / np.sin(np.radians(hangle))
        h_interval = h_len / (height - 1)
        x_map = np.zeros([height, width], np.float32) + RADIUS
        y_map = np.tile((np.arange(0, width) - c_x) * w_interval, [height, 1])
        z_map = -np.tile((np.arange(0, height) - c_y) * h_interval, [width, 1]).T
        D = np.sqrt(x_map**2 + y_map**2 + z_map**2)
        xyz = np.zeros([height, width, 3], np.float)
        xyz[:, :, 0] = (RADIUS / D * x_map)[:, :]
        xyz[:, :, 1] = (RADIUS / D * y_map)[:, :]
        xyz[:, :, 2] = (RADIUS / D * z_map)[:, :]

        y_axis = np.array([0.0, 1.0, 0.0], np.float32)
        z_axis = np.array([0.0, 0.0, 1.0], np.float32)
        [R1, _] = cv2.Rodrigues(z_axis * np.radians(THETA))
        [R2, _] = cv2.Rodrigues(np.dot(R1, y_axis) * np.radians(-PHI))

        xyz = xyz.reshape([height * width, 3]).T
        xyz = np.dot(R1, xyz)
        xyz = np.dot(R2, xyz).T
        lat = np.arcsin(xyz[:, 2] / RADIUS)
        lon = np.zeros([height * width], np.float)
        theta = np.arctan(xyz[:, 1] / xyz[:, 0])
        idx1 = xyz[:, 0] > 0
        idx2 = xyz[:, 1] > 0

        idx3 = ((1 - idx1) * idx2).astype(np.bool)
        idx4 = ((1 - idx1) * (1 - idx2)).astype(np.bool)

        lon[idx1] = theta[idx1]
        lon[idx3] = theta[idx3] + np.pi
        lon[idx4] = theta[idx4] - np.pi

        lon = lon.reshape([height, width]) / np.pi * 180
        lat = -lat.reshape([height, width]) / np.pi * 180
        lon = lon / 180 * equ_cx + equ_cx
        lat = lat / 90 * equ_cy + equ_cy
        #for x in range(width):
        #    for y in range(height):
        #        cv2.circle(self._img, (int(lon[y, x]), int(lat[y, x])), 1, (0, 255, 0))
        #return self._img

        persp = cv2.remap(self._img, lon.astype(np.float32), lat.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP)
        return persp

print("nothing here")
