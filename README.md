# Cirrus Job Images

This repository containd Docker files for creating Docker images used in Cirrus.




# GeoLambda Batch Job

This directory stores the Dockerfile and script for running a deployed Lambda function in a container. This can be useful to run jobs that don't fit into the requirements of a Lambda, such as taking too long or requiring too much storage space. When built, the Docker image can be run like an executable, passing in the Lambda ARN and an S3 URL to a JSON file.

When run, the container will fetch the code for the Lambda function, along with the JSON file. It will then run the function `lambda_handler.lambda_function` (currently not adjustable) with the JSON file as the event payload, and upload the resulting JSON output back to s3.

The Docker image created is based off [GeoLambda (Python)](https://github.com/developmentseed/geolambda), so contains common native geospatial libraries lile *PROJ* and *GDAL*, along with common geospatial Python libraries like *rasterio* and *pyproj*


## Versions



## TODO

- Put into separate repo: geolambda-batch, add license
- deploy to new repo
- Configurable name of lambda handler
- option to pass in JSON directly rather than fetch from s3
- make uploading JSON output to s3 optional
- add tests
- put run-batch in /usr/local/lib so can be called without qualifying directory (this involves using importlib in the code to properly import lambda handler which will now be in a different directory that the executable)




# Lambda Batch Job

This directory stores the Dockerfile and script for running a deployed Lambda function in a container. This can be useful to run jobs that don't fit into the requirements of a Lambda, such as taking too long or requiring too much storage space. When built, the Docker image can be run like an executable, passing in the Lambda ARN and an S3 URL to a JSON file.

When run, the container will fetch the code for the Lambda function, along with the JSON file. It will then run the function `lambda_handler.lambda_function` (currently not adjustable) with the JSON file as the event payload, and upload the resulting JSON output back to s3.

## Versions




## TODO

- Put into separate repo: geolambda-batch, add license
- deploy to new repo
- Configurable name of lambda handler
- option to pass in JSON directly rather than fetch from s3
- make uploading JSON output to s3 optional
- add tests
- put run-batch in /usr/local/lib so can be called without qualifying directory (this involves using importlib in the code to properly import lambda handler which will now be in a different directory that the executable)



## About

Cirrus is an open-source pipeline for processing geospatial data in AWS. Cirrus was developed by [Element 84](https://element84.com/) originally under a [NASA Access project].