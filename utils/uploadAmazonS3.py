import boto3, os

city = 'curitiba'
sample = 'urbanextent142'

inputDir = os.path.join("E:\\", 'streetview','samples',city, sample, 'low-res')
bucketName = city +'-'+ sample

print(bucketName)
s3 = boto3.client('s3')
bucket = s3.create_bucket(Bucket=bucketName)


for root, dirs, files in os.walk(inputDir):
    for imgDir in dirs:
        for root, dirs, files in os.walk(os.path.join(inputDir, imgDir)):
            for filename in files:
                newName = 'pano.jpg' if filename[:4] != 'view' else filename

                s3.upload_file(
                    os.path.join(inputDir, imgDir, filename), bucketName, os.path.join(imgDir, newName),
                    ExtraArgs={
                        'ACL': 'public-read',
                        'ContentType': 'image/jpeg'
                    }
                )
        print(imgDir +' uploaded.')
