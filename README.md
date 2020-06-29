# Cirrus Task Images

This repository contains Docker files for creating Docker images used for running Cirrus tasks in Batch. There are two general Docker images that are always available in Cirrus: `run-lambda` and `run-geolambda`. These images can be used to run *any* Lambda function as an AWS Batch job instead.

This repository exists to maintain public built Docker images that are referenced from a Cirrus deployment. See the Cirrus documentation for detailed usage of these images with Cirrus, a brief overview is provided below.

## Built Docker Images

| Image                   | Description |
| ----------------------- | ----------- |
| cirrusgeo/run-lambda    | Run Lambda code in a Docker container |
| cirrusgeo/run-geolambda | Run Lambda code in a Docker container with geospatial libraries |


## Usage

These Cirrus images are usually used by creating a Batch JobDefinition which is referenced from a Task in a Cirrus workflow. However as Docker images, they can be used locally or on other servers or clusters as well.
The built images are stored in Docker Hub in the [`cirrusgeo` organization](https://hub.docker.com/orgs/cirrusgeo/repositories).

In the case of `run-lambda` and `run-geolambda`, when used as a Task in Cirrus the Lambda Function ARN is provided as part of the JobDefinition (see Cirrus example workflows), and the payload will be automatically handed to the Batch job. 

They will also be used by calling the `cirruslib.utils.submit_as_batch_job` function from within a single Lambda function (such as a Cirrus feeder). This allows a Lambda function to be able to call it's own code, but run as a Batch process instead, such as when the running time is expected to be too long to run as a Lambda When started, the Docker container fetches the code for the Lambda function, along with the JSON file payload stored on s3. The function `lambda_handler.lambda_function` is run with the JSON file as the event payload, and the returned result is uploaded back to s3 with the same URL.

### run-lambda

The `run-lambda` image will run the code from any Lambda function you have access to. The Docker image is based on a basic Lambda runtime for Python and will have the same libraries as a Lambda does.

```
$ docker run -it cirrusgeo/run-lambda run <LambdaFunctionArn> <S3URLtoPayload>
```

### run-geolambda

The `run-geolambda` image will run the code from any Lambda function you have access to, just as `run-lambda`. Instead of a basic Lambda image, the [GeoLambda (Python)](https://github.com/developmentseed/geolambda) image is used. If the Lambda that is to be run uses GeoLambda layers, or requires the same geospatial libraries that are available in GeoLambda, then use this image. GeoLambda includes native geospatial libraries lile *PROJ* and *GDAL*, along with common geospatial Python libraries like *rasterio* and *pyproj*

## About

Cirrus is an open-source pipeline for processing geospatial data in AWS. Cirrus was developed by [Element 84](https://element84.com/) originally under a [NASA Access project].