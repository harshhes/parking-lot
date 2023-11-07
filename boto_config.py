from decouple import config

BUCKET_NAME = config("BUCKET_NAME")
aws_access_key_id = config("aws_access_key_id")
aws_secret_access_key = config("aws_secret_access_key")
aws_region = config("aws_region")