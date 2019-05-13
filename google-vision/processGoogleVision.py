import io, os, csv
import pandas as pd
from google.cloud import vision
import mysql.connector



sql = "DELETE FROM customers WHERE address = 'Mountain 21'"

class processGoogleVision:
    def __init__(self, city, sample, credentials_file, base_url, max_labels, score_threshold):
        print('Initialization the download of sample: '+ city +' - '+ sample)
        self._city = city
        self._sample = sample
        self._max_labels = max_labels
        self._base_url = base_url
        self._score_threshold = score_threshold
        self._engine = 'google_vision'

        '''
        self._input = os.path.join(csv_path, csv_file + '.csv')
        self._output_obs = os.path.join(csv_path, csv_file + '_googlevision_obs.csv') # file with the observations
        self._output_set = os.path.join(csv_path, csv_file + '_googlevision_set.csv') # file with the entire set
        '''

        self._credentials = os.path.join('..', 'safe', credentials_file)

        self._mydb = mysql.connector.connect(
          host="lbarleta.su.domains",
          user="lbarleta_urban",
          passwd="H!story55",
          database="lbarleta_discontents"
        )

        sql = "SELECT id, sample_id, city, sample, panoid, status FROM obss WHERE status = 'google_vision_pending' AND city = '"+ self._city +"' AND sample = '"+ self._sample +"'"
        self._list = pd.read_sql(sql, con=self._mydb);

        self.loadGoogleCV()
        self.iterateList()
        print("Execution ended.")

    def loadGoogleCV(self):
        print('Loading Google Vision credentials...')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self._credentials

        # Instantiates a Vision client
        self._cv_client = vision.ImageAnnotatorClient()

    def detectLabels(self, obs):
        print('Analyzing sample_id # '+ str(obs['id']))
        results = []
        for i in range(0,4):
            file = os.path.join(self._base_url, str(obs['sample_id']).rjust(6,'0') + '_' + obs['panoid'],  'view_'+ str(i) +'.jpg')
            #print(file)
            image = vision.types.Image()
            image.source.image_uri = file
            response = self._cv_client.label_detection(image=image, max_results=self._max_labels)
            labels = response.label_annotations

            for label in labels:
                if label.score > self._score_threshold:
                    results.append((label.description, label.score))

        return results

    def saveTag(self, tag):
        sql = "INSERT INTO tags (obs_id, tag, engine, score) VALUES (%s, %s, %s, %s)"
        self._mycursor.execute(sql, tuple(tag.values))
        return True

    def iterateList(self):
        print('Initiating processing of images through Google Vision...')
        for index, row in self._list.iterrows():
            tags = self.detectLabels(row)

            # Preping data
            df = pd.DataFrame.from_dict(tags)

            if df.empty:
                df = pd.DataFrame([['No tag', 0]], columns=['tag', 'score'])
            else:
                df.columns = ['tag','score']
                df = df.sort_values('score', ascending=False).drop_duplicates(subset='tag', keep='first')

            df['engine'] = self._engine
            df['obs_id'] = row['id']

            # Saving data
            self._mycursor = self._mydb.cursor()

            sql = "DELETE FROM tags WHERE obs_id = "+ str(row['id']) +" AND engine = '"+ self._engine +"'"
            self._mycursor.execute(sql)

            df[['obs_id', 'tag', 'engine', 'score']].apply(self.saveTag, axis=1)

            sql = "UPDATE obss SET status = 'google_vision_done' WHERE id = "+ str(row['id'])
            self._mycursor.execute(sql)

            print("Saved tags in database...")
            self._mydb.commit()
