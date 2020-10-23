#!/usr/bin/env python

import argparse
import os
import requests
from json import dumps
from logging import getLogger, StreamHandler
from sys import argv

from boto3 import client
from boto3utils import s3
from zipfile import ZipFile

# configure logger - CRITICAL, ERROR, WARNING, INFO, DEBUG
logger = getLogger(__name__)
logger.setLevel(os.getenv('CIRRUS_LOG_LEVEL', 'DEBUG'))
logger.addHandler(StreamHandler())
getLogger("boto3utils").propagate = True

lambda_client = client('lambda')


def fetch_lambda_code(lambda_name, path=''):
    """ Download Lambda function code """
    info = lambda_client.get_function(FunctionName=lambda_name)
    url = info['Code']['Location']
    filename = lambda_name + '.zip'
    logger.info('Downloading %s as %s' % (url, filename))
    headers = {}
    resp = requests.get(url, headers=headers, stream=True)
    if resp.status_code != 200:
        raise Exception("Unable to download file %s: %s" % (url, resp.text))
    with open(filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    with ZipFile(filename) as f:
        f.extractall(path)
    return path


if __name__ == "__main__":
    desc = 'Run a lambda function handler as a batch job'
    dhf = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=desc, formatter_class=dhf)
    parser.add_argument('lambda_function', help='Lambda function name')
    parser.add_argument('url', help='S3 URL to event JSON')
    args = parser.parse_args(argv[1:])

    # download and unzip lambda
    fetch_lambda_code(args.lambda_function)

    # get list of files
    filenames = os.listdir()

    if 'task.py' in filenames:
        msg = 'Importing handler from task.py'
        from task import handler
    elif 'feeder.py' in filenames:
        msg = 'Importing handler from feeder.py'
        from feeder import handler
    else:
        msg = 'Importing lambda_handler from lambda_function.py as handler'
        from lambda_function import lambda_handler as handler

    logger.info(msg)

    # fetch event payload
    payload = s3().read_json(args.url)

    # run handler with payload
    response = handler(payload)

    # write back output
    url = args.url.replace('.json', '_out.json')

    s3().upload_json(response, url)
    logger.debug(f"Completed, copied output back to {url}")