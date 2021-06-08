import logging
import re

import boto3
import botocore


logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("s3transfer").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("aiobotocore").setLevel(logging.ERROR)
logging.getLogger("s3fs").setLevel(logging.ERROR)
logger = logging.getLogger('s3')


def parse_s3(s3path):
    """
    Parse s3 to get bucket name and path name

    Args:
        s3path (str): the full s3 path

    Returns:
        s3bucket (str): s3 bucket name
        s3path (str): directory path within s3 bucket
    """
    
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path, s3path):
    """
    Upload local file to s3 bucket

    Args:
        local_path (str): the path that points to the local data
        s3path (str): the s3 path that the data will be uploaded to
        
    Returns: None
    """

    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)


def download_file_from_s3(local_path, s3path):
    """
    Download data from s3

    Args:
        local_path (str): the path that points to the local data
        s3path (str): the s3 path that the data will be downloaded from

    Returns: None
    """

    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.download_file(s3_just_path, local_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data downloaded from %s to %s', s3path, local_path)




