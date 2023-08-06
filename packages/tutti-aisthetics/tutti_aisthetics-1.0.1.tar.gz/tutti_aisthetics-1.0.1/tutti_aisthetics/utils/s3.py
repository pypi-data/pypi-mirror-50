import logging
import os

import boto3
import botocore

log = logging.getLogger(__name__)


def get_image_from_bucket(bucket_name: str, key: str):
    s3 = boto3.resource('s3')
    outfile = os.path.join(os.sep, 'tmp', key)
    try:
        s3.Bucket(bucket_name).download_file(key, os.path.join(os.sep, 'tmp', key))
        return outfile
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            log.error('The object does not exist.')
        else:
            raise
