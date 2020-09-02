#!/usr/bin/env python

import argparse
import requests

from boto3 import client
from boto3utils import s3
from json import dumps
from logging import getLogger, StreamHandler
from os import getenv
from sys import argv
from zipfile import ZipFile

# configure logger - CRITICAL, ERROR, WARNING, INFO, DEBUG
logger = getLogger(__name__)
logger.setLevel(getenv('CIRRUS_LOG_LEVEL', 'DEBUG'))
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
    logger.debug("Importing lambda_handler.lambda_function from fetched Lambda")
    from lambda_function import lambda_handler

    # fetch event payload
    payload = s3().read_json(args.url)
    logger.debug(f"Payload: {dumps(payload)}")
   
    # run handler with payload
    logger.debug(f"Running lambda_handler with payload from {args.url}")
    response = lambda_handler(payload)

    url = args.url.replace('.json', '_out.json')

    s3().upload_json(response, url)
    logger.debug(f"Completed, copied output back to {url}")