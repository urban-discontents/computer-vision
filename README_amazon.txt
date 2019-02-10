To make Rekognition work,

(1) Install boto3 and awscli through pip
(2) Run `aws configure`
(3) On the AWS Web Console, create a S3 bucket
(4) Properly configure par_amazon.py:
  - aws_bucket_name: the name of the S3 bucket created in step (3)
  - downloaded_imagelist_fname: the CSV file that download-streetview.py
    produces as output.
  - downloaded_images_folder: the folder where download-streetview.py saved
    its images.
(5) Run cv_amazon_upload.py
(6) Run cv_amazon_integration.py
