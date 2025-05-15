import os
AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME='hobbysite-space'
AWS_S3_ENDPOINT_URL = 'https://hobbysite-space.sgp1.digitaloceanspaces.com'

DEFAULT_FILE_STORAGE = "hobbysite.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "hobbysite.cdn.backends.StaticRootS3Boto3Storage"